import pytest
from src.explain import (
    generate_template_explanation, 
    audit_explanation_for_hallucinations,
    generate_explanation
)
from src.llm import LLMSessionTracker, LLMUnavailable

def test_template_variants_produce_distinct_copy():
    mock_prod = {
        "name": "Gentle Cleanser",
        "brand": "Cetaphil",
        "price_inr": 349,
        "key_ingredients": ["glycerin", "niacinamide"]
    }
    reasons = {
        "budget_ceiling": 500,
        "skin_type": "dry",
        "concern": "dryness",
        "matched_key_ingredients": ["Glycerin", "Niacinamide"]
    }

    t0 = generate_template_explanation(mock_prod, reasons, variant_index=0)
    t1 = generate_template_explanation(mock_prod, reasons, variant_index=1)
    t2 = generate_template_explanation(mock_prod, reasons, variant_index=2)

    assert "349" in t0 and "500" in t0
    assert "dry" in t0.lower()
    # Ensure variants are not identical
    assert t0 != t1
    assert t1 != t2

def test_hallucination_auditor_detects_unlisted_ingredients():
    mock_prod = {
        "name": "Hydrating Cleanser",
        "brand": "CeraVe",
        "price_inr": 490,
        "key_ingredients": ["ceramides", "hyaluronic_acid"],
        "full_ingredient_list": ["Water", "Glycerin", "Ceramide NP", "Sodium Hyaluronate"]
    }
    reasons = {
        "budget_ceiling": 600,
        "skin_type": "dry",
        "concern": "dryness",
        "matched_key_ingredients": ["Ceramides", "Hyaluronic Acid"]
    }

    # Case 1: Grounded text (should pass)
    grounded_text = "Picked for dry skin because it features Ceramides to help barrier hydration within your 600 budget."
    assert audit_explanation_for_hallucinations(grounded_text, mock_prod, reasons) is True

    # Case 2: Hallucinated ingredient (e.g. Retinol or Salicylic Acid not in formulation)
    hallucinated_text = "Features active Retinol and Salicylic Acid to brighten dull skin under 600."
    assert audit_explanation_for_hallucinations(hallucinated_text, mock_prod, reasons) is False

def test_silent_fallback_when_llm_unavailable():
    mock_prod = {
        "name": "Gentle Wash",
        "brand": "BrandX",
        "price_inr": 250,
        "key_ingredients": ["glycerin"]
    }
    reasons = {
        "budget_ceiling": 300,
        "skin_type": "sensitive",
        "concern": "none",
        "matched_key_ingredients": []
    }
    # LLM_PROVIDER is unset or none by default; should seamlessly return template without error
    result = generate_explanation(mock_prod, reasons)
    assert "250" in result
    assert "300" in result
