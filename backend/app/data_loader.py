import json
from typing import List, Dict, Any
from .config import PRODUCTS_FILE, INGREDIENT_KB_FILE

_products_cache: List[Dict[str, Any]] = []
_ingredient_kb_cache: List[Dict[str, Any]] = []

def load_products(force_reload: bool = False) -> List[Dict[str, Any]]:
    global _products_cache
    if not _products_cache or force_reload:
        with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
            _products_cache = json.load(f)
    return _products_cache

def load_ingredient_kb(force_reload: bool = False) -> List[Dict[str, Any]]:
    global _ingredient_kb_cache
    if not _ingredient_kb_cache or force_reload:
        with open(INGREDIENT_KB_FILE, "r", encoding="utf-8") as f:
            _ingredient_kb_cache = json.load(f)
    return _ingredient_kb_cache

def get_product_by_id(product_id: str) -> Dict[str, Any] | None:
    products = load_products()
    for p in products:
        if p.get("product_id") == product_id:
            return p
    return None
