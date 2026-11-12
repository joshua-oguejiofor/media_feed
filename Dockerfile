FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOME=/app

WORKDIR /app

# 1. Install system dependencies & clean apt cache
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. Create non-root system user with /app home directory
RUN adduser --system --home /app joshua

# 3. Install Python dependencies
COPY requirements.txt /app/
RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt

# 4. Copy project files and ensure ownership
COPY --chown=joshua:nogroup . /app/

# 5. Create staticfiles directory and set permissions
RUN mkdir -p /app/staticfiles && chown -R joshua:nogroup /app

# 6. Switch to non-root user
USER joshua

# 7. Collect static files as the joshua user
RUN python manage.py collectstatic --noinput

CMD ["sh", "-c", "gunicorn mediafeed.wsgi:application --bind 0.0.0.0:${PORT:-8000}"]