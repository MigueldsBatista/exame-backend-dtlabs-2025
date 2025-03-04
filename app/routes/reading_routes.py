from fastapi import APIRouter, Depends, status
from dependencies import get_current_user_dependency, get_reading_service
from services.reading_service import ReadingService
from mappers.reading_mapper import ReadingMapper
from schemas.user_schema import UserResponse
from schemas.reading_schema import PostReading, GetReadingParams

router = APIRouter()

@router.post("/data", status_code=status.HTTP_201_CREATED)
async def post_reading(
    post_reading: PostReading,
    reading_service: ReadingService = Depends(get_reading_service),
    ):

    reading_entity = ReadingMapper.from_post_to_entity(post_reading)
    saved_entity = reading_service.save(reading_entity)
    response_reading =  ReadingMapper.from_entity_to_response(saved_entity)
    return response_reading
    

@router.get("/data", status_code=status.HTTP_200_OK)
async def get_readings(
    current_user: UserResponse = Depends(get_current_user_dependency),
    filters : GetReadingParams = Depends(),
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
    
    # Return list of response DTOs
    return [response.model_dump(exclude_none=True) for response in responses]