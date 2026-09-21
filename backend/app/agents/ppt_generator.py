"""
PPT Generator Agent

Responsible for generating editable PowerPoint presentations.

Features:
    - Creates editable PPTX files.
    - Supports existing PPTX templates.
    - Preserves template slide dimensions.
    - Supports title/content slide generation.
    - Supports list, dictionary, and string content.
    - Supports both `filename` and `output_filename`.
    - Guarantees at least one slide.
    - Verifies the generated file.
"""

from pathlib import Path
from typing import Any

from pptx import Presentation
from pptx.util import Inches, Pt


class PPTGeneratorAgent:
    """
    Agent responsible for generating editable PowerPoint presentations.
    """

    def __init__(
        self,
        output_directory: str = "storage/generated",
    ) -> None:

        self.name = "PPTGeneratorAgent"

        self.output_directory = Path(
            output_directory
        )

        self.output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    # ==========================================================
    # MAIN GENERATION METHOD
    # ==========================================================

    def generate(
        self,
        title: str = "AI Generated Presentation",
        content: Any = None,
        template_path: str | None = None,
        output_filename: str = "generated_presentation.pptx",
        slide_count: int = 5,
        filename: str | None = None,
    ) -> dict[str, Any]:
        """
        Generate an editable PowerPoint presentation.

        Parameters
        ----------
        title:
            Presentation title.

        content:
            Content used to generate slides.

            Supported formats:

            1. List:

                [
                    {
                        "title": "Introduction",
                        "content": "..."
                    },
                    {
                        "title": "Architecture",
                        "content": "..."
                    }
                ]

            2. Dictionary:

                {
                    "slides": [...]
                }

            3. String:

                "Presentation content..."

        template_path:
            Optional path to an existing PPTX template.

        output_filename:
            Output filename.

        slide_count:
            Maximum number of generated slides for
            automatically split content.

        filename:
            Backward-compatible alias for output_filename.

            Existing workflow code may call:

                filename="proposal.pptx"

            while newer code may call:

                output_filename="proposal.pptx"
        """

        # ------------------------------------------------------
        # Backward compatibility
        # ------------------------------------------------------

        if filename:
            output_filename = filename

        # ------------------------------------------------------
        # Validate filename
        # ------------------------------------------------------

        if not output_filename:

            output_filename = (
                "generated_presentation.pptx"
            )

        if not output_filename.lower().endswith(
            ".pptx"
        ):

            output_filename += ".pptx"

        # ------------------------------------------------------
        # Validate slide count
        # ------------------------------------------------------

        if slide_count < 1:

            slide_count = 1

        # ------------------------------------------------------
        # Load template
        # ------------------------------------------------------

        template_used = False

        if template_path:

            template = Path(
                template_path
            )

            if template.exists():

                if template.suffix.lower() != ".pptx":

                    raise ValueError(
                        "PPT template must be a .pptx file."
                    )

                presentation = Presentation(
                    str(template)
                )

                template_used = True

            else:

                # Template was requested but was not found.
                # Create a normal presentation instead.

                presentation = Presentation()

        else:

            presentation = Presentation()

        # ------------------------------------------------------
        # Prepare slide content
        # ------------------------------------------------------

        slides_data = (
            self._prepare_slide_content(
                title=title,
                content=content,
                slide_count=slide_count,
            )
        )

        # ------------------------------------------------------
        # Add generated slides
        # ------------------------------------------------------

        for slide_data in slides_data:

            self._add_slide(
                presentation=presentation,
                slide_data=slide_data,
            )

        # ------------------------------------------------------
        # IMPORTANT SAFETY CHECK
        #
        # python-pptx cannot save an empty presentation.
        # Always guarantee at least one slide.
        # ------------------------------------------------------

        if len(presentation.slides) == 0:

            self._add_fallback_slide(
                presentation=presentation,
                title=title,
            )

        # ------------------------------------------------------
        # Output path
        # ------------------------------------------------------

        output_path = (
            self.output_directory
            / output_filename
        )

        # ------------------------------------------------------
        # Save PPTX
        # ------------------------------------------------------

        presentation.save(
            str(output_path)
        )

        # ------------------------------------------------------
        # Verify file
        # ------------------------------------------------------

        if not output_path.exists():

            raise RuntimeError(
                "PPTX generation failed: "
                "output file was not created."
            )

        if output_path.stat().st_size <= 0:

            raise RuntimeError(
                "PPTX generation failed: "
                "output file is empty."
            )

        # ------------------------------------------------------
        # Return generation information
        # ------------------------------------------------------

        return {
    "success": True,

    # File information
    "type": "pptx",
    "file_type": "pptx",
    "filename": output_path.name,

    # Keep all path aliases for compatibility
    "path": str(output_path),
    "file_path": str(output_path),
    "output_path": str(output_path),

    # Presentation information
    "slides": len(presentation.slides),
    "slide_count": len(presentation.slides),

    # Template information
    "template_used": template_used,

    # Editability
    "editable": True,
}

    # ==========================================================
    # PREPARE SLIDE CONTENT
    # ==========================================================

    def _prepare_slide_content(
        self,
        title: str,
        content: Any,
        slide_count: int,
    ) -> list[dict[str, Any]]:
        """
        Convert different content formats into a standard
        slide representation.
        """

        slides: list[dict[str, Any]] = []

        # ------------------------------------------------------
        # CASE 1: List of slides
        # ------------------------------------------------------

        if isinstance(
            content,
            list,
        ):

            for index, item in enumerate(
                content
            ):

                if isinstance(
                    item,
                    dict,
                ):

                    slide_title = item.get(
                        "title",
                        f"Slide {index + 1}",
                    )

                    slide_content = item.get(
                        "content",
                        item.get(
                            "body",
                            item.get(
                                "text",
                                "",
                            ),
                        ),
                    )

                else:

                    slide_title = (
                        f"Slide {index + 1}"
                    )

                    slide_content = str(
                        item
                    )

                slides.append(
                    {
                        "title": str(
                            slide_title
                        ),
                        "content": str(
                            slide_content
                        ),
                    }
                )

            if slides:

                return slides

        # ------------------------------------------------------
        # CASE 2: Dictionary
        # ------------------------------------------------------

        if isinstance(
            content,
            dict,
        ):

            # ----------------------------------------------
            # Standard AI-generated format
            # ----------------------------------------------

            if isinstance(
                content.get("slides"),
                list,
            ):

                return self._prepare_slide_content(
                    title=title,
                    content=content["slides"],
                    slide_count=slide_count,
                )

            # ----------------------------------------------
            # Sections format
            # ----------------------------------------------

            sections = content.get(
                "sections"
            )

            if isinstance(
                sections,
                list,
            ):

                for index, section in enumerate(
                    sections
                ):

                    if isinstance(
                        section,
                        dict,
                    ):

                        section_title = section.get(
                            "title",
                            f"Section {index + 1}",
                        )

                        section_content = section.get(
                            "content",
                            section.get(
                                "body",
                                "",
                            ),
                        )

                    else:

                        section_title = (
                            f"Section {index + 1}"
                        )

                        section_content = str(
                            section
                        )

                    slides.append(
                        {
                            "title": str(
                                section_title
                            ),
                            "content": str(
                                section_content
                            ),
                        }
                    )

                if slides:

                    return slides

            # ----------------------------------------------
            # Generic dictionary
            # ----------------------------------------------

            for key, value in content.items():

                if key in {
                    "slides",
                    "sections",
                }:

                    continue

                slides.append(
                    {
                        "title": str(key),
                        "content": str(value),
                    }
                )

            if slides:

                return slides

        # ------------------------------------------------------
        # CASE 3: String content
        # ------------------------------------------------------

        if isinstance(
            content,
            str,
        ) and content.strip():

            chunks = self._split_text(
                text=content.strip(),
                max_characters=800,
            )

            for index, chunk in enumerate(
                chunks[:slide_count]
            ):

                if index == 0:

                    slide_title = title

                else:

                    slide_title = (
                        f"{title} - "
                        f"{index + 1}"
                    )

                slides.append(
                    {
                        "title": slide_title,
                        "content": chunk,
                    }
                )

            if slides:

                return slides

        # ------------------------------------------------------
        # CASE 4: No content
        # ------------------------------------------------------

        slides.append(
            {
                "title": title,
                "content": (
                    "This presentation was "
                    "generated by the Multi-Agent "
                    "Document AI system."
                ),
            }
        )

        return slides

    # ==========================================================
    # SPLIT TEXT
    # ==========================================================

    @staticmethod
    def _split_text(
        text: str,
        max_characters: int = 800,
    ) -> list[str]:
        """
        Split long text into presentation-friendly chunks.
        """

        if not text.strip():

            return []

        paragraphs = [
            paragraph.strip()
            for paragraph in text.split(
                "\n"
            )
            if paragraph.strip()
        ]

        # If the text does not contain newlines,
        # split it into character-based chunks.

        if len(paragraphs) == 1:

            paragraph = paragraphs[0]

            if len(paragraph) <= max_characters:

                return [paragraph]

            return [
                paragraph[
                    start:start + max_characters
                ]
                for start in range(
                    0,
                    len(paragraph),
                    max_characters,
                )
            ]

        # ------------------------------------------------------
        # Paragraph-aware splitting
        # ------------------------------------------------------

        chunks: list[str] = []

        current = ""

        for paragraph in paragraphs:

            candidate = (
                f"{current}\n{paragraph}"
                if current
                else paragraph
            )

            if len(candidate) <= max_characters:

                current = candidate

            else:

                if current:

                    chunks.append(
                        current
                    )

                # Handle an individual paragraph
                # that is itself too large.

                if len(paragraph) > max_characters:

                    parts = [
                        paragraph[
                            start:start + max_characters
                        ]
                        for start in range(
                            0,
                            len(paragraph),
                            max_characters,
                        )
                    ]

                    if parts:

                        chunks.extend(
                            parts[:-1]
                        )

                        current = parts[-1]

                else:

                    current = paragraph

        if current:

            chunks.append(
                current
            )

        return chunks

    # ==========================================================
    # ADD SLIDE
    # ==========================================================

    def _add_slide(
        self,
        presentation: Presentation,
        slide_data: dict[str, Any],
    ) -> None:
        """
        Add an editable title/content slide.
        """

        layout = self._get_layout(
            presentation=presentation,
            preferred_indexes=[
                1,
                0,
            ],
        )

        slide = presentation.slides.add_slide(
            layout
        )

        slide_title = str(
            slide_data.get(
                "title",
                "Untitled Slide",
            )
        )

        slide_content = str(
            slide_data.get(
                "content",
                "",
            )
        )

        # ------------------------------------------------------
        # TITLE
        # ------------------------------------------------------

        if slide.shapes.title:

            slide.shapes.title.text = (
                slide_title
            )

            self._format_text_frame(
                slide.shapes.title.text_frame,
                font_size=28,
                bold=True,
            )

        else:

            title_box = slide.shapes.add_textbox(
                Inches(0.7),
                Inches(0.4),
                Inches(11.5),
                Inches(0.8),
            )

            title_frame = (
                title_box.text_frame
            )

            title_frame.text = (
                slide_title
            )

            self._format_text_frame(
                title_frame,
                font_size=28,
                bold=True,
            )

        # ------------------------------------------------------
        # BODY
        # ------------------------------------------------------

        body_placeholder = (
            self._find_body_placeholder(
                slide
            )
        )

        if body_placeholder:

            body_placeholder.text = (
                slide_content
            )

            self._format_text_frame(
                body_placeholder.text_frame,
                font_size=18,
                bold=False,
            )

        else:

            body_box = slide.shapes.add_textbox(
                Inches(0.8),
                Inches(1.5),
                Inches(11.0),
                Inches(5.0),
            )

            body_frame = (
                body_box.text_frame
            )

            body_frame.word_wrap = True

            body_frame.text = (
                slide_content
            )

            self._format_text_frame(
                body_frame,
                font_size=18,
                bold=False,
            )

    # ==========================================================
    # FIND BODY PLACEHOLDER
    # ==========================================================

    @staticmethod
    def _find_body_placeholder(
        slide,
    ):
        """
        Find a usable body/content placeholder.
        """

        for shape in slide.placeholders:

            # Skip title placeholder.

            if (
                slide.shapes.title
                and shape == slide.shapes.title
            ):

                continue

            # Placeholder with a text frame.

            if hasattr(
                shape,
                "text_frame",
            ):

                return shape

        return None

    # ==========================================================
    # FORMAT TEXT
    # ==========================================================

    @staticmethod
    def _format_text_frame(
        text_frame,
        font_size: int,
        bold: bool = False,
    ) -> None:
        """
        Apply basic editable text formatting.
        """

        for paragraph in (
            text_frame.paragraphs
        ):

            for run in paragraph.runs:

                run.font.size = Pt(
                    font_size
                )

                run.font.bold = bold

    # ==========================================================
    # FALLBACK SLIDE
    # ==========================================================

    def _add_fallback_slide(
        self,
        presentation: Presentation,
        title: str,
    ) -> None:
        """
        Guarantee at least one slide.
        """

        layout = self._get_layout(
            presentation=presentation,
            preferred_indexes=[
                0,
                1,
            ],
        )

        slide = presentation.slides.add_slide(
            layout
        )

        if slide.shapes.title:

            slide.shapes.title.text = (
                title
            )

            self._format_text_frame(
                slide.shapes.title.text_frame,
                font_size=28,
                bold=True,
            )

        else:

            textbox = slide.shapes.add_textbox(
                Inches(1),
                Inches(2),
                Inches(10),
                Inches(1),
            )

            textbox.text_frame.text = (
                title
            )

            self._format_text_frame(
                textbox.text_frame,
                font_size=28,
                bold=True,
            )

    # ==========================================================
    # GET LAYOUT
    # ==========================================================

    @staticmethod
    def _get_layout(
        presentation: Presentation,
        preferred_indexes: list[int],
    ):
        """
        Return a usable PowerPoint slide layout.
        """

        layouts = (
            presentation.slide_layouts
        )

        if len(layouts) == 0:

            raise RuntimeError(
                "Presentation contains no "
                "slide layouts."
            )

        for index in preferred_indexes:

            if (
                0 <= index < len(layouts)
            ):

                return layouts[index]

        return layouts[0]


# ==============================================================
# BACKWARD-COMPATIBILITY ALIAS
# ==============================================================

PPTGenerator = PPTGeneratorAgent


# ==============================================================
# MANUAL TEST
# ==============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("PPT GENERATOR TEST")
    print("=" * 70)

    agent = PPTGeneratorAgent()

    test_content = [
        {
            "title": "Introduction",
            "content": (
                "Multi-Agent Document AI is an "
                "AI-powered system for document "
                "and presentation generation."
            ),
        },
        {
            "title": "Architecture",
            "content": (
                "The system uses Supervisor, "
                "Research, RAG, Document, PPT, "
                "and Validation agents."
            ),
        },
        {
            "title": "Technology Stack",
            "content": (
                "FastAPI, Python, Gemini, "
                "ChromaDB and python-pptx."
            ),
        },
    ]

    # ----------------------------------------------------------
    # Test using output_filename
    # ----------------------------------------------------------

    result = agent.generate(
        title="Multi-Agent Document AI",
        content=test_content,
        output_filename=(
            "test_output_filename.pptx"
        ),
    )

    print()
    print("Test 1 - output_filename")
    print("-" * 70)

    print(
        "Success:",
        result["success"],
    )

    print(
        "File:",
        result["file_path"],
    )

    print(
        "Slides:",
        result["slides"],
    )

    print(
        "Template used:",
        result["template_used"],
    )

    print(
        "Editable:",
        result["editable"],
    )

    # ----------------------------------------------------------
    # Test using filename
    # ----------------------------------------------------------

    result_2 = agent.generate(
        title="Backward Compatibility Test",
        content=[
            {
                "title": "Compatibility",
                "content": (
                    "The filename parameter is "
                    "supported for existing workflows."
                ),
            }
        ],
        filename="test_filename_alias.pptx",
    )

    print()
    print("Test 2 - filename alias")
    print("-" * 70)

    print(
        "Success:",
        result_2["success"],
    )

    print(
        "File:",
        result_2["file_path"],
    )

    print(
        "Slides:",
        result_2["slides"],
    )

    print(
        "Template used:",
        result_2["template_used"],
    )

    print(
        "Editable:",
        result_2["editable"],
    )

    # ----------------------------------------------------------
    # Final
    # ----------------------------------------------------------

    print()
    print("=" * 70)
    print("PPT GENERATOR TEST PASSED")
    print("=" * 70)