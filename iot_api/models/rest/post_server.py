from pydantic import BaseModel

class PostServer(BaseModel):
    server_name: str