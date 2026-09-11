import re
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class MatchProfile(BaseModel):
    skin_type: str = Field(..., description="e.g. oily, dry, combination, sensitive, normal, not_sure")
    primary_concern: str = Field(..., description="e.g. acne, dullness, sensitivity, dryness, excess_oil, barrier_repair, rough_texture, pigmentation, none")
    budget_inr: float = Field(..., description="Hard maximum price in INR")
    avoided_ingredients: List[str] = Field(default_factory=list, description="List of avoided ingredients / flags")
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

# Ingredient keywords to detect in INCI lists
AVOIDANCE_PATTERNS = {
    "fragrance": [
        r"\bfragrance\b", r"\bparfum\b", r"\baroma\b", r"\bperfume\b"
    ],
    "sulfates": [
        r"\bsulfate\b", r"\bsulphate\b", r"\blauryl\s+sulfate\b", r"\blaureth\s+sulfate\b"
    ],
    "alcohol": [
        r"\balcohol\s+denat\b", r"\bdenatured\s+alcohol\b", r"\bsd\s+alcohol\b",
        r"\bisopropyl\s+alcohol\b", r"\bethanol\b"
    ],
    "essential_oils": [
        r"\boil\b", r"\bpeel\s+oil\b", r"\bleaf\s+oil\b", r"\bflower\s+oil\b",
        r"\blavender\b", r"\beucalyptus\b", r"\blimonene\b", r"\blinalool\b",
        r"\bgeraniol\b", r"\bcitronellol\b"
    ],
    "parabens": [
        r"\bparaben\b", r"\bmethylparaben\b", r"\bpropylparaben\b",
        r"\bbutylparaben\b", r"\bethylparaben\b"
    ]
}

def normalize_key(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())

def product_contains_avoided_item(product: Dict[str, Any], avoided_item: str) -> bool:
    """
    Checks if a product contains an ingredient the user wants to avoid.
    Checks flags, full_ingredient_list, and key_ingredients.
    """
    item_clean = avoided_item.strip().lower()
    if not item_clean:
        return False
    
    flags = [f.lower() for f in product.get("flags", [])]
    inci_list = product.get("full_ingredient_list", [])
    inci_text = " ".join(inci_list).lower()
    key_ingredients = [k.lower() for k in product.get("key_ingredients", [])]
    
    # 1. Check mapped common categories
    category_key = None
    if any(k in item_clean for k in ["fragrance", "parfum", "perfume", "scent"]):
        category_key = "fragrance"
        if "fragrance_free" in flags:
            # Explicitly certified fragrance-free
            return False
    elif any(k in item_clean for k in ["sulfate", "sulphate", "sls", "sles"]):
        category_key = "sulfates"
        if "sulfate_free" in flags:
            return False
    elif any(k in item_clean for k in ["alcohol", "denat", "ethanol"]):
        category_key = "alcohol"
        if "alcohol_free" in flags:
            return False
    elif any(k in item_clean for k in ["essential oil", "essential_oil", "fragrant plant"]):
        category_key = "essential_oils"
        if "essential_oil_free" in flags:
            return False
    elif "paraben" in item_clean:
        category_key = "parabens"
        if "paraben_free" in flags:
            return False
            
    if category_key and category_key in AVOIDANCE_PATTERNS:
        for pattern in AVOIDANCE_PATTERNS[category_key]:
            if re.search(pattern, inci_text):
                return True
        return False
        
    # 2. Check custom avoided ingredient text against INCI list & key ingredients
    # Example: "salicylic acid", "niacinamide", "tea tree", "phenoxyethanol"
    item_pattern = r"\b" + re.escape(item_clean) + r"\b"
    if re.search(item_pattern, inci_text):
        return True
        
    # Also check normalized substrings in key ingredients
    norm_item = normalize_key(item_clean)
    for k in key_ingredients:
        if norm_item in normalize_key(k):
            return True
            
    for inci in inci_list:
        if item_clean in inci.lower():
            return True
            
    return False

def calculate_product_score(
    product: Dict[str, Any], 
    skin_type: str, 
    primary_concern: str
) -> Dict[str, Any]:
    """
    Computes deterministic match score and transparent matching reasons.
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
    
    # --- Skin Type Scoring ---
    if st_clean in ["not_sure", "not sure", ""]:
        score += 1.0 # neutral base
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
        
    # --- Primary Concern Scoring ---
    if concern_clean and concern_clean not in ["none", "none in particular", ""]:
        # Map common user concern phrases to dataset tags
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
            
        # Key ingredients targeting this concern
        for ing in key_ingredients:
            ing_lower = ing.lower()
            if concern_clean == "acne" and any(a in ing_lower for a in ["salicylic", "zinc", "tea_tree", "bha", "neem"]):
                matched_key_ingredients.append(ing.replace("_", " ").title())
                score += 1.5
            elif concern_clean == "dullness" and any(a in ing_lower for a in ["glycolic", "vitamin_c", "lactic", "ascorbyl", "kojic", "niacinamide"]):
                matched_key_ingredients.append(ing.replace("_", " ").title())
                score += 1.5
            elif concern_clean in ["dryness", "sensitivity"] and any(a in ing_lower for a in ["ceramide", "hyaluronic", "oat", "panthenol", "allantoin", "cica", "glycerin"]):
                matched_key_ingredients.append(ing.replace("_", " ").title())
                score += 1.5
                
    # Deduplicate lists
    matched_skin_types = list(dict.fromkeys(matched_skin_types))
    matched_concerns = list(dict.fromkeys(matched_concerns))
    matched_key_ingredients = list(dict.fromkeys(matched_key_ingredients))
    
    return {
        "score": round(score, 2),
        "matched_skin_types": matched_skin_types,
        "matched_concerns": matched_concerns,
        "matched_key_ingredients": matched_key_ingredients
    }

def run_matching_engine(
    catalog: List[Dict[str, Any]], 
    profile: MatchProfile
) -> MatchResult:
    """
    FR-3.1 to FR-3.5:
    Deterministic matching engine with strict hard filtering.
    """
    passed_candidates: List[MatchCandidate] = []
    
    total_budget_excluded = 0
    total_avoidance_excluded = 0
    
    for product in catalog:
        price = product.get("price_inr", 0)
        
        # Hard Filter 1: Budget Ceiling (FR-3.2)
        if price > profile.budget_inr:
            total_budget_excluded += 1
            continue
            
        # Hard Filter 2: Avoided Ingredients (FR-3.3)
        has_avoided = False
        for avoided_item in profile.avoided_ingredients:
            if product_contains_avoided_item(product, avoided_item):
                has_avoided = True
                total_avoidance_excluded += 1
                break
                
        if has_avoided:
            continue
            
        # Product qualifies hard constraints! Now calculate deterministic score (FR-3.4)
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
        
        candidate = MatchCandidate(
            product=product,
            match_score=score_details["score"],
            reasons=reasons
        )
        passed_candidates.append(candidate)
        
    # Sort candidates by match_score descending, then price ascending (better value first)
    passed_candidates.sort(key=lambda c: (-c.match_score, c.product.get("price_inr", 0)))
    
    total_passed = len(passed_candidates)
    limited_results_warning = None
    
    # FR-3.5: Return top 3-5 results. If fewer than 3 products pass, do not loosen filters!
    if total_passed == 0:
        limited_results_warning = (
            f"No products in our curated catalog strictly met your budget (<= ₹{int(profile.budget_inr)}) "
            f"and avoided ingredient preferences. To protect your stated preferences, we did not loosen your filters."
        )
        top_picks = []
    elif total_passed < 3:
        limited_results_warning = (
            f"Only {total_passed} product(s) in our catalog strictly met both your budget ceiling of ₹{int(profile.budget_inr)} "
            f"and your avoided ingredient restrictions. We did not silently loosen your criteria."
        )
        top_picks = passed_candidates
    else:
        top_picks = passed_candidates[:5]
        
    return MatchResult(
        picks=top_picks,
        total_passed_filters=total_passed,
        filter_summary={
            "initial_catalog_size": len(catalog),
            "excluded_by_budget": total_budget_excluded,
            "excluded_by_avoidance": total_avoidance_excluded,
            "total_passed": total_passed
        },
        limited_results_warning=limited_results_warning
    )
