from fastapi import status, Depends, APIRouter
from exceptions.custom_exceptions import ConflictException, NotFoundException
from dependencies import get_current_user_dependency, get_server_service
from schemas.user_schema import UserResponse
from schemas.server_schema import PostServer
from services.server_service import ServerService
from mappers.server_mapper import ServerMapper

router = APIRouter()

@router.post("/servers", status_code=status.HTTP_201_CREATED)
async def post_server(
    server: PostServer,
    current_user: UserResponse = Depends(get_current_user_dependency),
    server_service: ServerService = Depends(get_server_service)
):
    if server_service.find_by_name(server.server_name):
        raise ConflictException("Server already exists")

    server_entity = ServerMapper.from_post_to_entity(server, current_user.id)
    saved_server = server_service.save(server_entity)
    server_response = ServerMapper.from_entity_to_response(saved_server)

    return server_response

@router.get("/health/all", status_code=status.HTTP_200_OK)
async def get_health(
        current_user: UserResponse = Depends(get_current_user_dependency),
        server_service: ServerService = Depends(get_server_service)
        ):
    
    all_server_status = server_service.get_server_health_all(user_id=current_user.id)
    
    if not all_server_status:
        return []
    
    server_status_responses = ServerMapper.from_aggregate_health_data_to_status_responses(all_server_status)

    return server_status_responses

@router.get("/health/{server_id}", status_code=status.HTTP_200_OK)
async def get_server_health(
        server_id: str,
        current_user: UserResponse = Depends(get_current_user_dependency),
        server_service: ServerService = Depends(get_server_service),
        ):

        # Get the server entity and its health status from the service
        if not server_service.find_by_id(server_id):
            raise NotFoundException(f"Server with id {server_id} not found")
        
        health_data = server_service.get_server_health_by_id(server_id)
        
        # Generate the appropriate response using the mapper
        if not health_data or health_data is []:
            # For servers with no readings, create an offline status response
            server_entity = server_service.find_by_id(server_id)
            return ServerMapper.create_offline_status_response(server_entity)
        
            # For servers with readings, map the health data to a response
        return ServerMapper.from_aggregate_health_data_to_status_response(health_data[0])

