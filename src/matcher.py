import re
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from .ingredient_aliases import product_contains_avoided_item

class MatchProfile(BaseModel):
    skin_type: str = Field(..., description="e.g. oily, dry, combination, sensitive, normal, not_sure")
    primary_concern: str = Field(..., description="e.g. acne, dullness, sensitivity, dryness, excess_oil, none")
    budget_inr: float = Field(..., description="Hard maximum price in INR")
    avoided_ingredients: List[str] = Field(default_factory=list, description="List of avoided ingredients / flags")
    free_text_avoid: Optional[str] = Field(default="", description="Additional free-text ingredient to avoid")
    routine_context: Optional[str] = Field(default="", description="Current skincare routine context")
    notes: Optional[str] = Field(default="", description="Any additional concerns or details")

class MatchCandidate(BaseModel):
    product: Dict[str, Any]
    match_score: float
    reasons: Dict[str, Any]

class MatchResult(BaseModel):
    picks: List[MatchCandidate]
    total_passed_filters: int
    filter_summary: Dict[str, Any]
    limited_results_warning: Optional[str] = None

def calculate_product_score(
    product: Dict[str, Any], 
    skin_type: str, 
    primary_concern: str
) -> Dict[str, Any]:
    """
    Computes transparent deterministic score (§5 of build spec):
    - Skin type match: +3.5 (+1.0 if not_sure)
    - Concern match: +4.0 (+1.5 for active targeting ingredients)
    """
    score = 0.0
    matched_skin_types = []
    matched_concerns = []
    matched_key_ingredients = []
    
    prod_skin_types = [st.lower() for st in product.get("skin_types", [])]
    prod_concerns = [c.lower() for c in product.get("concerns_addressed", [])]
    key_ingredients = product.get("key_ingredients", [])
    
    st_clean = skin_type.strip().lower()
    concern_clean = primary_concern.strip().lower()
    
    # 1. Skin type scoring
    if st_clean in ["not_sure", "not sure", ""]:
        score += 1.0  # neutral baseline
    elif st_clean in prod_skin_types:
        score += 3.5
        matched_skin_types.append(st_clean)
    elif "all" in prod_skin_types:
        score += 2.5
        matched_skin_types.append("all skin types")
    elif st_clean == "sensitive" and ("dry" in prod_skin_types or "sensitive" in prod_skin_types):
        score += 2.0
    elif st_clean == "combination" and ("oily" in prod_skin_types or "normal" in prod_skin_types):
        score += 2.0
        
    # 2. Concern scoring
    if concern_clean and concern_clean not in ["none", "none in particular", ""]:
        target_tags = [concern_clean]
        if concern_clean == "acne":
            target_tags.extend(["clogged_pores", "excess_oil", "blackheads"])
        elif concern_clean == "dullness":
            target_tags.extend(["pigmentation", "rough_texture"])
        elif concern_clean == "sensitivity":
            target_tags.extend(["redness", "barrier_repair"])
        elif concern_clean == "dryness":
            target_tags.extend(["dehydration", "barrier_repair"])
            
        found_concern = False
        for tag in target_tags:
            for pc in prod_concerns:
                if tag in pc or pc in tag:
                    matched_concerns.append(pc)
                    found_concern = True
        
        if found_concern:
            score += 4.0
            
        for ing in key_ingredients:
            ing_lower = ing.lower()
            if concern_clean == "acne" and any(a in ing_lower for a in ["salicylic", "zinc", "tea_tree", "bha"]):
                matched_key_ingredients.append(ing.replace("_", " ").title())
                score += 1.5
            elif concern_clean == "dullness" and any(a in ing_lower for a in ["glycolic", "vitamin_c", "lactic", "niacinamide"]):
                matched_key_ingredients.append(ing.replace("_", " ").title())
                score += 1.5
            elif concern_clean in ["dryness", "sensitivity"] and any(a in ing_lower for a in ["ceramide", "hyaluronic", "oat", "panthenol", "cica", "glycerin"]):
                matched_key_ingredients.append(ing.replace("_", " ").title())
                score += 1.5
                
    return {
        "score": round(score, 2),
        "matched_skin_types": list(dict.fromkeys(matched_skin_types)),
        "matched_concerns": list(dict.fromkeys(matched_concerns)),
        "matched_key_ingredients": list(dict.fromkeys(matched_key_ingredients))
    }

def run_matching_engine(
    catalog: List[Dict[str, Any]], 
    profile: MatchProfile
) -> MatchResult:
    """
    Deterministic matching engine with strict hard filtering (§5 of build spec).
    1. Hard budget ceiling filter (price <= budget_inr).
    2. Hard avoided ingredients filter (flags, INCI list regex, and free-text).
    3. Deterministic scoring without LLM hallucination.
    """
    passed_candidates: List[MatchCandidate] = []
    
    total_budget_excluded = 0
    total_avoidance_excluded = 0
    
    # Consolidate avoided list
    avoid_list = list(profile.avoided_ingredients)
    if profile.free_text_avoid and profile.free_text_avoid.strip():
        # split on commas if multiple
        for item in profile.free_text_avoid.split(","):
            if item.strip():
                avoid_list.append(item.strip())

    for product in catalog:
        price = product.get("price_inr", 0)
        
        # Hard Filter 1: Budget Ceiling
        if price > profile.budget_inr:
            total_budget_excluded += 1
            continue
            
        # Hard Filter 2: Avoided Ingredients
        has_avoided = False
        for avoided_item in avoid_list:
            if product_contains_avoided_item(product, avoided_item):
                has_avoided = True
                total_avoidance_excluded += 1
                break
                
        if has_avoided:
            continue
            
        # Deterministic scoring
        score_details = calculate_product_score(
            product=product,
            skin_type=profile.skin_type,
            primary_concern=profile.primary_concern
        )
        
        reasons = {
            "concern": profile.primary_concern,
            "skin_type": profile.skin_type,
            "price_inr": price,
            "budget_ceiling": profile.budget_inr,
            "matched_skin_types": score_details["matched_skin_types"],
            "matched_concerns": score_details["matched_concerns"],
            "matched_key_ingredients": score_details["matched_key_ingredients"],
            "flags": product.get("flags", [])
        }
        
        passed_candidates.append(
            MatchCandidate(
                product=product,
                match_score=score_details["score"],
                reasons=reasons
            )
        )
        
    # Sort candidates by score (descending), then price (ascending) as tiebreak
    passed_candidates.sort(key=lambda c: (-c.match_score, c.product.get("price_inr", 0)))
    
    top_picks = passed_candidates[:5]
    total_passed = len(passed_candidates)
    
    warning = None
    if total_passed == 0:
        warning = (
            f"No products in the catalog satisfied your hard criteria (Budget ceiling: ₹{int(profile.budget_inr)} "
            f"and avoided ingredients: {', '.join(avoid_list) if avoid_list else 'None'}). "
            f"Our system will never silently loosen your constraints. Please consider adjusting your budget or avoidance list."
        )
    elif total_passed < 3:
        warning = (
            f"Only {total_passed} product(s) satisfied your strict constraints. "
            f"We are showing what survived without compromising your preferences."
        )
        
    return MatchResult(
        picks=top_picks,
        total_passed_filters=total_passed,
        filter_summary={
            "total_catalog_size": len(catalog),
            "excluded_by_budget": total_budget_excluded,
            "excluded_by_avoidance": total_avoidance_excluded,
            "passed_count": total_passed
        },
        limited_results_warning=warning
    )
