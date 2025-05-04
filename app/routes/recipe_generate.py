from fastapi import APIRouter
from app.schemas.recipe import RecipeGenerateRequest
from app.services.recipe_generator import generate_recipe_from_ingredients

router = APIRouter()


@router.post("/generate")
async def generate_recipe(request: RecipeGenerateRequest):
    return generate_recipe_from_ingredients(
        ingredients=request.ingredients,
        dietary_preference=request.dietary_preference,
        max_prep_time=request.max_prep_time,
        max_cook_time=request.max_cook_time,
        excluded_allergens=request.excluded_allergens,
        preferred_cuisine=request.preferred_cuisine,
    )
