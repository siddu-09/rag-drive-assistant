"""
Sync service – orchestrates the full ingestion pipeline:
  Google Drive → download → parse → chunk → embed → store in FAISS
"""

import os
from typing import Dict

from app.connectors.gdrive import GoogleDriveConnector
from app.processing.parser import extract_text
from app.processing.chunking import chunk_text
from app.embedding.embedder import Embedder
from app.vectorstore.faiss_store import FAISSStore
from app.config.settings import settings


class SyncService:
    """Full ingestion pipeline from Google Drive to vector store."""

    def __init__(self):
        self.drive = GoogleDriveConnector()
        self.embedder = Embedder()
        self.store = FAISSStore()

    async def sync(self, folder_id: str) -> Dict:
        """
        Run the full sync pipeline.

        Args:
            folder_id: Google Drive folder ID to sync from.

        Returns:
            Dict with sync results including doc_count.
        """
        # 1. Download files from Google Drive
        file_paths = self.drive.fetch_all(folder_id)

        all_chunks = []
        all_metadata = []

        # 2. Parse and chunk each document
        for path in file_paths:
            try:
                text = extract_text(path)
                if text:
                    chunks = chunk_text(text)
                    all_chunks.extend(chunks)
                    all_metadata.extend(
                        [{"source": os.path.basename(path)}] * len(chunks)
                    )
            except ValueError as e:
                print(f"Skipping {path}: {e}")

        # 3. Generate embeddings
        if all_chunks:
            embeddings = self.embedder.embed(all_chunks)

            # 4. Store in FAISS
            self.store.add(embeddings, all_chunks, all_metadata)
            self.store.save()

        return {"doc_count": len(file_paths), "chunk_count": len(all_chunks)}
