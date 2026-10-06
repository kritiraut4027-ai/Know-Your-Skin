# Data Contribution Guide: Catalog & Knowledge Base 🌿

This document specifies the data entry standards and validation procedures for **Know Your Skin & Choose Wisely**.

---

## 1. Product Catalog (`data/products.csv` and `data/products.json`)

All entries represent real, commercially available cleansers in the Indian market.

### Schema Requirements

| Field | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `product_id` | `str` | Unique sequential identifier (`FW-XXX`) | `"FW-066"` |
| `name` | `str` | Exact commercial formulation name | `"Hydrating Cleanser"` |
| `brand` | `str` | Brand name | `"CeraVe"` |
| `price_inr` | `float` / `int` | Maximum Retail Price (MRP) in INR | `490` |
| `skin_types` | `list[str]` | Target skin types: `oily, dry, combination, sensitive, normal` | `["dry", "sensitive"]` |
| `concerns_addressed`| `list[str]` | Specific concerns: `acne, dryness, sensitivity, dullness, excess_oil, barrier_repair` | `["dryness", "sensitivity"]` |
| `key_ingredients` | `list[str]` | Prominently featured active or functional ingredients | `["ceramides", "hyaluronic_acid"]` |
| `full_ingredient_list` | `list[str]` | Complete INCI list in descending order of concentration | `["Water", "Glycerin", "Ceramide NP", ...]` |
| `flags` | `list[str]` | Certified purity flags: `fragrance_free, sulfate_free, alcohol_free, essential_oil_free, paraben_free` | `["fragrance_free", "sulfate_free"]` |
| `source_url` | `str` | URL where the INCI list was officially obtained | `"https://brand.com/product"` |

### Ground Truth Guidelines
1. **Never Invent Data**: INCI lists must be verified from published manufacturer packaging or official brand disclosures.
2. **No Scraped Bloat**: Manually enter and verify ingredient names rather than scraping unverified marketplace listings.
3. **Template**: Use [`data/products_template.csv`](./data/products_template.csv) for structure reference. **Never** include the template row `FW-000` in production data.

---

## 2. Ingredient Knowledge Base (`data/ingredient_kb.json`)

Each ingredient entry in the knowledge base serves as a grounded retrieval source for the chatbot.

### Schema Requirements

| Field | Type | Description |
| :--- | :--- | :--- |
| `ingredient_name` | `str` | Standardized cosmetic name (e.g. `"Salicylic Acid"`) |
| `aliases` | `list[str]` | Common nomenclature or acronyms (e.g. `["BHA", "Beta Hydroxy Acid"]`) |
| `function` | `str` | Plain-language mechanism of action in a rinse-off cleanser |
| `common_concerns` | `list[str]` | Targeted skincare concerns (e.g. `["acne", "clogged_pores"]`) |
| `caution_notes` | `str` | Safety guidance, photosensitivity warnings, or contraindications |
| `source` | `str` | **Required citation**: CIR Expert Panel, SCCS, AAD, or peer-reviewed journal |

---

## 3. Data Validation

Run the automated data validation script prior to any commit:

```bash
python scripts/validate_data.py
```

Any duplicate IDs, missing required fields, non-positive prices, or missing source citations will fail loudly with detailed line numbers.
