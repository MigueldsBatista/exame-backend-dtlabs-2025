from fastapi import status, HTTPException
from models.user import User
from services.auth_service import get_password_hash, verify_password, create_access_token
from fastapi import APIRouter

fake_users_db = {}

router = APIRouter()

#PREFIX /auth

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user):
    if user.username in fake_users_db:
        raise Exception("User already registered")
    
    hashed_password = get_password_hash(user.password)
    fake_users_db[user.username] = {"username": user.username, "password_hash": hashed_password}
    return {"msg": "User registered successfully"}

@router.post("/login")
async def login(user):
    db_user = fake_users_db.get(user.username)
    if not db_user or not verify_password(user.password, db_user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

