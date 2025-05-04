from pydantic import BaseModel
from typing import List, Optional


class RecipeGenerateRequest(BaseModel):
    ingredients: List[str]
    dietary_preference: Optional[str] = None
    max_prep_time: Optional[int] = None
    max_cook_time: Optional[int] = None
    excluded_allergens: Optional[List[str]] = None
    preferred_cuisine: Optional[str] = None
