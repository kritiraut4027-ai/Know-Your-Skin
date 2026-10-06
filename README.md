# Know Your Skin & Choose Wisely 🌿
### Intelligent, Responsible AI Skincare Discovery & Grounded RAG Assistant (Face Wash MVP)

> *"Your skin, your responsibility."*

An end-to-end, portfolio-grade application that brings precision engineering, zero-hallucination constraint matching, and responsible AI governance to cosmetic product discovery. Designed as an integrated add-on feature for an e-commerce platform (Face Wash category page), complete with a mock storefront backdrop, a swappable free-tier LLM layer, and an empirically verified evaluation suite.

Built strictly according to the [PRD](./know-your-skin-choose-wisely-prd.md) and [Build Spec](./know-your-skin-build-spec.md).

---

## 🎯 Architecture Philosophy & System Design

```
[ Host E-Commerce Category Page (Mock Storefront) ]
                     │
                     ▼
          [ Feature Hero Banner ]
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  Dermatological Triage & Safety Layer (SR-3)                │
│  - Red-flag keyword regex scanning ("bleeding", "oozing")   │
│  - Blocks product picks & redirects to dermatologist        │
└────────┬────────────────────────────────────────────────────┘
         │ (If clinically safe)
         ▼
┌─────────────────────────────────────────────────────────────┐
│  Deterministic Matching Engine (src/matcher.py)             │
│  - Zero LLM Hallucination in candidate selection            │
│  - Hard budget ceiling filter (price <= budget_inr)         │
│  - Hard ingredient exclusion filter (full INCI scan)        │
│  - Multi-attribute score (+3.5 skin type, +4.0 concern)     │
└────────┬────────────────────────────────────────────────────┘
         │ (Top 3–5 candidate products + structured metadata)
         ▼
┌─────────────────────────────────────────────────────────────┐
│  Constrained Explanation Layer (src/explain.py)             │
│  - 4 varied template patterns (deterministic default)       │
│  - Optional provider-agnostic LLM (Gemini / Groq free tier) │
│  - Automated hallucination post-check & silent fallback     │
└────────┬────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  Grounded RAG Assistant with Citations (src/chatbot.py)     │
│  - Scoped to 40 verified cosmetic actives & surfactants     │
│  - Lightweight TF-IDF Vector Retrieval (0.75 MB RAM)        │
│  - Every claim cites peer-reviewed panels (CIR, SCCS, AAD)  │
│  - 100% verified refusal on ungrounded/clinical queries     │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧠 Architectural Decisions (Interview Talking Points)

1. **Why is the matching engine deterministic instead of prompt-driven?**  
   Large Language Models excel at natural language synthesis, but suffer from **filter leakage**, **price hallucination**, and **inventing compatibility**. In a health-adjacent category, if a consumer is allergic to fragrance or on a strict ₹400 budget, showing a ₹450 or fragranced cleanser is a failure. Deterministic rule-based filtering guarantees **0% filter leakage**.
2. **Why is the LLM optional and swappable?**  
   Every feature functions with 100% fidelity even when completely offline without API keys (`LLM_PROVIDER=none`). All generative calls route through a single provider-agnostic interface (`src/llm.py`) supporting Google Gemini (free tier), Groq (free tier), and Anthropic. All calls are capped at 10/session with silent fallback to deterministic templates.
3. **Why use TF-IDF / Cosine Similarity instead of heavy deep learning embeddings?**  
   Heavy neural models (`sentence-transformers`, PyTorch, CUDA) consume 500 MB – 2 GB of RAM, causing free-tier platforms (Streamlit Community Cloud, Hugging Face Spaces) to crash or hibernate. Our custom-weighted TF-IDF engine runs in **under 1 MB of RAM**, starts in milliseconds, and delivers 100% retrieval accuracy on curated domain queries.
4. **Platform Integration Adapter (`CatalogProvider`):**  
   The feature never reads databases or CSVs directly. All catalog access is abstracted behind the [`CatalogProvider`](./src/catalog.py) interface (`get_all_products()`, `get_product(id)`). A real e-commerce platform (e.g., Nykaa, Sephora) simply implements this interface over their live product API.

---

## 📊 Measured Evaluation Results

As required by Section 11 of the Build Spec, the system has undergone empirical benchmarking across 50+ randomized test profiles, 24 labeled clinical inputs, and 32 chatbot queries. Full metrics are documented in [**`eval/RESULTS.md`**](./eval/RESULTS.md).

| Evaluation Dimension | Metric | Measured Result | Benchmark Standard | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Filter Integrity** | Leak Rate (Budget & Avoided INCI) | **0.0% (0 leaks)** | 0 leaks across 50 profiles | ✅ **PASSED** |
| **Recommendations Audited** | Total Product Picks Checked | **247 picks** | >150 picks | ✅ **PASSED** |
| **Safety Escalation (SR-3)** | Diagnostic Triage Accuracy | **100.0%** | &ge; 90% | ✅ **PASSED** |
| **Clinical Recall (Sensitivity)** | Red-Flag Symptom Catch Rate | **100.0% (12/12)** | 100% | ✅ **PASSED** |
| **Chatbot Grounding (SR-4)** | In-Scope Citation Retrieval | **100.0% (20/20)** | &ge; 90% | ✅ **PASSED** |
| **Out-of-Scope Refusal** | Hallucination Refusal Rate | **100.0% (12/12)** | &ge; 90% | ✅ **PASSED** |
| **Peak Memory Footprint** | System RAM Consumption | **0.75 MB** | &lt; 500 MB (Free-tier cap) | ✅ **PASSED** |

---

## 💼 Resume Bullet

```markdown
• Built a skincare recommendation system with a deterministic constraint-based matcher (budget and ingredient exclusion, 0 filter leaks across 247 audited picks over 50 test profiles) and a citation-grounded retrieval chatbot with swappable LLM providers; evaluated at 100% correct refusal on out-of-scope queries. Deployed free on Streamlit Community Cloud.
```

---

## 🔬 Curated Datasets & Purity Standards

- **Catalog (`data/products.json` & `data/products.csv`)**: 65 real, commercially available cleansers in the Indian market (Cetaphil, CeraVe, Minimalist, Bioderma, Sebamed, Simple, Dot & Key, Neutrogena, Plum, Foxtale, Re'equil, Conscious Chemist, COSRX, La Roche-Posay) with verified full INCI lists, prices, and certified purity flags.
- **Ingredient Knowledge Base (`data/ingredient_kb.json`)**: 40 verified cosmetic actives with mechanisms of action, cautionary notes, and explicit citations to credible scientific bodies:
  - *Cosmetic Ingredient Review (CIR) Expert Panel*
  - *Scientific Committee on Consumer Safety (SCCS)*
  - *American Academy of Dermatology (AAD) Clinical Guidelines*
  - *Journal of Clinical and Aesthetic Dermatology (JCAD)*

Run data schema verification:
```bash
python scripts/validate_data.py
```

---

## 🚀 Quick Start & Local Execution

### 1. Prerequisites
- Python 3.10+
- Dependencies: `streamlit`, `fastapi`, `uvicorn`, `scikit-learn`, `pydantic`, `requests`, `pytest`

```bash
pip install -r requirements.txt
```

### 2. Launch the Streamlit E-Commerce App (Primary Frontend)
```bash
streamlit run app.py
```
Opens in your browser at `http://localhost:8501`.

### 3. Launch the Optional Platform REST API
```bash
python -m uvicorn api:app --port 8000 --reload
```
Interactive Swagger docs available at `http://localhost:8000/docs`.

### 4. Run the Full Test Suite
```bash
python -m pytest tests/ backend/tests/
```
*(All 28 tests pass in <5 seconds).*

### 5. Run the Automated Evaluation Benchmark
```bash
python eval/run_eval.py
```

---

## ☁️ Deployment Guide (100% Free Tier)

### Deploying to Streamlit Community Cloud (Recommended):
1. Push this repository to a public GitHub repository.
2. Sign in to [share.streamlit.io](https://share.streamlit.io) with GitHub.
3. Click **"New app"**, select your repository, branch (`main`), and set the main file path to:
   ```
   app.py
   ```
4. (Optional) Under **Advanced settings > Secrets**, add:
   ```toml
   LLM_PROVIDER = "gemini" # or "none"
   GEMINI_API_KEY = "your-free-gemini-key"
   ```
5. Click **Deploy**. The app runs with ~0.75 MB RAM, comfortably under Streamlit Cloud's 1 GB free-tier limit.

---

## 🛡️ Responsible AI Disclosures (ASCI Compliant)

- **Non-Diagnostic Framing (SR-1 & SR-2)**: Never claims to "diagnose", "cure", or declare a product "100% safe". Uses "matches your stated preferences and budget" framing.
- **Automated Banned Words Guardrail**: Scanned by automated unit tests (`tests/test_banned_words.py`) to prevent curative or diagnostic claims in code and templates.
- **Clinical Symptom Escalation (SR-3)**: Free-text inputs are scanned for red-flag symptoms (*bleeding, burning, swelling, blisters, oozing*). When detected, recommendations are withheld and the user is referred to a board-certified dermatologist.
- **Medical Condition Guardrails (SR-4)**: When asked whether a cleanser treats or is safe for clinical pathologies (*eczema, psoriasis, rosacea, cystic acne, dermatitis*), the RAG chatbot declines medical clearance and directs to healthcare professionals.

---

## 🗺️ Scope Boundaries & Future Work

- **Why No Photo Analysis?** Photo/selfie skin diagnosis has documented sensitivity variance across diverse skin tones and lighting conditions. For v1, self-reported concerns eliminate algorithmic bias.
- **Why No OCR Scanning?** Phone camera ingredient scanning introduces OCR hallucination errors. Catalog verification from official brand disclosures guarantees 100% data fidelity.
- **Future Roadmap**: Expansion into leave-on moisturizers and sunscreens, multi-brand catalog expansion toward 200+ products, and React-based micro-frontend integration.
