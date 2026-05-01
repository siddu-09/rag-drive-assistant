# RAG Drive Assistant

RAG Drive Assistant is a small FastAPI application that syncs documents from Google Drive, converts them into embeddings, stores them in FAISS, and answers questions over the synced content with an OpenAI-compatible chat model.

## What It Does

The project follows a simple end-to-end Retrieval-Augmented Generation (RAG) flow:

1. Pull documents from a Google Drive folder.
2. Extract text from PDFs, DOCX files, and plain text files.
3. Split the text into overlapping chunks.
4. Create embeddings with `sentence-transformers`.
5. Store the chunks and vectors in FAISS.
6. Embed a user question and retrieve the most relevant chunks.
7. Send the question plus retrieved context to an LLM and return the answer.

## LLM And Embeddings

- Embedding model: `all-MiniLM-L6-v2`
- LLM: OpenAI ChatCompletion API via the `openai` Python package
- LLM model name: supplied by the app configuration layer at runtime

The repository does not hard-code a single chat model name in the generator, so the exact model depends on your configuration.

## Project Structure

```text
app/
  api/           FastAPI routes and request/response schemas
  config/        Shared configuration values
  connectors/    Google Drive integration
  embedding/     Text embedding logic
  llm/           Answer generation logic
  processing/    Parsing and chunking utilities
  retrieval/     Vector search and retrieval
  services/      Sync and query orchestration
  vectorstore/   FAISS persistence and search
scripts/
  run_sync.py    Manual sync script
tests/           Basic API, processing, and retrieval tests
```

## End-To-End Workflow

### 1. Sync documents

Use the sync endpoint or the sync script to ingest a Google Drive folder.

- Files are downloaded from Google Drive using a service account.
- `parser.py` extracts text from `.pdf`, `.docx`, `.doc`, and `.txt` files.
- `chunking.py` splits the text into chunks of 500 characters with 50 characters of overlap.
- `embedder.py` converts each chunk into a vector with `all-MiniLM-L6-v2`.
- `faiss_store.py` saves vectors, chunk text, and metadata to disk.

### 2. Ask questions

When a question comes in:

- The question is embedded with the same embedding model.
- FAISS retrieves the most similar chunks.
- The retrieved context is passed to the LLM.
- The LLM returns an answer grounded in the provided context.

### 3. Return the result

The API returns:

- the generated answer
- source snippets from the retrieved chunks

## API Endpoints

- `GET /` - service status message
- `GET /health` - health check
- `POST /api/v1/sync-drive` - sync a Google Drive folder into the vector store
- `POST /api/v1/ask` - ask a question against the synced documents

### Example Requests

Sync a folder:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/sync-drive \
  -H "Content-Type: application/json" \
  -d '{"folder_id":"YOUR_GOOGLE_DRIVE_FOLDER_ID"}'
```

Ask a question:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"What is this project about?"}'
```

## Setup

### 1. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure credentials

- Place your Google service account file at `credentials.json` in the project root.
- Make sure your Google Drive folder is shared with that service account.
- Configure your OpenAI API key and LLM model in your app settings or environment.

## Run The App

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Open the API at:

- `http://127.0.0.1:8000`
- `http://127.0.0.1:8000/docs`

## Run A Manual Sync

```bash
python scripts/run_sync.py YOUR_GOOGLE_DRIVE_FOLDER_ID
```

## Tests

```bash
pytest
```

## Notes

- The vector store is persisted under `data/vector_store/`.
- Downloaded source files are written under `data/raw/`.
- The code currently expects shared configuration values for chunking, vector storage, and LLM access.

## Tech Stack

- FastAPI
- FAISS
- Google Drive API
- SentenceTransformers
- OpenAI-compatible chat completion API
- PyMuPDF
- python-docx
