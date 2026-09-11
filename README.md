# Know Your Skin & Choose Wisely 🌿
### Intelligent, Responsible AI Skincare Discovery & Grounded RAG Assistant (Face Wash MVP)

> *"Your skin, your responsibility."*

An end-to-end portfolio-grade application that brings precision engineering and responsible AI governance to cosmetic product discovery. Built strictly according to the [Product Requirements Document (PRD)](./know-your-skin-choose-wisely-prd.md).

---

## 🎯 Architecture Philosophy: Deterministic Logic vs. Grounded LLMs

A key design highlight of this system is its deliberate boundary between **deterministic business logic** and **generative AI**:

```
[ User Questionnaire ]
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  Dermatological Triage & Safety Layer (§9 SR-3)             │
│  - Red-flag keyword detection ("bleeding", "swelling", etc.)│
│  - Redirects directly to board-certified dermatologist     │
└────────┬────────────────────────────────────────────────────┘
         │ (If safe)
         ▼
┌─────────────────────────────────────────────────────────────┐
│  Deterministic Matching Engine (§6.3 FR-3.1–3.5)            │
│  - Zero LLM Hallucination in product candidate selection    │
│  - Hard budget ceiling filter (price <= budget_inr)         │
│  - Hard avoided ingredient exclusion filter (full INCI scan)│
│  - Transparent multi-attribute scoring                      │
└────────┬────────────────────────────────────────────────────┘
         │ (Top 3–5 candidate products + structured metadata)
         ▼
┌─────────────────────────────────────────────────────────────┐
│  Constrained Explanation Layer (§6.4 FR-4.1–4.3)            │
│  - Structured prompt receiving ONLY verified match reasons  │
│  - Generates 1–2 natural plain-language sentences           │
│  - Prohibited from inventing ungrounded claims              │
└────────┬────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  Grounded RAG Assistant with Source Citations (§6.5)        │
│  - Scoped exclusively to 40+ verified ingredient entries    │
│  - Vector search using TF-IDF / Cosine Similarity           │
│  - Every claim cites peer-reviewed sources (CIR, SCCS, etc.)│
│  - Explicit deflection on unknown ingredients or medical    │
│    condition queries (SR-4)                                 │
└─────────────────────────────────────────────────────────────┘
```

### Why Not Let an LLM Pick the Products?
Large Language Models excel at natural language synthesis and rephrasing, but are prone to **filter leakage**, **price hallucination**, and **inventing nonexistent ingredient compatibility**. In a health-adjacent category like skincare:
1. **Hard Constraints Must Be Invariable**: If a consumer is allergic to fragrance or on a strict ₹400 budget, showing a ₹450 or fragranced product is a failure. Deterministic rule-based filtering guarantees 0% filter leakage.
2. **Transparent Explainability**: Every recommendation is computed from verified skin type compatibility and target concerns before any natural language is generated.
3. **Graceful Degradation**: The system functions with 100% fidelity even when offline or without external API keys via local deterministic template generators.

---

## 🔬 Curated Datasets

- **Curated Product Catalog (`data/products.json`)**:
  - 65 real, commercially available Face Wash products in the Indian market (Cetaphil, CeraVe, Minimalist, The Derma Co, Bioderma, Sebamed, Simple, Dot & Key, Neutrogena, Plum, Foxtale, Re'equil, Conscious Chemist, COSRX, La Roche-Posay, etc.).
  - Includes full INCI ingredient lists, price in INR, skin types, targeted concerns, active ingredients, and certified flags (`fragrance_free`, `sulfate_free`, `alcohol_free`, `essential_oil_free`, `paraben_free`).

- **Verified Ingredient Knowledge Base (`data/ingredient_kb.json`)**:
  - 40 verified cosmetic actives and functional surfactants (Salicylic Acid, Niacinamide, Hyaluronic Acid, Ceramides, Zinc PCA, Centella Asiatica, Glycolic Acid, Panthenol, Colloidal Oatmeal, Allantoin, Azelaic Acid, Squalane, etc.).
  - Each entry includes cosmetic function, target concerns, cautionary guidance, and explicit citations to credible bodies:
    - *Cosmetic Ingredient Review (CIR) Expert Panel*
    - *Journal of Clinical and Aesthetic Dermatology*
    - *British Journal of Dermatology*
    - *Scientific Committee on Consumer Safety (SCCS)*
    - *American Academy of Dermatology (AAD) Clinical Guidelines*

---

## 🛡️ Responsible AI & Safety Standards

Implemented in compliance with Indian ASCI guidelines and medical disclosure ethics:
- **Non-Diagnostic Framing (SR-1 & SR-2)**: Never claims to "diagnose", "cure", or declare a product "100% safe". Uses "matches your stated preferences and budget" framing.
- **Dermatological Triage Escalation (SR-3)**: Free-text inputs (routine context & notes) are analyzed for clinical red-flag symptoms (*bleeding, painful, burning, swelling, spreading, oozing, open wound, blisters*). If detected, product recommendations are withheld and the user is directed to consult a board-certified dermatologist.
- **Medical Condition Guardrails (SR-4)**: When asked whether a cleanser treats or is safe for clinical pathologies (*eczema, psoriasis, rosacea, cystic acne, dermatitis*), the RAG chatbot declines to give medical clearance and recommends clinical consultation.
- **Verified Source Citations**: Every RAG answer cites the governing cosmetic review panel or peer-reviewed journal.

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10+
- Dependencies: `fastapi`, `uvicorn`, `scikit-learn`, `pydantic`, `pandas`, `requests`, `pytest`

### 2. Run the Application
From the project root:
```bash
python -m uvicorn backend.app.main:app --port 8000 --reload
```
Open your browser and navigate to:
```
http://localhost:8000
```
The full interactive single-page application will be served directly by FastAPI.

### 3. Run Automated Tests
```bash
python -m pytest backend/tests -v
python backend/tests/test_e2e_api.py
```

---

## 🧪 Verification Matrix

| Test Suite | Coverage | Status |
|---|---|---|
| `test_hard_budget_filter` | Verifies 0% price leakage above stated ceiling | ✅ PASSED |
| `test_hard_avoidance_filter_fragrance` | Scans INCI for fragrance/parfum and certifies exclusion | ✅ PASSED |
| `test_hard_avoidance_filter_sulfates` | Ensures sulfate exclusion against flags and detergents | ✅ PASSED |
| `test_tight_budget_no_silent_loosening` | Verifies warning is shown without loosening filters when budget is tight | ✅ PASSED |
| `test_explanation_generation_content` | Validates plain-language non-diagnostic match rationale | ✅ PASSED |
| `test_why_not_recommended_explanation` | Evaluates 'Why wasn't Product X recommended?' against user session rules | ✅ PASSED |
| `test_safety_escalation_triggers` | 10 clinical red-flag test inputs trigger medical triage | ✅ PASSED |
| `test_safety_escalation_clean_inputs` | 10 normal cosmetic inputs pass without false alarms | ✅ PASSED |
| `test_medical_condition_deflection` | Checks medical condition queries (eczema, psoriasis) redirect to physician | ✅ PASSED |
| `test_out_of_kb_deflection` | 10 out-of-scope ingredient queries gracefully deflect without hallucination | ✅ PASSED |
| `test_e2e_api.py` | Full end-to-end integration across static assets, catalog, intake, and chat | ✅ PASSED |

---

## 📂 Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── config.py           # Configuration and environment setup
│   │   ├── data_loader.py      # Cached access to products and ingredient KB
│   │   ├── explanation.py      # Grounded 1-2 sentence rationale generator
│   │   ├── matcher.py          # Deterministic matching engine (FR-3.1–3.5)
│   │   ├── rag_engine.py       # Grounded RAG chatbot with source citations
│   │   ├── safety.py           # Clinical triage, red-flags, and disclaimers
│   │   └── main.py             # FastAPI server exposing API & static UI
│   └── tests/
│       ├── test_matcher.py     # Deterministic filter & ranking unit tests
│       ├── test_safety.py      # Safety triage & RAG deflection unit tests
│       └── test_e2e_api.py     # End-to-end integration test runner
├── data/
│   ├── build_data.py           # Dataset curation script
│   ├── products.json           # 65 curated face wash products with full INCI
│   └── ingredient_kb.json      # 40 verified ingredients with scientific citations
├── frontend/
│   ├── index.html              # Modern, accessible e-commerce discovery UI
│   ├── styles.css              # Editorial apothecary design tokens & glassmorphism
│   └── app.js                  # 6-step intake wizard, live triage, RAG drawer
├── know-your-skin-choose-wisely-prd.md
└── README.md
```
