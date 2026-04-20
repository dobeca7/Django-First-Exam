Dockerfile

# Base image

FROM python:3.14

# Create app directory

WORKDIR /app

# Install system dependencies

RUN apt-get update && apt-get install -y \

build-essential \

libpq-dev \

&& rm -rf /var/lib/apt/lists/*

# Copy requirements separately for caching

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install gunicorn psycopg2

# Copy project files

COPY . .

# Expose port for internal container use

EXPOSE 8000

# Gunicorn command

CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "future_stars.wsgi:application"]