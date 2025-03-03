from models.user import User
from repository.base_repository import BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self, db):
        super().__init__(User, db)


    def find_by_username(self, username: str):
        return self.db.query(User).filter(User.username == username).first()
    
