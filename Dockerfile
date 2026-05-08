# --- Build stage ---
FROM python:3.12-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Runtime stage ---
FROM python:3.12-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/pytest /usr/local/bin/pytest

# Copy application code
COPY app/ ./app/
COPY tests/ ./tests/
COPY test_selector.py .
COPY requirements.txt .

# Set Python path so imports resolve correctly
ENV PYTHONPATH=/app

# Default command runs the application via a simple health-check import
CMD ["python", "-c", "from app.user import User; from app.payment import Payment; print('App loaded successfully.')"]
