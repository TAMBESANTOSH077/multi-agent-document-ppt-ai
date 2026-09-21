"""
Integration test for the Multi-Agent Document AI workflow.
"""

import sys
from pathlib import Path


BACKEND_DIR = (
    Path(__file__)
    .resolve()
    .parents[1]
)

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(
        0,
        str(BACKEND_DIR),
    )


from app.workflows.workflow import (
    DocumentAIWorkflow,
)


def main():

    print("=" * 70)
    print("MULTI-AGENT WORKFLOW TEST")
    print("=" * 70)

    query = (
        "Create an enterprise proposal about "
        "generative AI trends and AI agents in 2026."
    )

    print("\n[1] Query")
    print(query)

    print(
        "\n[2] Initializing workflow..."
    )

    try:

        workflow = DocumentAIWorkflow()

        print(
            "Workflow initialized successfully."
        )

    except Exception as exc:

        print(
            "Workflow initialization failed:"
        )

        print(exc)

        return

    print(
        "\n[3] Running multi-agent workflow..."
    )

    try:

        result = workflow.run(
            query=query,
            generate_document=True,
            generate_presentation=True,
        )

    except Exception as exc:

        print(
            "Workflow execution failed:"
        )

        print(exc)

        return

    print(
        "\n[4] WORKFLOW RESULT"
    )

    print("-" * 70)

    print(
        "Success:",
        result.get("success"),
    )

    print(
        "Errors:",
        result.get("errors"),
    )

    # -----------------------------------------------------------
    # DOCX
    # -----------------------------------------------------------

    document = result.get(
        "generated_document"
    )

    if document:

        print("\nDOCX")

        print(
            "Path:",
            document.get(
                "file_path"
            ),
        )

        print(
            "Editable:",
            document.get(
                "editable"
            ),
        )

    # -----------------------------------------------------------
    # PPTX
    # -----------------------------------------------------------

    presentation = result.get(
        "generated_presentation"
    )

    if presentation:

        print("\nPPTX")

        print(
            "Path:",
            presentation.get(
                "file_path"
            ),
        )

        print(
            "Editable:",
            presentation.get(
                "editable"
            ),
        )

    # -----------------------------------------------------------
    # Validation
    # -----------------------------------------------------------

    validation = result.get(
        "validation"
    )

    print(
        "\nValidation:",
        validation,
    )

    print("\n" + "=" * 70)
    print("MULTI-AGENT WORKFLOW TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()