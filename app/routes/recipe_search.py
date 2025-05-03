from fastapi import APIRouter
from typing import List
from app.services.search_engine import RecipeSearchEngine
from app.utils.text_utils import clean_ingredient

router = APIRouter()
search_engine = RecipeSearchEngine()


@router.post("/search")
def search_recipes(user_ingredients: List[str]):
    parsed_ingredients = [clean_ingredient(i) for i in user_ingredients]
    result = search_engine.search(parsed_ingredients)

    if not result: 
        return {"message": "No match found. You may want to generate a recipe. "}
    return {"results": result}
