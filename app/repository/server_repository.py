from repository.base_repository import BaseRepository
from models.server import Server
import ulid

class ServerRepository(BaseRepository[Server]):
    def __init__(self, db):
        super().__init__(Server, db)

    def find_by_ulid(self, ulid: str):
        return self.db.query(Server).filter(Server.id == ulid).first()
    

    def save(self, obj):

        if not obj.id:  # Só gera um novo ID se não existir
            obj.id = str(ulid.new())  # Gera o ULID como string

        return super().save(obj)