"""
Document Analysis Agent

This agent analyzes extracted document text and creates a
structured profile of the document.

Responsibilities:
    - Identify document type and structure
    - Count words and characters
    - Identify headings
    - Identify tables
    - Estimate writing tone
    - Estimate writing style
    - Extract important topics
    - Create a short summary

The deterministic analysis is performed first. This gives us
a reliable document profile that can later be enhanced with
Gemini semantic analysis.
"""

import re
from typing import Any


class DocumentAnalysisAgent:
    """
    Analyze extracted document content.

    This class intentionally keeps the first analysis layer
    deterministic. It does not require an LLM, which makes it
    fast, predictable, and easy to test.
    """

    def analyze(
        self,
        document: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Analyze a document returned by document_service.

        Expected input:

            {
                "filename": "...",
                "file_type": "...",
                "text": "...",
                "character_count": 1234,
                "word_count": 250
            }
        """

        text = document.get("text", "").strip()

        if not text:
            raise ValueError(
                "Document contains no extractable text."
            )

        filename = document.get(
            "filename",
            "Unknown document",
        )

        file_type = document.get(
            "file_type",
            "unknown",
        )

        # -------------------------------------------------------
        # Basic statistics
        # -------------------------------------------------------

        words = text.split()

        paragraphs = [
            paragraph.strip()
            for paragraph in text.split("\n\n")
            if paragraph.strip()
        ]

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        # -------------------------------------------------------
        # Heading detection
        # -------------------------------------------------------

        headings = self._detect_headings(
            lines
        )

        # -------------------------------------------------------
        # Table detection
        # -------------------------------------------------------

        table_count = self._estimate_table_count(
            text
        )

        # -------------------------------------------------------
        # Tone and writing style
        # -------------------------------------------------------

        tone = self._detect_tone(
            text
        )

        writing_style = self._detect_writing_style(
            text,
            words,
        )

        # -------------------------------------------------------
        # Topic extraction
        # -------------------------------------------------------

        topics = self._extract_topics(
            text
        )

        # -------------------------------------------------------
        # Basic summary
        # -------------------------------------------------------

        summary = self._create_summary(
            paragraphs
        )

        return {
            "analysis_type": "deterministic_document_analysis",

            "document": {
                "filename": filename,
                "file_type": file_type,
            },

            "statistics": {
                "character_count": len(text),
                "word_count": len(words),
                "paragraph_count": len(paragraphs),
                "line_count": len(lines),
                "heading_count": len(headings),
                "table_count": table_count,
            },

            "structure": {
                "headings": headings,
                "paragraphs": paragraphs,
            },

            "style": {
                "tone": tone,
                "writing_style": writing_style,
            },

            "topics": topics,

            "summary": summary,
        }

    # ===========================================================
    # HEADING DETECTION
    # ===========================================================

    def _detect_headings(
        self,
        lines: list[str],
    ) -> list[str]:
        """
        Detect likely headings using simple structural signals.

        This is heuristic analysis, not semantic classification.
        """

        headings: list[str] = []

        for line in lines:

            cleaned = line.strip()

            if not cleaned:
                continue

            # Ignore very long lines because they are more likely
            # to be paragraph content.
            if len(cleaned) > 100:
                continue

            # Markdown-style headings.
            if cleaned.startswith("#"):
                headings.append(
                    cleaned.lstrip("#").strip()
                )
                continue

            # Numbered headings such as:
            # 1. Introduction
            # 2. Architecture
            if re.match(
                r"^\d+[\.\)]\s+\S+",
                cleaned,
            ):
                headings.append(cleaned)
                continue

            # Short lines with title-like capitalization.
            words = cleaned.split()

            if (
                1 <= len(words) <= 8
                and len(cleaned) <= 80
                and cleaned[-1] not in ".?!,:;"
            ):
                if cleaned[0].isupper():
                    headings.append(cleaned)

        return headings[:30]

    # ===========================================================
    # TABLE DETECTION
    # ===========================================================

    def _estimate_table_count(
        self,
        text: str,
    ) -> int:
        """
        Estimate tables in extracted text.

        The document extraction service represents table rows
        using pipe separators, for example:

            Name | Role | Experience

        This method therefore provides an approximate count.
        """

        table_rows = []

        for line in text.splitlines():

            if line.count("|") >= 2:
                table_rows.append(line)

        if not table_rows:
            return 0

        # Consecutive table rows are treated as one table.
        table_count = 1

        for index in range(1, len(table_rows)):

            previous = table_rows[index - 1]
            current = table_rows[index]

            if current.strip() == "":
                table_count += 1

        return table_count

    # ===========================================================
    # TONE DETECTION
    # ===========================================================

    def _detect_tone(
        self,
        text: str,
    ) -> str:
        """
        Estimate the document's general tone.

        This is a heuristic baseline. Later, Gemini can provide
        deeper semantic tone analysis.
        """

        lower_text = text.lower()

        business_words = {
            "business",
            "strategy",
            "market",
            "revenue",
            "customer",
            "company",
            "organization",
            "proposal",
            "investment",
            "growth",
        }

        technical_words = {
            "api",
            "database",
            "algorithm",
            "architecture",
            "python",
            "javascript",
            "software",
            "system",
            "model",
            "machine learning",
            "artificial intelligence",
        }

        business_score = sum(
            lower_text.count(word)
            for word in business_words
        )

        technical_score = sum(
            lower_text.count(word)
            for word in technical_words
        )

        if technical_score > business_score:
            return "technical"

        if business_score > technical_score:
            return "business"

        return "general"

    # ===========================================================
    # WRITING STYLE
    # ===========================================================

    def _detect_writing_style(
        self,
        text: str,
        words: list[str],
    ) -> str:
        """
        Estimate whether the writing is concise or detailed.
        """

        if not words:
            return "unknown"

        sentence_count = max(
            1,
            len(
                re.findall(
                    r"[.!?]+",
                    text,
                )
            ),
        )

        average_sentence_length = (
            len(words) / sentence_count
        )

        if average_sentence_length < 12:
            return "concise"

        if average_sentence_length > 25:
            return "detailed"

        return "balanced"

    # ===========================================================
    # TOPIC EXTRACTION
    # ===========================================================

    def _extract_topics(
        self,
        text: str,
    ) -> list[str]:
        """
        Identify common technology/business topics.

        This is a lightweight baseline. The future semantic
        analysis layer can replace this with LLM-based extraction.
        """

        topic_dictionary = {
            "Artificial Intelligence": [
                "artificial intelligence",
                " ai ",
            ],
            "Machine Learning": [
                "machine learning",
                " ml ",
            ],
            "Deep Learning": [
                "deep learning",
            ],
            "Generative AI": [
                "generative ai",
                "genai",
            ],
            "LLM": [
                "large language model",
                "llm",
                "llms",
            ],
            "RAG": [
                "retrieval augmented generation",
                "rag",
            ],
            "Python": [
                "python",
            ],
            "JavaScript": [
                "javascript",
            ],
            "Database": [
                "database",
                "sql",
                "mysql",
                "postgresql",
            ],
            "API": [
                "api",
            ],
            "Cloud": [
                "aws",
                "azure",
                "google cloud",
                "cloud computing",
            ],
        }

        lower_text = f" {text.lower()} "

        detected_topics: list[str] = []

        for topic, keywords in topic_dictionary.items():

            for keyword in keywords:

                if keyword in lower_text:
                    detected_topics.append(topic)
                    break

        return detected_topics

    # ===========================================================
    # SUMMARY
    # ===========================================================

    def _create_summary(
        self,
        paragraphs: list[str],
    ) -> str:
        """
        Create a simple deterministic summary.

        Currently we use the first few meaningful paragraphs.
        A Gemini-based summarizer can later improve this.
        """

        if not paragraphs:
            return ""

        summary_parts = paragraphs[:3]

        summary = " ".join(
            summary_parts
        )

        # Keep the deterministic summary reasonably short.
        if len(summary) > 800:
            summary = summary[:800].rsplit(
                " ",
                1,
            )[0] + "..."

        return summary