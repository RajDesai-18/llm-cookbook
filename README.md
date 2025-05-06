# AI-Based Recipe Generator & Recommender (LLM CookBook)

[![Python](https://img.shields.io/badge/python-%3E%3D3.8-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-%3E%3D0.65-green)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-%3E%3D1.0-orange)](https://streamlit.io/)

> **Turn your pantry into a personalized recipe book**  
> — Enter your ingredients, filter recipes by preferences or allergens, and generate new recipes using advanced NLP techniques and LLMs.

---

## 📖 Table of Contents

- [Features](#-features)
- [Tech Stack & Models](#-tech-stack--models)
- [Folder Structure](#-folder-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Clone & Install](#clone--install)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [API Endpoints & Usage](#-api-endpoints--usage)
- [Next Steps & Improvements](#-next-steps--improvements)

---

## 🚀 Features

- **Ingredient Parsing:** Normalizes and cleans ingredient lists.
- **Recipe Search:** Semantic search using embeddings (MiniLM + FAISS).
- **Fallback LLM Generation:** Generates recipes with a local LLM (Ollama - Nous Hermes 2) when no matches are found.
- **Dietary & Allergen Filters:** Personalized filtering including dietary restrictions and allergens.
- **Ingredient Substitution:** Intelligent allergen substitution.
- **User-Friendly Frontend:** Interactive frontend built with Streamlit.

**Note:** This project is currently an **MVP** (Minimum Viable Product).

---

## 🧰 Tech Stack & Models

- **Backend:** FastAPI, Uvicorn
- **Frontend:** Streamlit
- **Embeddings & Search:** SentenceTransformers (`all-MiniLM-L6-v2`), FAISS
- **LLM:** Ollama (Nous-Hermes-2), optionally OpenAI GPT-4
- **Data Processing:** Pandas, NumPy

---

## YouTube Demo:

[https://youtu.be/dU8jeaVeWb0](https://youtu.be/dU8jeaVeWb0)

---

## 🗂 Folder Structure

```
llm\_cookbook/
├─ backend/
│   ├─ app/
│   │   ├─ main.py
│   │   ├─ config.py
│   │   ├─ routes/
│   │   │   ├─ parse\_ingredients.py
│   │   │   ├─ recipe\_search.py
│   │   │   ├─ recipe\_generate.py
│   │   │   └─ substitute.py
│   │   ├─ services/
│   │   │   ├─ vector\_index.py
│   │   │   └─ recipe\_generator.py
│   │   └─ utils/
│   │       ├─ allergen\_utils.py
│   │       ├─ cuisine\_utils.py
│   │       └─ substitute.py
│   ├─ requirements.txt
│   └─ .venv/
├─ frontend/
│   └─ streamlit\_app/
│       ├─ app.py
│       └─ config.toml
├─ data/
│   └─ recipes.csv
├─ .gitignore
└─ README.md
```

---

## ⚙ Getting Started

### Prerequisites

- Python ≥ 3.8
- Git
- Ollama (Local LLM model inference)

Install Ollama and pull the required model:

```bash
ollama pull nous-hermes
```

### Clone & Install

```bash
git clone https://github.com/RajDesai-18/llm-cookbook.git
cd llm-cookbook

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r backend/requirements.txt
pip install streamlit
```

### Backend Setup

Start Ollama model:

```bash
ollama serve
```

Start FastAPI backend:

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

Visit FastAPI Swagger UI:
[http://localhost:8000/docs](http://localhost:8000/docs)

### Frontend Setup

Start Streamlit frontend:

```bash
cd frontend/streamlit_app
streamlit run app.py
```

Visit frontend app:
[http://localhost:8501](http://localhost:8501)

---

## 📡 API Endpoints & Usage

### 🔹 Parse Ingredients

**Request:**

```http
POST /parse-ingredients
["2 cups tomatoes", "1 tsp salt"]
```

**Response:**

```json
{ "parsed": ["tomatoes", "salt"] }
```

### 🔹 Recipe Search

**Request:**

```http
POST /recipes/search
["tomatoes", "salt"]
```

**Response:**

```json
{
  "results": [
    {"title": "...", "ingredients": [...], "instructions": [...]},
    ...
  ]
}
```

### 🔹 Generate Recipe

**Request:**

```http
POST /recipes/generate
{
  "ingredients": ["tomatoes", "salt"],
  "dietary_preference": "vegan",
  "excluded_allergens": ["peanuts"]
}
```

**Response:**

```json
{
  "recipe": {
    "title": "...",
    "prep_time": "...",
    "cook_time": "...",
    "servings": "...",
    "ingredients": [...],
    "instructions": [...]
  }
}
```

---

## 🎯 Next Steps & Improvements

- Ingredient Substitute Feature: Expand the existing ingredient substitution logic to suggest multiple alternatives and improve allergen substitution handling.
- Full-Fledged Frontend: Implement a comprehensive and responsive frontend using **React.js**, **TypeScript**, and **Tailwind CSS** for a richer user experience.
- Add unit and integration tests.
- Conduct user studies for usability feedback.
- Improve error handling and logging mechanisms.
- CI/CD integration and Docker containerization.
- Fine-tune the LLM on custom recipe data.

---
