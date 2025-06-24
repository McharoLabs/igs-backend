FROM python:3.12-alpine

# Install system dependencies
RUN apk update && \
    apk add --no-cache \
    postgresql-dev \
    gcc \
    python3-dev \
    musl-dev \
    libffi-dev \
    jpeg-dev \
    zlib-dev \
    gettext

# Create user and set permissions
RUN adduser -D appuser
WORKDIR /app

# Create logs directory and set permissions
RUN mkdir -p /app/logs && chown -R appuser:appuser /app/logs

# Ensure /app is owned by appuser (including logs)
RUN chown -R appuser:appuser /app

# Copy and install requirements
COPY --chown=appuser:appuser requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "university_api.wsgi"]
