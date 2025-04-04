# AI-Based Recipe Generator from Ingredients - llm-cookbook

## Overview

This project is designed to help users generate personalized recipe suggestions based on the ingredients they have at home. It aims to reduce food waste and make meal planning more convenient through intelligent recipe matching and generation.

## Features

- **Ingredient Input**: A web interface that allows users to enter available ingredients.
- **Recipe Matching**: Matches input with existing recipes using NLP techniques and vector similarity.
- **Personalization**: Filters results based on dietary restrictions, allergies, and nutritional preferences.
- **Cooking Guidance**: Provides step-by-step cooking instructions.
- **LLM-Driven Generation**: If no recipe matches are found, a large language model is used to generate recipes.

## Data Sources

- Kaggle Recipe Datasets
- Food.com
- Recipe1M+
- USDA FoodData Central

## Tech Stack

- Python (NLP Processing)
- TF-IDF, Word2Vec, FastText
- T5 / BART / GPT-4
- Web App (Frontend to be defined)
