import requests
import json
from typing import List

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "nous-hermes"


def detect_cuisine(ingredients: List[str]) -> str:
    """
    Ask the LLM to pick the single best cuisine for these ingredients.
    Safely falls back to "International".
    """
    prompt = (
        "You are a culinary expert. Given these ingredients:\n"
        f"{', '.join(ingredients)}\n\n"
        "Respond with valid JSON only:\n"
        '{ "cuisine": string }\n'
        "No extra text."
    )

    try:
        resp = requests.post(
            OLLAMA_URL,
            json={"model": MODEL_NAME, "prompt": prompt, "stream": False},
            timeout=10,
        )
        raw = resp.json().get("response", "").strip()
        data = json.loads(raw)
        return data.get("cuisine", "International")
    except Exception:
        return "International"
