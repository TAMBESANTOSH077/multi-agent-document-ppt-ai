"""
Document Analysis API

Provides an endpoint for running the Document Analysis Agent
against an uploaded document.
"""


from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.agents.document_agent import (
    DocumentAnalysisAgent
)
from app.services.document_service import (
    extract_document
)


router = APIRouter(
    prefix="/api/document-analysis",
    tags=["Document Agent"]
)


UPLOAD_DIR = Path("storage/uploads")

# Create one agent instance that can be reused.
document_agent = DocumentAnalysisAgent()


@router.get("/{file_id}")
def analyze_document(file_id: str):
    """
    Run the Document Analysis Agent.

    Flow:

        file_id
            ↓
        Find uploaded file
            ↓
        Extract content
            ↓
        Analyze document
            ↓
        Return structured analysis
    """

    # Find the uploaded file.
    matching_files = list(
        UPLOAD_DIR.glob(f"{file_id}.*")
    )

    if not matching_files:
        raise HTTPException(
            status_code=404,
            detail="Uploaded file not found."
        )

    file_path = matching_files[0]

    try:

        # First extract the raw document content.
        extracted_document = extract_document(
            str(file_path)
        )

        # Send extracted content to the agent.
        analysis = document_agent.analyze(
            extracted_document
        )

        return {
            "success": True,
            "file_id": file_id,
            "filename": file_path.name,
            "analysis": analysis
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Document analysis failed: {str(exc)}"
            )
        )