import faiss
import pickle
import pandas as pd
import numpy as np
import ast

from sentence_transformers import SentenceTransformer
from app.config import settings


class RecipeVectorIndex:
    def __init__(self):
        # 1) Load the raw CSV
        self.df = pd.read_csv(settings.DATA_PATH)

        for col in ("ingredients", "instructions"):
            self.df[col] = self.df[col].apply(self._parse_list_column)

        self.embed_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index_path = settings.EMBEDDING_CACHE_PATH
        self.embeddings = None
        self.index = None
        self.build_index()

    def _parse_list_column(self, value):
        if isinstance(value, str):
            try:
                return ast.literal_eval(value)
            except (ValueError, SyntaxError):
                return [value]
        return value

    def build_index(self):
        try:
            with open(self.index_path, "rb") as f:
                self.embeddings, self.index = pickle.load(f)
            print("Loaded existing FAISS index from cache.")
        except (OSError, IOError):
            print("Building FAISS index from scratch...")
            texts = self.df["cleaned_text"].tolist()
            embs = self.embed_model.encode(texts, show_progress_bar=True)
            self.embeddings = np.array(embs).astype("float32")
            self.index = faiss.IndexFlatL2(self.embeddings.shape[1])
            self.index.add(self.embeddings)
            with open(self.index_path, "wb") as f:
                pickle.dump((self.embeddings, self.index), f)

    def retrieve(self, ingredients: list[str], top_k: int = 5):
        # embed & search
        query_vec = self.embed_model.encode([" ".join(ingredients)]).astype("float32")
        D, I = self.index.search(query_vec, top_k)
        if D[0][0] > 1.5:
            return []

        # pull out the top‐k rows
        hits = self.df.iloc[I[0]].copy().reset_index(drop=True)

        # map your “predicted” CSV columns into the public fields
        # (replace these names if your CSV uses slightly different headers)
        if "predicted_prep_time_rounded" in hits.columns:
            hits["prep_time"] = hits["predicted_prep_time_rounded"]
        else:
            hits["prep_time"] = None

        if "predicted_cook_time_rounded" in hits.columns:
            hits["cook_time"] = hits["predicted_cook_time_rounded"]
        else:
            hits["cook_time"] = None

        if "estimated_servings" in hits.columns:
            hits["servings"] = hits["estimated_servings"]
        else:
            hits["servings"] = None

        # finally select exactly the six fields we expose
        cols = [
            "title",
            "ingredients",
            "instructions",
            "prep_time",
            "cook_time",
            "servings",
        ]
        return hits[cols].to_dict(orient="records")
