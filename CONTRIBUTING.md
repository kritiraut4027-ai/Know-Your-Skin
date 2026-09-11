# Contributing to "Know Your Skin & Choose Wisely"

Thank you for your interest in contributing! This project is designed to demonstrate applied judgment in structured skincare discovery, deterministic constraint matching, and grounded RAG explainability.

---

## Development Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/know-your-skin-choose-wisely.git
   cd know-your-skin-choose-wisely
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Development Server**:
   ```bash
   python -m uvicorn backend.app.main:app --port 8000 --reload
   ```

---

## Adding Products to the Catalog

All product entries in `data/products.json` must follow this schema:

```json
{
  "product_id": "FW-066",
  "name": "Product Name",
  "brand": "Brand Name",
  "price_inr": 399,
  "skin_types": ["oily", "combination"],
  "concerns_addressed": ["acne", "excess_oil"],
  "key_ingredients": ["salicylic_acid", "zinc_pca"],
  "full_ingredient_list": ["Water", "Glycerin", "..."],
  "flags": ["fragrance_free", "sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
}
```

*Note: INCI lists must be verified from published manufacturer packaging or official brand disclosures.*

---

## Adding Ingredients to the Knowledge Base

All ingredient entries in `data/ingredient_kb.json` require a verified credible source citation:

```json
{
  "ingredient_name": "Active Name",
  "aliases": ["alias 1", "alias 2"],
  "function": "Clear, non-marketing explanation of mechanism of action",
  "common_concerns": ["concern1", "concern2"],
  "caution_notes": "Usage restrictions, photosensitivity, or potential irritations",
  "source": "Citation (e.g. CIR Expert Panel, SCCS, or peer-reviewed journal)"
}
```

---

## Running Tests

Before submitting a Pull Request, ensure all tests pass cleanly:

```bash
python -m pytest backend/tests -v
python backend/tests/test_e2e_api.py
```
