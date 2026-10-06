from typing import Dict, Any, List, Optional
from .retrieval import get_ingredient_retriever
from .catalog import get_default_catalog_provider
from .ingredient_aliases import product_contains_avoided_item
from .safety import (
    check_for_escalation, 
    check_medical_condition_query, 
    check_pregnancy_query,
    MEDICAL_DISCLAIMER, 
    PREGNANCY_QUALIFIER
)
from .llm import generate, LLMUnavailable, LLMSessionTracker

def handle_why_not_query(query: str, session_profile: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    Answers 'Why wasn't [Product X] recommended?' based on deterministic session rules (§8.2).
    """
    triggers = ["why not", "why wasn't", "why was not", "why didn't", "didn't recommend", "what about"]
    query_lower = query.lower()
    if not any(t in query_lower for t in triggers):
        return None

    catalog = get_default_catalog_provider().get_all_products()
    matched_product = None
    for p in catalog:
        b = p["brand"].lower()
        n = p["name"].lower()
        if n in query_lower or f"{b} {n}" in query_lower or (b in query_lower and len(b) > 4):
            matched_product = p
            break

    if not matched_product:
        return None

    p_name = f"{matched_product['brand']} {matched_product['name']}"
    price = int(matched_product["price_inr"])

    if not session_profile:
        return {
            "answer": (
                f"**{p_name}** (₹{price}) is available in our catalog. "
                "Because no active questionnaire was completed for this session, "
                "we cannot evaluate why it was omitted against your specific constraints."
            ),
            "citations": [f"Catalog Record: {p_name} (₹{price})"],
            "disclaimer": MEDICAL_DISCLAIMER,
            "escalation": False
        }

    budget = int(session_profile.get("budget_inr", 9999))
    avoided = session_profile.get("avoided_ingredients", [])
    user_st = str(session_profile.get("skin_type", "")).lower()
    user_concern = str(session_profile.get("primary_concern", "")).lower()

    reasons = []
    if price > budget:
        reasons.append(f"its price of ₹{price} exceeds your stated budget ceiling of ₹{budget}")

    found_avoided = [item for item in avoided if product_contains_avoided_item(matched_product, item)]
    if found_avoided:
        reasons.append(f"it contains ingredients you chose to avoid ({', '.join(found_avoided)})")

    prod_skin_types = [s.lower() for s in matched_product.get("skin_types", [])]
    if user_st and user_st not in ["not_sure", "not sure", ""] and user_st not in prod_skin_types and "all" not in prod_skin_types:
        reasons.append(f"it is formulated for {', '.join(prod_skin_types)} skin rather than your {user_st} skin profile")

    if reasons:
        answer = f"**{p_name}** was filtered out of your recommendations because " + "; and ".join(reasons) + "."
    else:
        answer = (
            f"**{p_name}** passed your hard constraints (Price ₹{price} <= ₹{budget}), "
            f"but other cleansers had higher compatibility scores for your primary concern of '{user_concern}'."
        )

    return {
        "answer": answer,
        "citations": [f"Verified Catalog Attributes: {p_name} (MRP ₹{price})"],
        "disclaimer": MEDICAL_DISCLAIMER,
        "escalation": False
    }

def answer_question(
    query: str, 
    session_profile: Optional[Dict[str, Any]] = None,
    session_tracker: Optional[LLMSessionTracker] = None,
    override_api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Core grounded chatbot handler (§8.2).
    1. Safety escalation check (SR-3)
    2. Medical condition deflection (SR-4)
    3. Session 'Why wasn't product X picked' evaluation
    4. Grounded retrieval with out-of-KB refusal threshold
    5. Fallback/citation presentation
    """
    # 1. SR-3 Clinical symptom escalation
    should_escalate, symptoms = check_for_escalation(query)
    if should_escalate:
        sym_str = ", ".join(symptoms)
        return {
            "answer": (
                f"⚠️ **Dermatological Assessment Recommended**: Your message mentions symptoms ({sym_str}) "
                f"that require in-person clinical assessment. Please refrain from starting self-selected cosmetic "
                f"cleansers and visit a qualified board-certified dermatologist."
            ),
            "citations": [],
            "disclaimer": MEDICAL_DISCLAIMER,
            "escalation": True
        }

    # 2. SR-4 Medical condition deflection
    has_med, cond = check_medical_condition_query(query)
    if has_med:
        return {
            "answer": (
                f"While certain ingredients are designed to be non-irritating, this cosmetic discovery system "
                f"cannot evaluate whether a formulation is clinically safe or therapeutic for **{cond}**. "
                f"Please consult a dermatologist for medical guidance regarding {cond}."
            ),
            "citations": [],
            "disclaimer": MEDICAL_DISCLAIMER,
            "escalation": False
        }

    # 3. Why wasn't product X picked?
    why_not = handle_why_not_query(query, session_profile)
    if why_not:
        return why_not

    # 4. Grounded Knowledge Base Retrieval
    retriever = get_ingredient_retriever()
    retrieved = retriever.retrieve(query, top_k=2)

    # Out-of-KB refusal (§8.2)
    if not retrieved:
        return {
            "answer": (
                "I could not find a verified match for your query in our peer-reviewed cosmetic ingredient database. "
                "To prevent misinformation or ungrounded claims, this system does not generate cosmetic advice "
                "outside its verified literature base. Please consult an ingredient specialist or dermatologist."
            ),
            "citations": [],
            "disclaimer": MEDICAL_DISCLAIMER,
            "escalation": False
        }

    # Format grounded citations
    citations = []
    kb_summaries = []
    for doc, score in retrieved:
        name = doc.get("ingredient_name", "")
        fn = doc.get("function", "")
        caut = doc.get("caution_notes", "")
        src = doc.get("source", "")
        citations.append(f"{name}: {src}")
        kb_summaries.append(f"**{name}**\n- **Function**: {fn}\n- **Cautionary Notes**: {caut}")

    # Check for pregnancy query (SR-5)
    extra_note = f"\n\n> {PREGNANCY_QUALIFIER}" if check_pregnancy_query(query) else ""

    # 5. Presentation: Default no-LLM formatted answer
    default_answer = "\n\n".join(kb_summaries) + extra_note

    # Optional: LLM synthesis if active and grounded
    try:
        context_str = "\n".join([f"- {d['ingredient_name']}: {d['function']}. {d['caution_notes']}" for d, _ in retrieved])
        prompt = (
            f"Verified Literature Context:\n{context_str}\n\n"
            f"User Question: {query}\n\n"
            "Synthesize a clear, 2-3 sentence answer based ONLY on the verified context above. "
            "Never invent claims. Do not give medical clearance."
        )
        system = "You are a skincare ingredient advisor strictly citing peer-reviewed evidence. No medical claims."
        llm_reply = generate(
            prompt=prompt, 
            system=system, 
            session_tracker=session_tracker, 
            override_api_key=override_api_key
        )
        if llm_reply and len(llm_reply) > 20:
            default_answer = llm_reply + extra_note
    except (LLMUnavailable, Exception):
        pass  # Seamlessly keep default grounded KB summary

    return {
        "answer": default_answer,
        "citations": citations,
        "disclaimer": MEDICAL_DISCLAIMER,
        "escalation": False
    }
