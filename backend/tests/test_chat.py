"""
Chat API Integration Test

Tests:
    1. Chat API health endpoint
    2. Main conversational endpoint
    3. Supervisor workflow execution
    4. Research result
    5. RAG result
    6. DOCX artifact
    7. PPTX artifact
    8. Validation result
    9. Generated artifact list
"""

import sys
from pathlib import Path


# ------------------------------------------------------------------
# Add backend directory to Python path
# ------------------------------------------------------------------

BACKEND_DIR = Path(__file__).resolve().parents[1]

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


# ------------------------------------------------------------------
# FastAPI Test Client
# ------------------------------------------------------------------

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


# ------------------------------------------------------------------
# Main Test
# ------------------------------------------------------------------

def main():

    print("=" * 70)
    print("CHAT API TEST")
    print("=" * 70)

    # ==============================================================
    # 1. Chat API Health
    # ==============================================================

    print("\n[1] Testing Chat API health...")
    print("-" * 70)

    response = client.get(
        "/api/chat/health"
    )

    print(
        "Status Code:",
        response.status_code
    )

    print(
        "Response:",
        response.json()
    )

    if response.status_code != 200:
        raise RuntimeError(
            "Chat API health check failed."
        )

    health = response.json()

    if health.get("status") != "healthy":
        raise RuntimeError(
            "Chat API returned an unhealthy status."
        )

    print(
        "Chat API health check PASSED."
    )

    # ==============================================================
    # 2. Main Chat Endpoint
    # ==============================================================

    print("\n[2] Testing main Chat endpoint...")
    print("-" * 70)

    payload = {
        "message": (
            "Research the latest generative AI trends in 2026 "
            "and create a professional business proposal."
        ),

        "generate_document": True,

        "generate_ppt": True,

        "slide_count": 8,
    }

    response = client.post(
        "/api/chat/",
        json=payload,
    )

    print(
        "Status Code:",
        response.status_code
    )

    # ==============================================================
    # 3. API Error Handling
    # ==============================================================

    if response.status_code != 200:

        print("\nCHAT API ERROR")
        print("-" * 70)

        try:
            print(response.json())

        except Exception:
            print(response.text)

        raise RuntimeError(
            "Chat API request failed."
        )

    # ==============================================================
    # 4. Parse Response
    # ==============================================================

    result = response.json()

    print("\n[3] CHAT RESPONSE")
    print("-" * 70)

    print(
        "Success:",
        result.get("success")
    )

    print(
        "Message:",
        result.get("message")
    )

    # ==============================================================
    # 5. Supervisor Plan
    # ==============================================================

    print("\n[4] SUPERVISOR PLAN")
    print("-" * 70)

    plan = result.get("plan")

    if isinstance(plan, dict):

        for key, value in plan.items():

            print(
                f"{key}: {value}"
            )

    else:

        print(
            "No supervisor plan returned."
        )

    # ==============================================================
    # 6. Research
    # ==============================================================

    print("\n[5] RESEARCH")
    print("-" * 70)

    research = result.get("research")

    if isinstance(research, dict):

        print(
            "Query:",
            research.get("query")
        )

        print(
            "Result Count:",
            research.get("result_count")
        )

        sources = research.get(
            "sources",
            []
        )

        print(
            "Source Count:",
            len(sources)
        )

        for index, source in enumerate(
            sources,
            start=1,
        ):

            if not isinstance(
                source,
                dict,
            ):
                continue

            print(
                f"\nSource {index}:"
            )

            print(
                "Title:",
                source.get("title")
            )

            print(
                "URL:",
                source.get("url")
            )

            print(
                "Score:",
                source.get("score")
            )

    else:

        print(
            "No research result returned."
        )

    # ==============================================================
    # 7. RAG
    # ==============================================================

    print("\n[6] RAG")
    print("-" * 70)

    rag = result.get("rag")

    if rag:

        if isinstance(rag, dict):

            print(
                "RAG result:"
            )

            for key, value in rag.items():

                print(
                    f"{key}: {value}"
                )

        else:

            print(rag)

    else:

        print(
            "No RAG result returned."
        )

    # ==============================================================
    # 8. DOCX
    # ==============================================================

    print("\n[7] DOCX ARTIFACT")
    print("-" * 70)

    document = result.get(
        "document"
    )

    if isinstance(
        document,
        dict,
    ):

        document_path = (
            document.get("file_path")
            or document.get("path")
            or document.get("output_path")
        )

        print(
            "Path:",
            document_path
        )

        print(
            "Editable:",
            document.get(
                "editable",
                True,
            )
        )

        if document_path:

            path = Path(
                document_path
            )

            print(
                "Exists:",
                path.exists()
            )

            if path.exists():

                print(
                    "Size:",
                    path.stat().st_size,
                    "bytes"
                )

    else:

        print(
            "No DOCX artifact returned."
        )

    # ==============================================================
    # 9. PPTX
    # ==============================================================

    print("\n[8] PPTX ARTIFACT")
    print("-" * 70)

    ppt = result.get(
        "ppt"
    )

    if isinstance(
        ppt,
        dict,
    ):

        ppt_path = (
            ppt.get("file_path")
            or ppt.get("path")
            or ppt.get("output_path")
        )

        print(
            "Path:",
            ppt_path
        )

        print(
            "Editable:",
            ppt.get(
                "editable",
                True,
            )
        )

        if ppt_path:

            path = Path(
                ppt_path
            )

            print(
                "Exists:",
                path.exists()
            )

            if path.exists():

                print(
                    "Size:",
                    path.stat().st_size,
                    "bytes"
                )

    else:

        print(
            "No PPTX artifact returned."
        )

    # ==============================================================
    # 10. Validation
    # ==============================================================

    print("\n[9] VALIDATION")
    print("-" * 70)

    validation = result.get(
        "validation"
    )

    print(
        validation
    )

    # ==============================================================
    # 11. Generated Artifacts
    # ==============================================================

    print("\n[10] ARTIFACTS")
    print("-" * 70)

    artifacts = result.get(
        "artifacts",
        []
    )

    if artifacts:

        for index, artifact in enumerate(
            artifacts,
            start=1,
        ):

            print(
                f"\nArtifact {index}:"
            )

            if isinstance(
                artifact,
                dict,
            ):

                for key, value in artifact.items():

                    print(
                        f"{key}: {value}"
                    )

            else:

                print(
                    artifact
                )

    else:

        print(
            "No artifacts returned."
        )

    # ==============================================================
    # 12. Errors / Warnings
    # ==============================================================

    print("\n[11] ERRORS / WARNINGS")
    print("-" * 70)

    errors = result.get(
        "errors",
        []
    )

    if errors:

        for error in errors:

            print(
                "-",
                error
            )

    else:

        print(
            "No workflow errors."
        )

    # ==============================================================
    # Final Status
    # ==============================================================

    print("\n" + "=" * 70)
    print("CHAT API TEST COMPLETE")
    print("=" * 70)


# ------------------------------------------------------------------
# Script Entry Point
# ------------------------------------------------------------------

if __name__ == "__main__":
    main()