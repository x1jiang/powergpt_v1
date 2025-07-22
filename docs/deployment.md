# PowerGPT Deployment Guide

This guide provides comprehensive instructions for deploying PowerGPT on various platforms, from local development to production cloud environments.

## 📋 Table of Contents

1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Dify Platform Integration](#dify-platform-integration)
4. [Cloud Platform Deployment](#cloud-platform-deployment)
5. [Production Configuration](#production-configuration)

## 🏠 Local Development

### Prerequisites

- Python 3.8+
- R 4.0+
- Git

### Step-by-Step Setup

#### 1. Environment Setup

```bash
# Clone the repository
git clone https://github.com/your-username/powergpt.git
cd powergpt

# Create virtual environments
python -m venv frontend-env
python -m venv backend-env

# Activate environments
source frontend-env/bin/activate  # On Windows: frontend-env\Scripts\activate
source backend-env/bin/activate   # On Windows: backend-env\Scripts\activate
```

#### 2. Backend Setup

```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Install R dependencies
R -e "install.packages(c('pwr', 'survival', 'stats'), repos='https://cran.rstudio.com/')"

# Set R library path
export R_LIBS_USER=$(R -e "cat(Sys.getenv('R_LIBS_USER'))")

# Start the backend server
python app.py
```

**Expected Output:**
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:5000
```

#### 3. Frontend Setup

```bash
cd ../frontend

# Install dependencies
pip install -r requirements.txt

# Create environment file
cat > .env << EOF
FEEDBACK_API_KEY=your_dify_api_key_here
STATS_FILE=stats.json
EOF

# Start the frontend server
python main.py
```

**Expected Output:**
```
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

#### 4. Verification

Open your browser and navigate to:
- Frontend: http://localhost:8000
- Backend API: http://localhost:5000/docs

## 🐳 Docker Deployment

### Single Container Deployment

#### 1. Create Docker Compose File

```yaml
# docker-compose.yml
version: '3.8'

services:
  powergpt:
    build: .
    ports:
      - "8000:8000"
      - "5000:5000"
    environment:
      - FEEDBACK_API_KEY=${FEEDBACK_API_KEY}
      - R_LIBS_USER=/usr/local/lib/R/site-library
    volumes:
      - ./data:/app/data
    depends_on:
      - r-base
```

#### 2. Create Dockerfile

```dockerfile
# Dockerfile
FROM python:3.9-slim

# Install R and required packages
RUN apt-get update && apt-get install -y \
    r-base \
    r-base-dev \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    && rm -rf /var/lib/apt/lists/*

# Install R packages
RUN R -e "install.packages(c('pwr', 'survival', 'stats'), repos='https://cran.rstudio.com/')"

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY frontend/requirements.txt backend/requirements.txt ./
RUN pip install -r frontend/requirements.txt -r backend/requirements.txt

# Copy application code
COPY frontend/ ./frontend/
COPY backend/ ./backend/

# Create startup script
RUN echo '#!/bin/bash\n\
cd backend && python app.py &\n\
cd ../frontend && python main.py\n\
wait' > /app/start.sh && chmod +x /app/start.sh

# Expose ports
EXPOSE 8000 5000

# Start application
CMD ["/app/start.sh"]
```

#### 3. Deploy

```bash
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d --build
```

### Microservices Deployment

#### Frontend Service

```yaml
# docker-compose.frontend.yml
version: '3.8'

services:
  frontend:
    build:
      context: .
      dockerfile: frontend/Dockerfile
    ports:
      - "8000:8000"
    environment:
      - FEEDBACK_API_KEY=${FEEDBACK_API_KEY}
      - BACKEND_URL=http://backend:5000
    depends_on:
      - backend
```

#### Backend Service

```yaml
# docker-compose.backend.yml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: backend/Dockerfile
    ports:
      - "5000:5000"
    environment:
      - R_LIBS_USER=/usr/local/lib/R/site-library
    volumes:
      - r-data:/app/data
```

## 🤖 Dify Platform Integration

### Overview

PowerGPT is specifically designed for seamless integration with Dify's AI platform, enabling powerful AI-driven statistical consulting.

### Integration Steps

#### 1. Dify Account Setup

1. Create a Dify account at [dify.ai](https://dify.ai)
2. Set up a new workspace
3. Configure API keys and webhooks

#### 2. Backend API Configuration

```bash
# Deploy backend to cloud platform
# Example: Deploy to Google Cloud Run
gcloud run deploy powergpt-backend \
  --source backend/ \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### 3. Dify Workflow Configuration

1. **Create New Workflow**
   - Name: "PowerGPT Statistical Analysis"
   - Type: Chat Application

2. **Configure System Prompt**
   ```
   You are PowerGPT, an AI-powered statistical consultant. You can perform power analysis for various statistical tests including:
   
   - T-tests (one-sample, two-sample, paired)
   - ANOVA and regression analysis
   - Non-parametric tests
   - Survival analysis
   - Proportion tests
   
   When users ask for power analysis, use the PowerGPT API to calculate sample sizes and provide detailed explanations.
   ```

3. **Add API Integration**
   - Method: POST
   - URL: `https://your-backend-url.com/api/v1/{test_type}`
   - Headers: `Content-Type: application/json`
   - Body: Dynamic based on test type

#### 4. API Endpoint Mapping

| Statistical Test | Dify API Endpoint | Parameters |
|------------------|-------------------|------------|
| Two-Sample T-Test | `/api/v1/two_sample_t_test` | delta, sd, power |
| Log-Rank Test | `/api/v1/log_rank_test` | power, k, pE, pC, RR |
| Chi-Squared Test | `/api/v1/chi_squared_test` | w, df, power |
| ANOVA | `/api/v1/one_way_ANOVA` | k, f, power |

#### 5. Response Processing

Configure Dify to process API responses:

```javascript
// Example response processing
const response = await fetch(apiUrl, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(parameters)
});

const result = await response.json();
return `Sample size required: ${result.result} participants per group.`;
```

### Deployment to Dify

#### 1. Export Configuration

```bash
# Export Dify configuration
dify export --config dify-config.yml --output powergpt-dify.zip
```

#### 2. Import to Dify

1. Go to Dify workspace
2. Import workflow from `powergpt-dify.zip`
3. Configure environment variables
4. Deploy application

#### 3. Testing Integration

```bash
# Test API endpoints
curl -X POST "https://your-backend-url.com/api/v1/two_sample_t_test" \
  -H "Content-Type: application/json" \
  -d '{"delta": 0.5, "sd": 1.0, "power": 0.8}'
```

## ☁️ Cloud Platform Deployment

### Google Cloud Platform

#### 1. Cloud Run Deployment

```bash
# Deploy backend
gcloud run deploy powergpt-backend \
  --source backend/ \
  --platform managed \
  --region us-central1 \
  --memory 2Gi \
  --cpu 2 \
  --allow-unauthenticated

# Deploy frontend
gcloud run deploy powergpt-frontend \
  --source frontend/ \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### 2. Cloud Build Configuration

```yaml
# cloudbuild.yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/powergpt-backend', './backend']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/powergpt-backend']
  - name: 'gcr.io/cloud-builders/gcloud'
    args: ['run', 'deploy', 'powergpt-backend', '--image', 'gcr.io/$PROJECT_ID/powergpt-backend']
```

### AWS Deployment

#### 1. ECS Deployment

```yaml
# task-definition.json
{
  "family": "powergpt",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "containerDefinitions": [
    {
      "name": "powergpt-backend",
      "image": "your-registry/powergpt-backend:latest",
      "portMappings": [{"containerPort": 5000}],
      "environment": [
        {"name": "R_LIBS_USER", "value": "/usr/local/lib/R/site-library"}
      ]
    }
  ]
}
```

#### 2. Deploy with AWS CLI

```bash
# Register task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json

# Create service
aws ecs create-service \
  --cluster your-cluster \
  --service-name powergpt-service \
  --task-definition powergpt:1 \
  --desired-count 2
```

### Azure Deployment

#### 1. Container Instances

```bash
# Deploy to Azure Container Instances
az container create \
  --resource-group powergpt-rg \
  --name powergpt-backend \
  --image your-registry/powergpt-backend:latest \
  --ports 5000 \
  --environment-variables R_LIBS_USER=/usr/local/lib/R/site-library
```

## 🔧 Production Configuration

### Environment Variables

```bash
# Production environment file
FEEDBACK_API_KEY=your_production_dify_key
R_LIBS_USER=/usr/local/lib/R/site-library
LOG_LEVEL=INFO
DATABASE_URL=postgresql://user:pass@host:port/db
REDIS_URL=redis://host:port
```

### Security Configuration

#### 1. API Authentication

```python
# Add to backend/app.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def verify_token(token: str = Depends(security)):
    if not is_valid_token(token.credentials):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    return token.credentials
```

#### 2. CORS Configuration

```python
# Add to frontend/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Monitoring and Logging

#### 1. Health Checks

```python
# Add to backend/app.py
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}
```

#### 2. Logging Configuration

```python
# logging_config.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('powergpt.log'),
        logging.StreamHandler()
    ]
)
```

## 📊 Performance Optimization

### 1. Caching

```python
# Add Redis caching
import redis
from functools import wraps

redis_client = redis.Redis.from_url(REDIS_URL)

def cache_result(expire_time=3600):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            cached_result = redis_client.get(cache_key)
            if cached_result:
                return json.loads(cached_result)
            
            result = await func(*args, **kwargs)
            redis_client.setex(cache_key, expire_time, json.dumps(result))
            return result
        return wrapper
    return decorator
```

### 2. Load Balancing

```nginx
# nginx.conf
upstream powergpt_backend {
    server backend1:5000;
    server backend2:5000;
    server backend3:5000;
}

server {
    listen 80;
    location /api/ {
        proxy_pass http://powergpt_backend;
    }
}
```

## 🔍 Troubleshooting

### Common Issues

#### 1. R Package Installation

```bash
# If R packages fail to install
R -e "install.packages('pwr', repos='https://cran.rstudio.com/', dependencies=TRUE)"
```

#### 2. Port Conflicts

```bash
# Check port usage
lsof -i :5000
lsof -i :8000

# Kill processes if needed
kill -9 <PID>
```

#### 3. Memory Issues

```bash
# Increase memory for R
export R_MAX_MEM_SIZE=4G
```

### Debug Mode

```bash
# Run in debug mode
export LOG_LEVEL=DEBUG
python app.py --debug
```

## 📈 Scaling Considerations

### Horizontal Scaling

- Use load balancers for multiple backend instances
- Implement database connection pooling
- Use Redis for session management

### Vertical Scaling

- Increase CPU and memory allocation
- Optimize R package usage
- Implement result caching

---

For additional support, please refer to our [Support Documentation](support.md) or contact our team. 