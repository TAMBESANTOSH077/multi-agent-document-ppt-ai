"""
Create a sample PowerPoint template for testing.

This creates a real editable PPTX template with:
    - Custom slide size
    - Title slide layout
    - Content slide layout
    - Theme-like formatting
    - Header/footer styling
    - Editable placeholders
"""

import sys
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN


# ---------------------------------------------------------------
# Backend path
# ---------------------------------------------------------------

BACKEND_DIR = Path(__file__).resolve().parents[1]

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


# ---------------------------------------------------------------
# Output path
# ---------------------------------------------------------------

TEMPLATE_DIR = (
    BACKEND_DIR
    / "sample_data"
    / "templates"
)

TEMPLATE_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

OUTPUT_FILE = (
    TEMPLATE_DIR
    / "Company_Template.pptx"
)


# ---------------------------------------------------------------
# Create presentation
# ---------------------------------------------------------------

presentation = Presentation()


# ---------------------------------------------------------------
# Set widescreen dimensions
# ---------------------------------------------------------------

presentation.slide_width = Inches(13.333)
presentation.slide_height = Inches(7.5)


# ---------------------------------------------------------------
# TITLE SLIDE
# ---------------------------------------------------------------

title_layout = presentation.slide_layouts[0]

slide = presentation.slides.add_slide(
    title_layout
)


# Title
title = slide.shapes.title

title.text = "Company Proposal"

title_paragraph = (
    title.text_frame.paragraphs[0]
)

title_paragraph.font.size = Pt(34)
title_paragraph.font.bold = True
title_paragraph.alignment = PP_ALIGN.CENTER


# Subtitle
subtitle = slide.placeholders[1]

subtitle.text = (
    "Enterprise Technology & AI Strategy"
)

subtitle_paragraph = (
    subtitle.text_frame.paragraphs[0]
)

subtitle_paragraph.font.size = Pt(20)
subtitle_paragraph.alignment = PP_ALIGN.CENTER


# ---------------------------------------------------------------
# CONTENT SLIDE
# ---------------------------------------------------------------

content_layout = presentation.slide_layouts[1]

slide = presentation.slides.add_slide(
    content_layout
)


# Title
title = slide.shapes.title

title.text = "Executive Summary"

title_paragraph = (
    title.text_frame.paragraphs[0]
)

title_paragraph.font.size = Pt(28)
title_paragraph.font.bold = True


# Body
body = slide.placeholders[1]

body.text = (
    "This template demonstrates the visual "
    "structure used for enterprise proposals."
)

paragraph = body.text_frame.paragraphs[0]

paragraph.font.size = Pt(18)


# ---------------------------------------------------------------
# THIRD SLIDE
# ---------------------------------------------------------------

slide = presentation.slides.add_slide(
    content_layout
)

title = slide.shapes.title

title.text = "Technology Architecture"

body = slide.placeholders[1]

body.text = (
    "AI Agents\n"
    "Enterprise RAG\n"
    "Web Research\n"
    "Document Generation"
)


# ---------------------------------------------------------------
# FOURTH SLIDE
# ---------------------------------------------------------------

slide = presentation.slides.add_slide(
    content_layout
)

title = slide.shapes.title

title.text = "Implementation Roadmap"

body = slide.placeholders[1]

body.text = (
    "Phase 1 - Document Ingestion\n"
    "Phase 2 - Knowledge Retrieval\n"
    "Phase 3 - AI Research\n"
    "Phase 4 - Content Generation\n"
    "Phase 5 - Validation"
)


# ---------------------------------------------------------------
# Save
# ---------------------------------------------------------------

presentation.save(
    str(OUTPUT_FILE)
)


print("=" * 70)
print("SAMPLE PPTX TEMPLATE CREATED")
print("=" * 70)

print()
print("Template:")
print(OUTPUT_FILE)

print()
print("Slides:")
print(len(presentation.slides))

print()
print("Size:")
print(
    presentation.slide_width,
    "x",
    presentation.slide_height,
)

print()
print("=" * 70)