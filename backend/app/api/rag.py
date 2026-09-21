"""
RAG API

Provides endpoints for asking questions against the
indexed document knowledge base.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.agents.rag_agent import RAGAgent


router = APIRouter(
    prefix="/api/rag",
    tags=["RAG"],
)


class RAGSearchRequest(BaseModel):
    """
    Request model for RAG questions.
    """

    query: str = Field(
        ...,
        min_length=1,
        description="Question to ask about indexed documents",
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of document chunks to retrieve",
    )


@router.post("/search")
def search_documents(
    request: RAGSearchRequest,
):
    """
    Ask a question against the indexed document knowledge base.

    The RAG Agent retrieves relevant chunks from ChromaDB,
    sends grounded context to Gemini, and returns the answer
    together with source traceability.
    """

    try:
        agent = RAGAgent()

        result = agent.answer(
            query=request.query,
            top_k=request.top_k,
        )

        return {
            "success": True,
            **result,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"RAG agent failed: {str(exc)}",
        ) from exc