import re
from typing import Dict, Any, List, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from .data_loader import load_ingredient_kb, load_products
from .matcher import MatchProfile, product_contains_avoided_item
from .safety import check_medical_condition_query, check_for_escalation, MEDICAL_DISCLAIMER
from .config import ANTHROPIC_API_KEY, GEMINI_API_KEY

class IngredientRAGRetriever:
    def __init__(self):
        self.kb = load_ingredient_kb()
        self.documents = []
        self.doc_mapping = []
        self._build_index()
        
    def _build_index(self):
        self.documents = []
        self.doc_mapping = []
        for idx, entry in enumerate(self.kb):
            # Rich document text combining name, aliases, functions, concerns, and cautions
            text = (
                f"{entry.get('ingredient_name', '')} "
                f"{' '.join(entry.get('aliases', []))} "
                f"{entry.get('function', '')} "
                f"{' '.join(entry.get('common_concerns', []))} "
                f"{entry.get('caution_notes', '')}"
            )
            self.documents.append(text)
            self.doc_mapping.append(entry)
            
        # Filter out ubiquitous skincare and generic chemical form terms
        # so similarity requires actual active chemical identity
        generic_terms = [
            'skin', 'face', 'cleanser', 'cleansers', 'product', 'products', 'used', 'commonly',
            'topical', 'does', 'work', 'role', 'mechanism', 'washes', 'formulation',
            'oil', 'extract', 'water', 'powder', 'acid', 'solution', 'cure', 'reverse', 'treat'
        ]
        custom_stop_words = list(TfidfVectorizer(stop_words='english').get_stop_words()) + generic_terms
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words=custom_stop_words)
        self.tfidf_matrix = self.vectorizer.fit_transform(self.documents)
        
    def retrieve(self, query: str, top_k: int = 2, threshold: float = 0.35) -> List[Dict[str, Any]]:
        """
        Retrieves matching ingredient documents using cosine similarity with minimum threshold.
        """
        # Exact name / alias boost with word boundaries
        query_lower = query.lower()
        exact_matches = []
        for entry in self.kb:
            name_lower = entry["ingredient_name"].lower()
            # If name has distinctive words (e.g. "salicylic", "niacinamide", "tea tree", "centella")
            name_pattern = r"\b" + re.escape(name_lower) + r"\b"
            if re.search(name_pattern, query_lower):
                exact_matches.append(entry)
                continue
                
            for a in entry.get("aliases", []):
                alias_pattern = r"\b" + re.escape(a.lower()) + r"\b"
                if re.search(alias_pattern, query_lower):
                    exact_matches.append(entry)
                    break
                
        if exact_matches:
            return exact_matches[:top_k]

        query_vec = self.vectorizer.transform([query])
        # If no significant non-stopword tokens exist in query, return empty
        if query_vec.nnz == 0:
            return []
            
        sims = cosine_similarity(query_vec, self.tfidf_matrix)[0]
        
        best_indices = np.argsort(sims)[::-1]
        results = []
        for i in best_indices[:top_k]:
            if sims[i] >= threshold:
                results.append(self.doc_mapping[i])
                
        return results

# Singleton retriever
_retriever = None
def get_retriever() -> IngredientRAGRetriever:
    global _retriever
    if _retriever is None:
        _retriever = IngredientRAGRetriever()
    return _retriever

def handle_why_not_recommended(
    query: str, 
    session_profile: Optional[MatchProfile]
) -> Optional[Dict[str, Any]]:
    """
    FR-5.3: Answers 'Why wasn't [Product X] recommended?' based on deterministic session rules.
    """
    catalog = load_products()
    query_lower = query.lower()
    
    # Check if user is asking why a product wasn't picked
    triggers = ["why not", "why wasn't", "why was not", "why didn't", "didn't recommend", "why wasn't product", "what about"]
    is_why_not = any(t in query_lower for t in triggers)
    if not is_why_not:
        return None
        
    matched_product = None
    for p in catalog:
        brand = p["brand"].lower()
        name = p["name"].lower()
        full_title = f"{brand} {name}"
        if name in query_lower or full_title in query_lower or (brand in query_lower and len(brand) > 4):
            matched_product = p
            break
            
    if not matched_product:
        return None
        
    p_name = f"{matched_product['brand']} {matched_product['name']}"
    p_price = matched_product["price_inr"]
    
    if not session_profile:
        return {
            "answer": f"{p_name} is priced at ₹{p_price}. Without an active session questionnaire, we couldn't evaluate it against specific constraints.",
            "citations": [],
            "disclaimer": MEDICAL_DISCLAIMER
        }
        
    # Check budget
    reasons = []
    if p_price > session_profile.budget_inr:
        reasons.append(
            f"it is priced at ₹{p_price}, which exceeds your stated maximum budget ceiling of ₹{int(session_profile.budget_inr)}"
        )
        
    # Check avoided ingredients
    avoided_found = []
    for avoided in session_profile.avoided_ingredients:
        if product_contains_avoided_item(matched_product, avoided):
            avoided_found.append(avoided)
            
    if avoided_found:
        reasons.append(
            f"it contains or flags ingredients you chose to avoid ({', '.join(avoided_found)})"
        )
        
    # Check skin type / concern compatibility
    prod_skin_types = [s.lower() for s in matched_product.get("skin_types", [])]
    user_st = session_profile.skin_type.lower()
    if user_st not in ["not_sure", "not sure", ""] and user_st not in prod_skin_types and "all" not in prod_skin_types:
        reasons.append(
            f"it is targeted for {', '.join(prod_skin_types)} skin rather than your stated {user_st} skin profile"
        )
        
    if reasons:
        answer = f"**{p_name}** was not included in your Top Picks because " + "; and ".join(reasons) + "."
    else:
        answer = (
            f"**{p_name}** actually met your hard constraints (Price: ₹{p_price} <= ₹{int(session_profile.budget_inr)}), "
            f"but other cleansers scored higher for your primary concern of '{session_profile.primary_concern}'."
        )
        
    return {
        "answer": answer,
        "citations": [f"Catalog verification: {p_name} (Price ₹{p_price})"],
        "disclaimer": MEDICAL_DISCLAIMER
    }

def process_chat_query(
    query: str, 
    session_profile: Optional[MatchProfile] = None
) -> Dict[str, Any]:
    """
    Main RAG Chatbot entry point complying with FR-5.1 to FR-5.5 & SR-1 to SR-5.
    """
    # 1. Escalation check on chat input
    should_escalate, symptoms = check_for_escalation(query)
    if should_escalate:
        sym_str = ", ".join(symptoms)
        return {
            "answer": (
                f"⚠️ **Dermatological Attention Advised**: Your message mentions symptoms ({sym_str}) "
                f"that require direct medical assessment. Please refrain from starting self-selected cosmetic "
                f"cleansers and visit a qualified dermatologist for an in-person diagnosis."
            ),
            "citations": [],
            "disclaimer": MEDICAL_DISCLAIMER,
            "escalation": True
        }
        
    # 2. Check for clinical medical condition inquiry (SR-4)
    has_med, condition = check_medical_condition_query(query)
    if has_med:
        return {
            "answer": (
                f"While ingredients may be formulated for sensitive or reactive skin, this system cannot determine "
                f"whether any cosmetic cleanser is clinically safe or therapeutic for **{condition}**. "
                f"Please consult a dermatologist for prescription medical advice regarding {condition}."
            ),
            "citations": ["Clinical Safety Boundary: Non-diagnostic policy §9 SR-4"],
            "disclaimer": MEDICAL_DISCLAIMER
        }
        
    # 3. Check for 'Why wasn't product X recommended' (FR-5.3)
    why_not_resp = handle_why_not_recommended(query, session_profile)
    if why_not_resp:
        return why_not_resp
        
    # 4. Grounded retrieval against verified ingredient KB (FR-5.1)
    retriever = get_retriever()
    matched_entries = retriever.retrieve(query, top_k=2)
    
    # 5. Out of KB fallback (FR-5.2)
    if not matched_entries:
        return {
            "answer": (
                "Our curated, peer-verified ingredient knowledge base currently does not have verified scientific "
                "data for that specific question or ingredient. To ensure accuracy and avoid ungrounded AI speculation, "
                "we recommend reviewing the product manufacturer's packaging or asking a dermatologist."
            ),
            "citations": [],
            "disclaimer": MEDICAL_DISCLAIMER
        }
        
    # 6. Synthesize grounded answer with strict citations
    primary = matched_entries[0]
    ing_name = primary.get("ingredient_name")
    function = primary.get("function")
    concerns = ", ".join(primary.get("common_concerns", []))
    cautions = primary.get("caution_notes")
    source = primary.get("source")
    
    # Check session context fit (FR-5.4)
    session_note = ""
    if session_profile:
        st = session_profile.skin_type
        if st.lower() in ["dry", "sensitive"] and any(w in cautions.lower() for w in ["dryness", "irritation", "peeling"]):
            session_note = f"\n\n*Note for your {st} skin profile*: Be mindful that {cautions}"
        elif session_profile.primary_concern.lower() in primary.get("common_concerns", []):
            session_note = f"\n\n*Fit with your concern*: {ing_name} directly aligns with your stated priority of addressing {session_profile.primary_concern}."

    answer = (
        f"**{ing_name}**\n\n"
        f"• **Cosmetic Function**: {function}\n"
        f"• **Typical Skin Concerns**: {concerns}\n"
        f"• **Usage & Caution Notes**: {cautions}"
        f"{session_note}"
    )
    
    citations = [f"{ing_name}: {source}"]
    if len(matched_entries) > 1:
        sec = matched_entries[1]
        citations.append(f"{sec['ingredient_name']}: {sec['source']}")
        
    return {
        "answer": answer,
        "citations": citations,
        "disclaimer": MEDICAL_DISCLAIMER
    }
