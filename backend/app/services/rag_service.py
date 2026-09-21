"""
RAG Service

Handles:

    1. Document chunking
    2. Gemini embeddings
    3. ChromaDB storage
    4. Similarity search
    5. Retrieved context

This service is the main bridge between uploaded documents
and the RAG Agent.
"""

from pathlib import Path
from typing import Any
from uuid import uuid4

import chromadb

from app.config import settings
from app.services.document_service import extract_document
from app.services.embedding_service import EmbeddingService


class RAGService:
    """
    Enterprise-style local RAG service using ChromaDB.
    """

    def __init__(self) -> None:

        # -------------------------------------------------------
        # Create persistent ChromaDB client.
        # -------------------------------------------------------

        persist_directory = Path(
            settings.chroma_persist_directory
        )

        persist_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.client = chromadb.PersistentClient(
            path=str(persist_directory)
        )

        # -------------------------------------------------------
        # One collection for the application's knowledge base.
        # -------------------------------------------------------

        self.collection = self.client.get_or_create_collection(
            name="document_knowledge_base"
        )

        self.embedding_service = EmbeddingService()

    # ===========================================================
    # CHUNKING
    # ===========================================================

    def chunk_text(
        self,
        text: str,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ) -> list[str]:
        """
        Split document text into overlapping chunks.

        Example:

            chunk_size = 1000
            chunk_overlap = 200

        means every chunk can share 200 characters with the
        previous chunk.

        Overlap helps preserve context between chunks.
        """

        if not text.strip():
            return []

        if chunk_overlap >= chunk_size:
            raise ValueError(
                "chunk_overlap must be smaller than chunk_size."
            )

        chunks: list[str] = []

        start = 0
        text_length = len(text)

        while start < text_length:

            end = min(
                start + chunk_size,
                text_length,
            )

            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            if end >= text_length:
                break

            start = end - chunk_overlap

        return chunks

    # ===========================================================
    # INDEX DOCUMENT
    # ===========================================================

    def index_document(
        self,
        file_path: str,
    ) -> dict[str, Any]:
        """
        Extract, chunk, embed and store a document.

        This is the main ingestion pipeline.
        """

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Document not found: {file_path}"
            )

        # -------------------------------------------------------
        # 1. Extract document text.
        # -------------------------------------------------------

        document = extract_document(
            str(path)
        )

        text = document["text"]

        if not text.strip():
            raise ValueError(
                "No text could be extracted from the document."
            )

        # -------------------------------------------------------
        # 2. Split into chunks.
        # -------------------------------------------------------

        chunks = self.chunk_text(
            text=text,
            chunk_size=1000,
            chunk_overlap=200,
        )

        if not chunks:
            raise ValueError(
                "Document produced no usable chunks."
            )

        # -------------------------------------------------------
        # 3. Generate embeddings.
        # -------------------------------------------------------

        embeddings = (
            self.embedding_service.embed_documents(
                chunks
            )
        )

        # -------------------------------------------------------
        # 4. Prepare metadata.
        # -------------------------------------------------------

        document_id = str(uuid4())

        ids = [
            f"{document_id}_{index}"
            for index in range(len(chunks))
        ]

        metadatas = [
            {
                "document_id": document_id,
                "filename": document["filename"],
                "file_type": document["file_type"],
                "chunk_index": index,
            }
            for index in range(len(chunks))
        ]

        # -------------------------------------------------------
        # 5. Store vectors in ChromaDB.
        # -------------------------------------------------------

        self.collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        return {
            "success": True,
            "document_id": document_id,
            "filename": document["filename"],
            "file_type": document["file_type"],
            "chunk_count": len(chunks),
            "character_count": document[
                "character_count"
            ],
            "word_count": document[
                "word_count"
            ],
        }

    # ===========================================================
    # SEARCH
    # ===========================================================

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> dict[str, Any]:
        """
        Search the knowledge base using semantic similarity.
        """

        if not query.strip():
            raise ValueError(
                "Query cannot be empty."
            )

        if top_k < 1:
            raise ValueError(
                "top_k must be at least 1."
            )

        # -------------------------------------------------------
        # Convert user query into a vector.
        # -------------------------------------------------------

        query_embedding = (
            self.embedding_service.embed_query(
                query
            )
        )

        # -------------------------------------------------------
        # Search ChromaDB.
        # -------------------------------------------------------

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

        documents = results.get(
            "documents",
            [[]],
        )[0]

        metadatas = results.get(
            "metadatas",
            [[]],
        )[0]

        distances = results.get(
            "distances",
            [[]],
        )[0]

        retrieved_chunks = []

        for index, document in enumerate(
            documents
        ):

            retrieved_chunks.append(
                {
                    "text": document,
                    "metadata": (
                        metadatas[index]
                        if index < len(metadatas)
                        else {}
                    ),
                    "distance": (
                        distances[index]
                        if index < len(distances)
                        else None
                    ),
                }
            )

        return {
            "query": query,
            "results": retrieved_chunks,
        }