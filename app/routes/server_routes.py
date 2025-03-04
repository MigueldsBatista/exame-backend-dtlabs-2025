from fastapi import status, Depends, APIRouter
from schemas.error_schema import ConflictError, UnauthorizedError, ValidationErrorDetail, NotFoundError
from exceptions.custom_exceptions import ConflictException, NotFoundException
from dependencies import get_current_user_dependency, get_server_service
from schemas.user_schema import UserResponse
from schemas.server_schema import PostServer, ServerStatusResponse, ServerResponse
from services.server_service import ServerService
from mappers.server_mapper import ServerMapper

router = APIRouter(
    tags=["Server Management"],
)

@router.post(
    "/servers", 
    status_code=status.HTTP_201_CREATED,
    summary="Register a new server",
    description="""
    Creates a new server in the system linked to the current user,
    
    - server_name: A unique name to identify the server

    
    """,
    response_description="The created server details",
    response_model=ServerResponse,
        responses={
        401: {"model": UnauthorizedError, "description": "Authentication required"},
        409 :{"model": ConflictError, "description": "Conflict error"},
        422 :{"model": ValidationErrorDetail, "description": "Validation error"}

    }
)
async def create_server(
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

@router.get(
    "/health/all", 
    status_code=status.HTTP_200_OK,
    summary="Get health status of all servers",
    description="""
    Retrieve the health status for all servers associated with the current user.
    
    The health status includes:
    - Server identifier
    - Server name
    - Current status (online/offline)
    
    A server is considered online if it has sent data within the last 10 seconds.
    """,
    response_description="List of servers with their health status",
    response_model=list[ServerStatusResponse],
    responses={
        401: {"model": UnauthorizedError, "description": "Authentication required"},        
    }
)
async def get_all_server_health(
        current_user: UserResponse = Depends(get_current_user_dependency),
        server_service: ServerService = Depends(get_server_service)
        ):

    all_server_status = server_service.get_server_health_all(user_id=current_user.id)
    
    if not all_server_status:
        return []
    
    server_status_responses = ServerMapper.from_aggregate_health_data_to_status_responses(all_server_status)

    return server_status_responses

@router.get(
    "/health/{server_id}", 
    status_code=status.HTTP_200_OK,
    summary="Get health status of a specific server",
    description="""
        Retrieve the health status for a specific server.
        
        Parameters:
        - server_id: The unique identifier (ULID) of the server
        
        The health status includes:
        - Server identifier
        - Server name
        - Current status (online/offline)
        
        A server is considered online if it has sent data within the last 10 seconds.
        """,
    response_description="Server health status details",
    responses={
        401: {"model": UnauthorizedError, "description": "Authentication required"},
        422 :{"model": ValidationErrorDetail, "description": "Validation error"}
        
    },
    response_model=ServerStatusResponse
)
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

