import pytest
from backend.app.matcher import MatchProfile, run_matching_engine
from backend.app.data_loader import load_products
from backend.app.explanation import generate_template_explanation

def test_hard_budget_filter():
    catalog = load_products()
    budget = 350.0
    profile = MatchProfile(
        skin_type="oily",
        primary_concern="acne",
        budget_inr=budget,
        avoided_ingredients=[]
    )
    result = run_matching_engine(catalog, profile)
    assert len(result.picks) > 0
    for pick in result.picks:
        assert pick.product["price_inr"] <= budget, f"Product {pick.product['name']} price {pick.product['price_inr']} exceeds budget {budget}"

def test_hard_avoidance_filter_fragrance():
    catalog = load_products()
    profile = MatchProfile(
        skin_type="sensitive",
        primary_concern="dryness",
        budget_inr=1000.0,
        avoided_ingredients=["fragrance"]
    )
    result = run_matching_engine(catalog, profile)
    for pick in result.picks:
        inci_text = " ".join(pick.product["full_ingredient_list"]).lower()
        assert "fragrance" not in inci_text, f"{pick.product['name']} contains fragrance in INCI"
        assert "parfum" not in inci_text, f"{pick.product['name']} contains parfum in INCI"

def test_hard_avoidance_filter_sulfates():
    catalog = load_products()
    profile = MatchProfile(
        skin_type="dry",
        primary_concern="dryness",
        budget_inr=1000.0,
        avoided_ingredients=["sulfates"]
    )
    result = run_matching_engine(catalog, profile)
    for pick in result.picks:
        flags = pick.product.get("flags", [])
        assert "sulfate_free" in flags, f"{pick.product['name']} is not sulfate_free"

def test_tight_budget_no_silent_loosening():
    catalog = load_products()
    # Unreasonably low budget: no face wash in dataset is <= 50 INR
    profile = MatchProfile(
        skin_type="oily",
        primary_concern="acne",
        budget_inr=50.0,
        avoided_ingredients=[]
    )
    result = run_matching_engine(catalog, profile)
    assert len(result.picks) == 0
    assert result.limited_results_warning is not None
    assert "No products" in result.limited_results_warning

def test_explanation_generation_content():
    catalog = load_products()
    sample = catalog[0] # Cetaphil Gentle
    reasons = {
        "concern": "dryness",
        "skin_type": "dry",
        "price_inr": sample["price_inr"],
        "budget_ceiling": 500,
        "matched_key_ingredients": ["Glycerin", "Niacinamide"],
        "flags": sample["flags"]
    }
    explanation = generate_template_explanation(sample, reasons)
    assert len(explanation) > 15
def test_why_not_recommended_explanation():
    from backend.app.rag_engine import process_chat_query
    profile = MatchProfile(
        skin_type="oily",
        primary_concern="acne",
        budget_inr=500.0,
        avoided_ingredients=["fragrance"]
    )
    # Bioderma Sensibio is 890 INR (exceeds budget 500)
    resp = process_chat_query("Why wasn't Bioderma Sensibio Gel Moussant recommended?", session_profile=profile)
    assert "exceeds your stated maximum budget ceiling" in resp["answer"]
    assert "890" in resp["answer"]

