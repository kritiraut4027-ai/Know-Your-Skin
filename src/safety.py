import re
from typing import Tuple, List, Optional

# SR-3 Red-flag symptoms requiring immediate clinical escalation
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

# SR-4 Clinical medical conditions requiring deflection
MEDICAL_CONDITIONS = [
    "eczema", "psoriasis", "rosacea", "cystic acne", "dermatitis",
    "melasma", "hives", "urticaria", "fungal acne", "herpes", "cold sores"
]

# SR-5 Pregnancy & active conflicts
PREGNANCY_KEYWORDS = [
    r"\bpregnan(t|cy)\b",
    r"\bnursing\b",
    r"\bbreastfeeding\b"
]

# SR-2 Persistent non-diagnostic disclaimer
MEDICAL_DISCLAIMER = (
    "Disclaimer: This platform matches user-stated preferences and budget to publicly listed cosmetic formulations. "
    "It is not a diagnostic tool and does not provide medical advice, diagnosis, or treatments. "
    "Always consult a qualified, board-certified dermatologist for persistent, painful, or clinical skin concerns."
)

PREGNANCY_QUALIFIER = (
    "Note on Pregnancy / Nursing: While topical face washes are rinse-off products, certain actives "
    "(such as high-strength salicylic acid or retinoids) should always be verified with your healthcare provider or OB-GYN."
)

ESCALATION_MESSAGE = (
    "Your description indicates symptoms such as {symptoms}, which may suggest an active clinical condition, "
    "barrier disruption, or infection. Because this tool is strictly non-diagnostic and intended solely for general "
    "cosmetic cleanser selection, we strongly advise consulting a board-certified dermatologist for an in-person assessment "
    "before introducing new topical skincare products."
)

def check_for_escalation(text: Optional[str]) -> Tuple[bool, List[str]]:
    """
    Checks free-text inputs for clinical red flags (SR-3).
    Returns (should_escalate, matched_symptoms).
    """
    if not text:
        return False, []
    
    clean_text = text.lower()
    matched = []
    
    for pattern in ESCALATION_KEYWORDS:
        if re.search(pattern, clean_text):
            if "bleed" in pattern:
                matched.append("bleeding or broken skin")
            elif "pain" in pattern:
                matched.append("pain or tenderness")
            elif "swell" in pattern:
                matched.append("swelling")
            elif "burn" in pattern:
                matched.append("burning sensations")
            elif "blister" in pattern:
                matched.append("blistering")
            elif "spread" in pattern:
                matched.append("spreading symptoms")
            elif "heal" in pattern:
                matched.append("non-healing lesions")
            elif "ooz" in pattern or "pus" in pattern:
                matched.append("oozing or discharge")
            elif "infect" in pattern:
                matched.append("signs of infection")
            elif "crust" in pattern:
                matched.append("crusting")
            elif "rash" in pattern:
                matched.append("severe rash")
            else:
                matched.append(pattern)
                
    unique = list(dict.fromkeys(matched))
    return (len(unique) > 0, unique)

def check_medical_condition_query(text: str) -> Tuple[bool, Optional[str]]:
    """
    Detects if a user query asks whether a cleanser is 'safe' for or treats a medical condition (SR-4).
    """
    text_lower = text.lower()
    for cond in MEDICAL_CONDITIONS:
        if cond in text_lower:
            triggers = ["safe", "cure", "treat", "heal", "good for my", "okay for my", "fix"]
            if any(t in text_lower for t in triggers):
                return True, cond
    return False, None

def check_pregnancy_query(text: str) -> bool:
    """Detects inquiries regarding pregnancy or nursing suitability (SR-5)."""
    text_lower = text.lower()
    return any(re.search(pat, text_lower) for pat in PREGNANCY_KEYWORDS)
