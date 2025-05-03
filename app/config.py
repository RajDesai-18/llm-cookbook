import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

class Settings:
    PROJECT_NAME: str = "AI-Based Recipe Generator"
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")

    # You can add more configs here later (e.g., model paths, thresholds, etc.)
    DATA_PATH: str = str(BASE_DIR / "app" / "data" / "recipes.csv")
    EMBEDDING_CACHE_PATH: str = str(BASE_DIR / "app" / "data" / "precomputed_embeddings.pkl")
    SUBSTITUTION_DICT_PATH: str = str(BASE_DIR / "app" / "data" / "substitution_dict.json")

settings = Settings()
