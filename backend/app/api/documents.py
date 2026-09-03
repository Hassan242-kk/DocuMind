import os
import uuid
from typing import Any
from app.models.document import Document

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
    Depends,
)

from sqlalchemy.orm import Session

from app.database import get_db
from app.services.document_pipeline import DocumentPipeline


router = APIRouter()

pipeline = DocumentPipeline()

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
    ".jpg",
    ".jpeg",
    ".png",
}


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):

    # ----------------------------------------
    # Validate filename
    # ----------------------------------------

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required.",
        )

    original_filename = file.filename

    extension = os.path.splitext(
        original_filename
    )[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file type. "
                "Supported: PDF, DOCX, TXT, JPG, JPEG, PNG."
            ),
        )

    # ----------------------------------------
    # Generate unique document ID
    # ----------------------------------------

    document_id = str(uuid.uuid4())

    saved_filename = f"{document_id}{extension}"

    file_path = os.path.join(
        UPLOAD_DIR,
        saved_filename,
    )

    # ----------------------------------------
    # Save uploaded file
    # ----------------------------------------

    try:

        contents = await file.read()

        with open(file_path, "wb") as buffer:
            buffer.write(contents)

        file_size = len(contents)

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to save file: {str(error)}",
        )

    # ----------------------------------------
    # Process document
    # ----------------------------------------

    try:

        result = pipeline.process_document(
            db=db,
            document_id=document_id,
            file_path=file_path,
            original_filename=original_filename,
            saved_filename=saved_filename,
            file_type=extension,
            file_size=file_size,
        )

        if not result["success"]:

            raise HTTPException(
                status_code=500,
                detail=result.get(
                    "error",
                    "Document processing failed.",
                ),
            )

        document = result["document"]

        return {
            "success": True,
            "message": "Document uploaded and processed successfully.",
            "document": {
                "id": document.id,
                "filename": document.original_filename,
                "file_type": document.file_type,
                "file_size": document.file_size,
                "document_type": document.document_type,
                "classification_confidence": (
                    document.classification_confidence
                ),
                "processing_status": (
                    document.processing_status
                ),
                "structured_data": (
                    document.structured_data
                ),
                "created_at": document.created_at,
            },
            "chunks_created": result["chunks_created"],
        }

    except HTTPException:
        raise

    except Exception as error:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Document processing failed: {str(error)}",
        )
        
        
@router.get("/")
def get_documents(
    db: Session = Depends(get_db),
):
    documents = (
        db.query(Document)
        .order_by(Document.created_at.desc())
        .all()
    )

    return {
        "success": True,
        "count": len(documents),
        "documents": [
            {
                "id": document.id,
                "filename": document.original_filename,
                "file_type": document.file_type,
                "file_size": document.file_size,
                "document_type": document.document_type,
                "classification_confidence": (
                    document.classification_confidence
                ),
                "processing_status": document.processing_status,
                "structured_data": document.structured_data,
                "created_at": document.created_at,
            }
            for document in documents
        ],
    }
    
@router.get("/{document_id}")
def get_document(
    document_id: str,
    db: Session = Depends(get_db),
):
    document = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    return {
        "success": True,
        "document": {
            "id": document.id,
            "filename": document.original_filename,
            "file_type": document.file_type,
            "file_size": document.file_size,
            "document_type": document.document_type,
            "classification_confidence": (
                document.classification_confidence
            ),
            "processing_status": (
                document.processing_status
            ),
            "structured_data": (
                document.structured_data
            ),
            "extracted_text": (
                document.extracted_text
            ),
            "created_at": document.created_at,
        },
    }