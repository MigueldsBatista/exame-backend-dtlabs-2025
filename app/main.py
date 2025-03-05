from fastapi import FastAPI
from routes import auth_routes, server_routes, reading_routes
import uvicorn
from exceptions.handler import register_exception_handlers
from middlewares import register_middlewares
from core.database import create_tables
# Create FastAPI app with improved OpenAPI documentation
app = FastAPI(
    title="IoT Server Monitoring API",
    description="""
This API manages an IoT infrastructure where on-premise servers collect and transmit 

This API manages an IoT infrastructure where on-premise servers collect and transmit 
sensor data to a central database.

## System Architecture

- **Servers**: On-premise devices installed at client locations
- **Sensors**: Each server supports up to 4 different types of sensors
- **Data Collection**: Servers send data at frequencies between 1-10 Hz

## Sensor Types

Each server can have at most one of each sensor type:

- **Temperature Sensor**: Measures temperature in Celsius
- **Humidity Sensor**: Measures humidity as percentage (0-100%)
- **Voltage Sensor**: Measures electrical voltage in Volts
- **Current Sensor**: Measures electrical current in Amperes

## API Features

- User authentication and authorization
- Server registration and management
- Sensor data submission and querying
- Real-time server health monitoring
    """,
    version="1.0.0",
    # Configure docs URLs
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "Miguel Batista",
        "email": "miguelsbatista0610@gmail.com",
    }

)

create_tables()
register_exception_handlers(app)
register_middlewares(app)

# Include routers with better tag descriptions
app.include_router(auth_routes.router)
app.include_router(server_routes.router)
app.include_router(reading_routes.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
