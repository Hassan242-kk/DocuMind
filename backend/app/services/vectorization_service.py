from typing import List, Dict

from app.services.chunking_service import ChunkingService
from app.services.embedding_service import EmbeddingService


class VectorizationService:
    """
    Creates chunks and embeddings for a document.
    """

    def __init__(self):
        self.chunking_service = ChunkingService()
        self.embedding_service = EmbeddingService()

    def process_document(
        self,
        document_id: str,
        text: str,
    ) -> List[Dict]:

        chunks = self.chunking_service.create_chunks(
            text=text,
            document_id=document_id,
        )

        if not chunks:
            return []

        texts = [
            chunk["text"]
            for chunk in chunks
        ]

        embeddings = (
            self.embedding_service
            .create_embeddings(texts)
        )

        for chunk, embedding in zip(
            chunks,
            embeddings,
        ):
            chunk["embedding"] = embedding

        return chunks
    