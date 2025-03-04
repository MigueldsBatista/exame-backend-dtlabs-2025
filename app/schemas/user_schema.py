from pydantic import BaseModel
from pydantic import field_validator


class PostUser(BaseModel):
    username: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "password": "securepassword123"
            }
        }
    
    @field_validator("username", "password", mode="after")
    def check_empty(cls, value):
        if value is None or value == "":
            raise ValueError("Username and password are required")
        return value


class UserResponse(BaseModel):
    id: int
    username: str

class LoginRequest(BaseModel):
    """Schema for a login request
    This schema is used for direct JSON-based authentication."""
    username: str
    password: str

    @field_validator("username", "password", mode="after")
    def check_empty(cls, value):
        if value is None or value == "":
            raise ValueError("Username and password are required")
        return value

    class Config:
        schema_extra = {
            "example": {
                "username": "user123",
                "password": "securepassword"
            }
        }