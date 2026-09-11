import re
from typing import Tuple, List, Optional

# Keywords that warrant immediate dermatological escalation (SR-3)
ESCALATION_KEYWORDS = [
    r"\bbleed(ing|s)?\b",
    r"\bpain(ful|fully)?\b",
    r"\bswelling\b",
    r"\bswollen\b",
    r"\bburn(ing|s)?\b",
    r"\bblister(s|ing)?\b",
    r"\bspread(ing)?\b",
    r"\bwon'?t\s+heal\b",
    r"\bnot\s+healing\b",
    r"\booz(ing|e)?\b",
    r"\bpus\b",
    r"\binfect(ion|ed)?\b",
    r"\bcrust(ing|ed)?\b",
    r"\bsevere\s+rash\b",
    r"\bopen\s+wound\b",
    r"\braw\s+skin\b",
    r"\bdeep\s+cut\b"
]

# Medical condition inquiries that require cautious deflection (SR-4)
MEDICAL_CONDITIONS = [
    "eczema", "psoriasis", "rosacea", "cystic acne", "dermatitis",
    "melasma", "hives", "urticaria", "fungal acne", "herpes", "cold sores"
]

MEDICAL_DISCLAIMER = (
    "Disclaimer: This platform matches user-stated preferences and budget to publicly listed cosmetic formulations. "
    "It is not a diagnostic tool and does not provide medical advice or prescribe treatments. "
    "Always consult a qualified, board-certified dermatologist for persistent, painful, or clinical skin concerns."
)

ESCALATION_MESSAGE = (
    "Your description indicates symptoms such as {symptoms}, which may suggest an active skin condition, "
    "barrier disruption, or infection. Because this tool is non-diagnostic and designed solely for general "
    "cosmetic face wash selection, we strongly advise consulting a board-certified dermatologist or medical "
    "practitioner for an in-person assessment before introducing new topical products."
)

def check_for_escalation(text: Optional[str]) -> Tuple[bool, List[str]]:
    """
    Checks free-text user inputs for severe or medical warning keywords.
    Returns (should_escalate, matched_symptoms).
    """
    if not text:
        return False, []
    
    clean_text = text.lower()
    matched = []
    
    for pattern in ESCALATION_KEYWORDS:
        found = re.findall(pattern, clean_text)
        if found:
            # Extract root word for clean user reporting
            root = pattern.replace(r"\b", "").replace("?", "").replace(r"\s+", " ").strip("()|")
            # simplify display names
            if "bleed" in root:
                matched.append("bleeding or broken skin")
            elif "pain" in root:
                matched.append("pain or tenderness")
            elif "swell" in root:
                matched.append("swelling")
            elif "burn" in root:
                matched.append("burning sensations")
            elif "blister" in root:
                matched.append("blistering")
            elif "spread" in root:
                matched.append("spreading symptoms")
            elif "heal" in root:
                matched.append("non-healing lesions")
            elif "ooz" in root or "pus" in root:
                matched.append("oozing or discharge")
            elif "infect" in root:
                matched.append("signs of infection")
            elif "crust" in root:
                matched.append("crusting")
            elif "rash" in root:
                matched.append("severe rash")
            else:
                matched.append(root)
                
    # Deduplicate while preserving order
    unique_matched = list(dict.fromkeys(matched))
    return (len(unique_matched) > 0, unique_matched)

def check_medical_condition_query(text: str) -> Tuple[bool, Optional[str]]:
    """
    Checks if a query asks whether a product is 'safe' or treats a named clinical condition (SR-4).
    """
    text_lower = text.lower()
    for condition in MEDICAL_CONDITIONS:
        if condition in text_lower:
            # Check if intent is asking if it's safe or cures/treats
            if any(term in text_lower for term in ["safe", "cure", "treat", "heal", "good for my", "okay for my"]):
                return True, condition
    return False, None
