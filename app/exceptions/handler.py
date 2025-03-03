from datetime import datetime
from typing import Union
from fastapi import HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.exc import DataError, NoReferencedTableError, IntegrityError
from fastapi import FastAPI
from exceptions.custom import ConflictException, NotFoundException, UnauthorizedException
from jose.exceptions import JWTClaimsError, ExpiredSignatureError, JWTError
import json 

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

def error_response_builder(status_code, message, headers=None) -> JSONResponse:
    return JSONResponse(
        headers=headers,
        status_code=status_code, content={
        "status_code": status_code,
        "detail": message,
        "timestamp": datetime.now().isoformat()
    })

class JSONErrorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Check if it's a method that typically has a body
        if request.method in ["POST", "PUT", "PATCH"]:
            # Only try to parse JSON if the content type indicates JSON
            content_type = request.headers.get("content-type", "")
            if "application/json" in content_type:
                try:
                    await request.json()
                except json.JSONDecodeError as e:
                    # Return custom error response
                    return error_response_builder(status.HTTP_400_BAD_REQUEST, f"Invalid JSON: {str(e)}")
        
        # If no error or not applicable, proceed with the request
        return await call_next(request)

async def generic_exception_handler(request: Request, exc: Exception):
    return error_response_builder(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Internal server error: {str(exc)}")

async def request_validation_handler(request: Request, exc: RequestValidationError):
    error_messages = ", ".join(err["msg"] for err in exc.errors())
    return error_response_builder(status.HTTP_422_UNPROCESSABLE_ENTITY, error_messages)

async def validation_error_handler(request: Request, exc: ValidationError):
    error_messages = ", ".join(err["msg"] for err in exc.errors())
    return error_response_builder(status.HTTP_400_BAD_REQUEST, f"Validation failed: {error_messages}")


async def value_error_handler(request: Request, exc: ValueError):
    # Handle ValueError directly without trying to access as a dictionary
    return error_response_builder(status.HTTP_400_BAD_REQUEST, f"Validation failed: {str(exc)}")

async def data_error_handler(request: Request, exc: DataError):
    return error_response_builder(status.HTTP_400_BAD_REQUEST, f"Data error: {str(exc)}")

async def database_error_handler(request: Request, exc: Union[NoReferencedTableError, IntegrityError]):
    return error_response_builder(status.HTTP_400_BAD_REQUEST, f"Invalid data: {str(exc)}")


async def conflict_exception_handler(request: Request, exc: ConflictException):
    return error_response_builder(status.HTTP_409_CONFLICT, f"Conflict: {str(exc)}")

async def unauthorized_exception_handler(request: Request, exc: UnauthorizedException):
    return error_response_builder(status.HTTP_401_UNAUTHORIZED, f"Unauthorized: {str(exc)}", {"WWW-Authenticate": "Bearer"})

async def invalid_token_handler(request: Request, exc: Union[JWTClaimsError, ExpiredSignatureError, JWTError]):
    return error_response_builder(status.HTTP_401_UNAUTHORIZED, f"Token error: {str(exc)}", {"WWW-Authenticate": "Bearer"})

async def handle_http_exception(request: Request, exc: HTTPException):
    return error_response_builder(exc.status_code, exc.detail)


async def entry_not_found_handler(request: Request, exc: NotFoundException):
    return error_response_builder(status.HTTP_404_NOT_FOUND, f"Entry not found: {str(exc)}")

async def json_error_handler(request: Request, exc: json.JSONDecodeError):
    return error_response_builder(status.HTTP_400_BAD_REQUEST, f"Invalid JSON: {str(exc)}")

def register_exception_handlers(app : FastAPI):

    # Register the middleware first
    app.add_middleware(JSONErrorMiddleware)
    
    app.exception_handler(json.JSONDecodeError)(json_error_handler)
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