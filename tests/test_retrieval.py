"""Tests for retrieval logic."""

import numpy as np
from app.vectorstore.faiss_store import FAISSStore


def test_faiss_add_and_search():
    store = FAISSStore(dimension=4)
    embeddings = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], dtype="float32")
    texts = ["doc one", "doc two"]

    store.add(embeddings, texts)
    results = store.search(np.array([1, 0, 0, 0], dtype="float32"), top_k=1)

    assert len(results) == 1
    assert results[0][0] == "doc one"
