from sqlalchemy.orm import Session
from exceptions.custom import NotFoundException
from repository.server_repository import ServerRepository
from schemas.server_schema import ServerResponse, ServerStatusResponse
from schemas.server_schema import PostServer
from mappers.server_mapper import ServerMapper


class ServerService:

    def __init__(self, db: Session):
        """Initialize the service with a database session."""
        self.db = db
        self.server_repository = ServerRepository(db)
        
    def save(self, data: PostServer) -> ServerResponse:
        if not data:
            raise ValueError("Server cannot be None")
        
        entity = ServerMapper.from_post_to_entity(data)
        self.server_repository.save(entity)
        return ServerMapper.from_entity_to_response(entity)


    def find_all(self) -> list:
        return self.server_repository.find_all()
    
    def find_by_id(self, id: int) -> ServerResponse:
        entity = self.server_repository.find_by_id(id)
        if not entity:
            return None
        return ServerMapper.from_entity_to_response(entity)
    
    def delete_by_id(self, id: int) -> bool:
        return self.server_repository.delete(id)
    
    
    def _get_server_health(self, server_id: int= None) -> ServerStatusResponse:
        if server_id is None:
            servers = self.server_repository.get_server_health()

            return ServerMapper.from_tuples_to_responses(servers)
        
        entity = self.server_repository.find_by_id(server_id)
        if entity is None:
            raise NotFoundException(f"Entity with id: {server_id} not found")
        
        server_status = self.server_repository.get_server_health(entity.id)
        
        #Maybe the server has never been online and never recived readings
        if len(server_status) == 0:
            return ServerStatusResponse(
                server_ulid=entity.id,
                server_name=entity.server_name,
                status="offline"
            )
        
        return ServerMapper.from_tuple_to_response(server_status[0])#Always one element in the list

    def get_server_health_all(self) -> list:

        return self._get_server_health()
    
    def get_server_health_by_id(self, server_id: int) -> ServerStatusResponse:
        return self._get_server_health(server_id)