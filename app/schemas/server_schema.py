from pydantic import BaseModel, field_validator


class ServerResponse(BaseModel):
    """Schema for server response data
    This schema is used to structure the response data when querying server information."""
    server_name: str  # The name of the server
    server_ulid: str  # The unique identifier of the server


#-----------------------------------------------------------------------


class PostServer(BaseModel):
    """Schema for creating a new server
    This schema is used to validate the data when creating a new server."""
    server_name: str  # The name of the server to be created

    @field_validator("server_name", mode="before")
    def validate_server_name(cls, server_name: str):
        if not server_name or server_name.strip() == "":
            raise ValueError("Server name cannot be empty")
        return server_name

class ServerStatusResponse(BaseModel):
    """Schema for server status response data
    This schema is used to structure the response data when querying server status information."""
    server_ulid: str  # The unique identifier of the server
    server_name: str  # The name of the server
    status: str  # The status of the server (online or offline)