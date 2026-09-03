from typing import List, Dict


class ChunkingService:
    """
    Splits extracted document text into smaller overlapping chunks.
    """

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        if chunk_overlap >= chunk_size:
            raise ValueError(
                "chunk_overlap must be smaller than chunk_size."
            )

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def create_chunks(
        self,
        text: str,
        document_id: str,
    ) -> List[Dict]:

        if not text or not text.strip():
            return []

        text = text.strip()

        chunks = []

        start = 0
        chunk_index = 0

        while start < len(text):

            end = start + self.chunk_size

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append(
                    {
                        "document_id": document_id,
                        "chunk_index": chunk_index,
                        "text": chunk_text,
                        "start_position": start,
                        "end_position": min(
                            end,
                            len(text)
                        ),
                    }
                )

                chunk_index += 1

            next_start = end - self.chunk_overlap

            if next_start <= start:
                break

            start = next_start

        return chunks