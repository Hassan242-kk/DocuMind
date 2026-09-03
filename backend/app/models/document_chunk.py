from sqlalchemy import (
    Column,
    String,
    Integer,
    Text,
    ForeignKey,
)

from pgvector.sqlalchemy import Vector

from app.database import Base


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(
        String,
        primary_key=True,
    )

    document_id = Column(
        String,
        ForeignKey(
            "documents.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    chunk_index = Column(
        Integer,
        nullable=False,
    )

    text = Column(
        Text,
        nullable=False,
    )

    start_position = Column(
        Integer,
        nullable=True,
    )

    end_position = Column(
        Integer,
        nullable=True,
    )

    embedding = Column(
        Vector(384),
        nullable=False,
    )