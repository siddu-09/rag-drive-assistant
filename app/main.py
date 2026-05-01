"""
FastAPI application entry point.
"""

from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="RAG Drive Assistant",
    description="A RAG-powered assistant that syncs Google Drive documents and answers questions.",
    version="1.0.0",
)

app.include_router(router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "RAG Drive Assistant is running."}


@app.get("/health")
async def health():
    return {"status": "healthy"}
