from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Union
from pathlib import Path
import json
import csv

class CatalogProvider(ABC):
    """
    Abstract interface for catalog access (§1A.4 of build spec).
    Decouples domain logic from whether products are stored in CSV, JSON,
    or fetched from an external e-commerce platform product API/database.
    """
    
    @abstractmethod
    def get_all_products(self) -> List[Dict[str, Any]]:
        """Return all catalog products."""
        pass

    @abstractmethod
    def get_product(self, product_id: str) -> Optional[Dict[str, Any]]:
        """Return a single product by its unique product_id, or None if not found."""
        pass


class JsonCatalogProvider(CatalogProvider):
    """
    Loads product catalog from a JSON file.
    """
    def __init__(self, filepath: Union[str, Path]):
        self.filepath = Path(filepath)
        self._products: List[Dict[str, Any]] = []
        self._by_id: Dict[str, Dict[str, Any]] = {}
        self.reload()

    def reload(self):
        if not self.filepath.exists():
            raise FileNotFoundError(f"Catalog file not found: {self.filepath}")
        with open(self.filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Filter out any placeholder / example-only rows
            self._products = [
                p for p in data 
                if p.get("product_id") != "FW-000" and "EXAMPLE ONLY" not in p.get("name", "").upper()
            ]
        self._by_id = {p["product_id"]: p for p in self._products if "product_id" in p}

    def get_all_products(self) -> List[Dict[str, Any]]:
        return list(self._products)

    def get_product(self, product_id: str) -> Optional[Dict[str, Any]]:
        return self._by_id.get(product_id)


class CsvCatalogProvider(CatalogProvider):
    """
    Loads product catalog from a CSV file (§4.1 of build spec).
    Serializes list fields (skin_types, concerns, ingredients, flags) from
    either JSON arrays or semicolon-separated values.
    """
    def __init__(self, filepath: Union[str, Path]):
        self.filepath = Path(filepath)
        self._products: List[Dict[str, Any]] = []
        self._by_id: Dict[str, Dict[str, Any]] = {}
        self.reload()

    def _parse_list(self, val: Any) -> List[str]:
        if not val or not isinstance(val, str):
            return []
        v = val.strip()
        if v.startswith("[") and v.endswith("]"):
            try:
                parsed = json.loads(v)
                return [str(x).strip() for x in parsed if str(x).strip()]
            except Exception:
                pass
        # Fallback to semicolon or pipe separated
        delimiter = ";" if ";" in v else ("|" if "|" in v else ",")
        return [part.strip() for part in v.split(delimiter) if part.strip()]

    def reload(self):
        if not self.filepath.exists():
            raise FileNotFoundError(f"Catalog CSV not found: {self.filepath}")
        
        products = []
        with open(self.filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                pid = row.get("product_id", "").strip()
                name = row.get("name", "").strip()
                if pid == "FW-000" or "EXAMPLE ONLY" in name.upper():
                    continue  # skip placeholder template row
                
                try:
                    price = float(row.get("price_inr", 0))
                except (ValueError, TypeError):
                    price = 0.0

                prod = {
                    "product_id": pid,
                    "name": name,
                    "brand": row.get("brand", "").strip(),
                    "price_inr": price,
                    "skin_types": self._parse_list(row.get("skin_types")),
                    "concerns_addressed": self._parse_list(row.get("concerns_addressed")),
                    "key_ingredients": self._parse_list(row.get("key_ingredients")),
                    "full_ingredient_list": self._parse_list(row.get("full_ingredient_list")),
                    "flags": self._parse_list(row.get("flags")),
                    "source_url": row.get("source_url", "").strip()
                }
                products.append(prod)

        self._products = products
        self._by_id = {p["product_id"]: p for p in self._products if p.get("product_id")}

    def get_all_products(self) -> List[Dict[str, Any]]:
        return list(self._products)

    def get_product(self, product_id: str) -> Optional[Dict[str, Any]]:
        return self._by_id.get(product_id)


_DEFAULT_CATALOG_PROVIDER: Optional[CatalogProvider] = None

def get_default_catalog_provider() -> CatalogProvider:
    """
    Returns the singleton default CatalogProvider instance.
    Prefers products.csv if present, falls back to products.json.
    """
    global _DEFAULT_CATALOG_PROVIDER
    if _DEFAULT_CATALOG_PROVIDER is not None:
        return _DEFAULT_CATALOG_PROVIDER

    data_dir = Path(__file__).resolve().parent.parent / "data"
    csv_path = data_dir / "products.csv"
    json_path = data_dir / "products.json"

    if csv_path.exists():
        _DEFAULT_CATALOG_PROVIDER = CsvCatalogProvider(csv_path)
    elif json_path.exists():
        _DEFAULT_CATALOG_PROVIDER = JsonCatalogProvider(json_path)
    else:
        raise FileNotFoundError(f"Neither products.csv nor products.json found in {data_dir}")

    return _DEFAULT_CATALOG_PROVIDER
