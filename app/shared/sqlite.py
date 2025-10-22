from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///../recipes.db"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    # Base.metadata.drop_all(engine)
    # Base.metadata.create_all(engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# def get_local_session():
#     engine = create_engine("sqlite:///../recipes.db", echo=True)

#     Base.metadata.drop_all(engine)
#     Base.metadata.create_all(engine)
#     SessionLocal = sessionmaker(bind=engine)

#     return SessionLocal()
