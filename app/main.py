from fastapi import FastAPI, Depends, HTTPException, status
from schemas.server_schema import PostServer
from services.server_service import ServerService
from core.database import get_db
from auth import User, get_password_hash, verify_password, create_access_token, decode_access_token, oauth2_scheme
from schemas.reading_schema import PostReading, ReadingResponse
from schemas.reading_schema import GetReading
from services.reading_service import ReadingService
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoReferencedTableError

app = FastAPI()
fake_users_db = {}


@app.post("/auth/register")
async def register(user: User):
    """Register a new user.
    
    Args:
        user (User): The user data.
    
    Returns:
        dict: A success message.
    """
    if user.username in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    hashed_password = get_password_hash(user.password)
    fake_users_db[user.username] = {"username": user.username, "password_hash": hashed_password}
    return {"msg": "User registered successfully"}

@app.post("/auth/login")
async def login(user: User):
    """Login a user.
    
    Args:
        user (User): The user data.
    
    Returns:
        dict: The access token.
    """
    db_user = fake_users_db.get(user.username)
    if not db_user or not verify_password(user.password, db_user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/data", response_model=PostReading, status_code=status.HTTP_201_CREATED)
async def register_reading(reading: PostReading, db: Session = Depends(get_db)):
    """Register a new reading.
    
    Args:
        reading (PostReading): The reading data.
        db (Session): The database session.
    
    Returns:
        PostReading: The registered reading.
    """
    try:
        reading_service = ReadingService(db)
        
        new_reading = reading_service.create_reading(reading)

        return new_reading
    except NoReferencedTableError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Server ulid not found",
        )


@app.get("/data", status_code=status.HTTP_200_OK)
async def get_reading(filter_query: GetReading = Depends()):
    """Get readings with optional filters.
    
    Args:
        filter_query (GetReading): The filter query parameters.
    
    Returns:
        List[ReadingResponse]: The list of readings.
    """
    return filter_query


@app.post("/servers", status_code=status.HTTP_201_CREATED)
async def register_server(server : PostServer, db: Session = Depends(get_db)):

    server_service = ServerService(db)
    
    new_server = server_service.create_server(server)

    return new_server


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)

