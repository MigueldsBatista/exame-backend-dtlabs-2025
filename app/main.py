from routes import reading_routes, auth_routes, server_routes
from core.database import create_tables

import subprocess
from fastapi import FastAPI
from exceptions.handler import (
    register_exception_handlers,
)
from middlewares import register_middlewares

app = FastAPI(title="Server Monitoring API")

register_middlewares(app)

app.include_router(reading_routes.router)
app.include_router(auth_routes.router)
app.include_router(server_routes.router)

register_exception_handlers(app)

# Initialize database tables at startup
create_tables()


if __name__ == "__main__":
    import os
    os.chdir("app")
    subprocess.run(["uvicorn", "main:app", "--reload"])

