import os

# from dotenv import load_dotenv
from pathlib import Path

# — load .env from project root (if you have one) ——
BASE_DIR = Path(__file__).resolve().parent.parent
# load_dotenv(dotenv_path=BASE_DIR / ".env")


class Settings:
    PROJECT_NAME: str = "LLM CookBook"
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # your data files
    DATA_PATH: str = str(BASE_DIR / "app" / "data" / "recipes.csv")
    EMBEDDING_CACHE_PATH: str = str(
        BASE_DIR / "app" / "data" / "precomputed_embeddings.pkl"
    )
    SUBSTITUTION_DICT_PATH: str = str(
        BASE_DIR / "app" / "data" / "substitution_dict.json"
    )

    # any other constants
    OLLAMA_URL: str = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "nous-hermes")


settings = Settings()
