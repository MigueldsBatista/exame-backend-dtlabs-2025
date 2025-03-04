import pytest
from fastapi import status
from app.mappers.reading_mapper import ReadingMapper
from app.schemas.reading_schema import PostReading, GetReadingParams
from app.services.reading_service import ReadingService
import datetime
from .conftest import _create_test_data_for_aggregations

def test_post_invalid_reading(authenticated_client, db):
    response = authenticated_client.post("/servers", json={"server_name": "Dolly 1"})
    server_ulid = response.json()["server_ulid"]

    response = authenticated_client.post("/data", json={
        "server_ulid": server_ulid,
        "timestamp": "2025-10-01T12:00:00Z"
    })
    #The reading must contain at least one of the following fields: temperature, humidity, current, voltage
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_get_reading_not_logged_in(authenticated_client, db):
    authenticated_client.headers = {}
    response = authenticated_client.get("/data")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_invalid_date_range_reading(authenticated_client, db):
    response = authenticated_client.get("/data", params={"start_time": "2025-10-01T12:00:00Z", "end_time": "2025-10-01T11:00:00Z"})
    #The start time must be before the end time
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "Start time cannot be after end time" in response.json()["detail"]
    

def test_post_reading(authenticated_client, db):

    response = authenticated_client.post("/servers", json={"server_name": "Dolly 1"})
    
    server_ulid = response.json()["server_ulid"]
    response = authenticated_client.post("/data", json={
        "server_ulid": server_ulid,
        "temperature": 25.5,
        "timestamp": "2025-10-01T12:00:00Z"
    })
    assert response.status_code == status.HTTP_201_CREATED
    server_ulid = response.json()["server_ulid"]
    assert server_ulid is not None
  
def test_save_reading(authenticated_client, db):
    response = authenticated_client.post("/servers", json={"server_name": "Dolly 1"})
    server_ulid = response.json()["server_ulid"]

    reading_service = ReadingService(db)

    post_reading = PostReading(server_ulid=server_ulid, temperature=25.5, timestamp="2025-10-01T12:00:00Z")

    reading_entity = ReadingMapper.from_post_to_entity(post_reading)
    
    response = reading_service.save(reading_entity)

    assert response.server_ulid == server_ulid
    assert response.temperature == 25.5
    assert response.timestamp == datetime.datetime(2025, 10, 1, 12, 0)

    readings = reading_service.find_all()
    assert len(readings) == 1


def test_get_readings(authenticated_client, db):
    response = authenticated_client.get("/data")
    assert response.status_code == status.HTTP_200_OK


def test_get_filtered_server_readings(authenticated_client, db):
    response = authenticated_client.post("/servers", json={"server_name": "Dolly 1"})

    server_ulid1 = response.json()["server_ulid"]

    response = authenticated_client.post("/servers", json={"server_name": "Dolly 2"})

    response = authenticated_client.post("/data", json={
        "server_ulid": server_ulid1,
        "temperature": 25.5,
        "timestamp": "2025-10-01T12:00:00Z"
    })
    
    filters = {"server_ulid": server_ulid1}

    response = authenticated_client.get("/data", params=filters)

    assert response.status_code == status.HTTP_200_OK

    assert len(response.json()) == 1

    assert response.json()[0]["server_ulid"] == server_ulid1


    
def test_get_filtered_sensor_readings(authenticated_client, db):
    response = authenticated_client.post("/servers", json={"server_name": "Dolly 1"})
    server_ulid1 = response.json()["server_ulid"]

    response = authenticated_client.post("/data", json={
        "server_ulid": server_ulid1,
        "temperature": 25.5,
        "timestamp": "2025-10-01T12:00:00Z",
        "humidity": 70.0,
        "current": 1.0,
        "voltage": 220.0
    })
    
    filters = {"server_ulid": server_ulid1, "sensor_type": "temperature"}

    response = authenticated_client.get("/data", params=filters)

    assert response.status_code == status.HTTP_200_OK

    assert len(response.json()) == 1

    assert response.json()[0]["server_ulid"] == server_ulid1

    assert not any(key in response.json()[0] for key in ["humidity", "current", "voltage"])


def test_get_filtered_interval_readings(authenticated_client, db):
    response = authenticated_client.post("/servers", json={"server_name": "Dolly 1"})
    server_ulid1 = response.json()["server_ulid"]

    # First reading - at 13:00
    response = authenticated_client.post("/data", json={
        "server_ulid": server_ulid1,
        "temperature": 25.5,
        "timestamp": "2025-10-01T13:00:00Z",
        "humidity": 70.0,
        "current": 1.0,
        "voltage": 220.0
    })

    # Second reading - at 12:30
    response1 = authenticated_client.post("/data", json={
        "server_ulid": server_ulid1,
        "temperature": 26.5,
        "timestamp": "2025-10-01T12:30:00Z",
        "humidity": 71.0,
        "current": 1.1,
        "voltage": 221.0
    })
    
    # Filter for readings between 12:30:01 and 13:00:00
    filters = {"server_ulid": server_ulid1, "start_time": "2025-10-01T12:30:01Z", "end_time": "2025-10-01T13:00:00Z"}

    response = authenticated_client.get("/data", params=filters)

    assert response.status_code == status.HTTP_200_OK

    assert len(response.json()) == 1

    assert response.json()[0]["server_ulid"] == server_ulid1
    # Should be the first reading, not the second
    assert response.json()[0]["timestamp"] == "2025-10-01T13:00:00"
    assert response.json()[0]["temperature"] == 25.5


def test_get_aggregated_values_by_day(authenticated_client, db):
    """Test day-level aggregation of readings"""
    server_ulid = _create_test_data_for_aggregations(authenticated_client)
    
    # Request day aggregation
    response = authenticated_client.get("/data", params={
        "server_ulid": server_ulid,
        "aggregation": "day"
    })
    
    # Verify response
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert len(data) == 2, "Should have 2 days of aggregated data"
    
    # Sort data by timestamp if needed
    data.sort(key=lambda x: x["timestamp"])
    
    # Verify day 1 (Oct 1) - average of 2 readings
    assert data[0]["timestamp"].startswith("2025-10-01")
    assert round(data[0]["temperature"], 1) == 25.8  # (25.0 + 26.5) / 2
    assert round(data[0]["humidity"], 1) == 70.5     # (70.0 + 71.0) / 2
    
    # Verify day 2 (Oct 2) - average of 3 readings
    assert data[1]["timestamp"].startswith("2025-10-02")
    assert round(data[1]["temperature"], 1) == 27.5  # (27.0 + 27.5 + 28.0) / 3
    assert round(data[1]["humidity"], 1) == 73.0     # (72.0 + 73.0 + 74.0) / 3
    

def test_get_aggregated_values_by_hour(authenticated_client, db):
    """Test hour-level aggregation of readings"""
    server_ulid = _create_test_data_for_aggregations(authenticated_client)
    
    # Request hour aggregation
    response = authenticated_client.get("/data", params={
        "server_ulid": server_ulid,
        "aggregation": "hour"
    })
    # Verify response
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert len(data) == 4, "Should have 4 hours of aggregated data"
    
    # Sort data by timestamp
    data.sort(key=lambda x: x["timestamp"])
    
    # Check for the 4 different hours
    hours = [entry["timestamp"] for entry in data]
    assert any("2025-10-01T13" in h for h in hours), "Should have Oct 1, 13:00"
    assert any("2025-10-01T14" in h for h in hours), "Should have Oct 1, 14:00"
    assert any("2025-10-02T12" in h for h in hours), "Should have Oct 2, 12:00"  
    assert any("2025-10-02T13" in h for h in hours), "Should have Oct 2, 13:00"
    
    # Check a specific hour's data (Oct 2, 13:00 - has 2 readings)
    hour_13_day_2 = next(entry for entry in data if "2025-10-02T13" in entry["timestamp"])
    assert round(hour_13_day_2["temperature"], 1) == 27.8  # (27.5 + 28.0) / 2
    

def test_get_aggregated_values_by_minute(authenticated_client, db):
    """Test minute-level aggregation of readings"""
    server_ulid = _create_test_data_for_aggregations(authenticated_client)
    
    # Request minute aggregation
    response = authenticated_client.get("/data", params={
        "server_ulid": server_ulid,
        "aggregation": "minute"
    })
    
    # Verify response
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert len(data) == 5, "Should have 5 distinct minutes of data"
    
    # Check for the one minute that has two readings (Oct 2, 13:01)
    minute_entries = [entry for entry in data if "2025-10-02T13:01" in entry["timestamp"]]
    assert len(minute_entries) == 1
    assert minute_entries[0]["temperature"] == 28.0
    
