from typing import Annotated
from fastapi import Body, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from dependencies import get_current_user_dependency
from mappers.user_mapper import UserMapper
from core.database import get_db
from exceptions.custom import ConflictException, UnauthorizedException
from schemas.auth_schema import PostUser, UserResponse
from services.auth_service import  create_access_token
from fastapi import APIRouter
from sqlalchemy.orm import Session
from services.user_service import UserService
fake_users_db = {}

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user : PostUser = Body(), db : Session = Depends(get_db)):
    user_service = UserService(db)
    if user_service.find_by_username(user.username):
        raise ConflictException("User already exists")

    user_entity = UserMapper.from_post_to_entity(user)
    
    saved_user = user_service.save(user_entity)
    response = UserMapper.from_entity_to_response(saved_user)

    return response

@router.post("/login",status_code=status.HTTP_200_OK)
async def login(
    form_data : Annotated[OAuth2PasswordRequestForm, Depends()],
    db : Session = Depends(get_db)
    ):
    user_service = UserService(db)

    if not user_service.authenticate_user(form_data.username, form_data.password):
        raise UnauthorizedException("Invalid credentials")

    access_token = create_access_token(
        data={
            "sub": form_data.username
            })
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
async def get_current_user(current_user : UserResponse = Depends(get_current_user_dependency), db: Session = Depends(get_db)) -> UserResponse:
        
        return current_user
    
