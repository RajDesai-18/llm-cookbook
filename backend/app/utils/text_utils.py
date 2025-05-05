import re

def clean_ingredient(ingredient: str) -> str:
    ingredient = ingredient.lower()

    # Remove fractions and numbers
    ingredient = re.sub(r'\b\d+\b', '', ingredient)
    ingredient = re.sub(r'\d+\/\d+', '', ingredient)  # e.g., 1/2

    # Remove measurement units
    units = [
        "cup", "cups", "tablespoon", "tablespoons", "tbsp", "teaspoon", "teaspoons", "tsp",
        "pound", "pounds", "lb", "oz", "ounce", "ounces",
        "grams", "gram", "g", "kg", "ml", "liter", "liters",
        "clove", "cloves", "slice", "slices", "can", "cans", "package", "packages", "pinch", "of"
    ]
    unit_pattern = r'\b(?:' + '|'.join(units) + r')\b'
    ingredient = re.sub(unit_pattern, '', ingredient)

    # Remove extra spaces and punctuation
    ingredient = re.sub(r'[^\w\s]', '', ingredient)  # Remove punctuation
    ingredient = re.sub(r'\s+', ' ', ingredient).strip()

    return ingredient
