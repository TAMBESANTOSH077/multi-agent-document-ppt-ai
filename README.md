# Multi-Agent AI Chatbot for Document & PPT Generation

An AI-powered multi-agent chatbot that analyzes uploaded documents and presentation templates, performs knowledge retrieval and web research, and generates editable DOCX and PPTX files.

The project is built as a modular full-stack application with a React frontend and FastAPI backend.

---

## 🚀 Project Overview

This project implements a Multi-Agent AI system for intelligent document and presentation generation.

Users can:

- Upload PDF, DOCX, PPTX and image documents
- Extract and analyze document content
- Analyze document and presentation structure
- Ask questions about uploaded documents
- Retrieve relevant information using RAG
- Perform web research for current information
- Generate editable DOCX documents
- Generate editable PPTX presentations
- Modify generated content using natural-language instructions
- Maintain document structure and formatting during generation
- Validate generated artifacts
- Track sources and generated artifacts

The system uses specialized AI agents coordinated by a Supervisor Agent.

---

# ✨ Key Features

## 1. Multi-Agent Architecture

The system uses specialized agents instead of relying on a single AI agent.

### Agents

- Supervisor / Orchestrator Agent
- Document Analysis Agent
- PPT Analysis Agent
- Research Agent
- RAG Agent
- Document Generator Agent
- PPT Generator Agent
- Validation Agent
- Conversational Editing Agent

The Supervisor Agent determines which agent or workflow should handle the user's request.

---

## 2. Document Processing

The application supports:

- PDF
- DOCX
- PPTX
- Images
- Scanned documents

The document processing pipeline extracts:

- Text
- Paragraphs
- Tables
- Headings
- Document structure
- Metadata
- Presentation slide content
- Basic formatting information

For scanned or image-based documents, OCR processing can be used to extract text.

---

## 3. Document Analysis

The Document Analysis Agent analyzes uploaded documents and identifies:

- Document type
- Structure
- Headings
- Tables
- Writing style
- Tone
- Topics
- Content statistics
- Summary

This information is passed to downstream agents for retrieval and generation.

---

## 4. PPT Template Analysis

The PPT analysis workflow examines presentation templates and extracts information such as:

- Slide count
- Slide dimensions
- Slide layouts
- Text blocks
- Fonts
- Font sizes
- Colors
- Shapes
- Tables
- Positions
- Backgrounds

This allows generated presentations to follow the overall structure and visual style of the uploaded template.

---

## 5. RAG - Retrieval Augmented Generation

Uploaded documents can be converted into searchable knowledge.

### RAG Pipeline

```text
Uploaded Document
       ↓
Text Extraction
       ↓
Text Chunking
       ↓
Embedding Generation
       ↓
Vector Database
       ↓
Similarity Search
       ↓
Relevant Context
       ↓
LLM
       ↓
Grounded Answer




⚙️ Setup Instructions
Prerequisites

Install the following:

Python 3.10+
Node.js 18+
npm
Git
Tesseract OCR (required for OCR/image-based documents)
1. Clone the Repository
git clone https://github.com/TAMBESANTOSH077/multi-agent-document-ppt-ai.git
cd multi-agent-document-ppt-ai
2. Backend Setup
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
3. Configure Environment Variables

Create:

backend/.env

Add:

APP_NAME=Multi-Agent Document AI
APP_VERSION=1.0.0
DEBUG=True

MODEL_NAME=gemini-2.5-flash
EMBEDDING_MODEL=gemini-embedding-001

GOOGLE_API_KEY=your_google_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here

CHROMA_PERSIST_DIRECTORY=./storage/chroma
UPLOAD_DIRECTORY=./storage/uploads
GENERATED_DIRECTORY=./storage/generated
VERSION_DIRECTORY=./storage/versions

TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe

Never commit the real .env file or API keys to GitHub.

4. Start the Backend
python -m uvicorn app.main:app --reload

Backend:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs
5. Frontend Setup

Open a new terminal:

cd frontend
npm install
npm run dev

Frontend:

http://localhost:5173
📖 Usage Guidelines
1. Upload a Document

Open the application and upload a supported file:

PDF
DOCX
PPTX
PNG
JPG/JPEG

The system extracts the document content and analyzes its structure.

2. Ask Questions

After uploading a document, ask questions through the AI Assistant.

Example:

What is the purpose of this document?
What are the major requirements mentioned in the document?
Summarize the document.
3. Use RAG

Ask a question that requires information from the uploaded document:

According to the uploaded document, what are the key project requirements?

The RAG workflow retrieves relevant document chunks and provides them as context to the AI model.

4. Generate a PowerPoint

After uploading a document, enter:

Create a professional 8-slide PowerPoint presentation from my uploaded document. Make it editable.

The PPT Generator creates an editable .pptx presentation.

5. Generate a Document

Example:

Create a professional proposal based on my uploaded document.

The Document Generator creates an editable DOCX file.

6. Conversational Editing

Generated artifacts can be modified using natural-language instructions.

Examples:

Add an executive summary.
Make the presentation more concise.
Add a competitive analysis section.
Add a conclusion slide.
Update the report using the latest web information.
7. Web Research

For current information, ask:

Research the latest Generative AI trends and create a summary.

The Research Agent retrieves current information and combines it with relevant document knowledge.

8. Recommended Demo Workflow
Upload Document
       ↓
Ask Document Question
       ↓
Supervisor Agent
       ↓
Document / RAG Agent
       ↓
Generate Answer
       ↓
Generate PPT
       ↓
Validate Output
       ↓
Edit Generated Artifact






