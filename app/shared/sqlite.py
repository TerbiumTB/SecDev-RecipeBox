from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.schemas.orm import Base


def get_local_session():
    engine = create_engine("sqlite:///../recipes.db", echo=True)

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)

    return SessionLocal()
