from models.reading import Reading
from models.server import Server
from schemas.server_schema import ServerResponse, PostServer

class ServerMapper:

    @staticmethod
    def from_entity_to_response(entity: Server) -> ServerResponse:
        return ServerResponse(
            server_name=entity.server_name,
            server_ulid=entity.id
        )

    @staticmethod
    def from_post_to_entity(data: PostServer) -> ServerResponse:
        return Server(
            server_name=data.server_name,
        )

