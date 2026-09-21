from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile


router = APIRouter(
    prefix="/api/upload",
    tags=["File Upload"]
)


UPLOAD_DIR = Path("storage/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".ppt",
    ".pptx",
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
}


MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB


@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a supported document, presentation, or image.

    Supported:
    PDF, DOCX, PPT, PPTX, PNG, JPG, JPEG, WEBP
    """

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file selected."
        )

    original_filename = Path(file.filename).name
    extension = Path(original_filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unsupported file type: {extension}. "
                f"Allowed types: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
            )
        )

    file_content = await file.read()

    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size exceeds the 20 MB limit."
        )

    file_id = str(uuid4())
    stored_filename = f"{file_id}{extension}"
    file_path = UPLOAD_DIR / stored_filename

    file_path.write_bytes(file_content)

    return {
        "success": True,
        "file_id": file_id,
        "original_filename": original_filename,
        "stored_filename": stored_filename,
        "file_type": extension.replace(".", ""),
        "file_size": len(file_content),
        "path": str(file_path),
        "message": "File uploaded successfully."
    }