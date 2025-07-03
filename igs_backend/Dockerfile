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
RUN chown appuser:appuser /app

RUN mkdir -p /app/logs && chown appuser:appuser /app/logs
RUN mkdir -p /app/staticfiles && chown appuser:appuser /app/staticfiles
RUN mkdir -p /app/media && chown appuser:appuser /app/media

# Copy and install requirements
COPY --chown=appuser:appuser requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Your CMD
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "igs_backend.wsgi"]