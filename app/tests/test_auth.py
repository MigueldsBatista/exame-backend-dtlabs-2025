import logging 
from fastapi import status


def test_register_and_login(authenticated_client):
    response = authenticated_client.post("/auth/register", json={
        "username": "test",
        "password": "test"
    })

    assert response.status_code == status.HTTP_201_CREATED

    response = authenticated_client.post("/auth/login", data={
        "username": "test",
        "password": "test"
    })

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert "token_type" in response.json()


def test_login_invalid_user(authenticated_client):
    response = authenticated_client.post("/auth/login", data={
        "username": "invalid",
        "password": "invalid"
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
