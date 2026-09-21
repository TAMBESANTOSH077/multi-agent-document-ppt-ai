"""
Web Research Service

Provides real-time web search using Tavily.

Responsibilities:
    - Search the live web
    - Retrieve relevant search results
    - Return titles, URLs, snippets and scores
    - Keep web-search logic separate from the agents
"""

from typing import Any

from tavily import TavilyClient

from app.config import settings


class WebResearchService:
    """
    Service responsible for real-time web research.
    """

    def __init__(self):
        if not settings.tavily_api_key:
            raise ValueError(
                "TAVILY_API_KEY is not configured. "
                "Add it to the backend .env file."
            )

        self.client = TavilyClient(
            api_key=settings.tavily_api_key
        )

    # -----------------------------------------------------------
    # Web Search
    # -----------------------------------------------------------

    def search(
        self,
        query: str,
        max_results: int = 5,
        topic: str = "general",
    ) -> dict[str, Any]:
        """
        Search the live web using Tavily.

        Args:
            query:
                User's research question.

            max_results:
                Maximum number of search results.

            topic:
                Tavily search topic, normally "general"
                or "news".

        Returns:
            Structured web research results.
        """

        if not query or not query.strip():
            raise ValueError(
                "Search query cannot be empty."
            )

        if max_results < 1:
            raise ValueError(
                "max_results must be at least 1."
            )

        if max_results > 10:
            max_results = 10

        response = self.client.search(
            query=query.strip(),
            topic=topic,
            max_results=max_results,
            search_depth="advanced",
            include_answer=False,
            include_raw_content=False,
        )

        raw_results = response.get(
            "results",
            []
        )

        results = []

        for result in raw_results:
            results.append(
                {
                    "title": result.get(
                        "title",
                        ""
                    ),
                    "url": result.get(
                        "url",
                        ""
                    ),
                    "content": result.get(
                        "content",
                        ""
                    ),
                    "score": result.get(
                        "score"
                    ),
                }
            )

        return {
            "query": query.strip(),
            "results": results,
            "result_count": len(results),
        }