
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from core.database import get_db
from exceptions.custom import UnauthorizedException
from mappers.user_mapper import UserMapper
from schemas.auth_schema import UserResponse
from services.user_service import UserService
from models.user import User  # Importe o modelo User
from sqlalchemy.orm import Session

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user_dependency(
    token: str = Depends(oauth2_bearer),
    db: Session = Depends(get_db)
) -> UserResponse:
    user_service = UserService(db)
    user =  user_service.get_current_user(token)

    if not user:
        raise UnauthorizedException("User not logged in")
    
    return UserMapper.from_entity_to_response(user)


