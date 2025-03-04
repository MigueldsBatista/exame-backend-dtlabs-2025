from repository.user_repository import UserRepository
from models.user import User
from utils.password_utils import get_password_hash
from sqlalchemy.orm import Session


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository(db)
        
    def save(self, user: User) -> User:
        hashed_password = get_password_hash(user.password)
        user.password = hashed_password
        saved_user = self.repository.save(user)
        return saved_user
    
    def find_by_username(self, username: str) -> User:
        if not username:
            raise ValueError("Username cannot be None")
        return self.repository.find_by_username(username)
    
    def find_by_id(self, id: int) -> User:
        if not id:
            raise ValueError("Id cannot be None")
        return self.repository.find_by_id(id)
    
    def find_all(self) -> list:
        return self.repository.find_all()
    
    def delete(self, id: int) -> bool:
        if not id:
            raise ValueError("Id cannot be None")
        return self.repository.delete(id)
    
