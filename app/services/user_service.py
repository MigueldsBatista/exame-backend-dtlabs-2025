from repository.user_repository import UserRepository
from models.user import User
from services.auth_service import get_password_hash, verify_password, decode_access_token
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
        return self.repository.find_by_username(username)
    
    def find_by_id(self, id: int) -> User:
        return self.repository.find_by_id(id)
    
    def find_all(self) -> list:
        return self.repository.find_all()
    
    def delete(self, id: int) -> bool:
        return self.repository.delete(id)
    
    def authenticate_user(self, username, password) -> bool:
        saved_user = self.find_by_username(username)
        if not saved_user or not verify_password(password, saved_user.password):
            return False
        return True
    
    def get_current_user(self, token) -> User:
        user = decode_access_token(token)["sub"]
        stored_user = self.find_by_username(user)
        if not stored_user:
            return None
        return stored_user