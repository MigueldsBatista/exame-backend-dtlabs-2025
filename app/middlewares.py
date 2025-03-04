from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, status, FastAPI
from schemas.error_schema import ErrorResponse
import json
import time
from collections import defaultdict, deque
import os

class JSONErrorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method in ["POST", "PUT", "PATCH"]:
            content_type = request.headers.get("content-type", "")
            if "application/json" in content_type:
                try:
                    await request.json()
                except json.JSONDecodeError as e:
                    error = ErrorResponse.create(
                        detail=f"Invalid JSON: {str(e)}",
                        type="json_decode_error",
                        status_code=status.HTTP_400_BAD_REQUEST
                    )
                    return error.to_response()
                
        return await call_next(request)

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_rate_hz=10.0, window_size=1.0):
        super().__init__(app)
        self.max_rate_hz = max_rate_hz
        self.window_size = window_size 
        self.request_history = defaultdict(lambda: deque())
        self.disabled = os.getenv("DISABLE_RATE_LIMIT", "false").lower() == "true"
        
    def _get_client_id(self, request):
        device_id = request.headers.get("X-Device-ID")
        if device_id:
            return device_id

        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.client.host if request.client else "unknown"
    
    def _is_rate_limited(self, client_id):
        now = time.time()
        client_history = self.request_history[client_id]
        
        # Remove requests outside of the current window
        while client_history and client_history[0] < now - self.window_size:
            client_history.popleft()# Remove the oldest request
        
        client_history.append(now)
        
        current_rate = len(client_history) / self.window_size
        
        return current_rate > self.max_rate_hz
    
    async def dispatch(self, request: Request, call_next):
        if self.disabled:
            return await call_next(request)
        client_id = self._get_client_id(request)
        
        if self._is_rate_limited(client_id):
            error = ErrorResponse.create(
                detail=f"Rate limit exceeded. Maximum allowed rate is {self.max_rate_hz}Hz.",
                type="rate_limit_exceeded",
                status_code=status.HTTP_429_TOO_MANY_REQUESTS
            )
            return error.to_response()
        
        return await call_next(request)

def register_middlewares(app: FastAPI):
    app.add_middleware(JSONErrorMiddleware)
    app.add_middleware(RateLimitMiddleware, max_rate_hz=12, window_size=1.2)# plus 20% to avoid burst rates