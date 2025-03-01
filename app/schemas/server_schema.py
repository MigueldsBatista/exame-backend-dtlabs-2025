from pydantic import BaseModel

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