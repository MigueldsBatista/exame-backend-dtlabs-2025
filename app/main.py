from routes import reading_routes, auth_routes, server_routes
from core.database import get_db, create_tables

import subprocess
from fastapi import FastAPI
from exceptions.handler import (
    register_exception_handlers,
)

app = FastAPI(title="Server Monitoring API")

app.include_router(reading_routes.router)
app.include_router(auth_routes.router)
app.include_router(server_routes.router)

register_exception_handlers(app)

# Initialize database tables at startup
create_tables()

@app.get("/")
def read_root():
    return {"message": "App is running"}

if __name__ == "__main__":
    import os
    os.chdir("app")
    subprocess.run(["uvicorn", "main:app", "--reload"])

