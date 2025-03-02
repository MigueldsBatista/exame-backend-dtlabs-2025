from datetime import datetime
from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import DataError, NoReferencedTableError, IntegrityError
from fastapi import FastAPI

import logging
logger = logging.getLogger(__name__)

def error_response_builder(status_code, message) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={
        "status_code": status_code,
        "detail": message,
        "timestamp": datetime.now().isoformat()
    })


async def value_error_handler(request, exc):
    return error_response_builder(status.HTTP_400_BAD_REQUEST, f"Validation failed {str(exc)}")

async def data_error_handler(request, exc):
    return error_response_builder(status.HTTP_400_BAD_REQUEST, f"Data error {str(exc)}")


async def database_error_handler(request, exc):
    return error_response_builder(status.HTTP_400_BAD_REQUEST, f"Invalid data {str(exc)}")

async def generic_exception_handler(request, exc):
    return error_response_builder(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Internal server error {str(exc)}")

def register_exception_handlers(app : FastAPI):
    app.exception_handler(ValueError)(value_error_handler)
    app.exception_handler(DataError)(data_error_handler)
    app.exception_handler(NoReferencedTableError)(database_error_handler)
    app.exception_handler(IntegrityError)(database_error_handler)
    app.exception_handler(Exception)(generic_exception_handler)
