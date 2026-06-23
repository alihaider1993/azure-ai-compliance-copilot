import sys
import uuid
from pathlib import Path
from datetime import datetime, UTC

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

from services.document_intelligence_service import extract_document_from_file
from services.openai_service import generate_embedding
from services.search_service import upload_documents


BENCHMARK_FOLDER = ROOT_DIR / "benchmark"


def chunk_text(text: str, chunk_size: int = 2500, overlap: int = 300):
    chunks = []

    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk.strip())

        start += chunk_size - overlap

    return chunks


def detect_framework(file_name: str) -> str:
    name = file_name.lower()

    if "gdpr" in name or "data protection" in name or "privacy" in name:
        return "UK GDPR"

    if "security" in name or "iso" in name or "cyber" in name:
        return "Information Security Policy"

    if "health" in name or "safety" in name or "hse" in name:
        return "Health & Safety SOP"

    if "contract" in name or "supplier" in name or "purchase" in name:
        return "Supplier Contract Review"

    return "General Policy Review"


def ingest_benchmark_documents():
    if not BENCHMARK_FOLDER.exists():
        raise FileNotFoundError(
            f"Benchmark folder not found: {BENCHMARK_FOLDER}"
        )

    files = [
        file for file in BENCHMARK_FOLDER.iterdir()
        if file.suffix.lower() in [
            ".pdf",
            ".docx",
            ".txt",
            ".png",
            ".jpg",
            ".jpeg",
        ]
    ]

    if not files:
        print("No benchmark files found.")
        return

    for file_path in files:
        print(f"\nProcessing: {file_path.name}")

        extracted = extract_document_from_file(str(file_path))
        content = extracted.get("content", "")
        pages = extracted.get("pages", [])

        chunks = chunk_text(content)

        print(f"Chunks created: {len(chunks)}")

        documents = []

        for index, chunk in enumerate(chunks, start=1):
            print(f"Embedding chunk {index}/{len(chunks)}")

            embedding = generate_embedding(chunk)

            page_number = 1

            if pages:
                page_number = min(
                    index,
                    len(pages),
                )

            documents.append(
                {
                    "id": str(uuid.uuid4()),
                    "file_name": f"benchmark/{file_path.name}",
                    "chunk_text": chunk,
                    "page_number": page_number,
                    "source_type": "benchmark",
                    "framework": detect_framework(file_path.name),
                    "embedding": embedding,
                }
            )

        upload_documents(documents)

        print(
            f"Uploaded {len(documents)} chunks for {file_path.name}"
        )


if __name__ == "__main__":
    ingest_benchmark_documents()