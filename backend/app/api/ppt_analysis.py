"""
PPT Analysis API

Provides endpoints for analyzing uploaded PowerPoint
templates.
"""

from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.agents.ppt_agent import PPTAnalysisAgent
from app.services.ppt_service import extract_ppt_structure


router = APIRouter(
    prefix="/api/ppt-analysis",
    tags=["PPT Agent"],
)


UPLOAD_DIR = Path("storage/uploads")

ppt_agent = PPTAnalysisAgent()


def _find_ppt_file(file_id: str) -> Path:
    """
    Find an uploaded PPTX file using its file ID.
    """

    matching_files = list(
        UPLOAD_DIR.glob(f"{file_id}.*")
    )

    if not matching_files:
        raise HTTPException(
            status_code=404,
            detail="Presentation not found.",
        )

    file_path = matching_files[0]

    if file_path.suffix.lower() not in {
        ".ppt",
        ".pptx",
    }:
        raise HTTPException(
            status_code=400,
            detail="The selected file is not a PowerPoint file.",
        )

    return file_path


@router.get("/{file_id}")
def analyze_ppt(file_id: str):
    """
    Perform deterministic PPT template analysis.
    """

    file_path = _find_ppt_file(file_id)

    try:
        presentation = extract_ppt_structure(
            str(file_path)
        )

        analysis = ppt_agent.analyze(
            presentation
        )

        return {
            "success": True,
            "file_id": file_id,
            "filename": file_path.name,
            "analysis": analysis,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"PPT analysis failed: {str(exc)}",
        )


@router.get("/{file_id}/semantic")
def analyze_ppt_semantically(file_id: str):
    """
    Perform deterministic analysis followed by
    Gemini-powered semantic analysis.

    Workflow:

        PPTX
          ↓
        Extraction
          ↓
        Deterministic analysis
          ↓
        Gemini semantic analysis
    """

    file_path = _find_ppt_file(file_id)

    try:
        presentation = extract_ppt_structure(
            str(file_path)
        )

        template_profile = ppt_agent.analyze(
            presentation
        )

        semantic_analysis = (
            ppt_agent.analyze_semantically(
                template_profile
            )
        )

        return {
            "success": True,
            "file_id": file_id,
            "filename": file_path.name,
            "analysis": semantic_analysis,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=(
                "Semantic PPT analysis failed: "
                f"{str(exc)}"
            ),
        )