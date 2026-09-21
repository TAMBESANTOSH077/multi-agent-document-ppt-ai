"""
Test Document Generator Agent.
"""

import sys
from pathlib import Path


# ---------------------------------------------------------------
# Backend path
# ---------------------------------------------------------------

BACKEND_DIR = Path(
    __file__
).resolve().parents[1]

if str(BACKEND_DIR) not in sys.path:

    sys.path.insert(
        0,
        str(BACKEND_DIR),
    )


from app.agents.document_generator import (
    DocumentGeneratorAgent,
)


def main():

    print("=" * 70)
    print("DOCUMENT GENERATOR TEST")
    print("=" * 70)

    # -----------------------------------------------------------
    # Sample content
    # -----------------------------------------------------------

    content = {

        "title":
            "Generative AI Enterprise Proposal",

        "subtitle":
            "AI Strategy and Implementation - 2026",

        "sections": [

            {
                "heading":
                    "Executive Summary",

                "content":
                    (
                        "Generative AI is becoming "
                        "an important component of "
                        "enterprise technology strategy."
                    ),

                "bullets": [

                    "AI agents automate multi-step workflows.",

                    "RAG provides enterprise knowledge retrieval.",

                    "AI improves document generation.",

                ],
            },

            {
                "heading":
                    "Technology Architecture",

                "content":
                    (
                        "The proposed system uses "
                        "multiple specialized AI agents."
                    ),

                "bullets": [

                    "FastAPI backend",

                    "Gemini LLM",

                    "ChromaDB vector database",

                    "Tavily web research",

                    "RAG Agent",

                    "Research Agent",

                ],
            },

            {
                "heading":
                    "Implementation Roadmap",

                "numbered": [

                    "Document ingestion",

                    "Knowledge indexing",

                    "Web research",

                    "Content generation",

                    "Output validation",

                ],
            },
        ],

        "tables": [

            {
                "headers": [
                    "Technology",
                    "Purpose",
                ],

                "rows": [

                    [
                        "FastAPI",
                        "Backend API",
                    ],

                    [
                        "Gemini",
                        "LLM generation",
                    ],

                    [
                        "ChromaDB",
                        "Vector search",
                    ],

                    [
                        "Tavily",
                        "Web research",
                    ],

                ],
            },
        ],
    }

    # -----------------------------------------------------------
    # Initialize
    # -----------------------------------------------------------

    print("\n[1] Initializing Document Generator...")

    try:

        generator = (
            DocumentGeneratorAgent()
        )

        print(
            "Document Generator initialized successfully."
        )

    except Exception as exc:

        print(
            "Initialization failed:"
        )

        print(exc)

        return

    # -----------------------------------------------------------
    # Generate
    # -----------------------------------------------------------

    print(
        "\n[2] Generating DOCX..."
    )

    try:

        result = generator.generate(
            content=content,
            filename=(
                "sample_ai_enterprise_proposal.docx"
            ),
        )

    except Exception as exc:

        print(
            "DOCX generation failed:"
        )

        print(exc)

        return

    # -----------------------------------------------------------
    # Result
    # -----------------------------------------------------------

    print(
        "\n[3] GENERATION RESULT"
    )

    print("-" * 70)

    print(
        "Success:",
        result.get("success"),
    )

    print(
        "Filename:",
        result.get("filename"),
    )

    print(
        "Path:",
        result.get("file_path"),
    )

    print(
        "File type:",
        result.get("file_type"),
    )

    print(
        "Editable:",
        result.get("editable"),
    )

    print(
        "Template used:",
        result.get("template_used"),
    )

    print(
        "Paragraphs:",
        result.get("paragraph_count"),
    )

    print(
        "Tables:",
        result.get("table_count"),
    )

    # -----------------------------------------------------------
    # Validate file
    # -----------------------------------------------------------

    print(
        "\n[4] VALIDATING FILE"
    )

    output_path = Path(
        result["file_path"]
    )

    if not output_path.exists():

        print(
            "ERROR: DOCX file does not exist."
        )

        return

    if output_path.stat().st_size == 0:

        print(
            "ERROR: DOCX file is empty."
        )

        return

    print(
        "DOCX file exists successfully."
    )

    print(
        "File size:",
        output_path.stat().st_size,
        "bytes",
    )

    # -----------------------------------------------------------
    # Final
    # -----------------------------------------------------------

    print("\n" + "=" * 70)

    print(
        "DOCUMENT GENERATOR TEST PASSED"
    )

    print("=" * 70)


if __name__ == "__main__":

    main()