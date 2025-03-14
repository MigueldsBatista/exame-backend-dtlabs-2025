FROM python:3.12-slim-bullseye

WORKDIR /app

COPY requirements.txt .
COPY .env .

RUN pip install --no-cache-dir -r requirements.txt


COPY ./app /app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]