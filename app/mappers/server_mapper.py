from models.reading import Reading
from models.server import Server
from schemas.server_schema import ServerResponse, PostServer, ServerStatusResponse

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

    @staticmethod
    def from_tuple_to_response(data: tuple) -> ServerResponse:
        return ServerStatusResponse(
            server_ulid=data[0],
            status=data[1],
            server_name=data[2]
        )
    
    @staticmethod
    def from_tuples_to_responses(data: list[tuple]) -> list:
        return [ServerMapper.from_tuple_to_response(server) for server in data]