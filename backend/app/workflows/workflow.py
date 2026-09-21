"""
Multi-Agent Document AI Workflow.

Coordinates:
    - Supervisor Agent
    - Research Agent
    - RAG Agent
    - Document Analysis Agent
    - DOCX Generator
    - PPT Generator
    - Validation Agent

The workflow keeps the agents modular while providing
one orchestration layer for the complete document-generation
pipeline.
"""

from pathlib import Path
from typing import Any

from app.agents.supervisor import SupervisorAgent
from app.agents.research_agent import ResearchAgent
from app.agents.rag_agent import RAGAgent
from app.agents.document_agent import DocumentAnalysisAgent
from app.agents.document_generator import DocumentGeneratorAgent
from app.agents.ppt_generator import PPTGeneratorAgent
from app.agents.validation_agent import ValidationAgent


class DocumentAIWorkflow:
    """
    Orchestrates the multi-agent document generation workflow.
    """

    def __init__(self):

        # -------------------------------------------------------
        # Initialize agents
        # -------------------------------------------------------

        self.supervisor = SupervisorAgent()

        self.research_agent = ResearchAgent()

        self.rag_agent = RAGAgent()

        self.document_agent = (
            DocumentAnalysisAgent()
        )

        self.document_generator = (
            DocumentGeneratorAgent()
        )

        self.ppt_generator = (
            PPTGeneratorAgent()
        )

        self.validation_agent = (
            ValidationAgent()
        )

    # ===========================================================
    # MAIN WORKFLOW
    # ===========================================================

    def run(
        self,
        query: str,
        document_path: str | None = None,
        ppt_template_path: str | None = None,
        generate_document: bool = True,
        generate_presentation: bool = True,
    ) -> dict[str, Any]:
        """
        Execute the complete multi-agent workflow.

        Parameters
        ----------
        query:
            User's natural-language request.

        document_path:
            Optional source document.

        ppt_template_path:
            Optional PPTX template.

        generate_document:
            Whether DOCX should be generated.

        generate_presentation:
            Whether PPTX should be generated.

        Returns
        -------
        dict
            Complete workflow result.
        """

        if not query or not query.strip():

            raise ValueError(
                "Query cannot be empty."
            )

        # -------------------------------------------------------
        # Workflow state
        # -------------------------------------------------------

        state: dict[str, Any] = {

            "query": query,

            "document_path": document_path,

            "ppt_template_path": ppt_template_path,

            "research": None,

            "rag": None,

            "document_analysis": None,

            "generated_document": None,

            "generated_presentation": None,

            "validation": None,

            "errors": [],
        }

        # -------------------------------------------------------
        # STEP 1 — Supervisor
        # -------------------------------------------------------

        try:

            plan = self.supervisor.plan(
                query=query
            )

            state["plan"] = plan

        except Exception as exc:

            state["plan"] = {
                "task": "document_generation",
                "reason": "Default workflow fallback",
            }

            state["errors"].append(
                f"Supervisor: {exc}"
            )

        # -------------------------------------------------------
        # STEP 2 — Document Analysis
        # -------------------------------------------------------

        if document_path:

            try:

                document_path_obj = Path(
                    document_path
                )

                if document_path_obj.exists():

                    from app.services.document_service import (
                        extract_document,
                    )

                    extracted = extract_document(
                        str(document_path_obj)
                    )

                    state[
                        "document_analysis"
                    ] = self.document_agent.analyze(
                        extracted
                    )

            except Exception as exc:

                state["errors"].append(
                    f"Document analysis: {exc}"
                )

        # -------------------------------------------------------
        # STEP 3 — RAG
        # -------------------------------------------------------

        try:

            rag_result = self.rag_agent.answer(
                query,
                top_k=5,
            )

            state["rag"] = rag_result

        except Exception as exc:

            state["errors"].append(
                f"RAG: {exc}"
            )

            state["rag"] = {
                "answer": "",
                "sources": [],
                "retrieved_chunks": [],
            }

        # -------------------------------------------------------
        # STEP 4 — Web Research
        # -------------------------------------------------------

        try:

            research_result = (
                self.research_agent.research(
                    query,
                    max_results=5,
                )
            )

            state["research"] = (
                research_result
            )

        except Exception as exc:

            state["errors"].append(
                f"Research: {exc}"
            )

            state["research"] = {
                "query": query,
                "summary": "",
                "sources": [],
                "result_count": 0,
            }

        # -------------------------------------------------------
        # STEP 5 — Build generation content
        # -------------------------------------------------------

        content = self._build_content(
            query=query,
            state=state,
        )

        state["content"] = content

        # -------------------------------------------------------
        # STEP 6 — Generate DOCX
        # -------------------------------------------------------

        if generate_document:

            try:

                result = (
                    self.document_generator.generate(
                        content=content,
                        filename=(
                            "generated_document.docx"
                        ),
                    )
                )

                state[
                    "generated_document"
                ] = result

            except Exception as exc:

                state["errors"].append(
                    f"DOCX generation: {exc}"
                )

        # -------------------------------------------------------
        # STEP 7 — Generate PPTX
        # -------------------------------------------------------

        if generate_presentation:

            try:

                result = (
                    self.ppt_generator.generate(
                        content=content,
                        filename=(
                            "generated_presentation.pptx"
                        ),
                        template_path=(
                            ppt_template_path
                        ),
                    )
                )

                state[
                    "generated_presentation"
                ] = result

            except Exception as exc:

                state["errors"].append(
                    f"PPTX generation: {exc}"
                )

        # -------------------------------------------------------
        # STEP 8 — Validation
        # -------------------------------------------------------

        try:

            validation = (
                self._validate_outputs(
                    state
                )
            )

            state["validation"] = (
                validation
            )

        except Exception as exc:

            state["errors"].append(
                f"Validation: {exc}"
            )

        # -------------------------------------------------------
        # Final status
        # -------------------------------------------------------

        state["success"] = (
            state["generated_document"]
            is not None
            or state["generated_presentation"]
            is not None
        )

        return state

    # ===========================================================
    # BUILD CONTENT
    # ===========================================================

    def _build_content(
        self,
        query: str,
        state: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Convert research/RAG information into the
        structured content expected by the generators.
        """

        research = (
            state.get("research")
            or {}
        )

        rag = (
            state.get("rag")
            or {}
        )

        research_summary = (
            research.get(
                "summary",
                "",
            )
        )

        rag_answer = (
            rag.get(
                "answer",
                "",
            )
        )

        sources = (
            research.get(
                "sources",
                [],
            )
        )

        sections = []

        # -------------------------------------------------------
        # Executive Summary
        # -------------------------------------------------------

        summary_parts = []

        if research_summary:

            summary_parts.append(
                research_summary
            )

        if rag_answer:

            summary_parts.append(
                rag_answer
            )

        executive_summary = (
            "\n\n".join(summary_parts)
        )

        if not executive_summary:

            executive_summary = (
                "This document was generated "
                "using the Multi-Agent Document AI "
                "workflow."
            )

        sections.append(
            {
                "heading": "Executive Summary",

                "content": executive_summary,

                "bullets": [],
            }
        )

        # -------------------------------------------------------
        # Research Sources
        # -------------------------------------------------------

        source_bullets = []

        for source in sources:

            if not isinstance(
                source,
                dict,
            ):
                continue

            title = source.get(
                "title",
                "Source",
            )

            url = source.get(
                "url",
                "",
            )

            if url:

                source_bullets.append(
                    f"{title} - {url}"
                )

            else:

                source_bullets.append(
                    str(title)
                )

        if source_bullets:

            sections.append(
                {
                    "heading":
                        "Research Sources",

                    "content":
                        "Sources used during research.",

                    "bullets":
                        source_bullets,
                }
            )

        # -------------------------------------------------------
        # RAG Sources
        # -------------------------------------------------------

        rag_sources = (
            rag.get(
                "sources",
                [],
            )
        )

        rag_bullets = []

        for source in rag_sources:

            if isinstance(
                source,
                dict,
            ):

                filename = source.get(
                    "filename",
                    source.get(
                        "file",
                        "Document",
                    ),
                )

                chunk_index = source.get(
                    "chunk_index",
                    "",
                )

                rag_bullets.append(
                    f"{filename} "
                    f"(chunk {chunk_index})"
                )

        if rag_bullets:

            sections.append(
                {
                    "heading":
                        "Knowledge Base Sources",

                    "content":
                        "Relevant information retrieved "
                        "from the enterprise knowledge base.",

                    "bullets":
                        rag_bullets,
                }
            )

        # -------------------------------------------------------
        # Final structured content
        # -------------------------------------------------------

        return {

            "title":
                "AI-Generated Proposal",

            "subtitle":
                query,

            "sections":
                sections,

            "paragraphs": [],

            "tables": [],
        }

    # ===========================================================
    # VALIDATION
    # ===========================================================

    def _validate_outputs(
        self,
        state: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Perform basic output validation.
        """

        results = []

        # -------------------------------------------------------
        # DOCX
        # -------------------------------------------------------

        document_result = (
            state.get(
                "generated_document"
            )
        )

        if document_result:

            path = Path(
                document_result[
                    "file_path"
                ]
            )

            results.append(
                {
                    "type": "docx",

                    "exists":
                        path.exists(),

                    "size":
                        path.stat().st_size
                        if path.exists()
                        else 0,
                }
            )

        # -------------------------------------------------------
        # PPTX
        # -------------------------------------------------------

        presentation_result = (
            state.get(
                "generated_presentation"
            )
        )

        if presentation_result:

            path = Path(
                presentation_result[
                    "file_path"
                ]
            )

            results.append(
                {
                    "type": "pptx",

                    "exists":
                        path.exists(),

                    "size":
                        path.stat().st_size
                        if path.exists()
                        else 0,
                }
            )

        # -------------------------------------------------------
        # Overall
        # -------------------------------------------------------

        valid = all(
            item["exists"]
            and item["size"] > 0
            for item in results
        )

        return {
            "valid": valid,
            "artifacts": results,
        }