"""
Application Configuration

All environment-dependent settings are kept here.

This prevents API keys, file paths, model names,
and external tool configuration from being scattered
throughout the project.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # ---------------------------------------------------------------
    # Application
    # ---------------------------------------------------------------

    app_name: str = "Multi-Agent Document AI"
    app_version: str = "1.0.0"
    debug: bool = True

    # ---------------------------------------------------------------
    # AI Models
    # ---------------------------------------------------------------

    # Main Gemini model used for:
    # - reasoning
    # - summarization
    # - generation
    # - agent tasks
    model_name: str = "gemini-2.5-flash"

    # Gemini embedding model used for:
    # - document embeddings
    # - semantic search
    # - RAG retrieval
    embedding_model: str = "gemini-embedding-001"

    # ---------------------------------------------------------------
    # API Keys
    # ---------------------------------------------------------------

    google_api_key: str = ""
    tavily_api_key: str = ""

    # ---------------------------------------------------------------
    # Storage
    # ---------------------------------------------------------------

    # ChromaDB persistent vector storage.
    chroma_persist_directory: str = "./storage/chroma"

    # Uploaded user documents.
    upload_directory: str = "./storage/uploads"

    # Generated DOCX/PPTX files.
    generated_directory: str = "./storage/generated"

    # Previous generated versions.
    version_directory: str = "./storage/versions"

    # ---------------------------------------------------------------
    # OCR
    # ---------------------------------------------------------------

    # Windows path to Tesseract OCR.
    #
    # If Tesseract is already available in PATH,
    # this can remain empty.
    tesseract_cmd: str = ""

    # ---------------------------------------------------------------
    # Environment Configuration
    # ---------------------------------------------------------------

    # Load variables from backend/.env
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


# ---------------------------------------------------------------
# Global Settings Instance
# ---------------------------------------------------------------

# Import this object anywhere in the application:
#
#     from app.config import settings
#
settings = Settings()