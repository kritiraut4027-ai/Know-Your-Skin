import requests
import json

BASE = "http://127.0.0.1:8000"

def test_static_assets():
    # 1. Test index.html
    r = requests.get(f"{BASE}/")
    assert r.status_code == 200
    assert "Know Your Skin & Choose Wisely" in r.text
    assert "Your skin, your responsibility." in r.text
    
    # 2. Test styles.css
    r_css = requests.get(f"{BASE}/styles.css")
    assert r_css.status_code == 200
    assert "--primary:" in r_css.text

    # 3. Test app.js
    r_js = requests.get(f"{BASE}/app.js")
    assert r_js.status_code == 200
    assert "submitIntakeProfile" in r_js.text

def test_api_catalog():
    r = requests.get(f"{BASE}/api/products")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] >= 60

def test_api_recommend_success():
    payload = {
        "skin_type": "oily",
        "primary_concern": "acne",
        "budget_inr": 400,
        "avoided_ingredients": ["fragrance"]
    }
    r = requests.post(f"{BASE}/api/recommend", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["escalation_triggered"] is False
    assert len(data["top_picks"]) >= 3
    for pick in data["top_picks"]:
        assert pick["price_inr"] <= 400
        assert "fragrance" not in " ".join(pick["full_ingredient_list"]).lower()
        assert "explanation" in pick

def test_api_recommend_escalation():
    payload = {
        "skin_type": "sensitive",
        "primary_concern": "sensitivity",
        "budget_inr": 500,
        "avoided_ingredients": [],
        "routine_context": "",
        "notes": "My cheek is bleeding and extremely painful after washing."
    }
    r = requests.post(f"{BASE}/api/recommend", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["escalation_triggered"] is True
    assert len(data["top_picks"]) == 0
    assert "bleeding" in " ".join(data["symptoms_detected"])

def test_api_chat_rag():
    # 1. Active ingredient query with citations
    r = requests.post(f"{BASE}/api/chat", json={"query": "What does Salicylic Acid do in a cleanser?"})
    assert r.status_code == 200
    data = r.json()
    assert "Salicylic Acid" in data["answer"]
    assert len(data["citations"]) > 0
    assert "Non-diagnostic" in data["disclaimer"] or "Disclaimer" in data["disclaimer"]

    # 2. Safety escalation in chat
    r_esc = requests.post(f"{BASE}/api/chat", json={"query": "My skin has severe swelling and won't heal."})
    assert r_esc.status_code == 200
    assert r_esc.json()["escalation"] is True
    assert "dermatologist" in r_esc.json()["answer"].lower()

if __name__ == "__main__":
    test_static_assets()
    print("[OK] Static assets verified")
    test_api_catalog()
    print("[OK] Catalog API verified")
    test_api_recommend_success()
    print("[OK] Recommendations API verified")
    test_api_recommend_escalation()
    print("[OK] Safety escalation API verified")
    test_api_chat_rag()
    print("[OK] Grounded RAG Chatbot API verified")
    print("ALL E2E API & STATIC ASSETS TESTS PASSED!")

