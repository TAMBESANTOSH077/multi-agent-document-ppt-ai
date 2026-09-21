from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.services.document_service import extract_document


router = APIRouter(
    prefix="/api/analyze",
    tags=["Document Analysis"]
)


UPLOAD_DIR = Path("storage/uploads")


@router.get("/{file_id}")
def analyze_file(file_id: str):
    """Extract structured content from an uploaded file."""

    matching_files = list(
        UPLOAD_DIR.glob(f"{file_id}.*")
    )

    if not matching_files:
        raise HTTPException(
            status_code=404,
            detail="File not found."
        )

    file_path = matching_files[0]

    try:
        result = extract_document(
            str(file_path)
        )

        return {
            "success": True,
            "file_id": file_id,
            "filename": file_path.name,
            "data": result
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Document analysis failed: {str(exc)}"
        )