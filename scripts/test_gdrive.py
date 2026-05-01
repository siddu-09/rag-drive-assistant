from app.connectors.gdrive import list_files, download_file
from app.processing.parser import parse_pdf
from app.processing.chunking import chunk_text
from app.embedding.embedder import get_embeddings, get_single_embedding
from app.vectorstore.faiss_store import vector_store
from app.llm.generator import generate_answer

files = list_files()

# 🔁 INGESTION PIPELINE
for f in files:
    file_id = f["id"]
    file_name = f["name"]
    mime_type = f["mimeType"]

    path = download_file(file_id, file_name)
    print("Downloaded:", path)

    # Only PDFs
    if mime_type != "application/pdf":
        continue

    text = parse_pdf(path)

    if not text.strip():
        print("\n⚠️ No text found (scanned PDF). Skipping...\n")
        continue

    print("\n--- EXTRACTED TEXT ---\n")
    print(text[:500])

    chunks = chunk_text(text)

    print("\n--- CHUNKING INFO ---")
    print("Total chunks:", len(chunks))

    if len(chunks) == 0:
        continue

    embeddings = get_embeddings(chunks)

    print("\n--- EMBEDDINGS INFO ---")
    print("Total embeddings:", len(embeddings))
    print("Embedding dimension:", len(embeddings[0]))

    # Store in FAISS
    vector_store.add(embeddings, chunks)
    print("Stored in FAISS")

# 🔍 QUERY PIPELINE
query = "What is this document about?"
print("\n🔍 Query:", query)

# Convert query to embedding
query_embedding = get_single_embedding(query)

# Retrieve top chunks
results = vector_store.search(query_embedding, k=3)

if len(results) == 0:
    print("\n❌ No results found in vector store")
    exit()

print("\n--- RETRIEVED CHUNKS ---")
for i, r in enumerate(results):
    print(f"\nChunk {i+1}:\n{r[:300]}...")

# 🔥 Build context
context = "\n\n".join(results)

# 🔥 Generate answer using Groq
answer = generate_answer(context, query)

print("\n--- FINAL ANSWER ---\n")
print(answer)