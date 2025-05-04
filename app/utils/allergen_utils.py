from typing import List, Union

ALLERGEN_SYNONYMS: dict[str, List[str]] = {
    "milk": ["milk", "cream", "butter", "yogurt", "cheese", "paneer"],
    "eggs": ["egg", "eggs"],
    "fish": ["fish", "salmon", "tuna", "cod", "trout", "haddock"],
    "shellfish": ["shrimp", "prawn", "crab", "lobster", "oyster", "mussel"],
    "peanuts": ["peanut", "peanuts"],
    "tree nuts": [
        "almond",
        "almonds",
        "walnut",
        "walnuts",
        "cashew",
        "cashews",
        "pecan",
        "pecans",
        "hazelnut",
        "hazelnuts",
        "pistachio",
        "pistachios",
        "brazil nut",
        "brazil nuts",
        "macadamia",
        "pine nut",
        "pine nuts",
    ],
    "wheat": ["wheat", "whole wheat", "spelt", "bulgur"],
    "gluten": ["gluten", "barley", "rye"],
    "soy": ["soy", "tofu", "soy sauce", "edamame"],
    "sesame": ["sesame", "tahini"],
    "mustard": ["mustard"],
    "sulfites": ["sulfur dioxide", "sulfite", "sulfites"],
}


def detect_allergens(
    ingredients: List[Union[str, dict]], exclude_list: List[str]
) -> List[str]:
    """
    Return the list of allergen categories from exclude_list
    whose synonyms appear in the ingredients list.
    """
    # 1) Normalize all ingredients to strings (use .get('name') if it's a dict)
    normalized = []
    for item in ingredients:
        if isinstance(item, dict):
            # grab the 'name' field, or stringify the whole dict
            normalized.append(item.get("name", "") or "")
        else:
            normalized.append(str(item))
    text = " ".join(normalized).lower()

    found: set[str] = set()
    for category in exclude_list or []:
        synonyms = ALLERGEN_SYNONYMS.get(category.lower(), [category.lower()])
        for syn in synonyms:
            if syn in text:
                found.add(category)
                break

    return list(found)
