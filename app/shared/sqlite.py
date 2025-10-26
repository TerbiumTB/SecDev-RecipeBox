from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.shared.config import config

engine = create_engine(config.DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
