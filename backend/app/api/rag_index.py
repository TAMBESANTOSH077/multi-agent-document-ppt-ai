from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.config import settings
from app.services.rag_service import RAGService


router = APIRouter(
    prefix="/api/rag",
    tags=["RAG"],
)


@router.post("/index/{file_id}")
def index_document(file_id: str):
    """
    Extract, chunk, embed, and index an uploaded document
    into ChromaDB.
    """

    upload_directory = Path(settings.upload_directory)

    # Try the exact file ID first.
    file_path = upload_directory / file_id

    # If the exact path doesn't exist, search by filename.
    if not file_path.exists():
        matching_files = list(upload_directory.glob(file_id))

        if matching_files:
            file_path = matching_files[0]

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Uploaded file not found: {file_id}",
        )

    try:
        rag_service = RAGService()

        result = rag_service.index_document(
            str(file_path)
        )

        return {
            "success": True,
            "message": "Document indexed successfully.",
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to index document: {str(exc)}",
        ) from exc