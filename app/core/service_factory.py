from sqlalchemy.orm import Session
from services.reading_service import ReadingService
from services.server_service import ServerService
from services.user_service import UserService
from typing import Optional

class ServiceFactory:
    """Factory class for creating service instances with proper dependencies"""
    
    _instance: Optional['ServiceFactory'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ServiceFactory, cls).__new__(cls)
            cls._instance._services = {}
        return cls._instance
    
    def get_user_service(self, db: Session) -> UserService:
        """Get or create a UserService instance for the given db session"""
        service_key = f"user_service_{id(db)}"
        if service_key not in self._services:
            self._services[service_key] = UserService(db)
        return self._services[service_key]
    
    # You can add more service getters here as your application grows
    def get_reading_service(self, db: Session) -> ReadingService:
        """Get or create a ReadingService instance for the given db session"""
        service_key = f"reading_service_{id(db)}"
        if service_key not in self._services:
            self._services[service_key] = ReadingService(db)
        return self._services[service_key]
    
    def get_server_service(self, db: Session) -> ServerService:
        """Get or create a ServerService instance for the given db session"""
        service_key = f"server_service_{id(db)}"
        if service_key not in self._services:
            self._services[service_key] = ServerService(db)
        return self._services[service_key]
    
service_factory = ServiceFactory()
