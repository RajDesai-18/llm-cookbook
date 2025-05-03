import pandas as pd
import numpy as np
from tracemalloc import stop
from app.config import settings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class RecipeSearchEngine:
    def __init__(self):
        self.df = pd.read_csv(settings.DATA_PATH)
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.recipe_matrix = self.vectorizer.fit_transform(self.df["cleaned_text"])

    def search(self, query_ingredients: list[str], top_n: int = 5):
        query_str = " ".join(query_ingredients)
        query_vec = self.vectorizer.transform([query_str])
        scores = cosine_similarity(query_vec, self.recipe_matrix).flatten()

        if scores.max() == 0:
            return []
        
        top_indices = np.argsort(scores)[::-1][:top_n]
        return self.df.iloc[top_indices][["title", "ingredients", "instructions"]].to_dict(orient="records")