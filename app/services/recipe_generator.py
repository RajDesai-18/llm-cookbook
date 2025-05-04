import requests
import json
import re
from typing import List, Optional
from app.config import settings
from app.utils.allergen_utils import detect_allergens, ALLERGEN_SYNONYMS
from app.utils.cuisine_utils import detect_cuisine
from app.utils.substitute import substitute_ingredients

OLLAMA_URL = settings.OLLAMA_URL
MODEL_NAME = settings.MODEL_NAME


def generate_recipe_from_ingredients(
    ingredients: List[str],
    dietary_preference: Optional[str] = None,
    max_prep_time: Optional[int] = None,
    max_cook_time: Optional[int] = None,
    excluded_allergens: Optional[List[str]] = None,
    preferred_cuisine: Optional[str] = None,
) -> dict:
    # 0) Substitute any excluded-allergen ingredients first
    if excluded_allergens:
        ingredients = substitute_ingredients(ingredients, excluded_allergens)

    # 1) Decide cuisine
    if preferred_cuisine:
        cuisine = preferred_cuisine
    else:
        detected = detect_cuisine(ingredients)
        cuisine = detected if detected.lower() != "international" else None

    # 2) Build human-readable constraints
    constraints: List[str] = []
    if cuisine:
        constraints.append(f"Please style the recipe in {cuisine} cuisine.")
    if dietary_preference:
        constraints.append(f"Make sure the recipe is strictly {dietary_preference}.")
    if max_prep_time:
        constraints.append(f"Preparation time must not exceed {max_prep_time} minutes.")
    if max_cook_time:
        constraints.append(f"Cooking time must not exceed {max_cook_time} minutes.")
    if excluded_allergens:
        parts = []
        for cat in excluded_allergens:
            syns = ALLERGEN_SYNONYMS.get(cat.lower(), [cat])
            parts.append(f"{cat} ({', '.join(syns[:6])})")
        constraints.append(
            "Do NOT include any of these allergens or their common forms: "
            + "; ".join(parts)
        )

    constraint_text = "\n".join(constraints)

    # 3) Craft the JSON‑only prompt (no fences, no bullets)
    prompt = (
        "You are a world-renowned chef with over 20 years of experience.\n"
        "Using only these ingredients: "
        f"{', '.join(ingredients)}, create a complete, original recipe.\n"
        f"{constraint_text}\n\n"
        "Respond with ONLY a single JSON object that begins with '{' and ends with '}'.\n"
        "Do NOT include any markdown fences (```), bullets, or extra text.\n\n"
        "The JSON schema:\n"
        "{\n"
        '  "title": string,\n'
        '  "prep_time": string,\n'
        '  "cook_time": string,\n'
        '  "servings": string,\n'
        '  "ingredients": [list of strings],\n'
        '  "instructions": [list of strings]\n'
        "}\n"
    )

    # 4) Call the model
    resp = requests.post(
        OLLAMA_URL,
        json={"model": MODEL_NAME, "prompt": prompt, "stream": False},
        timeout=30,
    )
    raw: str = resp.json().get("response", "")

    # ——— Sanitize raw output —————————————————————————————
    raw = raw.strip()

    # 4a) If it’s wrapped in code fences, drop them
    if raw.startswith("```") and raw.endswith("```"):
        lines = raw.splitlines()
        raw = "\n".join(lines[1:-1]).strip()

    # 4b) Unwrap any surrounding quotes and decode escaped chars
    if raw.startswith('"') and raw.endswith('"'):
        raw = raw[1:-1].replace('\\"', '"')
    # Decode literal \n, \t, etc.
    raw = raw.encode("utf-8").decode("unicode_escape")

    # 4c) Remove any leading bullet markers ("- ") per line
    raw = re.sub(r"^\s*-\s*", "", raw, flags=re.MULTILINE)

    # ——— Parse JSON ——————————————————————————————————————
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as e:
        return {
            "error": "Failed to parse LLM JSON output.",
            "parse_error": str(e),
            "sanitized_raw": raw,  # expose sanitized for debugging
        }

    # 5) Post‑generation allergen check
    if excluded_allergens:
        found = detect_allergens(parsed.get("ingredients", []), excluded_allergens)
        if found:
            return {
                "error": f"⚠️ Recipe contains excluded allergens: {', '.join(found)}",
                "recipe": parsed,
            }

    # 6) Attach cuisine if we have one
    if cuisine:
        parsed["cuisine"] = cuisine

    return {"recipe": parsed}
