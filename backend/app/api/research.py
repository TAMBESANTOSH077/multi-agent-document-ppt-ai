
"""
Research API

Provides an API endpoint for real-time web research.

Flow:

    User Request
        ↓
    FastAPI
        ↓
    Research Agent
        ↓
    Tavily
        ↓
    Gemini
        ↓
    Research Summary + Sources
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.agents.research_agent import ResearchAgent


# ---------------------------------------------------------------
# Router
# ---------------------------------------------------------------

router = APIRouter(
    prefix="/api/research",
    tags=["Research"],
)


# ---------------------------------------------------------------
# Request Schema
# ---------------------------------------------------------------

class ResearchRequest(BaseModel):
    """
    Request model for web research.
    """

    query: str = Field(
        ...,
        min_length=1,
        description="Research question or topic",
    )

    max_results: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Maximum number of web sources",
    )

    topic: str = Field(
        default="general",
        description="Tavily search topic: general or news",
    )


# ---------------------------------------------------------------
# Research Endpoint
# ---------------------------------------------------------------

@router.post("/search")
def research(request: ResearchRequest):
    """
    Perform real-time web research.

    The Research Agent:
        1. Searches Tavily
        2. Collects relevant sources
        3. Sends source context to Gemini
        4. Generates a research summary
        5. Returns source URLs
    """

    try:
        agent = ResearchAgent()

        result = agent.research(
            query=request.query,
            max_results=request.max_results,
            topic=request.topic,
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
            detail=f"Research failed: {str(exc)}",
        ) from exc