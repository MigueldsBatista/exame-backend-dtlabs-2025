from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

from exceptions.custom import UnauthorizedException
from core.settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

from jose import jwt
#claim error
from jose.exceptions import JWTClaimsError
from jose.exceptions import JWTError
from jose.exceptions import ExpiredSignatureError


# Inicialização do contexto de criptografia
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Funções auxiliares
def get_password_hash(password: str) -> str:
    return password_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:

    return password_context.verify(plain_password, hashed_password)

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
    
