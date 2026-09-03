import uuid

from typing import List, Dict

from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.document_chunk import DocumentChunk


class VectorDatabaseService:

    def save_document(
        self,
        db: Session,
        document_data: Dict,
    ) -> Document:

        document = Document(
            id=document_data["id"],
            original_filename=document_data["original_filename"],
            saved_filename=document_data["saved_filename"],
            file_type=document_data["file_type"],
            file_size=document_data["file_size"],
            document_type=document_data.get("document_type"),
            classification_confidence=document_data.get(
                "classification_confidence"
            ),
            extracted_text=document_data.get("extracted_text"),
            structured_data=document_data.get("structured_data"),
            processing_status=document_data.get(
                "processing_status",
                "completed",
            ),
            processing_error=document_data.get(
                "processing_error"
            ),
        )

        db.add(document)

        db.commit()
        db.refresh(document)

        return document

    def save_chunks(
        self,
        db: Session,
        chunks: List[Dict],
    ) -> List[DocumentChunk]:

        database_chunks = []

        for chunk in chunks:

            database_chunk = DocumentChunk(
                id=str(uuid.uuid4()),
                document_id=chunk["document_id"],
                chunk_index=chunk["chunk_index"],
                text=chunk["text"],
                start_position=chunk.get("start_position"),
                end_position=chunk.get("end_position"),
                embedding=chunk["embedding"],
            )

            db.add(database_chunk)

            database_chunks.append(database_chunk)

        db.commit()

        return database_chunks

    def similarity_search(
        self,
        db: Session,
        query_embedding: List[float],
        limit: int = 5,
        document_id: str | None = None,
    ) -> List[DocumentChunk]:

        query = db.query(DocumentChunk)

        if document_id:
            query = query.filter(
                DocumentChunk.document_id == document_id
            )

        results = (
            query
            .order_by(
                DocumentChunk.embedding.cosine_distance(
                    query_embedding
                )
            )
            .limit(limit)
            .all()
        )

        return results