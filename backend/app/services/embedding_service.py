"""
Embedding Service

Uses a local Sentence Transformer model for document and query
embeddings.

Why local embeddings?

- No Gemini embedding API quota dependency
- No API cost for embeddings
- Works offline after the model is downloaded
- Suitable for ChromaDB semantic search
- Keeps Gemini available for generation/reasoning
"""

from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """
    Generate vector embeddings using a local
    Sentence Transformer model.
    """

    def __init__(self):
        # Lightweight and widely used sentence embedding model.
        #
        # Output dimension:
        # 384
        self.model_name = "all-MiniLM-L6-v2"

        print(
            f"Loading embedding model: {self.model_name}"
        )

        self.model = SentenceTransformer(
            self.model_name
        )

        print(
            "Embedding model loaded successfully."
        )

    # -----------------------------------------------------------
    # Document embeddings
    # -----------------------------------------------------------

    def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for document chunks.

        Returns:
            List of 384-dimensional vectors.
        """

        if not texts:
            return []

        cleaned_texts = [
            text.strip()
            for text in texts
            if text and text.strip()
        ]

        if not cleaned_texts:
            return []

        embeddings = self.model.encode(
            cleaned_texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=True,
        )

        return embeddings.tolist()

    # -----------------------------------------------------------
    # Query embedding
    # -----------------------------------------------------------

    def embed_query(
        self,
        query: str,
    ) -> list[float]:
        """
        Generate an embedding for a user search query.

        Returns:
            384-dimensional vector.
        """

        if not query or not query.strip():
            raise ValueError(
                "Query cannot be empty."
            )

        embedding = self.model.encode(
            query.strip(),
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return embedding.tolist()