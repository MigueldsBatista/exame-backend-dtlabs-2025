import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from core.database import get_db
from models.base_model import Base
import os

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

@pytest.fixture(scope="session", autouse=True)
def set_test_env():
    """Set environment variables for testing."""
    os.environ["DISABLE_RATE_LIMIT"] = "true"
    yield



def _create_test_data_for_aggregations(authenticated_client):
    """Helper function to create test data for aggregation tests"""
    response = authenticated_client.post("/servers", json={"server_name": "Dolly Aggregation"})
    server_ulid = response.json()["server_ulid"]
    
    # Day 1
    authenticated_client.post("/data", json={
        "server_ulid": server_ulid,
        "temperature": 25.0,
        "timestamp": "2025-10-01T13:00:00Z",
        "humidity": 70.0,
        "current": 1.0,
        "voltage": 220.0
    })
    
    authenticated_client.post("/data", json={
        "server_ulid": server_ulid,
        "temperature": 26.5,
        "timestamp": "2025-10-01T14:00:00Z",
        "humidity": 71.0,
        "current": 1.1,
        "voltage": 221.0
    })
    
    # Day 2
    authenticated_client.post("/data", json={
        "server_ulid": server_ulid,
        "temperature": 27.0,
        "timestamp": "2025-10-02T12:00:00Z",
        "humidity": 72.0,
        "current": 1.2,
        "voltage": 222.0
    })
    
    authenticated_client.post("/data", json={
        "server_ulid": server_ulid,
        "temperature": 27.5,
        "timestamp": "2025-10-02T13:00:00Z",
        "humidity": 73.0,
        "current": 1.3,
        "voltage": 223.0
    })
    
    authenticated_client.post("/data", json={
        "server_ulid": server_ulid,
        "temperature": 28.0,
        "timestamp": "2025-10-02T13:01:00Z",
        "humidity": 74.0, 
        "current": 1.4,
        "voltage": 224.0
    })
    
    return server_ulid
