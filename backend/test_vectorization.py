from app.services.vectorization_service import (
    VectorizationService
)


text = """
Artificial intelligence is transforming many industries.

Machine learning allows computers to learn patterns
from data without being explicitly programmed.

Deep learning uses neural networks with multiple layers
to solve complex problems such as image recognition,
natural language processing, and speech recognition.
"""


service = VectorizationService()

chunks = service.process_document(
    document_id="test-document-123",
    text=text,
)

print("Number of chunks:", len(chunks))

for chunk in chunks:
    print("\n----------------------")
    print("Chunk:", chunk["chunk_index"])
    print("Text:", chunk["text"])
    print(
        "Embedding dimensions:",
        len(chunk["embedding"])
    )