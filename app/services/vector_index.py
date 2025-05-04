import pandas as pd
import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer
from app.config import settings


class RecipeVectorIndex:
    def __init__(self):
        self.df = pd.read_csv(settings.DATA_PATH)
        self.embed_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index_path = settings.EMBEDDING_CACHE_PATH
        self.embeddings = None
        self.index = None
        self.build_index()

    def build_index(self):
        try:
            # Try loading precomputed embeddings and FAISS index from pickle
            with open(self.index_path, "rb") as f:
                self.embeddings, self.index = pickle.load(f)
            print("Loaded FAISS index from cache.")
        except:
            print("⚙️ No cache found — building FAISS index from scratch...")
            texts = self.df["cleaned_text"].tolist()

            # Embed the recipes using SentenceTransformer
            self.embeddings = self.embed_model.encode(texts, show_progress_bar=True)
            self.embeddings = np.array(self.embeddings).astype("float32")

            # Create and populate FAISS index
            self.index = faiss.IndexFlatL2(self.embeddings.shape[1])
            self.index.add(self.embeddings)

            # Save index and embeddings to disk
            with open(self.index_path, "wb") as f:
                pickle.dump((self.embeddings, self.index), f)
            print("FAISS index saved to disk.")

    def retrieve(self, query_ingredients: list[str], top_k: int = 5):
        query_str = " ".join(query_ingredients)
        query_vec = self.embed_model.encode([query_str]).astype("float32")

        D, I = self.index.search(query_vec, top_k)

        # Optional: ignore poor matches based on distance threshold
        if D[0][0] > 1.5:
            return []

        return self.df.iloc[I[0]][["title", "ingredients", "instructions"]].to_dict(
            orient="records"
        )
