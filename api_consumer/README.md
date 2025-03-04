# API Consumer Service for Server Metrics

This service sends simulated server metrics to the DTLabs API at configurable frequencies ranging from 1 to 10 Hz.

## Features

- Configurable frequency of data sending (1-10 Hz)
- Automatic server registration (optional)
- Randomized server metrics generation (CPU, memory, disk, network)
- Easy configuration via environment variables or command-line arguments

## Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Running Directly

You can run the service directly using Python:

```bash
python data_sender.py --api-url http://localhost:8000 --frequency 1.0 --server-name "MyServer" --auth-token "your-auth-token"
```

### Command-line Arguments

- `--api-url`: Base URL of the API (default: http://localhost:8000)
- `--frequency`: Frequency in Hz (1-10) (default: 1.0)
- `--server-id`: Server ID if already registered (optional)
- `--server-name`: Server name for registration (required if server-id not provided)
- `--auth-token`: Authentication token (required for server registration)

### Environment Variables

All command-line arguments can be set using environment variables:

- `API_URL`: Base URL of the API
- `FREQUENCY`: Frequency in Hz (1-10)
- `SERVER_ID`: Server ID if already registered
- `SERVER_NAME`: Server name for registration
- `AUTH_TOKEN`: Authentication token

## Using Docker

Build the Docker image:

```bash
docker build -t readings-sender .
```

Run the container:

```bash
docker run -e API_URL=http://your-api-url:8000 -e FREQUENCY=2.0 -e SERVER_NAME="Docker-Server" -e AUTH_TOKEN="your-auth-token" readings-sender
```

## Integration with Main Application

You can add this service to your existing docker-compose.yml:

```yaml
services:
  # ... existing services
  
  metrics-sender:
    build:
      context: ./api_consumer
      dockerfile: Dockerfile
    container_name: metrics-sender
    restart: always
    environment:
      - API_URL=http://app:8000
      - FREQUENCY=2.0
      - SERVER_NAME=MetricsServer
      - AUTH_TOKEN=your-auth-token
    networks:
      - dtlabs-network
    depends_on:
      - app
```
