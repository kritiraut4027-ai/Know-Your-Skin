import re
from typing import List, Dict, Any, Set

# Strict alias definitions for ingredient avoidance (§4.3 of build spec)
AVOIDANCE_PATTERNS: Dict[str, List[str]] = {
    "fragrance": [
        r"\bfragrance\b", r"\bparfum\b", r"\baroma\b", r"\bperfume\b", r"\bscent\b"
    ],
    "sulfates": [
        r"\bsulfate\b", r"\bsulphate\b", r"\blauryl\s+sulfate\b", r"\blaureth\s+sulfate\b",
        r"\bsls\b", r"\bsles\b", r"\bammonium\s+lauryl\s+sulfate\b"
    ],
    "alcohol": [
        r"\balcohol\s+denat\b", r"\bdenatured\s+alcohol\b", r"\bsd\s+alcohol\b",
        r"\bisopropyl\s+alcohol\b", r"\bethanol\b"
    ],
    "essential_oils": [
        r"\blavender\s+oil\b", r"\btea\s+tree\s+oil\b", r"\beucalyptus\b",
        r"\bpeppermint\s+oil\b", r"\bpeel\s+oil\b", r"\bleaf\s+oil\b", r"\bflower\s+oil\b",
        r"\bcitrus\b", r"\blimonene\b", r"\blinalool\b", r"\bgeraniol\b", r"\bcitronellol\b"
    ],
    "parabens": [
        r"\bparaben\b", r"\bmethylparaben\b", r"\bpropylparaben\b",
        r"\bbutylparaben\b", r"\bethylparaben\b", r"\bisobutylparaben\b"
    ]
}

KNOWN_ESSENTIAL_OILS = [
    "lavender", "tea tree", "peppermint", "citrus", "orange", "lemon", "lime",
    "bergamot", "eucalyptus", "rosemary", "ylang ylang", "clove", "cinnamon"
]

def derive_flags(full_ingredient_list: List[str]) -> List[str]:
    """
    Computes purity and safety flags dynamically from an INCI list (§4.3).
    """
    inci_text = " ".join(full_ingredient_list).lower()
    flags = []

    # Check Fragrance
    if not any(re.search(pat, inci_text) for pat in AVOIDANCE_PATTERNS["fragrance"]):
        flags.append("fragrance_free")

    # Check Sulfates
    if not any(re.search(pat, inci_text) for pat in AVOIDANCE_PATTERNS["sulfates"]):
        flags.append("sulfate_free")

    # Check Drying Alcohol
    if not any(re.search(pat, inci_text) for pat in AVOIDANCE_PATTERNS["alcohol"]):
        flags.append("alcohol_free")

    # Check Essential Oils
    has_eo = any(re.search(pat, inci_text) for pat in AVOIDANCE_PATTERNS["essential_oils"])
    if not has_eo:
        flags.append("essential_oil_free")

    # Check Parabens
    if not any(re.search(pat, inci_text) for pat in AVOIDANCE_PATTERNS["parabens"]):
        flags.append("paraben_free")

    return flags

def normalize_token(s: str) -> str:
    """Normalize string for fuzzy substring comparisons."""
    return re.sub(r"[^a-z0-9]", "", s.lower())

def product_contains_avoided_item(product: Dict[str, Any], avoided_item: str) -> bool:
    """
    Checks if a product contains an ingredient the user wants to avoid (§4.3 & §5).
    Scans certified flags, full INCI list, and key active ingredients.
    """
    item_clean = avoided_item.strip().lower()
    if not item_clean:
        return False

    flags = [f.lower() for f in product.get("flags", [])]
    inci_list = product.get("full_ingredient_list", [])
    inci_text = " ".join(inci_list).lower()
    key_ingredients = [k.lower() for k in product.get("key_ingredients", [])]

    # 1. Check known categories
    category_key = None
    if any(k in item_clean for k in ["fragrance", "parfum", "perfume", "scent"]):
        category_key = "fragrance"
        if "fragrance_free" in flags:
            return False
    elif any(k in item_clean for k in ["sulfate", "sulphate", "sls", "sles"]):
        category_key = "sulfates"
        if "sulfate_free" in flags:
            return False
    elif any(k in item_clean for k in ["alcohol", "denat", "ethanol"]):
        category_key = "alcohol"
        if "alcohol_free" in flags:
            return False
    elif any(k in item_clean for k in ["essential oil", "essential_oil", "plant oil"]):
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

    # 2. Check custom avoided ingredient text (free-text "other" avoided ingredient)
    item_pattern = r"\b" + re.escape(item_clean) + r"\b"
    if re.search(item_pattern, inci_text):
        return True

    norm_item = normalize_token(item_clean)
    for k in key_ingredients:
        if norm_item in normalize_token(k):
            return True

    for inci in inci_list:
        if item_clean in inci.lower():
            return True

    return False
