import pytest
import re
from pathlib import Path
from backend.app.explanation import generate_template_explanation
from backend.app.safety import MEDICAL_DISCLAIMER, ESCALATION_MESSAGE

BANNED_AFFIRMATIVE_WORDS = [
    r"\bwe diagnose\b",
    r"\bwill diagnose\b",
    r"\bdiagnose your\b",
    r"\bwe treat\b",
    r"\bwill treat\b",
    r"\btreat your\b",
    r"\bwill cure\b",
    r"\bcure your\b",
    r"\bcures\b",
    r"\bsafe for your skin\b",
    r"\b100% safe\b",
    r"\bguaranteed to cure\b"
]

def test_template_explanations_have_no_banned_claims():
    """
    SR-1 Requirement: Recommender copy must never promise diagnostic or curative claims.
    """
    mock_product = {
        "product_id": "FW-TEST",
        "name": "Test Gentle Cleanser",
        "brand": "TestBrand",
        "price_inr": 350,
        "flags": ["fragrance_free", "sulfate_free"]
    }
    mock_reasons = {
        "budget_ceiling": 500,
        "skin_type": "sensitive",
        "concern": "dryness",
        "matched_key_ingredients": ["Ceramides", "Glycerin"]
    }

    explanation = generate_template_explanation(mock_product, mock_reasons)
    exp_lower = explanation.lower()

    for banned_regex in BANNED_AFFIRMATIVE_WORDS:
        assert not re.search(banned_regex, exp_lower), (
            f"Banned affirmative claim pattern '{banned_regex}' found in template explanation: '{explanation}'"
        )

def test_disclaimers_maintain_non_diagnostic_framing():
    """
    SR-1 & SR-2: Must explicitly frame as preference matching and disclaim diagnosis.
    """
    assert "non-diagnostic" in MEDICAL_DISCLAIMER.lower() or "not a diagnostic tool" in MEDICAL_DISCLAIMER.lower()
    assert "matches" in MEDICAL_DISCLAIMER.lower() or "preferences" in MEDICAL_DISCLAIMER.lower()
    assert "dermatologist" in MEDICAL_DISCLAIMER.lower()

def test_scan_src_templates_for_banned_claims():
    """
    Scans Python code in src/ and backend/app/ to ensure system prompts and response templates
    never instruct the LLM to make medical claims or declare products '100% safe'.
    """
    root = Path(__file__).resolve().parent.parent
    scan_dirs = [root / "src", root / "backend" / "app"]
    
    for s_dir in scan_dirs:
        if not s_dir.exists():
            continue
        for py_file in s_dir.glob("*.py"):
            content = py_file.read_text(encoding="utf-8").lower()
            # Ensure no system prompt claims the tool can 'cure' or 'treat'
            assert "you diagnose" not in content
            assert "you cure" not in content
            assert "declare it 100% safe" not in content
