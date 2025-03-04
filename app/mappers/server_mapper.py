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
    def from_post_to_entity(data: PostServer, user_id: str) -> Server:
        return Server(
            server_name=data.server_name,
            created_by=user_id
        )


    @staticmethod
    def from_aggregate_health_data_to_status_response(data: tuple) -> ServerStatusResponse:
        return ServerStatusResponse(
            server_ulid=data[0],
            status=data[1],
            server_name=data[2]
        )
    
    @staticmethod
    def from_aggregate_health_data_to_status_responses(data: list[tuple]) -> list[ServerStatusResponse]:
        return [ServerMapper.from_aggregate_health_data_to_status_response(server) for server in data]
    
    @staticmethod
    def create_offline_status_response(server_entity: Server) -> ServerStatusResponse:

        return ServerStatusResponse(
            server_ulid=server_entity.id,
            server_name=server_entity.server_name,
            status="offline"
        )
