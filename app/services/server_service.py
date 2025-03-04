from sqlalchemy.orm import Session
from exceptions.custom_exceptions import NotFoundException
from repository.server_repository import ServerRepository
from models.server import Server


class ServerService:

    def __init__(self, db: Session):
        """Initialize the service with a repository."""
        self.repository = ServerRepository(db)
        
    def save(self, server: Server) -> Server:
        if not server:
            raise ValueError("Server cannot be None")
        
        return self.repository.save(server)

    def find_by_name(self, server_name: str) -> Server:
        if not server_name:
            raise ValueError("Server name cannot be None")
        
        return self.repository.find_by_name(server_name)

    def find_all(self) -> list:
        entities= self.repository.find_all()
        return entities if entities else []
    
    def find_by_id(self, id: int) -> Server:
        if not id:
            raise ValueError("Id cannot be None")
        
        return self.repository.find_by_id(id)

    
    def delete_by_id(self, id: int) -> bool:
        if not id:
            raise ValueError("Id cannot be None")
        
        return self.repository.delete(id)
    
    
    def _get_server_health(self, server_id: int= None, user_id :int =None) -> Server:
        if server_id is None and user_id is not None:
            return self.repository.get_server_health(user_id=user_id)

        
        entity = self.repository.find_by_id(server_id)
        if entity is None:
            raise NotFoundException(f"Entity with id: {server_id} not found")
        
        return self.repository.get_server_health(server_ulid=entity.id)
        

    def get_server_health_all(self, user_id: str) -> list:
        """Get health data for all servers created by the specified user"""
        return self.repository.get_server_health_all(user_id=user_id)
    
    def get_server_health_by_id(self, server_id: str) -> list:
        """Get health data for a specific server by ID"""
        if not server_id:
            raise ValueError("Server ID cannot be None")
        
        entity = self.find_by_id(server_id)
        if entity is None:
            raise NotFoundException(f"Server with id: {server_id} not found")
        
        return self.repository.get_server_health_by_id(server_id)