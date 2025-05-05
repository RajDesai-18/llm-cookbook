from fastapi import APIRouter
from typing import List
from app.utils.text_utils import clean_ingredient

router = APIRouter()

@router.post("/")
def parse_ingredients_endpoint(ingredients: list[str]):
    cleaned = [clean_ingredient(i) for i in ingredients]
    return {"parsed": cleaned} 