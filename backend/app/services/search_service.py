from typing import Any

from sqlalchemy.orm import Session

from app.services.embedding_service import (
    EmbeddingService
)

from app.services.vector_database_service import (
    VectorDatabaseService
)


class SearchService:
    """
    Performs semantic search over document chunks.
    """

    def __init__(self):
        self.embedding_service = (
            EmbeddingService()
        )

        self.vector_database_service = (
            VectorDatabaseService()
        )

    def search(
        self,
        db: Session,
        query: str,
        limit: int = 5,
        document_id: str | None = None,
    ) -> list[dict[str, Any]]:

        if not query.strip():
            return []

        # Convert user's question into a vector
        query_embedding = (
            self.embedding_service
            .create_embedding(query)
        )

        # Search PostgreSQL + pgvector
        chunks = (
            self.vector_database_service
            .similarity_search(
                db=db,
                query_embedding=query_embedding,
                limit=limit,
                document_id=document_id,
            )
        )

        results = []

        for chunk in chunks:

            results.append(
                {
                    "chunk_id": chunk.id,
                    "document_id": chunk.document_id,
                    "chunk_index": chunk.chunk_index,
                    "text": chunk.text,
                }
            )

        return results