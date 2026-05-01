import os
from dataclasses import dataclass


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Google Drive credentials can come from a checked-out file or an environment secret.
GOOGLE_CREDENTIALS = os.getenv("GOOGLE_CREDENTIALS", os.path.join(BASE_DIR, "credentials.json"))
GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH", GOOGLE_CREDENTIALS)
GOOGLE_CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS_JSON", "")

# LLM configuration.
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

# Chunking
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))

# Retrieval
TOP_K = int(os.getenv("TOP_K", "3"))

# Embedding
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

# Paths
DATA_PATH = os.path.join(BASE_DIR, "data")
RAW_DATA_PATH = os.path.join(DATA_PATH, "raw")
VECTOR_STORE_PATH = os.path.join(DATA_PATH, "vector_store")


@dataclass(frozen=True)
class Settings:
	google_credentials: str = GOOGLE_CREDENTIALS
	google_credentials_path: str = GOOGLE_CREDENTIALS_PATH
	google_credentials_json: str = GOOGLE_CREDENTIALS_JSON
	groq_api_key: str = GROQ_API_KEY
	groq_model: str = GROQ_MODEL
	chunk_size: int = CHUNK_SIZE
	chunk_overlap: int = CHUNK_OVERLAP
	top_k: int = TOP_K
	embedding_model: str = EMBEDDING_MODEL
	data_path: str = DATA_PATH
	raw_data_path: str = RAW_DATA_PATH
	vector_store_path: str = VECTOR_STORE_PATH


settings = Settings()