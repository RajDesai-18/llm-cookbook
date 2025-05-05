from fastapi import APIRouter
from typing import List
from app.services.vector_index import RecipeVectorIndex
from app.utils.text_utils import clean_ingredient

router = APIRouter()
vector_engine = RecipeVectorIndex()


@router.post("/search")
def search_recipes(user_ingredients: List[str]):
    parsed_ingredients = [clean_ingredient(i) for i in user_ingredients]
    result = vector_engine.retrieve(parsed_ingredients)

    if not result:
        return {"message": "No match found. You may want to generate a recipe. "}
    return {"results": result}
