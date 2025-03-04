from typing import Annotated
from fastapi import Body, Depends, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from dependencies import get_user_service
from mappers.user_mapper import UserMapper
from exceptions.custom_exceptions import ConflictException, UnauthorizedException
from schemas.user_schema import PostUser, UserResponse
from schemas.auth_schema import Token
from services.auth_service import create_access_token, authenticate_user
from services.user_service import UserService
from schemas.error_schema import ConflictError, UnauthorizedError
from schemas.error_schema import ValidationErrorDetail
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],

)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
    description="Registers a new user in the system. If the username is already in use, returns a conflict error.",
    response_model=UserResponse,
        responses={
        409: {"model": ConflictError, "description": "User already exists"},
        422 :{"model": ValidationErrorDetail, "description": "Validation error"}
    }
)
async def register(
    user: PostUser = Body(
        ..., 
        description="New user data, including username and password."
    ),
    user_service: UserService = Depends(get_user_service)
):
    """
    Registers a new user. Checks if the username is already registered,
    maps the data to the entity and persists it in the database.
    """
    if user_service.find_by_username(user.username):
        raise ConflictException("User already exists")

    user_entity = UserMapper.from_post_to_entity(user)
    saved_user = user_service.save(user_entity)
    user_response = UserMapper.from_entity_to_response(saved_user)

    return user_response

@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    summary="User login",
    description="""
    Authenticates a user and returns an access token (JWT).
    
    - grant_type: The OAuth2 grant type (password).
    - username: The username of the user.
    - password: The password of the user.
    - client_id: The OAuth2 client ID. (NOT IMPLEMENTED)
    - client_secret: The OAuth2 client secret. (NOT IMPLEMENTED)
    - scope: The OAuth2 scope. (NOT IMPLEMENTED)
    """,
    response_model=Token,
        responses={
        422 :{"model": ValidationErrorDetail, "description": "Validation error"},
        401: {"model": UnauthorizedError, "description": "Invalid credentials"}
    }
)
async def login(
    form_data: Annotated[
        OAuth2PasswordRequestForm, 
        Depends()
    ],
    user_service: UserService = Depends(get_user_service)
):
    """
    Performs login by authenticating user credentials and returns
    an access token (JWT) that can be used in protected routes.
    """
    if not authenticate_user(form_data.username, form_data.password, user_service):
        raise UnauthorizedException("Invalid credentials")

    access_token = create_access_token(
        data={"sub": form_data.username}
    )

    return {"access_token": access_token, "token_type": "bearer"}