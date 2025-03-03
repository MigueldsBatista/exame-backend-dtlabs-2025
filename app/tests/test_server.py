from datetime import datetime


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
