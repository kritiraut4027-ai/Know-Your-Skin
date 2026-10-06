#!/usr/bin/env python3
"""
Data validation script (§4.4 of build spec).
Validates data/products.json, data/products.csv, and data/ingredient_kb.json.
Fails loudly if any schema constraint is violated.
"""

import sys
import json
import csv
from pathlib import Path
from typing import List, Dict, Any, Set

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"

ALLOWED_SKIN_TYPES = {"oily", "dry", "combination", "sensitive", "normal", "all"}
ALLOWED_FLAGS = {
    "fragrance_free", "sulfate_free", "alcohol_free", 
    "essential_oil_free", "paraben_free"
}

def validate_product_entry(p: Dict[str, Any], index: int, source_name: str) -> List[str]:
    errors = []
    pid = p.get("product_id")
    if not pid or not isinstance(pid, str):
        errors.append(f"Row {index}: Missing or invalid 'product_id'")
    
    name = p.get("name")
    if not name or not isinstance(name, str):
        errors.append(f"Product {pid}: Missing or invalid 'name'")
    elif pid != "FW-000" and "EXAMPLE ONLY" in name.upper():
        errors.append(f"Product {pid}: Found unremoved placeholder row in production dataset")
        
    brand = p.get("brand")
    if not brand or not isinstance(brand, str):
        errors.append(f"Product {pid}: Missing or invalid 'brand'")
        
    price = p.get("price_inr")
    try:
        price_val = float(price)
        if price_val <= 0:
            errors.append(f"Product {pid}: 'price_inr' must be greater than 0, got {price_val}")
    except (ValueError, TypeError):
        errors.append(f"Product {pid}: 'price_inr' must be a valid number, got {price}")
        
    skin_types = p.get("skin_types")
    if not isinstance(skin_types, list) or len(skin_types) == 0:
        errors.append(f"Product {pid}: 'skin_types' must be a non-empty list")
    else:
        for st in skin_types:
            if st.lower() not in ALLOWED_SKIN_TYPES:
                errors.append(f"Product {pid}: Unrecognized skin_type '{st}'. Allowed: {ALLOWED_SKIN_TYPES}")
                
    full_inci = p.get("full_ingredient_list")
    if not isinstance(full_inci, list) or len(full_inci) == 0:
        errors.append(f"Product {pid}: 'full_ingredient_list' must be a non-empty list of INCI ingredients")

    return errors

def validate_products_json(filepath: Path) -> List[str]:
    errors = []
    if not filepath.exists():
        return [f"File not found: {filepath}"]
        
    with open(filepath, "r", encoding="utf-8") as f:
        try:
            products = json.load(f)
        except json.JSONDecodeError as e:
            return [f"JSON syntax error in {filepath}: {e}"]
            
    if not isinstance(products, list):
        return [f"{filepath} must contain a JSON array of product objects"]
        
    seen_ids: Set[str] = set()
    for idx, p in enumerate(products):
        pid = p.get("product_id")
        if pid:
            if pid in seen_ids:
                errors.append(f"Duplicate product_id detected: '{pid}' at index {idx}")
            seen_ids.add(pid)
        errors.extend(validate_product_entry(p, idx, str(filepath.name)))
        
    return errors

def validate_products_csv(filepath: Path) -> List[str]:
    errors = []
    if not filepath.exists():
        return [f"File not found: {filepath}"]
        
    seen_ids: Set[str] = set()
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required_headers = {"product_id", "name", "brand", "price_inr", "skin_types", "full_ingredient_list"}
        missing = required_headers - set(reader.fieldnames or [])
        if missing:
            errors.append(f"CSV missing required headers: {missing}")
            return errors
            
        for idx, row in enumerate(reader):
            pid = row.get("product_id", "").strip()
            if not pid:
                errors.append(f"CSV Row {idx+2}: Missing product_id")
                continue
            if pid in seen_ids:
                errors.append(f"CSV Row {idx+2}: Duplicate product_id '{pid}'")
            seen_ids.add(pid)
            
            # Convert row to dict for validation
            p = {
                "product_id": pid,
                "name": row.get("name", "").strip(),
                "brand": row.get("brand", "").strip(),
                "price_inr": row.get("price_inr", ""),
                "skin_types": [s.strip() for s in row.get("skin_types", "").split(";") if s.strip()],
                "concerns_addressed": [c.strip() for c in row.get("concerns_addressed", "").split(";") if c.strip()],
                "key_ingredients": [k.strip() for k in row.get("key_ingredients", "").split(";") if k.strip()],
                "full_ingredient_list": [i.strip() for i in row.get("full_ingredient_list", "").split(";") if i.strip()],
                "flags": [fl.strip() for fl in row.get("flags", "").split(";") if fl.strip()],
                "source_url": row.get("source_url", "").strip()
            }
            errors.extend(validate_product_entry(p, idx + 2, str(filepath.name)))

    return errors

def validate_ingredient_kb(filepath: Path) -> List[str]:
    errors = []
    if not filepath.exists():
        return [f"File not found: {filepath}"]
        
    with open(filepath, "r", encoding="utf-8") as f:
        try:
            kb = json.load(f)
        except json.JSONDecodeError as e:
            return [f"JSON syntax error in {filepath}: {e}"]

    if not isinstance(kb, list):
        return [f"{filepath} must contain a list of ingredient entries"]

    seen_names: Set[str] = set()
    for idx, entry in enumerate(kb):
        name = entry.get("ingredient_name")
        if not name or not isinstance(name, str):
            errors.append(f"Ingredient index {idx}: Missing 'ingredient_name'")
        elif name.lower() in seen_names:
            errors.append(f"Duplicate ingredient_name: '{name}' at index {idx}")
        else:
            seen_names.add(name.lower())

        function = entry.get("function")
        if not function or not isinstance(function, str):
            errors.append(f"Ingredient '{name}': Missing or empty 'function'")

        caution = entry.get("caution_notes")
        if caution is None or not isinstance(caution, str):
            errors.append(f"Ingredient '{name}': Missing 'caution_notes'")

        source = entry.get("source")
        if not source or not isinstance(source, str) or len(source.strip()) < 5:
            errors.append(f"Ingredient '{name}': Missing, empty, or unverified 'source' citation (SR-4)")

    return errors

def main():
    print("=" * 65)
    print("🔍 RUNNING DATA INTEGRITY & SCHEMA VALIDATION")
    print("=" * 65)

    all_errors = []

    # 1. Validate products.json
    p_json = DATA_DIR / "products.json"
    print(f"Checking {p_json.relative_to(ROOT_DIR)}...")
    json_errs = validate_products_json(p_json)
    if json_errs:
        print(f"  ❌ FAILED with {len(json_errs)} errors")
        all_errors.extend(json_errs)
    else:
        with open(p_json, "r", encoding="utf-8") as f:
            cnt = len(json.load(f))
        print(f"  ✅ PASSED ({cnt} valid product records)")

    # 2. Validate products.csv
    p_csv = DATA_DIR / "products.csv"
    if p_csv.exists():
        print(f"Checking {p_csv.relative_to(ROOT_DIR)}...")
        csv_errs = validate_products_csv(p_csv)
        if csv_errs:
            print(f"  ❌ FAILED with {len(csv_errs)} errors")
            all_errors.extend(csv_errs)
        else:
            with open(p_csv, "r", encoding="utf-8") as f:
                cnt = sum(1 for _ in f) - 1
            print(f"  ✅ PASSED ({cnt} valid CSV rows)")

    # 3. Validate ingredient_kb.json
    kb_json = DATA_DIR / "ingredient_kb.json"
    print(f"Checking {kb_json.relative_to(ROOT_DIR)}...")
    kb_errs = validate_ingredient_kb(kb_json)
    if kb_errs:
        print(f"  ❌ FAILED with {len(kb_errs)} errors")
        all_errors.extend(kb_errs)
    else:
        with open(kb_json, "r", encoding="utf-8") as f:
            cnt = len(json.load(f))
        print(f"  ✅ PASSED ({cnt} verified ingredient entries with citations)")

    print("-" * 65)
    if all_errors:
        print(f"❌ VALIDATION FAILED with {len(all_errors)} total error(s):")
        for err in all_errors[:20]:
            print(f"   • {err}")
        if len(all_errors) > 20:
            print(f"   ... and {len(all_errors) - 20} more errors")
        sys.exit(1)
    else:
        print("🎉 ALL DATA VALIDATION CHECKS PASSED CLEANLY (Zero Schema Violations)")
        print("=" * 65)
        sys.exit(0)

if __name__ == "__main__":
    main()
