import uuid

from sqlalchemy import Column, String, Integer, Text, Float, DateTime, JSON
from sqlalchemy.sql import func

from app.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    original_filename = Column(
        String,
        nullable=False,
    )

    saved_filename = Column(
        String,
        nullable=False,
    )

    file_type = Column(
        String,
        nullable=False,
    )

    file_size = Column(
        Integer,
        nullable=False,
    )

    document_type = Column(
        String,
        nullable=True,
    )

    classification_confidence = Column(
        Float,
        nullable=True,
    )

    extracted_text = Column(
        Text,
        nullable=True,
    )

    structured_data = Column(
        JSON,
        nullable=True,
    )

    processing_status = Column(
        String,
        nullable=False,
        default="completed",
    )

    processing_error = Column(
        Text,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )