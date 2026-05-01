import faiss
import numpy as np
import os
import pickle

from app.config.settings import VECTOR_STORE_PATH


class FAISSStore:
    def __init__(self, dim=384, dimension=None, index_path=None, meta_path=None):
        self.dim = dimension or dim
        self.index_path = index_path or os.path.join(VECTOR_STORE_PATH, "faiss.index")
        self.meta_path = meta_path or os.path.join(VECTOR_STORE_PATH, "texts.pkl")
        self.metadata_path = os.path.join(VECTOR_STORE_PATH, "metadata.pkl")

        # Create FAISS index
        self.index = faiss.IndexFlatL2(self.dim)

        # Store text chunks
        self.texts = []
        self.metadata = []

        # Load if exists
        self.load()

    def add(self, embeddings, texts, metadata=None):
        vectors = np.array(embeddings).astype("float32")

        self.index.add(vectors)
        self.texts.extend(texts)
        if metadata:
            self.metadata.extend(metadata)
        else:
            self.metadata.extend([{}] * len(texts))

        self.save()

    def search(self, query_embedding, top_k=3, k=None):
        if self.index.ntotal == 0:
            return []

        if k is not None:
            top_k = k

        query_vector = np.array([query_embedding]).astype("float32")

        distances, indices = self.index.search(query_vector, top_k)

        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx < len(self.texts):
                results.append((self.texts[idx], float(distance)))

        return results

    # ✅ SAVE INDEX
    def save(self):
        os.makedirs(VECTOR_STORE_PATH, exist_ok=True)

        faiss.write_index(self.index, self.index_path)

        with open(self.meta_path, "wb") as f:
            pickle.dump(self.texts, f)

        with open(self.metadata_path, "wb") as f:
            pickle.dump(self.metadata, f)

        print("💾 FAISS saved!")

    # ✅ LOAD INDEX
    def load(self):
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)

            if os.path.exists(self.meta_path):
                with open(self.meta_path, "rb") as f:
                    self.texts = pickle.load(f)

            if os.path.exists(self.metadata_path):
                with open(self.metadata_path, "rb") as f:
                    self.metadata = pickle.load(f)

            print("📂 FAISS loaded from disk!")

        else:
            print("🆕 New FAISS index created")


# Global instance
vector_store = FAISSStore()