from passlib.context import CryptContext
"""
This module is used to decouple the auth service from user service
it serves as an interface between these two services
"""
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return password_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)
