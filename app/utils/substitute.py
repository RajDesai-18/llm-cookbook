from typing import List, Dict
from app.utils.allergen_utils import ALLERGEN_SYNONYMS

SUBSTITUTION_MAP: Dict[str, List[str]] = {
    "egg": ["chia seeds", "flaxseed meal"],
    "milk": ["soy milk", "oat milk", "coconut milk"],
    "butter": ["olive oil", "coconut oil"],
    "honey": ["maple syrup", "agave nectar"],
    "cream": ["coconut cream", "cashew cream"],
    "cheese": ["nutritional yeast", "vegan cheese"],
    "yogurt": ["coconut yogurt", "soy yogurt"],
    "mayonnaise": ["vegan mayo", "mashed avocado"],
    "beef": ["tofu", "tempeh", "jackfruit"],
    "chicken": ["tofu", "seitan", "mushrooms"],
    "pork": ["tempeh", "jackfruit"],
    "fish": ["tofu", "seaweed-seasoned tofu"],
    "shellfish": ["hearts of palm", "artichoke hearts"],
    "gelatin": ["agar agar"],
    "lard": ["vegetable shortening", "coconut oil"],
    "whipped cream": ["coconut whipped cream"],
}


def substitute_ingredients(
    ingredients: List[str], excluded_allergens: List[str]
) -> List[str]:
    """
    Replace any ingredient that belongs to an excluded allergen category
    (via ALLERGEN_SYNONYMS) with a safe substitute from SUBSTITUTION_MAP.
    Tries singular forms if needed, otherwise drops the ingredient.
    """
    out: List[str] = []
    for ing in ingredients:
        lower = ing.lower()
        # 1) Check if this ingredient violates any excluded allergen
        violate = False
        for cat in excluded_allergens:
            for syn in ALLERGEN_SYNONYMS.get(cat.lower(), []):
                if syn in lower:
                    violate = True
                    break
            if violate:
                break

        if not violate:
            out.append(ing)
            continue

        # 2) Attempt to substitute
        # Try exact key
        substitute = SUBSTITUTION_MAP.get(lower)
        # If not found, try singular (strip trailing 's')
        if not substitute and lower.endswith("s"):
            singular = lower[:-1]
            substitute = SUBSTITUTION_MAP.get(singular)

        if substitute:
            # Capitalize to match original style
            rep = substitute[0]
            # Preserve casing of first letter
            out.append(rep.capitalize() if ing[0].isupper() else rep)
        # else: drop it entirely

    return out
