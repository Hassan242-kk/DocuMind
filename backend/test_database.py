from app.database import SessionLocal
from app.models import Document


db = SessionLocal()

try:

    document = Document(
        id="test-document-1",
        original_filename="test.pdf",
        saved_filename="test-document-1.pdf",
        file_type=".pdf",
        file_size=1024,
        document_type="report",
        classification_confidence=0.85,
        extracted_text="This is a test document.",
    )

    db.add(document)
    db.commit()

    print(
        "Document saved successfully."
    )

finally:
    db.close()