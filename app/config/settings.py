import os

# Google Drive
GOOGLE_CREDENTIALS = "credentials.json"

# Chunking
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Embedding
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

DATA_PATH = os.path.join(BASE_DIR, "data")
RAW_DATA_PATH = os.path.join(DATA_PATH, "raw")
VECTOR_STORE_PATH = os.path.join(DATA_PATH, "vector_store")