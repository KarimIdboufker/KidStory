# Backend Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./backend /app/backend
COPY ./models /app/models

CMD ["uvicorn", "backend.backend:app", "--host", "0.0.0.0", "--port", "8000"]