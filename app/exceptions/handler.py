from datetime import datetime
from typing import Union, Dict, Any
from fastapi import HTTPException, status, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
from sqlalchemy.exc import DataError, NoReferencedTableError, IntegrityError
from psycopg2.errors import UniqueViolation, ForeignKeyViolation
from exceptions.custom_exceptions import ConflictException, NotFoundException, UnauthorizedException
from jose.exceptions import JWTClaimsError, ExpiredSignatureError, JWTError
import json

from schemas.error_schema import (
    ErrorResponse,
    ValidationErrorResponse,
    NotFoundError,
    ConflictError,
    UnauthorizedError,
    HTTPValidationError
)


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return ErrorResponse.create(
        detail=f"Internal server error: {str(exc)}",
        type="internal_server_error", 
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    ).to_response()


async def request_validation_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return ValidationErrorResponse.from_request_validation_error(
        exc.errors()
    ).to_response()


async def validation_error_handler(request: Request, exc: ValidationError) -> JSONResponse:
    return ValidationErrorResponse.from_request_validation_error(
        exc.errors()
    ).to_response()


async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
    return HTTPValidationError.create(
        detail=f"Validation failed: {str(exc)}",
    ).to_response()


async def data_error_handler(request: Request, exc: DataError) -> JSONResponse:
    return ErrorResponse.create(
        detail=f"Data error: {str(exc)}",
        type="data_error",
        status_code=status.HTTP_400_BAD_REQUEST
    ).to_response()


async def database_error_handler(request: Request, exc: Union[NoReferencedTableError, IntegrityError]) -> JSONResponse:
    return ErrorResponse.create(
        detail=f"Invalid data: {str(exc)}",
        type="database_error",
        status_code=status.HTTP_400_BAD_REQUEST
    ).to_response()


async def conflict_exception_handler(request: Request, exc: ConflictException) -> JSONResponse:
    return ConflictError.create(
        detail=f"Conflict: {str(exc)}",
    ).to_response()


async def unauthorized_exception_handler(request: Request, exc: UnauthorizedException) -> JSONResponse:
    return UnauthorizedError.create(
        detail=f"Unauthorized: {str(exc)}",
    ).to_response({"WWW-Authenticate": "Bearer"})


async def invalid_token_handler(request: Request, exc: Union[JWTClaimsError, ExpiredSignatureError, JWTError]) -> JSONResponse:
    return UnauthorizedError.create(
        detail=f"Token error: {str(exc)}",
    ).to_response({"WWW-Authenticate": "Bearer"})


async def handle_http_exception(request: Request, exc: HTTPException) -> JSONResponse:
    return ErrorResponse.create(
        detail=exc.detail,
        type="http_exception",
        status_code=exc.status_code
    ).to_response()


async def entry_not_found_handler(request: Request, exc: NotFoundException) -> JSONResponse:
    return NotFoundError.create(
        detail=f"Entry not found: {str(exc)}",
    ).to_response()


async def json_error_handler(request: Request, exc: json.JSONDecodeError) -> JSONResponse:
    return ErrorResponse.create(
        detail=f"Invalid JSON: {str(exc)}",
        type="json_decode_error",
        status_code=status.HTTP_400_BAD_REQUEST
    ).to_response()


async def handle_unique_violation(request: Request, exc: UniqueViolation) -> JSONResponse:
    return ConflictError.create(
        detail=f"Conflict: {str(exc)}",
    ).to_response()


async def handle_foreign_key_violation(request: Request, exc: ForeignKeyViolation) -> JSONResponse:
    return ErrorResponse.create(
        detail=f"Invalid data: {str(exc)}",
        type="foreign_key_violation_error",
        status_code=status.HTTP_400_BAD_REQUEST
    ).to_response()


def register_exception_handlers(app: FastAPI):
    # Register the exception handlers
    app.add_exception_handler(RequestValidationError, request_validation_handler)
    app.add_exception_handler(ValidationError, validation_error_handler)
    app.add_exception_handler(ValueError, value_error_handler)
    app.add_exception_handler(DataError, data_error_handler)
    app.add_exception_handler(NoReferencedTableError, database_error_handler)
    app.add_exception_handler(IntegrityError, database_error_handler)
    app.add_exception_handler(ConflictException, conflict_exception_handler)
    app.add_exception_handler(UnauthorizedException, unauthorized_exception_handler)
    app.add_exception_handler(JWTClaimsError, invalid_token_handler)
    app.add_exception_handler(ExpiredSignatureError, invalid_token_handler)
    app.add_exception_handler(JWTError, invalid_token_handler)
    app.add_exception_handler(HTTPException, handle_http_exception)
    app.add_exception_handler(NotFoundException, entry_not_found_handler)
    app.add_exception_handler(json.JSONDecodeError, json_error_handler)
    # This should be the last one
    app.add_exception_handler(Exception, generic_exception_handler)