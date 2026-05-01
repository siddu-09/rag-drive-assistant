"""
Pydantic request/response models for the API.
"""

from typing import List, Optional
from pydantic import BaseModel


class SyncRequest(BaseModel):
    folder_id: str


class SyncResponse(BaseModel):
    status: str
    message: str
    doc_count: int


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str
    sources: Optional[List[str]] = []
