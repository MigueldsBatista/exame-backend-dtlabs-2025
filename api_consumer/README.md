# Data Sender Utility

This is a mockup service that simulates servers sending sensor data readings to the API at configurable frequencies. It can create multiple virtual servers and continuously send randomized sensor data. Its used to test frequency limit rates, and how te api handles various requests por second.

## Features

- Automatically registers users and servers
- Sends randomized temperature, voltage, current, and humidity readings
- Configurable sending frequency (1-10 Hz)
- Supports multiple virtual servers
- Docker ready

## Requirements

- Python 3.11 or higher
- Required Python packages (see `requirements.txt`):
  - aiohttp
  - schedule

## Installation

### Local Installation

1. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### Docker Installation

Build the Docker image:
```
docker build -t data-sender .
```

## Usage

### Command Line Arguments

The application accepts the following command line arguments:

| Argument | Description | Default |
|----------|-------------|---------|
| `--api-url` | Base URL of the API | http://host.docker.internal:8000 |
| `--frequency` | Frequency in Hz (1-10) | 1.0 |
| `--num-servers` | Number of servers to create | 1 |
| `--username` | Username for authentication | admin |
| `--password` | Password for authentication | admin |

NOTE: The API only allows up to 10hz frequencies from one server, more than that it will return code 429

### Environment Variables

The application also accepts the following environment variables (which override command line arguments):

| Variable | Description | Default |
|----------|-------------|---------|
| `API_URL` | Base URL of the API | http://host.docker.internal:8000 |
| `FREQUENCY` | Frequency in Hz (1-10) | 1.0 |
| `NUM_SERVERS` | Number of servers to create | 1 |
| `USERNAME` | Username for authentication | admin |
| `PASSWORD` | Password for authentication | admin |
| `SERVER_NAME` | Custom server name | Auto-Sensor |

### Running Locally

Run the application with default settings:
```
python data_sender.py
```

Run with custom settings:
```
python data_sender.py --api-url http://host.docker.internal:8000 --frequency 5.0 --num-servers 3 --username user1 --password pass123
```

### Running with Docker

Run with default settings:
```
docker run -d data-sender
```

Run with environment variables:
```
docker run -d \
  -e API_URL=http://host.docker.internal:8000 \
  -e FREQUENCY=5.0 \
  -e NUM_SERVERS=3 \
  -e USERNAME=admin \
  -e PASSWORD=admin \
  data-sender
```

## How It Works

1. The utility first attempts to register the user; if the user exists, it proceeds to login
2. After successful authentication, it registers the specified number of servers
3. For each registered server, it generates random sensor readings at the specified frequency
4. Readings are sent to the API endpoint (`/data`) continuously until the application is stopped

## Sensor Data Format

Each reading includes:

```json
{
  "server_ulid": "server_id_here",
  "timestamp": "2023-01-01T12:00:00.000000",
  "temperature": 75.42,  // Optional, can be null
  "voltage": 110.25,     // Optional, can be null
  "current": 5.67,       // Optional, can be null
  "humidity": 45.89      // Optional, can be null
}
```

## Troubleshooting

- If you see authentication errors, check that the API is running and accessible
- If server registration fails, ensure the server name is unique
- For connection issues, verify the API_URL is correct and the API is running

## License

This project is licensed under the MIT License - see the LICENSE file for details.