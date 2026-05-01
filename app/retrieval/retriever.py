"""
Retriever – fetches the most relevant chunks for a given query.
"""

from typing import List, Tuple

from app.embedding.embedder import Embedder
from app.vectorstore.faiss_store import FAISSStore
from app.config.settings import settings


class Retriever:
    """Retrieves relevant document chunks using vector similarity search."""

    def __init__(self, embedder: Embedder = None, store: FAISSStore = None):
        self.embedder = embedder or Embedder()
        self.store = store or FAISSStore()

    def load_store(self):
        """Load the persisted vector store from disk."""
        self.store.load()

    def retrieve(self, query: str, top_k: int = None) -> List[Tuple[str, float]]:
        """
        Retrieve the top-k most relevant text chunks for a query.

        Args:
            query: The user question.
            top_k: Number of results to return.

        Returns:
            List of (chunk_text, distance) tuples.
        """
        top_k = top_k or settings.TOP_K
        query_embedding = self.embedder.embed_query(query)
        results = self.store.search(query_embedding, top_k=top_k)
        return results
