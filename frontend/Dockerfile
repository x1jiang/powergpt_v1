# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY main.py ./
COPY templates/ ./templates/
COPY static/ ./static/
COPY stats.json ./

# Create data directory
RUN mkdir -p /app/data

# Add health check endpoint
RUN echo 'from fastapi import FastAPI\n\
from datetime import datetime\n\
\n\
app = FastAPI()\n\
\n\
@app.get("/health")\n\
async def health_check():\n\
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}\n\
' > health_check.py

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Run the application
CMD ["python", "main.py"]
