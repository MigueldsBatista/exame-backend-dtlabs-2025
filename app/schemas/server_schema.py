from pydantic import BaseModel, field_validator


class ServerResponse(BaseModel):
    """Schema for server response data
    This schema is used to structure the response data when querying server information."""
    server_name: str  # The name of the server
    server_ulid: str  # The unique identifier of the server

    model_config = {
        "json_schema_extra": {
            "example": {
                "server_name": "production-server-01",
                "server_ulid": "01HGYX7TBDFRX8HRJC5RF7Z3GY"
            }
        },
        "from_attributes": True
    }


#-----------------------------------------------------------------------


class PostServer(BaseModel):
    """Schema for creating a new server"""
    server_name: str  # The name of the server to be created

    @field_validator("server_name", mode="before")
    def validate_server_name(cls, server_name: str):
        if not server_name or server_name.strip() == "":
            raise ValueError("Server name cannot be empty")
        return server_name
        
    model_config = {
        "json_schema_extra": {
            "example": {
                "server_name": "production-server-01"
            },
            "description": "Data required to register a new server in the system"
        }
    }
#-----------------------------------------------------------------------

class ServerStatusResponse(BaseModel):
    server_ulid: str  # The unique identifier of the server
    server_name: str  # The name of the server
    status: str  # The status of the server (online or offline)
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "server_ulid": "01HGYX7TBDFRX8HRJC5RF7Z3GY",
                "server_name": "production-server-01",
                "status": "online"
            }
        },
        "from_attributes": True
    }