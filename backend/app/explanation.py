from typing import Dict, Any, Optional
import os
import json
from .config import ANTHROPIC_API_KEY, GEMINI_API_KEY

def build_structured_prompt(product: Dict[str, Any], reasons: Dict[str, Any]) -> str:
    """
    Constructs a rigid structured input prompt per FR-4.1.
    """
    data = {
        "product_name": product.get("name"),
        "brand": product.get("brand"),
        "price_inr": product.get("price_inr"),
        "budget_ceiling_inr": reasons.get("budget_ceiling"),
        "skin_type": reasons.get("skin_type"),
        "primary_concern": reasons.get("concern"),
        "key_active_ingredients": reasons.get("matched_key_ingredients", []),
        "flags": product.get("flags", [])
    }
    return json.dumps(data, indent=2)

def generate_template_explanation(product: Dict[str, Any], reasons: Dict[str, Any]) -> str:
    """
    Deterministic rule-based explanation strictly grounded in provided attributes (FR-4.2).
    Always available without network/API dependencies.
    """
    brand = product.get("brand", "")
    name = product.get("name", "")
    price = product.get("price_inr", 0)
    budget = int(reasons.get("budget_ceiling", price))
    skin_type = reasons.get("skin_type", "").lower()
    concern = reasons.get("concern", "").replace("_", " ")
    key_ings = reasons.get("matched_key_ingredients", [])
    flags = [f.replace("_", " ") for f in product.get("flags", [])]
    
    parts = []
    
    # Sentence 1: Budget and skin type / active match
    if key_ings:
        ings_str = ", ".join(key_ings[:2])
        if concern and concern not in ["none", "none in particular"]:
            parts.append(
                f"Selected for your {skin_type} skin because it features {ings_str} to target {concern}."
            )
        else:
            parts.append(
                f"Selected for your {skin_type} skin profile with gentle support from {ings_str}."
            )
    else:
        parts.append(
            f"Formulated to suit {skin_type} skin without aggravating sensitivity."
        )
        
    # Sentence 2: Budget qualification & purity flags
    flag_highlight = ""
    if "fragrance free" in flags:
        flag_highlight = "is completely fragrance-free and "
    elif "sulfate free" in flags:
        flag_highlight = "features a gentle sulfate-free base and "
        
    parts.append(
        f"At ₹{price}, it {flag_highlight}sits comfortably within your stated ₹{budget} ceiling."
    )

    
    return " ".join(parts)

def generate_explanation(product: Dict[str, Any], reasons: Dict[str, Any]) -> str:
    """
    Generates 1-2 sentence natural explanation.
    Uses Anthropic / Gemini API if configured; falls back reliably to template generation.
    """
    # If Claude key is available:
    if ANTHROPIC_API_KEY:
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
            prompt_json = build_structured_prompt(product, reasons)
            
            system_prompt = (
                "You are an explainability module for a skincare recommendation system. "
                "Your task: Rephrase the provided structured match attributes into exactly 1 or 2 natural, concise sentences "
                "explaining why this product was picked for the user. "
                "CRITICAL RULES: "
                "1. NEVER invent any ingredient, medical claim, or benefit not explicitly present in the input JSON. "
                "2. Mention how it satisfies their budget ceiling and stated skin type/concern. "
                "3. Never use words like 'diagnose', 'cure', or '100% safe'."
            )
            
            response = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=150,
                temperature=0.2,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": f"Structured input:\n{prompt_json}\nExplain why this was picked:"}
                ]
            )
            text = response.content[0].text.strip()
            if text:
                return text
        except Exception:
            pass
            
    # Default fallback
    return generate_template_explanation(product, reasons)
