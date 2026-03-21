# Dockerfile
FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY . .

# Create directory for logs
RUN mkdir -p /app/logs

# Expose ports for all services
EXPOSE 8000 8001 8002 8003 8501

# Copy entrypoint script
COPY run_servers.sh /run_servers.sh
RUN chmod +x /entrypoint.sh

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Use entrypoint script to start all services
ENTRYPOINT ["/run_servers.sh"]
