from typing import List

from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """
    Converts text into vector embeddings using
    a local Sentence Transformer model.
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
    ):
        self.model_name = model_name

        self.model = SentenceTransformer(
            model_name
        )

    def create_embedding(
        self,
        text: str,
    ) -> List[float]:

        if not text or not text.strip():
            raise ValueError(
                "Cannot create embedding for empty text."
            )

        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    def create_embeddings(
        self,
        texts: List[str],
    ) -> List[List[float]]:

        if not texts:
            return []

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
        )

        return embeddings.tolist()