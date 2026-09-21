"""
RAG Agent

Responsible for:
    1. Receiving a user question
    2. Retrieving relevant chunks from ChromaDB
    3. Building grounded context
    4. Sending the context to Gemini
    5. Returning an answer with source traceability

The agent is instructed to answer only from the retrieved
document context and not invent unsupported information.
"""

from typing import Any

from app.services.rag_service import RAGService
from app.services.llm_service import LLMService


class RAGAgent:
    """
    Retrieval-Augmented Generation agent.

    Workflow:

        User Question
              ↓
        ChromaDB Retrieval
              ↓
        Relevant Chunks
              ↓
        Context Construction
              ↓
        Gemini
              ↓
        Grounded Answer + Sources
    """

    def __init__(self):
        self.rag_service = RAGService()
        self.llm_service = LLMService()

    # -----------------------------------------------------------
    # Public method
    # -----------------------------------------------------------

    def answer(
        self,
        query: str,
        top_k: int = 5,
    ) -> dict[str, Any]:
        """
        Answer a question using the indexed document knowledge base.
        """

        if not query or not query.strip():
            raise ValueError("Query cannot be empty.")

        if top_k < 1:
            raise ValueError("top_k must be at least 1.")

        query = query.strip()

        # -------------------------------------------------------
        # Step 1: Retrieve relevant document chunks
        # -------------------------------------------------------

        retrieval_result = self.rag_service.search(
            query=query,
            top_k=top_k,
        )

        retrieved_chunks = retrieval_result.get(
            "results",
            []
        )

        # -------------------------------------------------------
        # Step 2: Handle no relevant information
        # -------------------------------------------------------

        if not retrieved_chunks:
            return {
                "answer": (
                    "I could not find relevant information "
                    "in the indexed documents."
                ),
                "query": query,
                "sources": [],
                "retrieved_chunks": 0,
            }

        # -------------------------------------------------------
        # Step 3: Build grounded context
        # -------------------------------------------------------

        context_parts = []

        for index, chunk in enumerate(
            retrieved_chunks,
            start=1,
        ):
            metadata = chunk.get("metadata") or {}

            filename = metadata.get(
                "filename",
                "Unknown document",
            )

            chunk_index = metadata.get(
                "chunk_index",
                "Unknown",
            )

            text = chunk.get(
                "text",
                "",
            )

            context_parts.append(
                f"""
SOURCE {index}
Filename: {filename}
Chunk: {chunk_index}

Content:
{text}
""".strip()
            )

        context = "\n\n".join(context_parts)

        # -------------------------------------------------------
        # Step 4: Create grounded LLM prompt
        # -------------------------------------------------------

        prompt = f"""
You are a Retrieval-Augmented Generation assistant.

Answer the user's question using ONLY the information
provided in the retrieved document context below.

Important rules:

1. Do not invent facts.
2. Do not use information that is not supported by the
   retrieved context.
3. If the context does not contain enough information,
   clearly say that the information is not available
   in the indexed documents.
4. Give a concise and useful answer.
5. When possible, mention the relevant source filename.
6. Do not claim that you searched the internet.
7. Do not fabricate citations or source names.

User Question:
{query}

Retrieved Document Context:
---------------------------
{context}
---------------------------

Now provide the answer.
""".strip()

        # -------------------------------------------------------
        # Step 5: Generate grounded answer
        # -------------------------------------------------------

        answer = self.llm_service.generate_text(
            prompt
        )

        # -------------------------------------------------------
        # Step 6: Build source traceability
        # -------------------------------------------------------

        sources = []

        for chunk in retrieved_chunks:
            metadata = chunk.get("metadata") or {}

            source = {
                "filename": metadata.get(
                    "filename"
                ),
                "file_type": metadata.get(
                    "file_type"
                ),
                "chunk_index": metadata.get(
                    "chunk_index"
                ),
                "distance": chunk.get(
                    "distance"
                ),
            }

            sources.append(source)

        # -------------------------------------------------------
        # Step 7: Return structured result
        # -------------------------------------------------------

        return {
            "answer": answer,
            "query": query,
            "sources": sources,
            "retrieved_chunks": len(
                retrieved_chunks
            ),
        }