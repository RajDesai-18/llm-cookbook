from sys import prefix
from fastapi import FastAPI
from app.routes import (
    parse_ingredients,
    recipe_search,
    recipe_summarize,
    recipe_generate,
    substitute
)

app = FastAPI(title="AI-Based Recipe Generator & Recommender")

# Include API routes
app.include_router(parse_ingredients.router, prefix="/parse-ingredients")
app.include_router(recipe_search.router, prefix="/recipes")
app.include_router(recipe_generate.router, prefix="/recipes")
app.include_router(recipe_summarize.router, prefix="/recipe")
app.include_router(substitute.router, prefix="/ingredients")