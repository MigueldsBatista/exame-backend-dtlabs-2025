import pytest
from fastapi import status
from app.schemas.reading_schema import PostReading, GetReading  
from app.services.reading_service import ReadingService  
import datetime

def test_post_reading(client, db):

    response = client.post("/servers", json={"server_name": "Dolly 1"})
    server_ulid = response.json()["server_ulid"]
    print(server_ulid)
    response = client.post("/data", json={
        "server_ulid": server_ulid,
        "temperature": 25.5,
        "timestamp": "2025-10-01T12:00:00Z"
    })

    assert response.status_code == status.HTTP_201_CREATED
    print(response.json())
    server_ulid = response.json()["server_ulid"]
    assert server_ulid is not None
    
  
def test_save_reading(client, db):
    response = client.post("/servers", json={"server_name": "Dolly 1"})
    server_ulid = response.json()["server_ulid"]

    reading_service = ReadingService(db)

    reading = PostReading(server_ulid=server_ulid, temperature=25.5, timestamp="2025-10-01T12:00:00Z")
    response = reading_service.save(reading)

    assert response.server_ulid == server_ulid
    assert response.temperature == 25.5
    assert response.timestamp == datetime.datetime(2025, 10, 1, 12, 0)

    readings = reading_service.find_all()
    assert len(readings) == 1

#FIXME
def test_get_readings(client, db):
    response = client.post("/servers", json={"server_name": "Dolly 1"})
    server_ulid = response.json()["server_ulid"]
    reading_service = ReadingService(db)
    reading1 = PostReading(server_ulid=server_ulid, temperature=25.5, timestamp="2025-10-01T12:00:00Z")
    reading2 = PostReading(server_ulid=server_ulid, humidity=30.0, timestamp="2025-10-01T13:00:00Z")
    reading_service.save(reading1)
    reading_service.save(reading2)

    # Faz a requisição GET sem filtros
    response = client.get("/data")

    # Verifica a resposta
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2


#FIXME
def test_get_filtered_readings(client, db):
    response = client.post("/servers", json={"server_name": "Dolly 1"})
    server_ulid1 = response.json()["server_ulid"]

    response = client.post("/servers", json={"server_name": "Dolly 2"})
    server_ulid2 = response.json()["server_ulid"]

    reading_service = ReadingService(db)
    reading1 = PostReading(server_ulid=server_ulid1, temperature=25.5, timestamp="2025-10-01T12:00:00Z")
    reading2 = PostReading(server_ulid=server_ulid2, humidity=30.0, timestamp="2025-10-01T13:00:00Z")

    reading_service.save(reading1)
    reading_service.save(reading2)


    filters = {"server_ulid": server_ulid1}
    response = client.get("/data", params=filters)
    # Verifica a resposta filtrada
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert response.json()[0]["sensor_id"] == server_ulid1