import uuid
from datetime import datetime, UTC

from services.storage_service import upload_file
from services.document_intelligence_service import (
    extract_document_from_file,
)
from services.cosmos_service import upsert_item


def process_document(
    local_file_path: str,
    file_name: str,
) -> dict:

    document_id = str(uuid.uuid4())

    blob_name = (
        f"reviews/{document_id}_{file_name}"
    )

    document_url = upload_file(
        local_file_path,
        blob_name,
    )

    extracted_data = extract_document_from_file(
        local_file_path
    )

    # NEW: make filename available to downstream agents
    extracted_data["file_name"] = file_name
    
    print(
    "Agent1 extracted filename:",
    extracted_data["file_name"]
    )

    document_record = {
        "id": document_id,
        "document_id": document_id,
        "file_name": file_name,
        "blob_name": blob_name,
        "document_url": document_url,
        "page_count": len(
            extracted_data.get("pages", [])
        ),
        "created_at": datetime.now(
            UTC
        ).isoformat(),
        "status": "extracted",
    }

    upsert_item(
        "documents",
        document_record,
    )

    return {
        "document_id": document_id,
        "file_name": file_name,
        "document_url": document_url,
        "extracted_data": extracted_data,
    }