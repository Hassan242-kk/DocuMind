from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.rag_service import RAGService


router = APIRouter()

rag_service = RAGService()


class ChatRequest(BaseModel):
    question: str
    document_id: str | None = None
    top_k: int = 5


@router.post("/")
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
):

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    if request.top_k < 1 or request.top_k > 10:
        raise HTTPException(
            status_code=400,
            detail="top_k must be between 1 and 10.",
        )

    try:

        result = rag_service.answer_question(
            db=db,
            question=request.question,
            document_id=request.document_id,
            top_k=request.top_k,
        )

        return result

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"RAG processing failed: {str(error)}",
        )