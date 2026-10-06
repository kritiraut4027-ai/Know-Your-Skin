import json
import re
from typing import Dict, Any, List, Optional
from .llm import generate, LLMUnavailable, LLMSessionTracker

# Variant templates for natural phrasing variety (§6 of build spec)
TEMPLATE_VARIANTS = [
    # Variant A: Standard balanced
    "Selected for your {skin_type} skin profile and {concern_text}. "
    "Features {key_ings} without unnecessary additives. "
    "At ₹{price}, it fits well under your ₹{budget} ceiling.",

    # Variant B: Action-first
    "Formulated to target {concern_text} with active support from {key_ings}. "
    "Compatible with {skin_type} skin and priced at ₹{price} (within your ₹{budget} limit).",

    # Variant C: Ingredient & barrier focus
    "Delivers {key_ings} specifically chosen for {concern_text} on {skin_type} skin. "
    "Maintains a gentle profile and sits comfortably inside your ₹{budget} budget at ₹{price}.",

    # Variant D: Budget & purity emphasis
    "A budget-conscious match at ₹{price} (max ₹{budget}) for {skin_type} skin. "
    "Provides targeted {concern_text} care through {key_ings}."
]

def format_concern(concern: str) -> str:
    if not concern or concern.lower() in ["none", "none in particular", ""]:
        return "daily maintenance"
    return concern.replace("_", " ").lower()

def generate_template_explanation(product: Dict[str, Any], reasons: Dict[str, Any], variant_index: int = 0) -> str:
    """
    Deterministic rule-based explanation strictly grounded in provided attributes (§6).
    Uses 4 template variants to avoid repetitive copy across multiple product cards.
    """
    price = int(product.get("price_inr", 0))
    budget = int(reasons.get("budget_ceiling", price))
    skin_type = str(reasons.get("skin_type", "balanced")).lower()
    concern_text = format_concern(str(reasons.get("concern", "")))
    
    key_ings_list = reasons.get("matched_key_ingredients", [])
    if not key_ings_list:
        key_ings_list = product.get("key_ingredients", [])
    
    if key_ings_list:
        # Clean formatting
        clean_ings = [k.replace("_", " ").title() for k in key_ings_list[:2]]
        key_ings_str = " and ".join(clean_ings)
    else:
        flags = product.get("flags", [])
        if "fragrance_free" in flags:
            key_ings_str = "a fragrance-free base"
        else:
            key_ings_str = "gentle surfactants"

    template = TEMPLATE_VARIANTS[variant_index % len(TEMPLATE_VARIANTS)]
    return template.format(
        skin_type=skin_type,
        concern_text=concern_text,
        key_ings=key_ings_str,
        price=price,
        budget=budget
    )

def audit_explanation_for_hallucinations(
    generated_text: str, 
    product: Dict[str, Any], 
    reasons: Dict[str, Any]
) -> bool:
    """
    Post-generation verification (§6 of build spec):
    Scans generated text to confirm no ungrounded ingredients were fabricated by the LLM.
    Returns True if safe/grounded, False if hallucinated claims detected.
    """
    text_lower = generated_text.lower()
    
    # Authorized ingredients (from structured reasons + product record)
    allowed_ingredients: List[str] = []
    for ing in reasons.get("matched_key_ingredients", []):
        allowed_ingredients.append(ing.lower().replace("_", " "))
    for ing in product.get("key_ingredients", []):
        allowed_ingredients.append(ing.lower().replace("_", " "))
    for inci in product.get("full_ingredient_list", []):
        allowed_ingredients.append(inci.lower())

    # Watchlist of common cosmetics ingredients that LLMs love to hallucinate
    hallucination_suspects = [
        "retinol", "retinoid", "bakuchiol", "vitamin c", "ascorbic acid",
        "salicylic acid", "glycolic acid", "lactic acid", "benzoyl peroxide",
        "ceramide", "hyaluronic acid", "centella", "cica", "niacinamide",
        "snail mucin", "azelaic acid", "tea tree", "zinc pca", "kojic acid"
    ]

    for suspect in hallucination_suspects:
        # If the suspect is mentioned in generated text, it MUST exist in allowed ingredients
        if re.search(r"\b" + re.escape(suspect) + r"\b", text_lower):
            found_in_allowed = any(suspect in allowed for allowed in allowed_ingredients)
            if not found_in_allowed:
                return False  # Hallucinated ingredient detected!

    # Check for prohibited medical words (SR-1)
    banned_words = ["diagnose", "cure", "treat your", "100% safe", "guaranteed"]
    for bw in banned_words:
        if bw in text_lower:
            return False

    return True

def generate_explanation(
    product: Dict[str, Any], 
    reasons: Dict[str, Any],
    variant_index: int = 0,
    session_tracker: Optional[LLMSessionTracker] = None,
    override_api_key: Optional[str] = None
) -> str:
    """
    Generates a 1-2 sentence match explanation.
    Tries provider-agnostic LLM if enabled; performs strict hallucination audit.
    Silently falls back to deterministic template on any failure or audit rejection.
    """
    template_fallback = generate_template_explanation(product, reasons, variant_index)
    
    # Prepare structured JSON prompt (§6)
    structured_payload = {
        "product_name": product.get("name"),
        "brand": product.get("brand"),
        "price_inr": product.get("price_inr"),
        "budget_ceiling_inr": reasons.get("budget_ceiling"),
        "user_skin_type": reasons.get("skin_type"),
        "user_primary_concern": reasons.get("concern"),
        "verified_active_ingredients": reasons.get("matched_key_ingredients", []),
        "flags": product.get("flags", [])
    }
    
    prompt = (
        f"Input structured match facts:\n{json.dumps(structured_payload, indent=2)}\n\n"
        "Explain why this cleanser was picked for this user in exactly 1 or 2 concise, natural sentences."
    )
    
    system = (
        "You are an explainability module for a cosmetic face wash discovery system. "
        "Strict rules: "
        "1. NEVER invent or mention any ingredient, medical claim, or benefit not present in the input JSON. "
        "2. State how the product matches their skin type, concern, and budget ceiling. "
        "3. Do not use words like 'diagnose', 'cure', 'prescribe', or '100% safe'."
    )
    
    try:
        llm_output = generate(
            prompt=prompt,
            system=system,
            override_api_key=override_api_key,
            session_tracker=session_tracker
        )
        if not llm_output or len(llm_output) < 15:
            return template_fallback
            
        # Post-check audit for hallucinated ingredients
        is_grounded = audit_explanation_for_hallucinations(llm_output, product, reasons)
        if not is_grounded:
            return template_fallback
            
        return llm_output
    except (LLMUnavailable, Exception):
        return template_fallback
