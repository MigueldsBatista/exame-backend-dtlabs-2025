from datetime import datetime
from typing import Union
from fastapi import HTTPException, status, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.exc import DataError, NoReferencedTableError, IntegrityError
from psycopg2.errors import UniqueViolation, ForeignKeyViolation
from exceptions.custom_exceptions import ConflictException, NotFoundException, UnauthorizedException
from jose.exceptions import JWTClaimsError, ExpiredSignatureError, JWTError
import json


def error_response_builder(status_code, message, type, headers=None) -> JSONResponse:
    return JSONResponse(
        headers=headers,
        status_code=status_code, content={
        "type": type,
        "status_code": status_code,
        "detail": message,
        "timestamp": datetime.now().isoformat()
    })


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return error_response_builder(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Internal server error: {str(exc)}", "internal_server_error")

async def request_validation_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    error_messages = ", ".join(f"{err['msg']}: {err['loc']}" for err in exc.errors())
    return error_response_builder(status.HTTP_422_UNPROCESSABLE_ENTITY, error_messages, "request_validation_error")

async def validation_error_handler(request: Request, exc: ValidationError) -> JSONResponse:
    error_messages = ", ".join(f"{err['msg']}: {err['loc']}" for err in exc.errors())
    return error_response_builder(status.HTTP_422_UNPROCESSABLE_ENTITY, f"Validation failed: {error_messages}", "validation_error")

async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
    # Handle ValueError directly without trying to access as a dictionary
    return error_response_builder(status.HTTP_400_BAD_REQUEST, f"Validation failed: {str(exc)}", "value_error")

async def data_error_handler(request: Request, exc: DataError) -> JSONResponse:
    return error_response_builder(status.HTTP_400_BAD_REQUEST, f"Data error: {str(exc)}", "data_error")

async def database_error_handler(request: Request, exc: Union[NoReferencedTableError, IntegrityError]) -> JSONResponse:
    return error_response_builder(status.HTTP_400_BAD_REQUEST, f"Invalid data: {str(exc)}", "database_error")

async def conflict_exception_handler(request: Request, exc: ConflictException) -> JSONResponse:
    return error_response_builder(status.HTTP_409_CONFLICT, f"Conflict: {str(exc)}", "conflict_error")

async def unauthorized_exception_handler(request: Request, exc: UnauthorizedException) -> JSONResponse:
    return error_response_builder(status.HTTP_401_UNAUTHORIZED, f"Unauthorized: {str(exc)}", "unauthorized_error", {"WWW-Authenticate": "Bearer"})

async def invalid_token_handler(request: Request, exc: Union[JWTClaimsError, ExpiredSignatureError, JWTError]) -> JSONResponse:
    return error_response_builder(status.HTTP_401_UNAUTHORIZED, f"Token error: {str(exc)}", "token_error", {"WWW-Authenticate": "Bearer"})

async def handle_http_exception(request: Request, exc: HTTPException) -> JSONResponse:
    return error_response_builder(exc.status_code, exc.detail, "http_exception")

async def entry_not_found_handler(request: Request, exc: NotFoundException) -> JSONResponse:
    return error_response_builder(status.HTTP_404_NOT_FOUND, f"Entry not found: {str(exc)}", "not_found_error")

async def json_error_handler(request: Request, exc: json.JSONDecodeError) -> JSONResponse:
    return error_response_builder(status.HTTP_400_BAD_REQUEST, f"Invalid JSON: {str(exc)}", "json_decode_error")

async def handle_unique_violation(request: Request, exc: UniqueViolation) -> JSONResponse:
    return error_response_builder(status.HTTP_409_CONFLICT, f"Conflict: {str(exc)}", "unique_violation_error")

async def handle_foreign_key_violation(request: Request, exc: ForeignKeyViolation) -> JSONResponse:
    return error_response_builder(status.HTTP_400_BAD_REQUEST, f"Invalid data: {str(exc)}", "foreign_key_violation_error")

def register_exception_handlers(app : FastAPI):

    app.exception_handler(RequestValidationError)(request_validation_handler)
    app.exception_handler(ValidationError)(validation_error_handler)
    app.exception_handler(ValueError)(value_error_handler)
    app.exception_handler(DataError)(data_error_handler)
    app.exception_handler(NoReferencedTableError)(database_error_handler)
    app.exception_handler(IntegrityError)(database_error_handler)
    app.exception_handler(ConflictException)(conflict_exception_handler)
    app.exception_handler(UnauthorizedException)(unauthorized_exception_handler)

    app.exception_handler(JWTClaimsError)(invalid_token_handler)
    app.exception_handler(ExpiredSignatureError)(invalid_token_handler)
    app.exception_handler(JWTError)(invalid_token_handler)
        
    app.exception_handler(HTTPException)(handle_http_exception)
    
    app.exception_handler(NotFoundException)(entry_not_found_handler)
    #Needs to be the last one
    app.exception_handler(Exception)(generic_exception_handler)