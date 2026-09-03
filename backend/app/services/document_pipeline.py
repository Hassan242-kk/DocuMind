from typing import Any

from sqlalchemy.orm import Session

from app.services.document_processor import DocumentProcessor
from app.services.classification_service import ClassificationService
from app.services.extraction_service import ExtractionService
from app.services.vectorization_service import VectorizationService
from app.services.vector_database_service import VectorDatabaseService


class DocumentPipeline:
    """
    Main document processing pipeline.

    Upload
       ↓
    Text Extraction
       ↓
    Classification
       ↓
    Structured Extraction
       ↓
    Chunking
       ↓
    Embeddings
       ↓
    Database Storage
    """

    def __init__(self):
        self.document_processor = DocumentProcessor()
        self.classification_service = ClassificationService()
        self.extraction_service = None
        self.vectorization_service = VectorizationService()
        self.vector_database_service = VectorDatabaseService()

    def process_document(
        self,
        db: Session,
        document_id: str,
        file_path: str,
        original_filename: str,
        saved_filename: str,
        file_type: str,
        file_size: int,
    ) -> dict[str, Any]:

        try:
            # ------------------------------------------------
            # 1. Extract text
            # ------------------------------------------------
            extracted_text = self.document_processor.extract_text(
                file_path
            )

            extracted_text = self.document_processor.clean_text(
                extracted_text
            )

            # ------------------------------------------------
            # 2. Classify document
            # ------------------------------------------------
            classification = self.classification_service.classify(
                extracted_text
            )

            document_type = classification["document_type"]
            confidence = classification["confidence"]

            # ------------------------------------------------
            # 3. Structured extraction
            # ------------------------------------------------
            extraction = {
                "success": False,
                "data": {},
            }

            if (
                document_type != "unknown"
                and extracted_text.strip()
            ):
                try:
                    if self.extraction_service is None:
                        self.extraction_service = ExtractionService()

                    extraction = self.extraction_service.extract(
                        document_text=extracted_text,
                        document_type=document_type,
                    )

                except Exception as error:
                    extraction = {
                        "success": False,
                        "error": str(error),
                        "data": {},
                    }

            # ------------------------------------------------
            # 4. Create document record
            # ------------------------------------------------
            document_data = {
                "id": document_id,
                "original_filename": original_filename,
                "saved_filename": saved_filename,
                "file_type": file_type,
                "file_size": file_size,
                "document_type": document_type,
                "classification_confidence": confidence,
                "extracted_text": extracted_text,
                "structured_data": extraction.get("data", {}),
                "processing_status": "processing",
                "processing_error": None,
            }

            document = self.vector_database_service.save_document(
                db=db,
                document_data=document_data,
            )

            # ------------------------------------------------
            # 5. Create chunks + embeddings
            # ------------------------------------------------
            chunks = self.vectorization_service.process_document(
                document_id=document_id,
                text=extracted_text,
            )

            saved_chunks = []

            if chunks:
                saved_chunks = self.vector_database_service.save_chunks(
                    db=db,
                    chunks=chunks,
                )

            # ------------------------------------------------
            # 6. Mark processing as completed
            # ------------------------------------------------
            document.processing_status = "completed"

            db.commit()
            db.refresh(document)

            return {
                "success": True,
                "document": document,
                "classification": classification,
                "extraction": extraction,
                "chunks_created": len(saved_chunks),
            }

        except Exception as error:

            db.rollback()

            return {
                "success": False,
                "error": str(error),
            }