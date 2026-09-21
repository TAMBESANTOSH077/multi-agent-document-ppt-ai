"""
OCR Service

Responsible for extracting text from image-based content.

Used by:
    - Image files
    - Scanned PDF pages

Technology:
    - Pillow
    - pytesseract
    - Tesseract OCR
"""

from pathlib import Path

import pytesseract
from PIL import Image

from app.config import settings


def configure_tesseract() -> None:
    """
    Configure the Tesseract OCR executable.

    If TESSERACT_CMD is provided in .env, use that path.
    Otherwise, pytesseract searches for Tesseract in PATH.
    """

    if settings.tesseract_cmd:
        pytesseract.pytesseract.tesseract_cmd = (
            settings.tesseract_cmd
        )


def extract_text_from_image(file_path: str) -> str:
    """
    Extract text from an image file using OCR.

    Args:
        file_path: Path to the image.

    Returns:
        OCR-extracted text.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Image not found: {file_path}"
        )

    configure_tesseract()

    try:
        image = Image.open(path)

        text = pytesseract.image_to_string(image)

        return text.strip()

    except Exception as exc:
        raise RuntimeError(
            f"Image OCR failed: {str(exc)}"
        ) from exc


def extract_text_from_image_object(image: Image.Image) -> str:
    """
    Extract text from an already-loaded PIL image.

    This function is useful for scanned PDF pages because
    we can convert a PDF page into an image in memory
    without creating a temporary image file.
    """

    configure_tesseract()

    try:
        text = pytesseract.image_to_string(image)

        return text.strip()

    except Exception as exc:
        raise RuntimeError(
            f"Image OCR failed: {str(exc)}"
        ) from exc