"""
Test PPTX generation using an existing PPTX template.
"""

import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.agents.ppt_generator import PPTGeneratorAgent


def main():

    print("=" * 70)
    print("PPTX TEMPLATE GENERATION TEST")
    print("=" * 70)

    template_path = (
        BACKEND_DIR
        / "sample_data"
        / "templates"
        / "Company_Template.pptx"
    )

    if not template_path.exists():

        print("\nTemplate not found:")
        print(template_path)

        print(
            "\nPlace your PPTX template at:"
        )

        print(
            "backend/sample_data/templates/Company_Template.pptx"
        )

        return

    content = {
        "title": "AI Transformation Proposal",

        "subtitle": (
            "Enterprise Generative AI Strategy"
        ),

        "slides": [

            {
                "heading": "Executive Summary",

                "content": (
                    "This proposal presents a "
                    "multi-agent AI architecture "
                    "for enterprise document automation."
                ),

                "bullets": [
                    "Enterprise RAG",
                    "Real-time web research",
                    "Editable document generation",
                ],
            },

            {
                "heading": "AI Architecture",

                "content": (
                    "The system combines specialized "
                    "agents coordinated by a supervisor."
                ),

                "bullets": [
                    "Supervisor Agent",
                    "RAG Agent",
                    "Research Agent",
                    "Document Generator",
                    "PPT Generator",
                ],
            },

            {
                "heading": "Implementation",

                "bullets": [
                    "Document ingestion",
                    "Template analysis",
                    "Knowledge retrieval",
                    "Web research",
                    "Content generation",
                    "Validation",
                ],
            },
        ],
    }

    generator = PPTGeneratorAgent()

    try:

        result = generator.generate(
            content=content,
            filename="template_based_proposal.pptx",
            template_path=str(template_path),
        )

    except Exception as exc:

        print("\nTemplate generation failed:")
        print(exc)

        return

    print("\nGenerated successfully.")

    print(
        "File:",
        result["file_path"],
    )

    print(
        "Slides:",
        result["slide_count"],
    )

    print(
        "Template used:",
        result["template_used"],
    )

    output_path = Path(
        result["file_path"]
    )

    if output_path.exists():

        print("\n" + "=" * 70)
        print("PPTX TEMPLATE TEST PASSED")
        print("=" * 70)

    else:

        print(
            "\nGenerated file was not found."
        )


if __name__ == "__main__":
    main()