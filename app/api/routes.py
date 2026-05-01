"""
FastAPI routes for the RAG Drive Assistant.
Endpoints: /sync-drive, /ask
"""

from fastapi import APIRouter, HTTPException
from app.api.schemas import SyncRequest, SyncResponse, AskRequest, AskResponse
from app.services.sync_service import SyncService
from app.services.query_service import QueryService

router = APIRouter()

sync_service = SyncService()
query_service = QueryService()


@router.post("/sync-drive", response_model=SyncResponse)
async def sync_drive(request: SyncRequest):
    """Sync documents from Google Drive and ingest into vector store."""
    try:
        result = await sync_service.sync(request.folder_id)
        return SyncResponse(
            status="success",
            message=f"Synced {result['doc_count']} documents.",
            doc_count=result["doc_count"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest):
    """Ask a question against the synced documents."""
    try:
        answer = await query_service.query(request.question)
        return AskResponse(answer=answer["answer"], sources=answer.get("sources", []))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
