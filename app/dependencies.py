from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from services.reading_service import ReadingService
from core.database import get_db
from exceptions.custom_exceptions import UnauthorizedException
from schemas.user_schema import UserResponse
from mappers.user_mapper import UserMapper
from services.auth_service import get_current_user
from services.user_service import UserService
from core.service_factory import service_factory
from services.server_service import ServerService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return service_factory.get_user_service(db)

def get_reading_service(db: Session = Depends(get_db)) -> ReadingService:
    return service_factory.get_reading_service(db)

def get_server_service(db: Session = Depends(get_db)) -> ServerService:
    return service_factory.get_server_service(db)

async def get_current_user_dependency(
    token: str = Depends(oauth2_scheme), 
    user_service: UserService = Depends(get_user_service)
) -> UserResponse:
    """
    Dependency that provides the current authenticated user.
    Uses the user_service dependency to get user information.
    """
    current_user = get_current_user(token, user_service)
    
    if current_user is None:
        raise UnauthorizedException("Invalid authentication credentials")
    
    return UserMapper.from_entity_to_response(current_user)


