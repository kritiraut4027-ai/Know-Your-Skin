import json
from typing import List, Dict, Any, Optional
from .config import INGREDIENT_KB_FILE
from src.catalog import get_default_catalog_provider

_ingredient_kb_cache: List[Dict[str, Any]] = []

def load_products(force_reload: bool = False) -> List[Dict[str, Any]]:
    """Retrieves products via the platform CatalogProvider adapter."""
    provider = get_default_catalog_provider()
    if force_reload and hasattr(provider, "reload"):
        provider.reload()
    return provider.get_all_products()

def load_ingredient_kb(force_reload: bool = False) -> List[Dict[str, Any]]:
    global _ingredient_kb_cache
    if not _ingredient_kb_cache or force_reload:
        with open(INGREDIENT_KB_FILE, "r", encoding="utf-8") as f:
            _ingredient_kb_cache = json.load(f)
    return _ingredient_kb_cache

def get_product_by_id(product_id: str) -> Optional[Dict[str, Any]]:
    return get_default_catalog_provider().get_product(product_id)
