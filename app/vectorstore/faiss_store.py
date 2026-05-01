"""
FAISS vector store – manages indexing and similarity search.
"""

import os
import json
from typing import List, Tuple

import faiss
import numpy as np

from app.config.settings import settings


class FAISSStore:
    """Manages a FAISS index for storing and querying document embeddings."""

    def __init__(self, dimension: int = None):
        self.dimension = dimension or settings.EMBEDDING_DIMENSION
        self.index = faiss.IndexFlatL2(self.dimension)
        self.documents: List[str] = []  # parallel list of chunk texts
        self.metadata: List[dict] = []  # parallel list of metadata

    def add(self, embeddings: np.ndarray, texts: List[str], metadata: List[dict] = None):
        """Add embeddings and their corresponding texts to the index."""
        self.index.add(embeddings.astype("float32"))
        self.documents.extend(texts)
        if metadata:
            self.metadata.extend(metadata)
        else:
            self.metadata.extend([{}] * len(texts))

    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[Tuple[str, float]]:
        """Search for the most similar documents to the query embedding."""
        query_embedding = np.array([query_embedding]).astype("float32")
        distances, indices = self.index.search(query_embedding, top_k)

        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.documents):
                results.append((self.documents[idx], float(distances[0][i])))
        return results

    def save(self, path: str = None):
        """Persist the FAISS index and document store to disk."""
        path = path or settings.VECTOR_STORE_DIR
        os.makedirs(path, exist_ok=True)
        faiss.write_index(self.index, os.path.join(path, "index.faiss"))
        with open(os.path.join(path, "documents.json"), "w") as f:
            json.dump({"documents": self.documents, "metadata": self.metadata}, f)

    def load(self, path: str = None):
        """Load a FAISS index and document store from disk."""
        path = path or settings.VECTOR_STORE_DIR
        self.index = faiss.read_index(os.path.join(path, "index.faiss"))
        with open(os.path.join(path, "documents.json"), "r") as f:
            data = json.load(f)
            self.documents = data["documents"]
            self.metadata = data.get("metadata", [{}] * len(self.documents))
