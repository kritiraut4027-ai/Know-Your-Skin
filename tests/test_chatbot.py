import pytest
from src.chatbot import answer_question
from src.retrieval import get_ingredient_retriever

def test_in_scope_ingredient_retrieval_and_citations():
    query = "What does Salicylic Acid do in a cleanser?"
    resp = answer_question(query)
    assert "Salicylic Acid" in resp["answer"]
    assert len(resp["citations"]) > 0
    assert any("CIR" in c or "Journal" in c or "Cosmetic" in c for c in resp["citations"])
    assert resp["escalation"] is False

def test_out_of_scope_ingredient_refusal():
    query = "What are the benefits of snail secretion filtrate and bee venom?"
    resp = answer_question(query)
    assert "could not find a verified match" in resp["answer"].lower()
    assert len(resp["citations"]) == 0
    assert resp["escalation"] is False

def test_clinical_symptom_escalation_in_chat():
    query = "My face is swollen, bleeding, and severely painful."
    resp = answer_question(query)
    assert resp["escalation"] is True
    assert "dermatological" in resp["answer"].lower() or "dermatologist" in resp["answer"].lower()

def test_why_not_product_omission_reasoning():
    session = {
        "budget_inr": 300,
        "avoided_ingredients": ["fragrance"],
        "skin_type": "oily",
        "primary_concern": "acne"
    }
    # Bioderma Sensibio is ₹495 (exceeds ₹300)
    query = "Why wasn't Bioderma Sensibio recommended?"
    resp = answer_question(query, session_profile=session)
    assert "Bioderma" in resp["answer"]
    assert "exceeds your stated budget ceiling" in resp["answer"]
