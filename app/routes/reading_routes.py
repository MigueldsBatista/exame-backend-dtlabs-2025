from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from dependencies import get_current_user_dependency
from schemas.auth_schema import UserResponse
from models.user import User
from core.database import get_db
from schemas.reading_schema import PostReading, GetReading
from services.reading_service import ReadingService

router = APIRouter()

@router.post("/data", status_code=status.HTTP_201_CREATED)
async def post_reading(
    reading: PostReading,
    db: Session = Depends(get_db),
    ):

    reading_service = ReadingService(db)
    new_reading = reading_service.save(reading)
    return new_reading
    

@router.get("/data", status_code=status.HTTP_200_OK)
async def get_readings(
    filters : GetReading = Depends(),
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user_dependency)
    ):

    reading_service = ReadingService(db)
    readings = reading_service.find_by_filters(filters)
    if not readings:
        return []
    
    return [reading.model_dump(exclude_none=True) for reading in readings]