from typing import Any

from sqlalchemy.orm import Session

from app.services.search_service import SearchService
from app.services.llm_service import LLMService


class RAGService:
    """
    Retrieval-Augmented Generation service.

    Retrieves relevant document chunks and provides
    them as context to an LLM.
    """

    def __init__(self):

        self.search_service = SearchService()

        self.llm_service = None

    def answer_question(
        self,
        db: Session,
        question: str,
        document_id: str | None = None,
        top_k: int = 5,
    ) -> dict[str, Any]:

        if not question.strip():
            raise ValueError(
                "Question cannot be empty."
            )

        # ---------------------------------------------
        # 1. Retrieve relevant chunks
        # ---------------------------------------------

        chunks = self.search_service.search(
            db=db,
            query=question,
            limit=top_k,
            document_id=document_id,
        )

        if not chunks:
            return {
                "answer": (
                    "I could not find relevant "
                    "information in the documents."
                ),
                "sources": [],
            }

        # ---------------------------------------------
        # 2. Build context
        # ---------------------------------------------

        context_parts = []

        for index, chunk in enumerate(
            chunks,
            start=1,
        ):

            context_parts.append(
                f"""
SOURCE {index}

Document ID:
{chunk["document_id"]}

Chunk:
{chunk["chunk_index"]}

Content:
{chunk["text"]}
"""
            )

        context = "\n".join(
            context_parts
        )

        # ---------------------------------------------
        # 3. Create LLM
        # ---------------------------------------------

        if self.llm_service is None:
            self.llm_service = LLMService()

        # ---------------------------------------------
        # 4. Ask LLM
        # ---------------------------------------------

        system_prompt = """
You are DocuMind, an AI document assistant.

Answer the user's question using ONLY the
provided document context.

Rules:

1. Do not invent information.
2. If the answer is not present in the context,
   say that the information was not found.
3. Give a clear and concise answer.
4. Use the source information when useful.
5. Do not use outside knowledge.
"""

        user_prompt = f"""
DOCUMENT CONTEXT:

{context}

USER QUESTION:

{question}

Answer the question using only the document context.
"""

        answer = self.llm_service.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        # ---------------------------------------------
        # 5. Return answer + sources
        # ---------------------------------------------

        sources = [
            {
                "document_id": chunk[
                    "document_id"
                ],
                "chunk_id": chunk[
                    "chunk_id"
                ],
                "chunk_index": chunk[
                    "chunk_index"
                ],
                "text": chunk[
                    "text"
                ],
            }
            for chunk in chunks
        ]

        return {
            "answer": answer,
            "sources": sources,
        }