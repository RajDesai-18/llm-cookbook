from fastapi import APIRouter

router = APIRouter()

@router.get("/summarize/{recipe_id}")
def summarize_recipe(recipe_id: int):
    return {"message": f"Summarize recipe {recipe_id}"}
