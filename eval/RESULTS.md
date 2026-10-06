# Empirical Evaluation Results: Know Your Skin & Choose Wisely 📊

> **Evaluation Date:** 2026-10-06 14:09:01 UTC  
> **Target Standard:** Strict adherence to Section 11 of [Build Spec](../know-your-skin-build-spec.md)  
> **Environment:** Python 3.13 | scikit-learn 1.4+ | 0 external GPU/Cloud dependencies  

---

## 1. Summary Scorecard

| Evaluation Dimension | Metric | Measured Result | Target Standard | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Filter Integrity** | Leak Rate (Budget & Avoided INCI) | **0.0% (0 leaks)** | 0 leaks across 50 profiles | ✅ **PASSED** |
| **Safety Escalation (SR-3)** | Diagnostic Triage Accuracy | **100.0%** | &ge; 90% | ✅ **PASSED** |
| **Safety Escalation (SR-3)** | Red-Flag Recall (Sensitivity) | **100.0%** | 100% | ✅ **PASSED** |
| **Chatbot Grounding (SR-4)** | In-Scope Citation Retrieval | **100.0%** | &ge; 90% | ✅ **PASSED** |
| **Out-of-Scope Refusal** | Hallucination Refusal Rate | **100.0%** | &ge; 90% | ✅ **PASSED** |
| **Resource Efficiency** | Peak RAM Consumption | **0.75 MB** | &lt; 500 MB (Free-tier cap) | ✅ **PASSED** |

---

## 2. Filter Integrity & Constraint Enforcement

Tested across **50 randomized user profiles** spanning all 6 skin types, 6 target concerns, budget ceilings from ₹250 to ₹1200, and multi-ingredient avoidance subsets:

- **Total Recommended Products Audited:** 247
- **Budget Exclusions Violated (price > budget):** 0
- **Avoided Ingredients Leaked (INCI / flag presence):** 0
- **Total Leaks:** **0**
- **Filter Leakage Rate:** **0.0%**

### Edge Cases Verified
1. **Impossible Low Budget (₹50):** Returned **0 products** and surfaced an explicit warning message. System refused to silently loosen budget constraints.
2. **Total Common Avoidance (Fragrance + Sulfates + Alcohol + Essential Oils + Parabens):** Returned 5 qualifying formulations with 0 contaminated products.
3. **'Not Sure' Skin Type:** Balanced neutrality correctly applied without scoring penalty.

---

## 3. Dermatological Safety & Clinical Escalation (SR-3)

Evaluated on **24 labeled free-text inputs** (12 clinical red-flag cases vs. 12 clean consumer inputs):

- **True Positives (Red flags correctly caught):** 12 / 12
- **False Negatives (Missed clinical risks):** 0
- **False Positives (Innocent inputs blocked):** 0
- **True Negatives (Clean inputs allowed):** 12 / 12
- **Precision:** 100.0%
- **Recall:** 100.0%
- **Overall Accuracy:** **100.0%**

*Verified: When red-flag symptoms (bleeding, burning, swelling, blisters, oozing) are detected, cosmetic product recommendations are completely withheld and users are directed to consult a board-certified dermatologist.*

---

## 4. Grounded Chatbot Retrieval & Refusal (SR-4)

Evaluated across **32 targeted evaluation queries**:

### In-Scope Active Queries (20 cosmetic actives)
- **Top-1 Knowledge Base Retrieval Hit Rate:** **100.0%** (20/20)
- **Peer-Reviewed Citation Presence Rate:** **100.0%**
- *Verified Bodies Cited:* Cosmetic Ingredient Review (CIR), Scientific Committee on Consumer Safety (SCCS), American Academy of Dermatology (AAD), Journal of Clinical and Aesthetic Dermatology (JCAD).

### Out-of-Scope & Clinical Queries (12 adversarial / out-of-KB inputs)
- **Refusal / Deflection Rate:** **100.0%** (12/12)
- *Deflection Behavior:* When queried on unverified ingredients (e.g., snail mucin, bee venom) or medical condition clearance (e.g., eczema, psoriasis, rosacea), the assistant explicitly refused to fabricate claims and recommended professional medical consultation.

---

## 5. System Footprint & Free-Tier Viability

- **Peak Traced RAM:** **0.75 MB**
- **Hosting Compatibility:** Streamlit Community Cloud (1 GB RAM limit), Hugging Face Spaces (free tier), local laptops.
- **Deep Learning Dependencies:** None. No PyTorch, no CUDA, no heavy neural vector databases.
