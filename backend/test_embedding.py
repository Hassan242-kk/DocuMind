from app.services.embedding_service import EmbeddingService


embedding_service = EmbeddingService()

text = "Machine learning is a branch of artificial intelligence."

embedding = embedding_service.create_embedding(
    text
)

print("Embedding dimensions:", len(embedding))
print("First 10 values:", embedding[:10])