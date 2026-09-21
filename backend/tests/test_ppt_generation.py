"""
Manual test for PPTX generation.
"""

import sys
from pathlib import Path


# ---------------------------------------------------------------
# Add backend to Python path
# ---------------------------------------------------------------

BACKEND_DIR = Path(__file__).resolve().parents[1]

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


from app.agents.ppt_generator import (
    PPTGeneratorAgent,
)


def main():

    print("=" * 70)
    print("PPTX GENERATOR TEST")
    print("=" * 70)

    # -----------------------------------------------------------
    # Sample presentation content
    # -----------------------------------------------------------

    content = {

        "title": (
            "Generative AI Enterprise Proposal"
        ),

        "subtitle": (
            "AI Strategy and Implementation - 2026"
        ),

        "slides": [

            {
                "heading": "Executive Summary",

                "content": (
                    "Generative AI is becoming "
                    "an important component of "
                    "enterprise technology strategy."
                ),

                "bullets": [
                    "AI agents automate multi-step workflows.",
                    "RAG provides access to enterprise knowledge.",
                    "AI-assisted content generation improves productivity.",
                ],
            },

            {
                "heading": "Technology Architecture",

                "content": (
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
                "heading": "Business Benefits",

                "bullets": [
                    "Automated document generation",
                    "Real-time research",
                    "Enterprise knowledge retrieval",
                    "Editable DOCX and PPTX output",
                    "Conversational editing",
                ],
            },

            {
                "heading": "Implementation Roadmap",

                "content": (
                    "The implementation will proceed "
                    "through modular AI agents and "
                    "validated generation pipelines."
                ),
            },

        ],
    }

    # -----------------------------------------------------------
    # Initialize generator
    # -----------------------------------------------------------

    print("\n[1] Initializing PPT Generator...")

    try:

        generator = PPTGeneratorAgent()

        print(
            "PPT Generator initialized successfully."
        )

    except Exception as exc:

        print(
            f"PPT Generator initialization failed: {exc}"
        )

        return

    # -----------------------------------------------------------
    # Generate PPTX
    # -----------------------------------------------------------

    print("\n[2] Generating presentation...")

    try:

        result = generator.generate(
            content=content,
            filename=(
                "sample_ai_enterprise_proposal.pptx"
            ),
        )

    except Exception as exc:

        print(
            f"PPTX generation failed: {exc}"
        )

        return

    # -----------------------------------------------------------
    # Display result
    # -----------------------------------------------------------

    print("\n[3] GENERATION RESULT")
    print("-" * 70)

    print(
        "Success:",
        result["success"],
    )

    print(
        "Filename:",
        result["filename"],
    )

    print(
        "Path:",
        result["file_path"],
    )

    print(
        "File type:",
        result["file_type"],
    )

    print(
        "Editable:",
        result["editable"],
    )

    print(
        "Slide count:",
        result["slide_count"],
    )

    print(
        "Template used:",
        result["template_used"],
    )

    # -----------------------------------------------------------
    # Validate output
    # -----------------------------------------------------------

    output_path = Path(
        result["file_path"]
    )

    print("\n[4] VALIDATING FILE")
    print("-" * 70)

    if not output_path.exists():

        print(
            "ERROR: Generated PPTX file does not exist."
        )

        return

    if output_path.stat().st_size == 0:

        print(
            "ERROR: Generated PPTX file is empty."
        )

        return

    print(
        "Generated PPTX exists successfully."
    )

    print(
        "File size:",
        output_path.stat().st_size,
        "bytes",
    )

    # -----------------------------------------------------------
    # Final status
    # -----------------------------------------------------------

    print("\n" + "=" * 70)
    print("PPTX GENERATOR TEST PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()