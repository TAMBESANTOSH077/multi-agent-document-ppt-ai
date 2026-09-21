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