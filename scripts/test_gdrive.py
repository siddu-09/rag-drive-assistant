from app.connectors.gdrive import list_files, download_file
from app.processing.parser import parse_pdf
from app.processing.chunking import chunk_text

files = list_files()

for f in files:
    file_id = f["id"]
    file_name = f["name"]
    mime_type = f["mimeType"]

    path = download_file(file_id, file_name)
    print("Downloaded:", path)

    if mime_type == "application/pdf":
        text = parse_pdf(path)

    if not text.strip():
        print("\n⚠️ No text found in this PDF (likely scanned). Skipping...\n")
        continue

    print("\n--- EXTRACTED TEXT ---\n")
    print(text[:500])

    chunks = chunk_text(text)

    print("\n--- CHUNKING INFO ---")
    print("Total chunks:", len(chunks))

    if len(chunks) > 0:
        print("\nFirst chunk:\n", chunks[0])

    if len(chunks) > 1:
        print("\nSecond chunk:\n", chunks[1])