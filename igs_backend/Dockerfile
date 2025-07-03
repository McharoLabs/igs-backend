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
# Ensure /app is owned by appuser
RUN chown appuser:appuser /app

# This is crucial for your Django app to write logs
RUN mkdir -p /app/logs && chown appuser:appuser /app/logs
RUN mkdir -p /app/staticfiles && chown appuser:appuser /app/staticfiles # Already handled by collectstatic, but good practice
RUN mkdir -p /app/media && chown appuser:appuser /app/media # Already handled by collectstatic, but good practice


# Copy and install requirements
COPY --chown=appuser:appuser requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "university_api.wsgi"]