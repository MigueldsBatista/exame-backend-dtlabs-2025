from fastapi import status, Depends, APIRouter
from sqlalchemy.orm import Session
from dependencies import get_current_user_dependency
from schemas.auth_schema import UserResponse
from core.database import get_db
from schemas.server_schema import PostServer
from services.server_service import ServerService

router = APIRouter()

@router.post("/servers", status_code=status.HTTP_201_CREATED)
async def post_server(server : PostServer, db: Session = Depends(get_db)):
    server_service = ServerService(db)
    new_server = server_service.save(server)

    return new_server

@router.get("/health/all", status_code=status.HTTP_200_OK)
async def get_health(
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user_dependency)
        ):
    
    server_service = ServerService(db)

    return server_service.get_server_health_all()

@router.get("/health/{server_id}", status_code=status.HTTP_200_OK)
async def get_health(
        server_id: str,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user_dependency)
        ):
    
    server_service = ServerService(db)

    return server_service.get_server_health_by_id(server_id)

