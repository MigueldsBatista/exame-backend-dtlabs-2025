from fastapi import status, Depends, APIRouter
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.server_schema import PostServer
from services.server_service import ServerService

router = APIRouter()

@router.post("/servers", status_code=status.HTTP_201_CREATED)
async def post_server(server : PostServer, db: Session = Depends(get_db)):
    server_service = ServerService(db)
    new_server = server_service.create_server(server)

    return new_server