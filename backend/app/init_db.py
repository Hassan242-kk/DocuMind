from sqlalchemy import text

from app.database import Base, engine

from app.models import (
    Document,
    DocumentChunk,
)


def initialize_database():
    """
    Initialize PostgreSQL extensions and tables.
    """

    with engine.begin() as connection:

        connection.execute(
            text(
                "CREATE EXTENSION IF NOT EXISTS vector"
            )
        )

    Base.metadata.create_all(
        bind=engine
    )


if __name__ == "__main__":
    initialize_database()

    print(
        "Database initialized successfully."
    )