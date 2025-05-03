from fastapi import APIRouter

router = APIRouter()

@router.get("/substitute/{ingredient}")
def substitute_ingredient(ingredient: str):
    return {"message": f"Substitute suggestion for {ingredient}"}
