# Stage 1: Builder
FROM python:3.14-slim AS builder

WORKDIR /app

# Install poetry and its export plugin
RUN pip install --no-cache-dir poetry==2.2.1 && poetry self add poetry-plugin-export

# Copy poetry dependency files
COPY pyproject.toml poetry.lock* ./

# Export to requirements to build pure python wheels
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Compile wheels for all dependencies
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Stage 2: Runtime
FROM python:3.14-slim

# Install system dependencies (OpenMP for LightGBM)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m -r appuser
WORKDIR /app

# Copy compiled wheels from builder and install them (efficient cache layer)
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache /wheels/*

# Copy application source code
COPY . .

# Set ownership to non-root user
RUN chown -R appuser:appuser /app
USER appuser

# Expose port (internal docker network only)
EXPOSE 8000

# Start FastAPI application
CMD ["uvicorn", "src.presentation.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
