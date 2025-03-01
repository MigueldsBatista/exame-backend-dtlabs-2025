from sqlalchemy.orm import Session
from repository.server_repository import ServerRepository
from schemas.server_schema import ServerResponse
from schemas.server_schema import PostServer
from mappers.server_mapper import ServerMapper


class ServerService:
    """Service for Server operations
    This service handles the business logic for Server operations."""

    def __init__(self, db: Session):
        """Initialize the service with a database session."""
        self.db = db
        self.server_repository = ServerRepository(db)
        
    def create_server(self, data: PostServer) -> ServerResponse:
        if data is None:
            raise ValueError("Server cannot be None")
        
        entity = ServerMapper.from_post_to_entity(data)
        self.server_repository.save(entity)
        return ServerMapper.from_entity_to_response(entity)

