from typing import Annotated
from fastapi import Body, Depends, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from dependencies import  get_user_service
from mappers.user_mapper import UserMapper
from exceptions.custom_exceptions import ConflictException, UnauthorizedException
from schemas.user_schema import PostUser
from services.auth_service import create_access_token, authenticate_user
from fastapi import APIRouter
from services.user_service import UserService

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    user: PostUser = Body(),
    user_service: UserService = Depends(get_user_service)
):
    if user_service.find_by_username(user.username):
        raise ConflictException("User already exists")

    user_entity = UserMapper.from_post_to_entity(user)
    saved_user = user_service.save(user_entity)
    user_response = UserMapper.from_entity_to_response(saved_user)

    return user_response

@router.post("/login",status_code=status.HTTP_200_OK)
async def login(
    form_data : Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: UserService = Depends(get_user_service)
):
    if not authenticate_user(form_data.username, form_data.password, user_service):
        raise UnauthorizedException("Invalid credentials")

    access_token = create_access_token(
        data={
            "sub": form_data.username
            })
    
    return {"access_token": access_token, "token_type": "bearer"}


