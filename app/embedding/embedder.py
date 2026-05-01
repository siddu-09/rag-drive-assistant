from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np

from app.config.settings import EMBEDDING_MODEL


class Embedder:
    def __init__(self, model_name: str = EMBEDDING_MODEL):
        """
        Initialize embedding model
        """
        print(f"🔄 Loading embedding model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        print("✅ Model loaded successfully!")

    def get_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        Convert list of texts into embeddings

        Args:
            texts (List[str]): list of text chunks

        Returns:
            np.ndarray: embeddings matrix
        """
        if not texts:
            return np.array([])

        embeddings = self.model.encode(
            texts,
            batch_size=32,
            show_progress_bar=True,
            convert_to_numpy=True
        )

        return embeddings

    def embed(self, texts: List[str]) -> np.ndarray:
        return self.get_embeddings(texts)

    def get_single_embedding(self, text: str) -> np.ndarray:
        """
        Convert single text into embedding

        Args:
            text (str)

        Returns:
            np.ndarray
        """
        return self.model.encode(
            [text],
            convert_to_numpy=True
        )[0]

    def embed_query(self, text: str) -> np.ndarray:
        return self.get_single_embedding(text)


# ✅ Create a global instance (used across project)
embedder = Embedder()


# ✅ Helper functions (for easy import)
def get_embeddings(texts: List[str]):
    return embedder.get_embeddings(texts)


def get_single_embedding(text: str):
    return embedder.get_single_embedding(text)