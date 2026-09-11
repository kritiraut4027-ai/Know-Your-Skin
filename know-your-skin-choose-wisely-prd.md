# Product Requirements Document
## "Know Your Skin & Choose Wisely" — MVP

| | |
|---|---|
| **Author** | Kritika |
| **Version** | 1.0 (Draft for build) |
| **Status** | Ready to build |
| **Type** | Solo student project — AI/DS portfolio piece |
| **Related work** | Market/competitive research completed (see Appendix A) |

---

### Assumptions & defaults used in this PRD
This document makes a few calls to keep scope buildable. Each is flagged inline where it matters, but the headline ones are:

- **Category for MVP: Face Wash.** It's your own example in the original concept, and cleansers have a small, well-bounded set of decision variables (surfactant type, foaming vs. non-foaming, pH claims, common irritants), which makes for a cleaner v1 than a more complex category like serums.
- **Catalog: a small, hand-curated dataset (60–100 real products), not a live marketplace integration.** Data curation is the actual hard part here, not the AI — scope it accordingly.
- **Stack: Python/FastAPI backend, FAISS for retrieval, Claude API for generation, Streamlit for the MVP UI** (React later if you want a portfolio-polish pass — you've already built a polished frontend for Hamshakal Finder, so that's a known quantity for you, not a risk).
- **Timeline: ~6 weeks part-time**, sequenced so something demoable exists early. Adjust freely — the phase order matters more than the exact dates.

Change any of these and the rest of the document mostly still holds — flag what you want different and I'll adjust.

---

## 1. Overview

"Know Your Skin & Choose Wisely" is a feature that sits inside an existing skincare e-commerce category page (Face Wash, for MVP). Instead of browsing dozens of products with no filter beyond price and star rating, the user answers a short structured questionnaire about their skin type, concern, budget, and any ingredients they want to avoid. The system returns a small set of "Top Picks" from a curated catalog, each with a plain-language explanation of *why* it was picked, and a follow-up chatbot the user can ask ingredient/product questions to.

It is explicitly **not** a diagnostic tool. It matches stated preferences to a catalog — it does not assess skin health or make medical claims.

## 2. Why build this (honest framing, carried over from the research)

This pattern already exists at scale — Sephora's Skincare iQ has run since 2012, Myntra is running an almost identical campaign right now, and Nykaa, L'Oréal, and the big horizontal marketplaces (Amazon, Flipkart, Meesho) all have some version of AI-assisted product discovery live in India today. **This MVP is not being built to be first to market.** It's being built to demonstrate, in a portfolio-grade project, applied judgment on: structured personalization design, when to use an LLM vs. deterministic logic, RAG grounding, and responsible-AI boundaries in a health-adjacent category. The differentiation angle worth leaning into in any writeup or demo: **budget and avoided-ingredients as hard constraints, and a chatbot that cites where its ingredient claims come from** — both genuinely underserved even by the big players, per the competitive research.

## 3. Goals

| Goal | Why it matters |
|---|---|
| Working end-to-end demo (intake → picks → explanation → chat) | This is what gets shown in interviews/portfolio, not slideware |
| Demonstrate RAG grounding done correctly | Retrieval restricted to a verified KB, not general model knowledge — the exact thing separating a toy chatbot from a defensible one |
| Demonstrate responsible-AI judgment | Non-diagnostic language, visible disclosures, escalation logic — shows product maturity beyond "I called an LLM API" |
| Small, clean, well-documented codebase | More valuable for placements than a bigger, messier one |

### Non-Goals (explicitly out of scope for v1)

- ❌ No photo/selfie-based skin analysis — sidesteps the accuracy-and-bias problems documented in the dermatology-AI literature (wide sensitivity variance, weaker performance on darker skin tones)
- ❌ No OCR ingredient-label scanning — even barcode scanning gave Yuka's engineering team real accuracy problems; photographed ingredient text is harder, not easier
- ❌ No live multi-brand marketplace catalog integration
- ❌ No medical claims, diagnosis, or treatment recommendations of any kind
- ❌ No persistent user accounts/login (session-based state is enough for a demo)
- ❌ No multi-language support in v1

## 4. Target Users (from the research segmentation)

1. **The overwhelmed first-timer** — new to skincare, no mental model for ingredients, most helped by structured guidance.
2. **The budget-constrained shopper** — price is their top decision factor; wants picks that respect a stated ceiling, not a post-hoc filter.
3. **The ingredient-cautious shopper** — has specific ingredients to avoid (allergy, past bad reaction, "clean beauty" preference) and currently has to read every label manually to check.

## 5. User Flow

```
1. User searches/browses "Face Wash" category page
2. Banner/entry point: "Know Your Skin & Choose Wisely" → tagline "Your skin, your responsibility."
3. User taps in → 5-6 screen guided questionnaire:
     Q1: Skin type (Oily / Dry / Combination / Sensitive / Not sure)
     Q2: Primary concern for this product (Acne / Dullness / Sensitivity / None in particular)
     Q3: Budget ceiling (free-text or slider, in ₹)
     Q4: Ingredients to avoid (multi-select common list + free-text "other")
     Q5: Current routine context (optional, short free text)
     Q6: Anything else? (optional free text — also functions as the safety-escalation check, see §11)
4. System computes matches against curated catalog (deterministic, see §8.3)
5. Results page: 3-5 "Top Picks," each with:
     - Product name, price, image placeholder
     - 1-2 sentence plain-language "why this was picked"
     - Full ingredient list (collapsible)
6. "Ask about these products" chat entry point
7. RAG chatbot: user asks follow-up questions about ingredients/products, grounded only in curated KB
8. Non-medical-advice footer visible throughout steps 3-7
```

## 6. Functional Requirements

### 6.1 Entry Point
| ID | Requirement | Priority |
|---|---|---|
| FR-1.1 | A banner/card labeled "Know Your Skin & Choose Wisely" appears on the Face Wash category page | P0 |
| FR-1.2 | Tapping it starts the questionnaire in a modal or new screen (no page-context loss) | P0 |

### 6.2 Structured Intake Questionnaire
| ID | Requirement | Priority |
|---|---|---|
| FR-2.1 | Collect: skin type, primary concern, budget ceiling, avoided ingredients (multi-select + free text), current routine (optional), open text field | P0 |
| FR-2.2 | Budget is collected as a hard numeric ceiling, not a vague "low/medium/high" tier | P0 |
| FR-2.3 | Avoided ingredients list includes at minimum: fragrance/parfum, sulfates (SLS/SLES), alcohol (denat.), essential oils, parabens — plus free-text "other" | P0 |
| FR-2.4 | All questions except budget and skin type are skippable | P1 |
| FR-2.5 | Progress indicator shown across steps | P1 |

### 6.3 Recommendation / Matching Engine
| ID | Requirement | Priority |
|---|---|---|
| FR-3.1 | Matching is deterministic/rule-based (attribute filtering + simple scoring), **not** LLM-generated. No LLM call decides which products qualify. | P0 |
| FR-3.2 | Budget is a hard filter: products above the stated ceiling are excluded outright, not just deprioritized | P0 |
| FR-3.3 | Avoided ingredients are a hard filter: any product containing a flagged ingredient is excluded outright | P0 |
| FR-3.4 | Remaining products are ranked by concern-match and skin-type-match score | P0 |
| FR-3.5 | Return top 3–5 results; if fewer than 3 products pass the hard filters, show what's available and say plainly that the strict budget/ingredient combination limited results (do not silently loosen the filters) | P0 |

### 6.4 Explanation Generation (LLM layer #1)
| ID | Requirement | Priority |
|---|---|---|
| FR-4.1 | The LLM receives a **structured prompt** containing only pre-verified match reasons (e.g., `{concern: "acne", matching_ingredient: "salicylic acid", price: 349, budget_ceiling: 500}`) and rephrases it into 1-2 natural sentences | P0 |
| FR-4.2 | The LLM must not introduce any product attribute, claim, or ingredient not present in the structured input | P0 |
| FR-4.3 | Recommended model: a small, cheap model is sufficient here — this is rephrasing, not reasoning (Claude Haiku 4.5 is a good fit for cost) | P1 |

### 6.5 RAG Chatbot (LLM layer #2)
| ID | Requirement | Priority |
|---|---|---|
| FR-5.1 | Chatbot answers are grounded via retrieval against the curated ingredient knowledge base (§7.2) — not the model's general training knowledge | P0 |
| FR-5.2 | If retrieval returns nothing relevant to the question, the chatbot says so explicitly and suggests asking a dermatologist, rather than answering from general knowledge | P0 |
| FR-5.3 | Chatbot can answer: "why wasn't product X recommended," "what does ingredient Y do," "is this suitable for [stated skin type]" | P0 |
| FR-5.4 | Chatbot conversation is scoped to the current session's stated profile (budget, avoided ingredients, skin type) for context | P1 |
| FR-5.5 | Every chatbot response involving ingredient safety/suitability carries a visible "not medical advice" marker | P0 |

### 6.6 Safety & Disclosure Layer
See §11 — treated as its own section given how central it was to the research.

## 7. Data Requirements

### 7.1 Product Catalog Schema
Minimum ~60–100 real Face Wash products, hand-curated from publicly listed ingredient information on brand sites (do not scrape without checking terms; manual entry from published INCI lists is the safe path for a student dataset).

| Field | Type | Example |
|---|---|---|
| `product_id` | string | `FW-014` |
| `name` | string | "Cetaphil Gentle Skin Cleanser" |
| `brand` | string | "Cetaphil" |
| `price_inr` | number | 349 |
| `skin_types` | list | `["dry", "sensitive"]` |
| `concerns_addressed` | list | `["sensitivity", "dryness"]` |
| `key_ingredients` | list | `["glycerin", "niacinamide"]` |
| `full_ingredient_list` | list | (complete INCI list) |
| `flags` | list | `["fragrance_free", "sulfate_free"]` |

### 7.2 Ingredient Knowledge Base Schema
This is what the RAG layer retrieves from. Each entry sourced from a credible reference (e.g., INCI function databases, dermatology-reviewed consumer sources) — not generated by the LLM itself.

| Field | Type | Example |
|---|---|---|
| `ingredient_name` | string | "Salicylic Acid" |
| `function` | string | "Beta-hydroxy acid; exfoliates inside pores, commonly used for acne-prone skin" |
| `common_concerns` | list | `["acne", "blackheads"]` |
| `caution_notes` | string | "Can increase sun sensitivity; avoid combining with other strong exfoliants" |
| `source` | string | Citation for where this entry came from |

**Note:** the `source` field is what enables the "chatbot cites where its claims come from" differentiator — don't skip it even though it's tempting to for MVP speed.

## 8. Technical Architecture

```
┌─────────────────┐      ┌──────────────────────┐
│   Frontend       │──────▶  FastAPI backend      │
│ (Streamlit/React)│      │                        │
└─────────────────┘      │  ┌──────────────────┐  │
                          │  │ Matching engine   │  │  ← deterministic, §6.3
                          │  │ (rules + scoring) │  │
                          │  └────────┬─────────┘  │
                          │           │             │
                          │  ┌────────▼─────────┐  │
                          │  │ Explanation LLM   │  │  ← Claude Haiku 4.5, §6.4
                          │  │ (structured input)│  │
                          │  └──────────────────┘  │
                          │                          │
                          │  ┌──────────────────┐  │
                          │  │ RAG chatbot        │  │
                          │  │ FAISS retrieval +  │  │  ← §6.5
                          │  │ Claude generation  │  │
                          │  └──────────────────┘  │
                          └──────────────┬───────────┘
                                          │
                          ┌───────────────▼──────────────┐
                          │ Curated product + ingredient  │
                          │ dataset (JSON/CSV → embeddings)│
                          └────────────────────────────────┘
```

**Notes:**
- FAISS for the ingredient KB vector index — lightweight, and you've already used it for Hamshakal Finder, so this isn't new ground.
- Keep the matching engine and the LLM calls as separate, independently testable modules. This is the single most important architectural decision from the earlier AI/RAG analysis: the system should work (in a degraded, un-explained way) even with the LLM calls stubbed out, because the *recommendation logic* is deterministic. That separation is also a great thing to point to in an interview — it shows you know where AI adds value and where it doesn't.
- For the explanation layer, consider Claude's structured output / tool-use support to force the model to return the explanation as JSON rather than free text — makes it easier to keep it from wandering off the structured input.

## 9. Responsible AI / Safety Requirements

Carried directly from the research findings on where this category goes wrong:

| ID | Requirement |
|---|---|
| SR-1 | Never use the words "diagnose," "treat," "cure," or "safe for your skin." Use "matches your stated preferences and budget" framing throughout. |
| SR-2 | A visible, persistent disclosure: this tool matches stated preferences to products; it is not medical advice and does not replace a dermatologist. |
| SR-3 | **Escalation logic:** the free-text fields (Q5, Q6) are checked against a small set of concern-pattern keywords (e.g., "painful," "bleeding," "won't heal," "spreading," "burning," "swelling"). If matched, show a message recommending they see a dermatologist, in place of — not in addition to — a product recommendation for that session. |
| SR-4 | The chatbot must decline to confirm a product is "safe" for a named medical condition (e.g., "is this safe for my eczema") and should redirect to professional advice instead. |
| SR-5 | No ingredient-conflict or pregnancy-safety claims without an explicit, visible "verify with a doctor" qualifier attached. |

## 10. Definition of Done (MVP)

Since this is a prototype, not a live product, "success" is functional and evaluative, not a business KPI:

- [ ] Full flow (intake → picks → explanation → chat) runs end to end without manual intervention
- [ ] Hard filters (budget, avoided ingredients) never leak an excluded product into results — test explicitly
- [ ] Explanation text never mentions an attribute absent from the structured input (spot-check ~20 outputs manually)
- [ ] Chatbot declines or deflects on at least 10 test questions outside the curated KB, instead of hallucinating an answer
- [ ] Escalation logic triggers correctly on a test set of ~10 "should escalate" and ~10 "should not escalate" free-text inputs
- [ ] README documents the deterministic-vs-LLM architecture decision explicitly (this is your strongest talking point — write it down)

## 11. Build Plan (assumes ~6 weeks part-time — adjust freely)

| Phase | Focus | Rough time |
|---|---|---|
| 0 | Curate product dataset (60–100 items) + ingredient KB (30–50 entries) | 1.5 weeks |
| 1 | Intake questionnaire UI + deterministic matching engine (no LLM yet) | 1 week |
| 2 | Explanation generation layer (structured prompt → LLM → text) | 3-4 days |
| 3 | RAG chatbot: embed KB, retrieval, grounded generation, fallback handling | 1 week |
| 4 | Safety/escalation layer + disclosure UI | 2-3 days |
| 5 | Polish, README, demo recording/screenshots | 3-4 days |

Phase 0 is intentionally the longest — it's genuinely the hard part, and rushing it is the most common way this kind of project ends up looking hollow in a demo.

## 12. Risks

| Risk | Mitigation |
|---|---|
| Data curation takes longer than planned | It's scoped to one category on purpose — resist the urge to expand categories before the pipeline works on one |
| RAG chatbot hallucinates outside the KB | Explicit fallback response (FR-5.2) tested before demo, not assumed to work |
| Scope creep toward photo-analysis or OCR mid-build | Both are explicitly Non-Goals (§3) — if tempted, add to a "future scope" note instead of the sprint |
| Demo reads as "yet another skincare quiz" | Counter this directly in the pitch/README by naming the competitive landscape and explaining the specific gap this fills (hard constraints + cited chatbot) — see §2 |

## 13. Open Questions (for you to decide before or during build)

1. Confirm Face Wash as the MVP category, or swap to another single category?
2. Deploy publicly (e.g., a hosted demo link) or keep it local + a recorded walkthrough for portfolio purposes?
3. Streamlit for speed, or go straight to a React frontend for a more polished portfolio look?
4. Solo build, or would this suit being submitted to one of the hackathons flagged earlier (Flipkart GRiD / Amazon HackOn) if the timing and track fit?

---

## Appendix A: Research Basis (condensed)

**Problem validation:** Choice overload and ingredient confusion in skincare are documented across multiple independent studies from 2017–2025 (Provoke Insights, Simple's "Simple Truth" report, Label Insight, BeautyMatter, McKinsey *State of Fashion: Beauty 2025*, which surveyed 15,000+ consumers across 13 markets including India). Budget materially affects skincare choice, and India is a market where BCG specifically found stated price sensitivity predicts actual purchasing behavior (unlike many other markets studied).

**Competitive landscape:** The core pattern (questionnaire → personalized picks → explanation) is not new. Sephora's Skincare iQ launched in 2012. Myntra is running a near-identical "Beauty Made Personal" campaign as of mid-2026. Nykaa (Skin Scan) and L'Oréal (Beauty Genius) both ship AI-driven personalization. Separately, Amazon (Rufus), Flipkart (Flippi/SLAP), and Meesho (Vaani) have all launched general-purpose conversational AI shopping assistants in India within the last two years — none with a skincare-specific structured intake, which is the actual remaining gap.

**Differentiation:** Not novelty — precision and explainability. Budget and avoided-ingredients as hard constraints (not passive filters), and a chatbot that cites its sources, were not found combined anywhere in the competitive research. This is the angle to lead with in any writeup.

**Safety grounding:** Curology deliberately keeps AI out of its prescribing decisions, using licensed providers instead — direct industry precedent for keeping this tool non-diagnostic. Dermatology-AI accuracy research shows wide variance and weaker performance on darker skin tones, reinforcing the choice to avoid photo-based analysis in v1. India's ASCI has active 2025–2026 draft guidelines on AI disclosure and health-content credentialing, relevant to how this feature should present itself.

*(Full research detail, citations, and the competitor gap table are in the earlier conversation thread.)*
