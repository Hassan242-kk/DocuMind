from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.search_service import SearchService


router = APIRouter()

search_service = SearchService()


@router.get("/")
def search_documents(
    query: str,
    limit: int = 5,
    document_id: str | None = None,
    db: Session = Depends(get_db),
):

    if not query.strip():
        raise HTTPException(
            status_code=400,
            detail="Search query cannot be empty.",
        )

    if limit < 1 or limit > 20:
        raise HTTPException(
            status_code=400,
            detail="Limit must be between 1 and 20.",
        )

    results = search_service.search(
        db=db,
        query=query,
        limit=limit,
        document_id=document_id,
    )

    return {
        "query": query,
        "results": results,
        "count": len(results),
    }