from fastapi import FastAPI
from app.connectors.gdrive import list_files, download_file
from app.processing.parser import parse_pdf
from app.processing.chunking import chunk_text
from app.embedding.embedder import get_embeddings, get_single_embedding
from app.vectorstore.faiss_store import vector_store
from app.llm.generator import generate_answer

app = FastAPI()


@app.get("/")
def home():
    return {"message": "RAG Drive Assistant API is running"}


@app.post("/sync-drive")
def sync_drive():
    files = list_files()
    total_chunks = 0

    for f in files:
        file_id = f["id"]
        file_name = f["name"]
        mime_type = f["mimeType"]

        path = download_file(file_id, file_name)

        if mime_type != "application/pdf":
            continue

        text = parse_pdf(path)

        if not text.strip():
            continue

        chunks = chunk_text(text)

        if len(chunks) == 0:
            continue

        embeddings = get_embeddings(chunks)
        vector_store.add(embeddings, chunks)

        total_chunks += len(chunks)
    vector_store.save()

    return {
        "status": "success",
        "total_chunks_indexed": total_chunks
    }


# ✅ OUTSIDE sync_drive (correct)
@app.post("/ask")
def ask_question(query: str):
    # 🔍 Convert query to embedding
    query_embedding = get_single_embedding(query)

    # 🔎 Search relevant chunks
    results = vector_store.search(query_embedding, k=3)

    # 🧠 Combine context
    context = "\n\n".join(text for text, _distance in results)

    # 🤖 Generate answer
    answer = generate_answer(context, query)

    return {
        "query": query,
        "answer": answer,
        "chunks_used": len(results)
    }
