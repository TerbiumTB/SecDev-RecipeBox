import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import main
from app.schemas.orm import Base
from app.shared.config import config
from app.shared.db import get_db

mock_engine = create_engine(config.MOCK_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=mock_engine, autoflush=False, autocommit=False)


@pytest.fixture(scope="session", autouse=True)
def setup_mock_db():
    Base.metadata.create_all(bind=mock_engine)
    yield
    Base.metadata.drop_all(bind=mock_engine)


@pytest.fixture
def mock_db_session():
    connection = mock_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(mock_db_session):
    def get_mock_db():
        try:
            yield mock_db_session
        finally:
            pass

    main.app.dependency_overrides[get_db] = get_mock_db

    client = TestClient(main.app)
    yield client

    main.app.dependency_overrides.clear()
