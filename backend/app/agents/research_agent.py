"""
Web Research Agent

Responsible for:

    1. Receiving a research request
    2. Searching the live web using Tavily
    3. Collecting relevant sources
    4. Asking Gemini to synthesize the findings
    5. Falling back to Tavily content when Gemini is unavailable
    6. Returning source URLs for traceability
"""

from typing import Any

from app.services.web_service import WebResearchService
from app.services.llm_service import LLMService


class ResearchAgent:
    """
    Agent responsible for real-time web research.

    Workflow:

        Research Question
                ↓
          Tavily Search
                ↓
         Web Sources
                ↓
        Context Builder
                ↓
             Gemini
                ↓
        ┌───────────────┐
        │ Gemini works? │
        └───────┬───────┘
           Yes  │  No / 429
                │
          ┌─────┴─────┐
          ↓           ↓
       Summary    Tavily Fallback
          │           │
          └─────┬─────┘
                ↓
         Research Summary
                ↓
          Source URLs
    """

    def __init__(self):
        """
        Initialize the research agent.
        """

        self.web_service = WebResearchService()
        self.llm_service = LLMService()

        self.name = "ResearchAgent"

    # ===========================================================
    # MAIN RESEARCH METHOD
    # ===========================================================

    def research(
        self,
        query: str,
        max_results: int = 5,
        topic: str = "general",
    ) -> dict[str, Any]:
        """
        Perform real-time web research and synthesize
        the retrieved information.

        Gemini is used when available.

        If Gemini is unavailable because of:
            - quota exhaustion
            - rate limiting
            - API errors
            - temporary service errors

        the agent falls back to the Tavily search results.

        Parameters
        ----------
        query:
            Research question.

        max_results:
            Maximum number of web results.

        topic:
            Tavily search topic.

        Returns
        -------
        dict
            Structured research result containing:

                query
                summary
                sources
                result_count
                synthesis_method
        """

        # -------------------------------------------------------
        # Validate query
        # -------------------------------------------------------

        if not query or not query.strip():
            raise ValueError(
                "Research query cannot be empty."
            )

        query = query.strip()

        # -------------------------------------------------------
        # Validate max_results
        # -------------------------------------------------------

        if max_results < 1:
            raise ValueError(
                "max_results must be at least 1."
            )

        # -------------------------------------------------------
        # Step 1: Search the live web
        # -------------------------------------------------------

        print(
            f"\n[ResearchAgent] Searching web for: {query}"
        )

        search_result = self.web_service.search(
            query=query,
            max_results=max_results,
            topic=topic,
        )

        results = search_result.get(
            "results",
            [],
        )

        # -------------------------------------------------------
        # Step 2: Handle no results
        # -------------------------------------------------------

        if not results:

            print(
                "[ResearchAgent] No web results found."
            )

            return {
                "query": query,
                "summary": (
                    "No relevant web sources were found "
                    "for this research query."
                ),
                "sources": [],
                "result_count": 0,
                "synthesis_method": "none",
            }

        print(
            f"[ResearchAgent] Found {len(results)} web sources."
        )

        # -------------------------------------------------------
        # Step 3: Build research context
        # -------------------------------------------------------

        context = self._build_context(
            results
        )

        # -------------------------------------------------------
        # Step 4: Build Gemini prompt
        # -------------------------------------------------------

        prompt = self._build_prompt(
            query=query,
            context=context,
        )

        # -------------------------------------------------------
        # Step 5: Try Gemini synthesis
        # -------------------------------------------------------

        summary = None
        synthesis_method = "tavily_fallback"

        try:

            print(
                "[ResearchAgent] Generating Gemini summary..."
            )

            summary = self.llm_service.generate_text(
                prompt
            )

            if summary and summary.strip():

                summary = summary.strip()

                synthesis_method = "gemini"

                print(
                    "[ResearchAgent] Gemini summary generated successfully."
                )

            else:

                print(
                    "[ResearchAgent] Gemini returned an empty response."
                )

        except Exception as exc:

            # ---------------------------------------------------
            # Gemini failed.
            #
            # This can happen because of:
            #   - HTTP 429 quota exhaustion
            #   - API rate limits
            #   - temporary Gemini errors
            #   - network errors
            #
            # Do NOT fail the complete research workflow.
            # Use the already retrieved Tavily sources.
            # ---------------------------------------------------

            print(
                "\n[ResearchAgent] WARNING:"
            )

            print(
                "Gemini research summarization failed."
            )

            print(
                f"Reason: {exc}"
            )

            print(
                "Using Tavily results as fallback summary."
            )

        # -------------------------------------------------------
        # Step 6: Tavily fallback
        # -------------------------------------------------------

        if not summary:

            summary = self._fallback_summary(
                query=query,
                results=results,
            )

            synthesis_method = "tavily_fallback"

        # -------------------------------------------------------
        # Step 7: Preserve source traceability
        # -------------------------------------------------------

        sources = self._build_sources(
            results
        )

        # -------------------------------------------------------
        # Step 8: Return structured result
        # -------------------------------------------------------

        return {
            "query": query,
            "summary": summary,
            "sources": sources,
            "result_count": len(results),
            "synthesis_method": synthesis_method,
        }

    # ===========================================================
    # BUILD RESEARCH CONTEXT
    # ===========================================================

    @staticmethod
    def _build_context(
        results: list[dict[str, Any]],
    ) -> str:
        """
        Convert Tavily search results into a structured
        context string for Gemini.
        """

        context_parts: list[str] = []

        for index, result in enumerate(
            results,
            start=1,
        ):

            title = result.get(
                "title",
                "",
            )

            url = result.get(
                "url",
                "",
            )

            content = (
                result.get("content")
                or result.get("snippet")
                or result.get("description")
                or ""
            )

            context_parts.append(
                f"""
SOURCE {index}

Title:
{title}

URL:
{url}

Content:
{content}
""".strip()
            )

        return "\n\n".join(
            context_parts
        )

    # ===========================================================
    # BUILD GEMINI PROMPT
    # ===========================================================

    @staticmethod
    def _build_prompt(
        query: str,
        context: str,
    ) -> str:
        """
        Build the prompt used by Gemini to synthesize
        the web research results.
        """

        return f"""
You are a professional web research assistant.

Research question:
{query}

Use ONLY the web sources provided below.

Instructions:

1. Summarize the information clearly.
2. Do not invent facts.
3. Do not introduce unsupported claims.
4. Identify important facts and trends.
5. If sources disagree, explicitly mention the disagreement.
6. Keep the response structured and useful.
7. Do not fabricate URLs.
8. Do not claim that information came from a source
   unless it is present in that source.
9. Prefer information supported by multiple sources.
10. Keep the final response concise but informative.

Web Sources:
-------------------------
{context}
-------------------------

Provide a concise research summary.
""".strip()

    # ===========================================================
    # TAVILY FALLBACK SUMMARY
    # ===========================================================

    @staticmethod
    def _fallback_summary(
        query: str,
        results: list[dict[str, Any]],
    ) -> str:
        """
        Create a research summary directly from Tavily results.

        This method does not call Gemini.

        It is used when Gemini is unavailable, for example
        because the API quota has been exhausted.
        """

        if not results:

            return (
                f"No web research results were found "
                f"for: {query}"
            )

        lines: list[str] = []

        lines.append(
            f"Research results for: {query}"
        )

        lines.append("")

        lines.append(
            "The following information was retrieved "
            "from live web sources:"
        )

        lines.append("")

        # -------------------------------------------------------
        # Add each source
        # -------------------------------------------------------

        for index, result in enumerate(
            results,
            start=1,
        ):

            title = (
                result.get("title")
                or "Untitled source"
            )

            url = (
                result.get("url")
                or ""
            )

            content = (
                result.get("content")
                or result.get("snippet")
                or result.get("description")
                or ""
            )

            # Clean whitespace
            clean_content = " ".join(
                str(content).split()
            )

            # Keep fallback output readable.
            # Avoid putting extremely large web pages
            # into the generated document.
            if len(clean_content) > 700:
                clean_content = (
                    clean_content[:700]
                    + "..."
                )

            lines.append(
                f"{index}. {title}"
            )

            if clean_content:

                lines.append(
                    f"   {clean_content}"
                )

            if url:

                lines.append(
                    f"   Source: {url}"
                )

            lines.append("")

        return "\n".join(
            lines
        ).strip()

    # ===========================================================
    # BUILD SOURCE METADATA
    # ===========================================================

    @staticmethod
    def _build_sources(
        results: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """
        Preserve source metadata for traceability.
        """

        sources: list[dict[str, Any]] = []

        for result in results:

            sources.append(
                {
                    "title": result.get(
                        "title"
                    ),
                    "url": result.get(
                        "url"
                    ),
                    "score": result.get(
                        "score"
                    ),
                }
            )

        return sources

    # ===========================================================
    # SIMPLE QUERY METHOD
    # ===========================================================

    def search(
        self,
        query: str,
        max_results: int = 5,
        topic: str = "general",
    ) -> dict[str, Any]:
        """
        Convenience method.

        Allows callers to use:

            agent.search(...)

        instead of:

            agent.research(...)
        """

        return self.research(
            query=query,
            max_results=max_results,
            topic=topic,
        )


# ===============================================================
# MANUAL TEST
# ===============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("RESEARCH AGENT TEST")
    print("=" * 70)

    agent = ResearchAgent()

    print()
    print("[1] Research Agent initialized successfully.")

    query = "latest generative AI trends in 2026"

    print()
    print("[2] Research Query")
    print("-" * 70)
    print(query)

    print()
    print("[3] Running research...")
    print("-" * 70)

    result = agent.research(
        query=query,
        max_results=3,
    )

    print()
    print("[4] RESEARCH SUMMARY")
    print("-" * 70)

    print(
        result["summary"]
    )

    print()
    print("[5] SYNTHESIS METHOD")
    print("-" * 70)

    print(
        result["synthesis_method"]
    )

    print()
    print("[6] SOURCES")
    print("-" * 70)

    for index, source in enumerate(
        result["sources"],
        start=1,
    ):

        print()
        print(
            f"Source {index}"
        )

        print(
            "Title:",
            source.get("title"),
        )

        print(
            "URL:",
            source.get("url"),
        )

        print(
            "Score:",
            source.get("score"),
        )

    print()
    print("[7] RESULT COUNT")
    print("-" * 70)

    print(
        result["result_count"]
    )

    print()
    print("=" * 70)
    print("RESEARCH AGENT TEST COMPLETE")
    print("=" * 70)