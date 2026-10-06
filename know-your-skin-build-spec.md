# Build Spec: "Know Your Skin & Choose Wisely"
**For:** Antigravity (AI coding agent) | **Owner:** Kritika | **Type:** Solo student portfolio project (AI & Data Science)

Read this whole document first. Then build in the phase order given in Section 12. Ask the owner before deviating from the constraints in Sections 2 and 3.

---

## 1. What we are building

A face-wash recommender with a small, hand-curated catalog. The user answers a short questionnaire (skin type, concern, budget in INR, ingredients to avoid). The system returns 3-5 "Top Picks" with a plain-language reason for each, then offers a chatbot for ingredient and product questions that answers only from a curated, cited knowledge base.

It is **not** a diagnostic tool. It matches stated preferences to a catalog. It makes no medical claims.

**Why it exists (portfolio angle):** to show good judgment about where an LLM belongs and where it does not. The differentiators are:
1. **Budget and avoided ingredients are hard constraints**, not passive filters.
2. **The chatbot cites its sources** and refuses when the knowledge base has no answer.
3. **The system works with no LLM at all**, and the LLM is swappable across providers.
4. **It is evaluated**, with reported numbers, not just demoed.

---

## 1A. Platform context: this is a FEATURE inside an e-commerce site, not a standalone app

"Know Your Skin & Choose Wisely" is an add-on feature for an existing skincare e-commerce platform. In the real world it would sit on the **Face Wash category page**, next to the normal product grid, search, and filters. The user enters it from a banner on that page, gets recommendations, and then continues shopping on the same platform.

Because we do not have access to a real platform, the demo must **simulate the host site** and show the feature plugged into it:

1. **Mock storefront (host site):** a simple Face Wash category page built from the same catalog. It shows a product grid (name, brand, price, image placeholder, "View product" and "Add to cart" buttons that do nothing real), plus the usual price sort. This is only a backdrop. Keep it minimal.
2. **Entry point:** the "Know Your Skin & Choose Wisely" banner sits at the top of that category page. Clicking it opens the feature **in a modal/panel or a sub-page that keeps the category-page context** (the user can return to the grid at any time).
3. **Results look like the platform's own product cards.** Top Picks reuse the same card component as the storefront grid, with an added "Why this was picked" line. They should feel native, not bolted on.
4. **Catalog adapter (important):** the feature must never read the catalog directly. All catalog access goes through a `CatalogProvider` interface in `src/catalog.py` with two methods, `get_all_products()` and `get_product(product_id)`. For the demo, implement `CsvCatalogProvider` reading `data/products.csv`. A real platform would implement the same interface over its product API or database. State this in the README as the integration point.
5. **Thin service API (optional, not deployed):** expose the core logic as plain Python functions first (`recommend(profile)`, `answer(question, session)`). Then add an optional FastAPI wrapper in `api.py` with `POST /recommend` and `POST /chat`, so it is clear how a real platform's frontend would call it. The Streamlit app calls the Python functions directly. Do not deploy the FastAPI wrapper (keeps hosting free and simple), but include it with a couple of tests and document it in the README.
6. **Platform-realistic behaviors to respect:**
   - Products shown in picks must come from the same catalog as the storefront (same IDs, names, prices), so the picks are consistent with what the shopper sees on the page.
   - "View product" on a pick should navigate to or highlight that product on the mock storefront.
   - Respect the platform's existing page: do not take over the whole site, and keep the disclosure footer visible within the feature.
7. **What is deliberately NOT simulated:** real cart, checkout, payment, user accounts, inventory, order history, reviews. Do not build these.

---

## 2. Non-negotiable design principles

1. **Deterministic core.** The matching engine is plain Python rules and scoring. No LLM ever decides which products qualify or rank.
2. **LLM is optional.** Every feature must work in a no-LLM mode. The LLM only rephrases text that the deterministic layers already produced.
3. **Provider-agnostic.** All LLM calls go through one function/interface (Section 7). No provider SDK is imported anywhere else.
4. **Free to run.** Hosting must be free. The LLM mode must work on a free-tier API. Do not make a paid API a required dependency.
5. **Small memory footprint.** The deployed app must stay comfortably under ~500 MB RAM. Do **not** use PyTorch or `sentence-transformers`.
6. **Separate, testable modules.** Matching, explanation, retrieval, chatbot, safety, and UI are independent modules with their own tests.
7. **Never fabricate data.** See Section 4. Product and ingredient data are entered by the owner from public sources. The agent builds the scaffolding and validators, and does **not** invent real product names, prices, or ingredient lists.

## 3. Non-goals (do not build)

- No photo/selfie skin analysis.
- No OCR or barcode ingredient scanning.
- No live marketplace/scraping integration.
- No medical claims, diagnosis, or treatment advice.
- No user accounts or login (session state only).
- No multi-language support.
- No categories other than Face Wash.
- No real cart, checkout, payments, inventory, or reviews. The storefront is a mock backdrop only (see Section 1A).

---

## 4. Data (owner supplies the content; agent builds the structure)

### 4.1 Product catalog: `data/products.csv` (or `.json`)

Target: 25 products for the demo, growing toward 60-100 later. Entered manually from brand-published ingredient lists.

| Field | Type | Example |
|---|---|---|
| `product_id` | string | `FW-014` |
| `name` | string | (real product name) |
| `brand` | string | |
| `price_inr` | number | 349 |
| `skin_types` | list | `["dry","sensitive"]` |
| `concerns_addressed` | list | `["sensitivity","dryness"]` |
| `key_ingredients` | list | `["glycerin","niacinamide"]` |
| `full_ingredient_list` | list | complete INCI list |
| `flags` | list | derived in code, see 4.3 |
| `source_url` | string | page the ingredient list came from |

Allowed `skin_types`: `oily, dry, combination, sensitive`.
Allowed concerns: `acne, dullness, sensitivity, dryness, none`.

### 4.2 Ingredient knowledge base: `data/ingredients_kb.json`

Target: 30 entries for Phase 2. Each entry must come from a credible reference, never generated by an LLM.

| Field | Type | Example |
|---|---|---|
| `ingredient_name` | string | "Salicylic Acid" |
| `aliases` | list | `["BHA","beta hydroxy acid"]` |
| `function` | string | what it does, in plain words |
| `common_concerns` | list | `["acne","blackheads"]` |
| `caution_notes` | string | e.g. may increase sun sensitivity |
| `source` | string | citation or URL (required, no empty values) |

### 4.3 Derived flags (computed in code, not typed by hand)

Compute flags from `full_ingredient_list` using an alias map in `src/ingredient_aliases.py`:

| Avoid option | Matches (case-insensitive substring/alias) |
|---|---|
| fragrance/parfum | fragrance, parfum, aroma |
| sulfates | sodium lauryl sulfate, sodium laureth sulfate, SLS, SLES, ammonium lauryl sulfate |
| alcohol (denat.) | alcohol denat, denatured alcohol, SD alcohol |
| essential oils | any ingredient containing "oil" that is a known essential oil from a maintained list (e.g. lavender, tea tree, peppermint, citrus/orange, eucalyptus) |
| parabens | methylparaben, ethylparaben, propylparaben, butylparaben, any "*paraben" |

Free-text "other" avoided ingredients are matched by normalized substring against `full_ingredient_list`.

### 4.4 Data tooling the agent should build

- `scripts/validate_data.py`: checks required fields, allowed values, no empty `source`, no duplicate IDs, prices are positive numbers. Fails loudly.
- `data/products_template.csv` with headers and **one clearly marked fake placeholder row** (`FW-000, "EXAMPLE ONLY"`) so tests can run. The placeholder must be removable and must never ship in the final dataset.
- A short `DATA_GUIDE.md` telling the owner how to enter a product and where to find INCI lists on brand sites. Do not scrape sites.

---

## 5. Matching engine: `src/matcher.py` (Phase 1, no LLM)

Input: a `UserProfile` (skin_type, concern, budget_inr, avoid_list, free_text_avoid).

Algorithm:
1. **Hard filter, budget:** exclude products with `price_inr > budget_inr`.
2. **Hard filter, ingredients:** exclude any product whose ingredient list matches any avoided ingredient (via alias map and free-text substring match).
3. **Score** remaining products:
   - Skin-type match: +3 if user's type is in `skin_types`. If user picked "Not sure", skip this term.
   - Concern match: +3 if the concern is in `concerns_addressed`. If concern is "none", skip.
   - Optional tiebreak: lower price ranks higher.
4. Return top 3-5, sorted by score then price.
5. **If fewer than 3 products survive the hard filters**, return what exists plus a plain message stating that the strict budget/ingredient combination limited the results. **Never silently loosen filters.**
6. The function returns structured match reasons per product, e.g.
   `{product_id, score, reasons: {skin_type_match: True, concern_match: "acne", matching_ingredients: ["salicylic acid"], price: 349, budget: 500}}`.
   These reasons are the only input to the explanation layer.

---

## 6. Explanation layer: `src/explain.py`

Two modes, same input (the structured reasons from Section 5):

- **Template mode (default, free, no LLM):** fill a template, e.g.
  "Picked for {skin_type} skin and {concern}: contains {ingredient}. ₹{price}, within your ₹{budget} budget."
  Write 3-4 template variants so results do not all read identically.
- **LLM mode (optional):** send the structured reasons to `generate()` and ask for 1-2 natural sentences. The prompt must state: use only the facts provided; do not add any ingredient, claim, or attribute not in the input. Request JSON output and parse it. On any failure or malformed output, **fall back to template mode silently**.

Add a post-check: if the LLM text mentions an ingredient name not in the structured input, discard it and use the template.

---

## 7. LLM abstraction: `src/llm.py`

One public function: `generate(prompt: str, system: str | None = None, json_mode: bool = False) -> str`.

- Provider selected by environment variable `LLM_PROVIDER` = `none | gemini | groq | anthropic` (default `none`).
- Free-tier options to implement first: **Google Gemini** and **Groq**. Anthropic is an optional extra provider, never required. The owner must confirm current free-tier availability and limits on each provider's own page.
- Keys are read from environment variables or Streamlit secrets. **Never commit keys.** Include `.env.example`.
- Handle timeouts, rate-limit errors, and empty responses by raising a typed `LLMUnavailable` exception that callers catch to fall back to no-LLM behavior.
- **Per-session cap:** maximum 10 LLM calls per session (configurable). After that, auto-switch to no-LLM mode with a small notice.
- **Bring-your-own-key option:** a sidebar field where a viewer can paste their own key to enable LLM mode for their session only. Keep it in session state only. Never log or store it.
- No other module may import a provider SDK.

---

## 8. Chatbot: `src/retrieval.py` and `src/chatbot.py` (Phase 2)

### 8.1 Retrieval
- Corpus: `ingredients_kb.json` (plus product facts from the catalog for "why wasn't X recommended" questions).
- Implement a `Retriever` interface with two interchangeable backends:
  1. **BM25** (`rank_bm25`) or TF-IDF (scikit-learn) as the default. Tiny and fast.
  2. **`fastembed` (ONNX) + FAISS** as an optional upgrade.
- Do not use PyTorch or `sentence-transformers`.
- Return top-k entries with scores. Apply a **relevance threshold**: if the best score is below it, treat the query as "not in the knowledge base."

### 8.2 Behavior
- **No-LLM mode (default):** show the retrieved KB entries as a formatted answer with the `source` shown for each. This is the retrieval-only grounded chatbot.
- **LLM mode:** pass only the retrieved entries as context to `generate()` and instruct it to answer only from that context, cite the source, and say so if the context does not answer the question. Fall back to no-LLM mode on any failure.
- **Out-of-KB fallback (required):** if retrieval is below the threshold, reply that this is not in the knowledge base and suggest asking a dermatologist. Never answer from general model knowledge.
- Supported question types: "what does ingredient Y do", "why wasn't product X recommended" (answered from the deterministic matcher's filter results, not from the LLM), "is this suitable for my stated skin type" (answered only in terms of the stated profile and catalog tags).
- Scope the conversation to the session profile (budget, avoided ingredients, skin type).
- Every answer touching ingredient safety/suitability shows the visible "not medical advice" marker.

---

## 9. Safety and responsible-AI layer: `src/safety.py`

| ID | Requirement |
|---|---|
| SR-1 | Never output the words "diagnose," "treat," "cure," or "safe for your skin." Use "matches your stated preferences and budget" framing. Add a unit test that scans all templates and prompts for banned words. |
| SR-2 | A visible, persistent disclosure on every screen: this tool matches stated preferences to products, is not medical advice, and does not replace a dermatologist. |
| SR-3 | **Escalation:** free-text fields (routine, "anything else") are checked against concern patterns such as "painful", "bleeding", "won't heal", "spreading", "burning", "swelling", "pus", "rash". If matched, show a message recommending a dermatologist **in place of** product recommendations for that session. Keep patterns in a config list. |
| SR-4 | The chatbot must decline to confirm a product is "safe" for a named medical condition (e.g. "is this safe for my eczema") and redirect to professional advice. |
| SR-5 | Any ingredient-conflict or pregnancy-related statement carries a visible "verify with a doctor" qualifier. |

If the owner chooses to ship Phase 1 without free-text fields, SR-3 can be deferred to Phase 2, but SR-1 and SR-2 are required from the first deployed version.

---

## 10. UI: `app.py` (Streamlit)

Flow:
1. Mock storefront: the Face Wash category page (product grid built from the catalog, price sort) with the banner "Know Your Skin & Choose Wisely" and the tagline "Your skin, your responsibility." at the top. Clicking the banner opens the feature while keeping the user able to return to the grid (Section 1A).
2. Questionnaire with a progress indicator:
   - Skin type (required): Oily / Dry / Combination / Sensitive / Not sure
   - Primary concern (optional): Acne / Dullness / Sensitivity / None in particular
   - Budget ceiling in ₹ (required, numeric)
   - Ingredients to avoid (optional, multi-select from Section 4.3 plus free-text "other")
   - Phase 2 additions: current routine (optional free text), anything else (optional free text)
3. Results page: 3-5 Top Picks, each with name, price, image placeholder, the "why picked" text, and a collapsible full ingredient list. Show the "limited results" message when applicable.
4. "Ask about these products" chat panel (Phase 2).
5. Sidebar: mode indicator ("No-LLM mode" / "LLM mode"), optional bring-your-own-key field, link to the README.
6. Disclosure footer on every screen.

Keep the UI clean and simple. Use session state only.

---

## 11. Evaluation and tests (Phase 3, this is what makes the project stand out)

Create a `tests/` folder and an `eval/` folder. Output a results table to `eval/RESULTS.md` that the README links to.

1. **Filter integrity (pytest):** run at least 50 generated profiles. Assert that no product above budget and no product containing an avoided ingredient ever appears in results. Target: **0 leaks**.
2. **Edge cases:** budget lower than every product, all ingredients avoided, "Not sure" skin type, free-text "other" ingredient, fewer than 3 survivors.
3. **Escalation:** a labeled set of ~10 "should escalate" and ~10 "should not escalate" free-text inputs. Report precision/recall or simple accuracy.
4. **Chatbot grounding:** ~20 in-scope questions and ~10 out-of-scope questions. Report (a) how often in-scope questions retrieve the correct KB entry and (b) how often out-of-scope questions are correctly refused. Run once in no-LLM mode and once in LLM mode if a free API key is available.
5. **Explanation faithfulness:** programmatically check that LLM-mode explanations mention no ingredient outside the structured input, and the owner spot-checks ~20 outputs by hand.
6. **Banned-words test (SR-1).**
7. **Memory check:** document peak RAM of the deployed app.

Report real numbers only. Never invent or estimate results.

---

## 12. Build order (do not skip ahead)

**Phase 0: Scaffolding**
- Repo structure, `requirements.txt` (pinned, minimal), `.gitignore`, `.env.example`, `DATA_GUIDE.md`, `scripts/validate_data.py`, placeholder data template.

**Phase 1: Demo (no LLM)**
- Alias map and flag derivation, matcher, template explanations, Streamlit questionnaire and results page, disclosure footer, filter-integrity tests.
- **Gate:** the app runs end to end with the owner's 20-25 real products and passes the 0-leak test. Deploy to Streamlit Community Cloud.

**Phase 2: AI layer**
- `llm.py` with provider abstraction, caps, and fallbacks. LLM-mode explanations. Knowledge-base retrieval (BM25 first). Chatbot in no-LLM then LLM mode. Free-text fields and escalation (SR-3, SR-4, SR-5).

**Phase 3: Evaluation and polish**
- Full test and eval suite from Section 11, `eval/RESULTS.md`, README, screenshots, demo recording script.

**Optional upgrades (only after Phases 1-3 pass):** `fastembed` + FAISS backend, expanded catalog toward 60-100 products, React frontend.

---

## 13. Deployment (free)

- **Primary:** Streamlit Community Cloud (free for public apps, deploys from a GitHub repo). Note that free apps hibernate after a period of inactivity, and resource limits may change.
- **Backup:** Hugging Face Spaces on the free CPU tier, as a second public link.
- Render's free tier has a 512 MB limit and sleeps quickly, so treat it as a last resort.
- Secrets go in Streamlit's secrets manager, never in the repo.
- Default deployed mode is **no-LLM**. LLM mode activates only when a key is configured or a viewer supplies their own.
- Keep the repo public and clean for portfolio use.

---

## 14. Repository layout

```
know-your-skin/
├── app.py                  # Streamlit entry: mock storefront + the feature
├── api.py                  # optional FastAPI wrapper (not deployed)
├── requirements.txt
├── .env.example
├── README.md
├── DATA_GUIDE.md
├── data/
│   ├── products.csv
│   └── ingredients_kb.json
├── src/
│   ├── catalog.py          # CatalogProvider interface + CsvCatalogProvider
│   ├── matcher.py
│   ├── ingredient_aliases.py
│   ├── explain.py
│   ├── llm.py
│   ├── retrieval.py
│   ├── chatbot.py
│   └── safety.py
├── scripts/
│   └── validate_data.py
├── tests/
└── eval/
    └── RESULTS.md
```

---

## 15. README requirements

The README must include:
1. One-paragraph description and a live demo link. State clearly that this is a feature designed to plug into an existing skincare e-commerce platform, demonstrated on a mock storefront, with an "Integration" section covering the `CatalogProvider` adapter and the `/recommend` and `/chat` API.
2. **An "Architecture decisions" section** explaining why matching is deterministic, why the LLM is optional and swappable, and why retrieval uses BM25/ONNX instead of heavy models. This is the owner's main interview talking point.
3. A short competitive-context note: AI-assisted skincare discovery already exists at scale (e.g. Sephora, Nykaa, Myntra); this project's angle is hard constraints plus a cited, refusing chatbot.
4. The evaluation results table (real numbers).
5. Limitations and non-goals (no medical advice, small hand-curated catalog).
6. "Future work": photo analysis and OCR are explicitly out of scope for v1 because of accuracy and bias concerns, plus a larger catalog and a React frontend.
7. Setup instructions and how to run tests.

Resume bullet to aim for once numbers exist (fill in real values only):
> Built a skincare recommendation system with a deterministic constraint-based matcher (budget and ingredient exclusion, 0 filter leaks across N test cases) and a citation-grounded retrieval chatbot with swappable LLM providers; evaluated at X% correct refusal on out-of-scope queries. Deployed free on Streamlit Community Cloud.

---

## 16. Definition of done

- [ ] Full flow runs end to end in both no-LLM and LLM modes
- [ ] 0 filter leaks across the filter-integrity test set
- [ ] SR-1 to SR-5 implemented and tested
- [ ] Chatbot refuses correctly on out-of-scope questions, with measured results
- [ ] Escalation accuracy measured on the labeled test set
- [ ] App deployed on free hosting with a public link
- [ ] Mock storefront shows the Face Wash grid with the feature banner, and picks use the same product cards and catalog as the grid
- [ ] All catalog access goes through `CatalogProvider` (no module reads the CSV directly)
- [ ] `api.py` exposes `/recommend` and `/chat`, with tests, and the README explains how a real platform would integrate
- [ ] No API keys in the repo
- [ ] README documents the architecture decisions and real evaluation numbers
- [ ] `validate_data.py` passes on the final dataset and the placeholder row is removed

## 17. Instructions to the agent about working style

- Work one phase at a time and stop at each gate for the owner to review.
- Keep the code small, readable, and commented where a design decision is non-obvious.
- Prefer fewer dependencies. Justify any new one.
- If anything in this document conflicts with itself or is ambiguous, ask the owner instead of guessing.
- Never invent product data, ingredient data, citations, or evaluation numbers.
