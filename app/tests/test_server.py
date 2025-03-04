from datetime import datetime

from services.server_service import ServerService

from .conftest import _create_test_data_for_aggregations


def test_post_empty_server_name(authenticated_client, db):
    response = authenticated_client.post("/servers", json={"server_name": ""})
    assert response.status_code == 422


def test_post_server(authenticated_client, db):
    response = authenticated_client.post("/servers", json={
        "server_name": "Dolly 1"
    })
    
    assert response.status_code == 201
    assert response.json()["server_ulid"] is not None
    assert response.json()["server_name"] == "Dolly 1"

def test_get_health_all(authenticated_client, db):
    response = authenticated_client.get("/health/all")
    
    assert response.status_code == 200
    assert len(response.json()) == 0

def test_get_health_by_id(authenticated_client, db):
    response = authenticated_client.post("/servers", json={
        "server_name": "Dolly 1"
    })
    
    authenticated_client.post("/data", json={
        "server_ulid": response.json()["server_ulid"],
        "temperature": 25.5,
        "timestamp": datetime.now().isoformat()
    })

    server_ulid = response.json()["server_ulid"]
    
    response = authenticated_client.get(f"/health/{server_ulid}")
    
    assert response.status_code == 200
    assert response.json()["server_name"] == "Dolly 1"
    assert response.json()["server_ulid"] == server_ulid
    assert response.json()["status"] == "online"


def test_get_health_by_id_not_logged_in(authenticated_client, db):
    authenticated_client.headers = {}
    response = authenticated_client.get("/health/dontneedarealidbecauseimnotlogged")
    assert response.status_code == 401

def test_get_health_all_not_logged_in(authenticated_client, db):
    authenticated_client.headers = {}
    response = authenticated_client.get("/health/all")
    assert response.status_code == 401

def test_find_server_by_ulid(authenticated_client, db):
    response = authenticated_client.post("/servers", json={
        "server_name": "Dolly 1"
    })
    
    server_ulid = response.json()["server_ulid"]
    
    server_service = ServerService(db)

    server = server_service.find_by_id(server_ulid)
    
    assert server.server_name == "Dolly 1"
    assert server.id == server_ulid


def test_find_health_only_for_user(authenticated_client, db):
    _create_test_data_for_aggregations(authenticated_client)#creates at least one server

    authenticated_client.post("/auth/register", json={
        "username": "user",
        "password": "123456"
    })

    response = authenticated_client.post("/auth/login", data={
        "username": "user",
        "password": "123456"
    })

    token = response.json()["access_token"]

    authenticated_client.headers["Authorization"] = f"Bearer {token}"#change the token to the new user

    response = authenticated_client.post("/servers", json={
        "server_name": "Dolly 2"
    })
    
    server_ulid=response.json()["server_ulid"]

    response = authenticated_client.get("/health/all")
    
    assert len(response.json()) == 1
    assert response.json()[0]["server_ulid"] == server_ulid
    assert response.json()[0]["server_name"] == "Dolly 2"
    assert response.json()[0]["status"] == "offline"