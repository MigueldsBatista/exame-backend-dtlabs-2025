from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict, Union
from datetime import datetime
from fastapi.responses import JSONResponse

"""
Module for error response schemas and generation

This module contains Pydantic models for error responses and methods to generate
consistent error responses throughout the API.
"""

class ErrorResponse(BaseModel):
    """Base schema for error responses"""
    type: str = Field(..., description="Error type identifier")
    status_code: int = Field(..., description="HTTP status code")
    detail: str = Field(..., description="Detailed error message")
    timestamp: str = datetime.now().isoformat()

    @classmethod
    def create(cls, detail: str, **kwargs) -> "ErrorResponse":
        """Create an instance of the error response"""
        return cls(
            detail=detail,
            **kwargs
        )
    
    def to_response(self, headers: Optional[Dict[str, str]] = None) -> JSONResponse:
        """Convert to a JSONResponse"""
        return JSONResponse(
            status_code=self.status_code,
            content=self.model_dump(),
            headers=headers
        )



class ValidationErrorResponse(BaseModel):
    """Schema for validation error responses with detailed information"""
    type: str = "validation_error"
    status_code: int = 422
    detail: str = Field(..., description="Validation error message with all errors combined")
    timestamp: str = datetime.now().isoformat()

    @classmethod
    def from_request_validation_error(cls, errors) -> "ValidationErrorResponse":
        """Create from RequestValidationError with single string format
        
        Combines all error messages and locations into a single string
        """
        formatted_errors = []
        for err in errors:
            # Format the location path
            loc_path = " → ".join(str(loc_part) for loc_part in err["loc"])
            # Combine message and location
            formatted_error = f"{err['msg']}: {loc_path}"
            formatted_errors.append(formatted_error)
            
        # Join all errors with semicolons
        combined_error = "; ".join(formatted_errors)
            
        return cls(
            detail=combined_error
        )
    
    def to_response(self, headers: Optional[Dict[str, str]] = None) -> JSONResponse:
        """Convert to a JSONResponse"""
        return JSONResponse(
            status_code=self.status_code,
            content=self.model_dump(),
            headers=headers
        )


class HTTPValidationError(ErrorResponse):
    """Schema for HTTP validation error responses"""
    type: str = "validation_error"
    status_code: int = 422
    detail: str = "Validation failed"

class NotFoundError(ErrorResponse):
    """Schema for not found error responses"""
    type: str = "not_found_error"
    status_code: int = 404
    detail: str = "Resource not found"


class ConflictError(ErrorResponse):
    """Schema for conflict error responses"""
    type: str = "conflict_error"
    status_code: int = 409
    detail: str ="Conflict error message"

class UnauthorizedError(ErrorResponse):
    """Schema for unauthorized error responses"""
    type: str = "unauthorized_error"
    status_code: int = 401
    detail: str = "Unauthorized access"

class ValidationErrorDetail(ValidationErrorResponse):
    type: str = "validation_error"
    status_code: int = 422
    detail: str ="Validation error message with all errors combined"


class InvalidJsonError(ErrorResponse):
    type: str = "invalid_json_error"
    status_code: int = 400
    detail: str = "Invalid JSON format"