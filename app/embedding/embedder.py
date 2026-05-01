"""
Embedding module – generates vector embeddings for text chunks.
"""

from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer

from app.config.settings import settings


class Embedder:
    """Generates embeddings using a SentenceTransformer model."""

    def __init__(self, model_name: str = None):
        self.model_name = model_name or settings.EMBEDDING_MODEL
        self.model = SentenceTransformer(self.model_name)

    def embed(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for a list of text chunks.

        Args:
            texts: List of text strings to embed.

        Returns:
            Numpy array of shape (n_texts, embedding_dim).
        """
        embeddings = self.model.encode(texts, show_progress_bar=True)
        return np.array(embeddings)

    def embed_query(self, query: str) -> np.ndarray:
        """Generate an embedding for a single query string."""
        return self.model.encode([query])[0]
