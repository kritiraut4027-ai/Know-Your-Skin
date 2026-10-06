import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_api_health_and_catalog():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"

    res_cat = client.get("/api/products")
    assert res_cat.status_code == 200
    assert res_cat.json()["total"] >= 60

def test_api_recommend_deterministic():
    payload = {
        "skin_type": "oily",
        "primary_concern": "acne",
        "budget_inr": 450,
        "avoided_ingredients": ["fragrance"]
    }
    res = client.post("/api/recommend", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["escalation_triggered"] is False
    assert len(data["top_picks"]) >= 3
    for pick in data["top_picks"]:
        assert pick["price_inr"] <= 450
        assert "fragrance" not in " ".join(pick["full_ingredient_list"]).lower()
        assert "explanation" in pick

def test_api_recommend_escalation():
    payload = {
        "skin_type": "sensitive",
        "primary_concern": "sensitivity",
        "budget_inr": 500,
        "notes": "My face has active blisters oozing fluid and burning."
    }
    res = client.post("/api/recommend", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["escalation_triggered"] is True
    assert len(data["top_picks"]) == 0

def test_api_chat():
    res = client.post("/api/chat", json={"query": "What does Niacinamide do in a cleanser?"})
    assert res.status_code == 200
    data = res.json()
    assert "Niacinamide" in data["answer"]
    assert len(data["citations"]) > 0
