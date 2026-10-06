import pytest
from pathlib import Path
from src.catalog import JsonCatalogProvider, CsvCatalogProvider, get_default_catalog_provider

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def test_json_catalog_provider():
    p_json = DATA_DIR / "products.json"
    assert p_json.exists()
    provider = JsonCatalogProvider(p_json)
    products = provider.get_all_products()
    assert len(products) >= 60

    # Test lookup by ID
    p1 = provider.get_product("FW-001")
    assert p1 is not None
    assert p1["brand"] == "Cetaphil"
    assert p1["price_inr"] > 0
    assert len(p1["skin_types"]) > 0
    assert len(p1["full_ingredient_list"]) > 0

    # Ensure placeholder was filtered
    p0 = provider.get_product("FW-000")
    assert p0 is None

def test_csv_catalog_provider():
    p_csv = DATA_DIR / "products.csv"
    assert p_csv.exists()
    provider = CsvCatalogProvider(p_csv)
    products = provider.get_all_products()
    assert len(products) >= 60

    p1 = provider.get_product("FW-001")
    assert p1 is not None
    assert p1["name"] == "Gentle Skin Cleanser"
    assert isinstance(p1["skin_types"], list)
    assert isinstance(p1["full_ingredient_list"], list)
    assert len(p1["full_ingredient_list"]) > 0

def test_default_catalog_provider():
    provider = get_default_catalog_provider()
    prods = provider.get_all_products()
    assert len(prods) >= 60
