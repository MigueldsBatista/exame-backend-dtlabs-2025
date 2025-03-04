from fastapi import APIRouter, Depends, status
from dependencies import get_current_user_dependency, get_reading_service
from services.reading_service import ReadingService
from mappers.reading_mapper import ReadingMapper
from schemas.user_schema import UserResponse
from schemas.reading_schema import PostReading, GetReadingParams, ReadingResponse
from schemas.error_schema import NotFoundError, ValidationErrorDetail, UnauthorizedError
from typing import List, Dict, Any

router = APIRouter(
    prefix="/data",
    tags=["Sensor Data"],

)

@router.post(
    "", 
    status_code=status.HTTP_201_CREATED,
    summary="Submit sensor reading",
    description="""
    Submit a new sensor reading with the following information:
    
    - server_ulid: The unique identifier for the server
    - timestamp: The timestamp when the reading was taken (ISO8601 format)
    - temperature: Optional temperature reading (can be null)
    - humidity: Optional humidity reading (can be null, range 0-100%)
    - voltage: Optional voltage reading (can be null)
    - current: Optional current reading (can be null)
    
    At least one of the sensor readings must be provided.
    """, 
    response_description="The submitted sensor reading data",
    response_model=ReadingResponse,
        responses={
        401: {"model": UnauthorizedError, "description": "Authentication required"},
        404: {"model": NotFoundError, "description": "Server ulid not found"},
        422 :{"model": ValidationErrorDetail, "description": "Validation error"}
    }
)
async def submit_reading(
    post_reading: PostReading,
    reading_service: ReadingService = Depends(get_reading_service),
    ):

    reading_entity = ReadingMapper.from_post_to_entity(post_reading)
    saved_entity = reading_service.save(reading_entity)
    response_reading = ReadingMapper.from_entity_to_response(saved_entity)
    return response_reading
    

@router.get(
    "", 
    status_code=status.HTTP_200_OK,
    summary="Query sensor readings",
    description="""
    Retrieve sensor readings with optional filters:
    
    Filters:
    - server_ulid: Filter by specific server ULID (the server must exist)
    - sensor_type: Filter by sensor type (temperature, humidity, voltage, current)
    - aggregation: Aggregate data by (day, hour, minute)
    - start_time: Filter readings starting from this time (ISO8601 format)
    - end_time: Filter readings up to this time (ISO8601 format)
    
    If no filters are provided, returns all available readings.

    If aggregation is provided, returns aggregated data instead with only one value per sensor type.

    Pydantic models are used to validate the query parameters.
    """,
    response_description="List of sensor readings or aggregated data",
    response_model=List[ReadingResponse],
        responses={
        401: {"model": UnauthorizedError, "description": "Authentication required"},
        422 :{"model": ValidationErrorDetail, "description": "Validation error"}
    },
    response_model_exclude_none=True# Exclude None values from the response
)
async def query_readings(
    current_user: UserResponse = Depends(get_current_user_dependency),
    filters: GetReadingParams = Depends(),
    reading_service: ReadingService = Depends(get_reading_service)
    ):

    readings = reading_service.find_readings_by_params(filters)
    
    if not readings:
        return []
    
    if hasattr(readings[0], '__table__'):  # Check if it's an ORM entity
        # If readings are entities
        responses = ReadingMapper.from_entities_to_responses(readings, filters)
    else:
        # If readings are tuples from an aggregate query
        responses = ReadingMapper.from_aggregate_tuples_to_responses(readings, filters)
    
    return responses