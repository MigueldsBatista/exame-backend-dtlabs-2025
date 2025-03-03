import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from core.database import get_db
from models.base_model import Base

TEST_DATABASE_URL = "sqlite:///test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_local_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client():
    app.dependency_overrides[get_db] = get_local_db

    Base.metadata.create_all(bind=engine)


    with TestClient(app) as client:
        yield client

    Base.metadata.drop_all(bind=engine)
    

@pytest.fixture(scope="function")
def authenticated_client(client: TestClient):
    response = client.post("/auth/register", json={
        "username": "admin",
        "password": "admin"
    })
    assert response.status_code == 201, f"Erro no registro: {response.json()}"

    response = client.post("/auth/login", data={
        "username": "admin",
        "password": "admin"
    })
    
    assert response.status_code == 200, f"Erro no login: {response.json()}"

    token = response.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token}"})
    
    return client

@pytest.fixture(scope="function")
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

