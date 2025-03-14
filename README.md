# IoT Server Monitoring API

A FastAPI application for managing IoT servers and sensor data, running with PostgreSQL in Docker containers.

![Swagger UI](media/swagger1.png)

## Project Overview

This system enables:
- Registration and management of IoT servers
- Collection of sensor data (temperature, humidity, voltage, current)
- Real-time server health monitoring
- User authentication and authorization
- Data aggregation and analysis

## System Architecture

- **Backend API**: FastAPI application handling requests and business logic
- **Database**: PostgreSQL storing server information and sensor readings
- **API Sender Service**: Utility for simulating IoT device requests

![System Architecture](media/swagger2.png)

## Prerequisites

- Docker installed ([Docker Installation](https://docs.docker.com/get-docker/))
- Docker Compose installed ([Docker Compose Installation](https://docs.docker.com/compose/install/))

## Environment Configuration

1. **Configure environment variables**:

   Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```

   Edit the `.env` file with your settings:
   ```properties
   # Database credentials
   DB_USER=postgres
   DB_PASSWORD=your_secure_password
   DB_NAME=dtlabs
   SECRET_KEY=your_very_long_and_secure_secret_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   ENV=Docker
   DB_HOST=db
   ```
   
   **Important**: Replace default values with secure ones in production environments.

## How to Run the Project

1. **Clone the repository**:
    ```bash
    git clone https://github.com/MigueldsBatista/exame-backend-dtlabs-2025.git
    cd exame-backend-dtlabs-2025
    ```

2. **Build and run the containers**:
    ```bash
    docker-compose up --build
    ```

    This will:
    - Build the FastAPI application image
    - Start the PostgreSQL database
    - Run the FastAPI application

3. **Access the application**:
    - API at [http://localhost:8000](http://localhost:8000)
    - Interactive API documentation at [http://localhost:8000/docs](http://localhost:8000/docs)


## API Router code sample -> [CLICK HERE](/app/routes/reading_routes.py)


![Code Sample](media/code_sample.png)

## Test code sample -> [CLICK HERE](app/tests/test_reading.py)

![Code Sample](media/code_sample_test.png)


### Running the API Sender:

## Useful Commands

| Command | Description |
|---------|-------------|
| `docker-compose ps` | Check running containers |
| `docker-compose down` | Stop containers |
| `docker-compose down -v` | Remove containers and volumes |
| `docker-compose logs app` | View application logs |
| `docker-compose logs db` | View database logs |
| `docker-compose exec app bash` | Access the application container shell |
| `docker-compose exec db psql -U my_user -d my_database` | Access the database shell |

## Resolving Port Conflicts

If you already have PostgreSQL running on your machine using port 5432:

### Option 1: Stop local PostgreSQL

**Linux**:
```bash
sudo systemctl stop postgresql
```

**macOS** (Homebrew):
```bash
brew services stop postgresql
```

**Windows**:
Stop the PostgreSQL service through "Services Manager"

### Option 2: Change the port in docker-compose.yml

```yaml
ports:
  - "5433:5432"
```

## Verify database connection
```bash
docker-compose exec app psql -h db -U postgres -d dtlabs
```

## How to run tests inside the container
```bash
docker-compose exec app bash
```

### Run all tests
```bash
pytest
```

### Run tests with verbose output
```bash
pytest -v
```

### Run tests in a specific file
```bash
pytest app/tests/test_specific_file.py
```

