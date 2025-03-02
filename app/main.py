from routes import reading_routes, auth_routes, server_routes

import subprocess
from fastapi import FastAPI
from exceptions.handler import (
    register_exception_handlers,
)

app = FastAPI()

app.include_router(reading_routes.router)
app.include_router(auth_routes.router, prefix="/auth")
app.include_router(server_routes.router)

register_exception_handlers(app)

if __name__ == "__main__":
    import os
    os.chdir("app")
    subprocess.run(["uvicorn", "main:app", "--reload"])

