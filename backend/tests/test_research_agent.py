"""
Manual test for the Research Agent.

Tests:
    1. ResearchAgent initialization
    2. Tavily web search
    3. Gemini research synthesis
    4. Source URL preservation
"""

import sys
from pathlib import Path


# ---------------------------------------------------------------
# Add backend directory to Python path
# ---------------------------------------------------------------
#
# File location:
#
# backend/
# ├── app/
# └── tests/
#     └── test_research_agent.py
#
# parents[1] points to:
# backend/
#
# This allows:
#     from app.agents.research_agent import ResearchAgent
#
# to work when running:
#     python tests/test_research_agent.py
# ---------------------------------------------------------------

BACKEND_DIR = Path(__file__).resolve().parents[1]

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


# ---------------------------------------------------------------
# Import Research Agent
# ---------------------------------------------------------------

from app.agents.research_agent import ResearchAgent


# ---------------------------------------------------------------
# Main Test
# ---------------------------------------------------------------

def main():
    """
    Run the complete Research Agent test.
    """

    print("=" * 70)
    print("RESEARCH AGENT TEST")
    print("=" * 70)

    # -----------------------------------------------------------
    # Initialize agent
    # -----------------------------------------------------------

    print("\n[1] Initializing Research Agent...")

    try:
        agent = ResearchAgent()

        print("Research Agent initialized successfully.")

    except Exception as exc:
        print("\nERROR: Failed to initialize Research Agent.")
        print(f"Details: {exc}")
        return

    # -----------------------------------------------------------
    # Research query
    # -----------------------------------------------------------

    query = "latest generative AI trends in 2026"

    print("\n[2] Research Query")
    print("-" * 70)
    print(query)

    # -----------------------------------------------------------
    # Execute research
    # -----------------------------------------------------------

    print("\n[3] Searching the web and generating research summary...")
    print("-" * 70)

    try:
        result = agent.research(
            query=query,
            max_results=3,
        )

    except Exception as exc:
        print("\nERROR: Research Agent failed.")
        print(f"Details: {exc}")
        return

    # -----------------------------------------------------------
    # Display query
    # -----------------------------------------------------------

    print("\n[4] QUERY")
    print("-" * 70)

    print(result.get("query", query))

    # -----------------------------------------------------------
    # Display summary
    # -----------------------------------------------------------

    print("\n[5] RESEARCH SUMMARY")
    print("-" * 70)

    summary = result.get(
        "summary",
        "No summary returned.",
    )

    print(summary)

    # -----------------------------------------------------------
    # Display sources
    # -----------------------------------------------------------

    print("\n[6] SOURCES")
    print("-" * 70)

    sources = result.get(
        "sources",
        [],
    )

    if not sources:
        print("No sources returned.")

    else:
        for index, source in enumerate(
            sources,
            start=1,
        ):
            print(f"\nSource {index}")

            print(
                "Title:",
                source.get("title", "N/A"),
            )

            print(
                "URL:",
                source.get("url", "N/A"),
            )

            print(
                "Score:",
                source.get("score", "N/A"),
            )

    # -----------------------------------------------------------
    # Display result count
    # -----------------------------------------------------------

    result_count = result.get(
        "result_count",
        len(sources),
    )

    print("\n[7] RESULT COUNT")
    print("-" * 70)

    print(result_count)

    # -----------------------------------------------------------
    # Final status
    # -----------------------------------------------------------

    print("\n" + "=" * 70)

    if result_count > 0 and summary:
        print("RESEARCH AGENT TEST PASSED")
    else:
        print("RESEARCH AGENT TEST COMPLETED")
        print("No usable research results were returned.")

    print("=" * 70)


# ---------------------------------------------------------------
# Script Entry Point
# ---------------------------------------------------------------

if __name__ == "__main__":
    main()