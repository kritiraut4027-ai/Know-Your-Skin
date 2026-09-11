from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

from .data_loader import load_products, load_ingredient_kb, get_product_by_id
from .matcher import MatchProfile, run_matching_engine
from .safety import check_for_escalation, ESCALATION_MESSAGE, MEDICAL_DISCLAIMER
from .explanation import generate_explanation
from .rag_engine import process_chat_query

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI(
    title="Know Your Skin & Choose Wisely API",
    description="Responsible AI skincare discovery and grounded RAG ingredient assistant for cleansers.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "frontend"


class RecommendResponse(BaseModel):
    escalation_triggered: bool = False
    escalation_message: Optional[str] = None
    symptoms_detected: List[str] = Field(default_factory=list)
    top_picks: List[Dict[str, Any]] = Field(default_factory=list)
    total_passed_filters: int = 0
    filter_summary: Dict[str, Any] = Field(default_factory=dict)
    limited_results_warning: Optional[str] = None
    disclaimer: str = MEDICAL_DISCLAIMER

class ChatRequest(BaseModel):
    query: str
    session_profile: Optional[MatchProfile] = None

class ChatResponse(BaseModel):
    answer: str
    citations: List[str] = Field(default_factory=list)
    disclaimer: str
    escalation: bool = False

class TriageRequest(BaseModel):
    text: str

class TriageResponse(BaseModel):
    should_escalate: bool
    symptoms: List[str]
    message: Optional[str] = None

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Know Your Skin & Choose Wisely",
        "category": "Face Wash"
    }

@app.get("/api/products")
def get_products(
    skin_type: Optional[str] = None,
    concern: Optional[str] = None,
    max_price: Optional[float] = None
):
    catalog = load_products()
    results = catalog
    if max_price is not None:
        results = [p for p in results if p.get("price_inr", 0) <= max_price]
    if skin_type:
        st_clean = skin_type.lower()
        results = [p for p in results if st_clean in [s.lower() for s in p.get("skin_types", [])] or "all" in [s.lower() for s in p.get("skin_types", [])]]
    if concern:
        c_clean = concern.lower()
        results = [p for p in results if any(c_clean in c.lower() for c in p.get("concerns_addressed", []))]
    return {"total": len(results), "products": results}

@app.get("/api/products/{product_id}")
def get_product(product_id: str):
    product = get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.get("/api/ingredients")
def get_ingredients():
    kb = load_ingredient_kb()
    return {"total": len(kb), "ingredients": kb}

@app.post("/api/triage-check", response_model=TriageResponse)
def triage_check(req: TriageRequest):
    should_escalate, symptoms = check_for_escalation(req.text)
    msg = None
    if should_escalate:
        msg = ESCALATION_MESSAGE.format(symptoms=", ".join(symptoms))
    return TriageResponse(should_escalate=should_escalate, symptoms=symptoms, message=msg)

@app.post("/api/recommend", response_model=RecommendResponse)
def recommend_products(profile: MatchProfile):
    # Step 1: Safety & Triage check on free-text inputs (SR-3)
    combined_free_text = f"{profile.routine_context or ''} {profile.notes or ''}"
    should_escalate, symptoms = check_for_escalation(combined_free_text)
    
    if should_escalate:
        msg = ESCALATION_MESSAGE.format(symptoms=", ".join(symptoms))
        return RecommendResponse(
            escalation_triggered=True,
            escalation_message=msg,
            symptoms_detected=symptoms,
            top_picks=[],
            total_passed_filters=0,
            filter_summary={"status": "escalated_to_medical_professional"},
            limited_results_warning="Recommendation halted due to symptoms requiring physician assessment."
        )
        
    # Step 2: Deterministic Matching Engine (FR-3.1 to FR-3.5)
    catalog = load_products()
    match_result = run_matching_engine(catalog, profile)
    
    # Step 3: Explanation generation for top picks (FR-4.1)
    enriched_picks = []
    for candidate in match_result.picks:
        explanation = generate_explanation(candidate.product, candidate.reasons)
        pick_dict = {
            **candidate.product,
            "match_score": candidate.match_score,
            "match_reasons": candidate.reasons,
            "explanation": explanation
        }
        enriched_picks.append(pick_dict)
        
    return RecommendResponse(
        escalation_triggered=False,
        top_picks=enriched_picks,
        total_passed_filters=match_result.total_passed_filters,
        filter_summary=match_result.filter_summary,
        limited_results_warning=match_result.limited_results_warning
    )

@app.post("/api/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    result = process_chat_query(req.query, req.session_profile)
    return ChatResponse(
        answer=result.get("answer", ""),
        citations=result.get("citations", []),
        disclaimer=result.get("disclaimer", MEDICAL_DISCLAIMER),
        escalation=result.get("escalation", False)
    )

# Mount frontend UI assets
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")

