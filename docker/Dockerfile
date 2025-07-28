FROM python:3.11-slim

WORKDIR /app

COPY app/requirements.txt .

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY app /app

CMD ["uvicorn", "app.asgi:application", "--host", "0.0.0.0", "--port", "8000", "--lifespan", "on"]

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/healthz || exit 1