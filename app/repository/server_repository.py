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
    
    def get_server_health(self, server_ulid: str = None):
        # Calculate the threshold time for "online" status (10 seconds ago)
        threshold_time = datetime.now() - timedelta(seconds=10)
        
        # Build query using SQLAlchemy expressions
        query = (
            self.db.query(
                Reading.server_ulid,
                case(
                    (func.max(Reading.timestamp_ms) >= threshold_time, 'online'),
                    else_='offline'
                ).label('status'),
                Server.server_name
            )
            .join(Server, Server.id == Reading.server_ulid)
            .group_by(Reading.server_ulid, Server.server_name)
            .order_by(func.max(Reading.timestamp_ms).asc())
        )
        
        # Apply server_ulid filter if provided
        if server_ulid:
            query = query.filter(Reading.server_ulid == server_ulid)
        
        return query.all()
