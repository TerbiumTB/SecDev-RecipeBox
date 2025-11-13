from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.schemas.orm import Base
from app.shared.config import config

postgres_engine = None
PostgresSessionLocal = None

if config.APP_ENV != "test":
    postgres_engine = create_engine(config.DATABASE_URL, echo=True)
    PostgresSessionLocal = sessionmaker(bind=postgres_engine, autoflush=False, autocommit=False)

    Base.metadata.create_all(bind=postgres_engine)


def get_db():
    if PostgresSessionLocal is None:
        raise RuntimeError("Database connection not initialized")
    db = PostgresSessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_db_health() -> str:
    if postgres_engine is None:
        return "error"

    try:
        with postgres_engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return "ok"
    except Exception:
        return "error"
