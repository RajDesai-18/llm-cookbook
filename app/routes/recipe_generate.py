from fastapi import APIRouter
from typing import List

router = APIRouter()

@router.post("/generate")
def generate_recipe(user_ingredients: List[str]):
    return {"message": "Generate recipe fallback", "ingredients": user_ingredients}
