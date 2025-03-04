FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Default environment variables (can be overridden when running the container)
ENV API_URL=http://host.docker.internal:8000
ENV FREQUENCY=1.0
ENV SERVER_NAME="Auto-Sensor"

CMD ["python", "data_sender.py"]
