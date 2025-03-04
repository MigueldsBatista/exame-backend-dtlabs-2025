from typing import List, Tuple
from sqlalchemy import text, case, func, select, join
from repository.base_repository import BaseRepository
from models.server import Server
from models.reading import Reading
import ulid
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

class ServerRepository(BaseRepository[Server]):
    def __init__(self, db):
        super().__init__(Server, db)

    def find_by_ulid(self, ulid: str):
        return self.db.query(Server).filter(Server.id == ulid).first()
    
    def save(self, obj):
        if not obj.id:
            obj.id = str(ulid.new())
        return super().save(obj)
    
    def get_server_health(self, server_ulid: str = None, user_id: str = None):
        # Calculate the threshold time for "online" status (10 seconds ago)
        threshold_time = datetime.now() - timedelta(seconds=10)
        
        # Build query using SQLAlchemy expressions
        query = (
            self.db.query(
                Server.id,
                case(
                    (func.max(Reading.timestamp) >= threshold_time, 'online'),
                    else_='offline'
                ).label('status'),
                Server.server_name
            )
            .outerjoin(Reading, Server.id == Reading.server_ulid)
            .group_by(Server.id, Server.server_name)
            .order_by(func.max(Reading.timestamp).asc())
        )
        
        # Apply server_ulid filter if provided
        if server_ulid:
            query = query.filter(Reading.server_ulid == server_ulid)
            
        if user_id:
            query = query.filter(Server.created_by == user_id)
            
        return query.all()
    

        
    def get_server_health_all(self, user_id: str = None) -> List[Tuple]:
        """Get health data for all servers, optionally filtered by user"""
        return self.get_server_health(user_id=user_id)
    
    def get_server_health_by_id(self, server_id: str) -> List[Tuple]:
        """Get health data for a specific server"""
        return self.get_server_health(server_ulid=server_id)
    
    def find_by_name(self, server_name: str):
        return self.db.query(Server).filter(Server.server_name == server_name).first()
