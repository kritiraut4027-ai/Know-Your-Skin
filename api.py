"""
Optional FastAPI Service Wrapper (api.py)
Implements §1A.5 & §14 of build spec: Exposes core Python functions
(recommend, answer) as REST endpoints demonstrating host platform integration.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

from src.catalog import get_default_catalog_provider
from src.matcher import MatchProfile, run_matching_engine
from src.safety import check_for_escalation, MEDICAL_DISCLAIMER, ESCALATION_MESSAGE
from src.explain import generate_explanation
from src.chatbot import answer_question

app = FastAPI(
    title="Know Your Skin & Choose Wisely - Platform API",
    description="E-commerce category integration API for deterministic constraint matching and cited RAG chatbot.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RecommendRequest(BaseModel):
    skin_type: str
    primary_concern: str
    budget_inr: float
    avoided_ingredients: List[str] = Field(default_factory=list)
    free_text_avoid: Optional[str] = ""
    routine_context: Optional[str] = ""
    notes: Optional[str] = ""

class ChatApiRequest(BaseModel):
    query: str
    session_profile: Optional[Dict[str, Any]] = None

@app.get("/health")
def health():
    return {"status": "ok", "service": "know-your-skin-recommender"}

@app.get("/api/products")
def get_catalog():
    catalog = get_default_catalog_provider().get_all_products()
    return {"total": len(catalog), "products": catalog}

@app.post("/api/recommend")
def recommend_products(req: RecommendRequest):
    # 1. SR-3 Clinical Triage on notes & routine
    combined_notes = f"{req.routine_context or ''} {req.notes or ''}".strip()
    should_escalate, symptoms = check_for_escalation(combined_notes)
    if should_escalate:
        sym_str = ", ".join(symptoms)
        return {
            "escalation_triggered": True,
            "escalation_message": ESCALATION_MESSAGE.format(symptoms=sym_str),
            "symptoms_detected": symptoms,
            "top_picks": [],
            "total_passed_filters": 0,
            "disclaimer": MEDICAL_DISCLAIMER
        }

    # 2. Deterministic Matching
    profile = MatchProfile(
        skin_type=req.skin_type,
        primary_concern=req.primary_concern,
        budget_inr=req.budget_inr,
        avoided_ingredients=req.avoided_ingredients,
        free_text_avoid=req.free_text_avoid,
        routine_context=req.routine_context,
        notes=req.notes
    )
    catalog = get_default_catalog_provider().get_all_products()
    result = run_matching_engine(catalog, profile)

    # 3. Constrained Explanations
    picks_payload = []
    for idx, candidate in enumerate(result.picks):
        explanation = generate_explanation(
            product=candidate.product,
            reasons=candidate.reasons,
            variant_index=idx
        )
        p_dict = dict(candidate.product)
        p_dict["match_score"] = candidate.match_score
        p_dict["reasons"] = candidate.reasons
        p_dict["explanation"] = explanation
        picks_payload.append(p_dict)

    return {
        "escalation_triggered": False,
        "top_picks": picks_payload,
        "total_passed_filters": result.total_passed_filters,
        "filter_summary": result.filter_summary,
        "limited_results_warning": result.limited_results_warning,
        "disclaimer": MEDICAL_DISCLAIMER
    }

@app.post("/api/chat")
def chat_endpoint(req: ChatApiRequest):
    res = answer_question(req.query, session_profile=req.session_profile)
    return res
