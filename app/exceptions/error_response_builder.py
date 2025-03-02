from datetime import datetime

from fastapi.responses import JSONResponse


def error_response_builder(status_code, message) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={
        "status_code": status_code,
        "detail": message,
        "timestamp": datetime.now().isoformat()
    })