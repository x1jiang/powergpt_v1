# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV R_LIBS_USER=/usr/local/lib/R/site-library
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    r-base \
    r-base-dev \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    libgdal-dev \
    libproj-dev \
    libgeos-dev \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install R packages
RUN R -e "install.packages(c('pwr', 'survival', 'stats', 'MASS'), repos='https://cran.rstudio.com/', dependencies=TRUE)"

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy R scripts
COPY *.R ./

# Copy Python application
COPY app.py ./

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
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Run the application
CMD ["python", "app.py"]
