from datetime import datetime, timedelta, timezone

from services.user_service import UserService
from exceptions.custom_exceptions import UnauthorizedException
from core.settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

from jose import jwt
from jose.exceptions import JWTClaimsError, JWTError, ExpiredSignatureError
from utils.password_utils import verify_password
from models.user import User

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    
    except JWTClaimsError:
        raise UnauthorizedException("Invalid token claims")
    
    except ExpiredSignatureError:
        raise UnauthorizedException("Token expired")
    
    except JWTError:
        raise UnauthorizedException("Could not validate token")

def authenticate_user(username: str, password: str, user_service: UserService) -> bool:
    saved_user = user_service.find_by_username(username)
    if not saved_user or not verify_password(password, saved_user.password):
        return False
    return True

def get_current_user(token: str, user_service: UserService) -> User:
    user = decode_access_token(token)["sub"]
    stored_user = user_service.find_by_username(user)
    if not stored_user:
        return None
    return stored_user