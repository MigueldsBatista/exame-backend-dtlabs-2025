from models.user import User
from schemas.auth_schema import PostUser, UserResponse


class UserMapper:


    @staticmethod
    def from_entity_to_response(entity: User) -> UserResponse:
        return UserResponse(
            username=entity.username,
            id=entity.id
        )
    
    @staticmethod
    def from_post_to_entity(data: PostUser) -> User:
        return User(
            username=data.username,
            password=data.password
        )