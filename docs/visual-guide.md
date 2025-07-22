# PowerGPT Visual Deployment Guide

This visual guide provides step-by-step instructions with screenshots for deploying PowerGPT on various platforms.

## 📋 Table of Contents

1. [Local Development Setup](#local-development-setup)
2. [Docker Deployment](#docker-deployment)
3. [Dify Platform Integration](#dify-platform-integration)
4. [Cloud Platform Deployment](#cloud-platform-deployment)
5. [Troubleshooting](#troubleshooting)

## 🏠 Local Development Setup

### Step 1: Repository Structure

```
PowerGPT/
├── frontend/          # FastAPI web interface
│   ├── main.py       # Main application
│   ├── templates/    # HTML templates
│   ├── static/       # CSS, JS, images
│   └── requirements.txt
├── backend/          # Statistical API
│   ├── app.py        # API endpoints
│   ├── *.R          # R statistical scripts
│   └── requirements.txt
├── docs/            # Documentation
├── deployment/      # Docker configs
└── README.md
```

### Step 2: Environment Setup

**Terminal Commands:**
```bash
# Clone repository
git clone https://github.com/your-username/powergpt.git
cd powergpt

# Create virtual environments
python -m venv frontend-env
python -m venv backend-env

# Activate environments
source frontend-env/bin/activate  # Linux/Mac
# or
frontend-env\Scripts\activate     # Windows
```

**Expected Output:**
```
(backend-env) user@machine:~/powergpt$ 
```

### Step 3: Backend Setup

**Install Dependencies:**
```bash
cd backend
pip install -r requirements.txt

# Install R packages
R -e "install.packages(c('pwr', 'survival', 'stats'), repos='https://cran.rstudio.com/')"
```

**Start Backend Server:**
```bash
python app.py
```

**Expected Output:**
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:5000
```

**Backend API Documentation:**
- Open browser to: http://localhost:5000/docs
- You should see the FastAPI interactive documentation

### Step 4: Frontend Setup

**Install Dependencies:**
```bash
cd ../frontend
pip install -r requirements.txt
```

**Create Environment File:**
```bash
cat > .env << EOF
FEEDBACK_API_KEY=your_dify_api_key_here
STATS_FILE=stats.json
EOF
```

**Start Frontend Server:**
```bash
python main.py
```

**Expected Output:**
```
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Frontend Interface:**
- Open browser to: http://localhost:8000
- You should see the PowerGPT main page

## 🐳 Docker Deployment

### Step 1: Docker Installation

**Verify Docker Installation:**
```bash
docker --version
docker-compose --version
```

**Expected Output:**
```
Docker version 20.10.21, build baeda1f
docker-compose version 1.29.2, build 5becea4c
```

### Step 2: Build and Run

**Navigate to Deployment Directory:**
```bash
cd deployment
```

**Build and Start Services:**
```bash
docker-compose up --build
```

**Expected Output:**
```
Creating powergpt_backend_1 ... done
Creating powergpt_frontend_1 ... done
Creating powergpt_redis_1 ... done
Creating powergpt_nginx_1 ... done
Attaching to powergpt_backend_1, powergpt_frontend_1, powergpt_redis_1, powergpt_nginx_1
```

### Step 3: Verify Deployment

**Check Service Status:**
```bash
docker-compose ps
```

**Expected Output:**
```
Name                    Command               State           Ports         
--------------------------------------------------------------------------------
powergpt_backend_1      python app.py                        Up      0.0.0.0:5000->5000/tcp
powergpt_frontend_1     python main.py                       Up      0.0.0.0:8000->8000/tcp
powergpt_nginx_1        /docker-entrypoint.sh nginx -g ...   Up      0.0.0.0:443->443/tcp, 0.0.0.0:80->80/tcp
powergpt_redis_1        docker-entrypoint.sh redis-se ...   Up      0.0.0.0:6379->6379/tcp
```

**Access Services:**
- Frontend: http://localhost:8000
- Backend API: http://localhost:5000/docs
- Nginx Proxy: http://localhost (port 80)

### Step 4: Production Deployment

**Environment Configuration:**
```bash
# Create production environment file
cat > .env.prod << EOF
FEEDBACK_API_KEY=your_production_dify_key
R_LIBS_USER=/usr/local/lib/R/site-library
LOG_LEVEL=INFO
DATABASE_URL=postgresql://user:pass@host:port/db
REDIS_URL=redis://host:port
EOF
```

**Deploy with Production Config:**
```bash
docker-compose -f docker-compose.yml --env-file .env.prod up -d
```

## 🤖 Dify Platform Integration

### Step 1: Dify Account Setup

1. **Visit Dify Platform:**
   - Go to [dify.ai](https://dify.ai)
   - Click "Sign Up" or "Get Started"

2. **Create Workspace:**
   - Click "Create Workspace"
   - Enter workspace name: "PowerGPT Statistical Consultant"
   - Choose workspace type: "Personal" or "Team"

3. **Generate API Key:**
   - Go to Settings → API Keys
   - Click "Generate New Key"
   - Copy the API key for PowerGPT configuration

### Step 2: Create Dify Application

1. **Create New App:**
   - Click "Create App" button
   - Select "Chat Application"
   - Name: "PowerGPT Statistical Consultant"

2. **Configure System Prompt:**
   ```
   You are PowerGPT, an AI-powered statistical consultant specializing in power analysis.
   
   Your capabilities include:
   - T-tests (one-sample, two-sample, paired)
   - ANOVA and regression analysis
   - Non-parametric tests
   - Survival analysis
   - Proportion tests
   - Correlation analysis
   
   When users ask for power analysis:
   1. Identify the appropriate statistical test
   2. Extract relevant parameters
   3. Call the PowerGPT API
   4. Provide detailed interpretation
   5. Include educational context
   ```

### Step 3: Configure API Integration

1. **Add API Tool:**
   - Go to Tools → API
   - Click "Add API"
   - Configure settings as shown below

2. **API Configuration:**
   ```yaml
   Name: PowerGPT Statistical API
   Base URL: https://your-powergpt-backend-url.com
   Authentication: None (for development)
   ```

3. **Add Endpoints:**
   
   **Two-Sample T-Test:**
   ```yaml
   Method: POST
   Path: /api/v1/two_sample_t_test
   Headers: 
     Content-Type: application/json
   Body:
     {
       "delta": {{delta}},
       "sd": {{sd}},
       "power": {{power}}
     }
   ```

### Step 4: Create Workflow

1. **Add Workflow Nodes:**
   
   **User Input Node:**
   - Type: User Input
   - Variable: `user_query`
   
   **Parameter Extraction Node:**
   - Type: LLM
   - Prompt: Extract statistical parameters from user query
   
   **API Call Node:**
   - Type: API
   - API: PowerGPT Statistical API
   - Endpoint: Dynamic based on test type
   
   **Response Generation Node:**
   - Type: LLM
   - Prompt: Generate comprehensive response

2. **Connect Workflow:**
   ```
   User Input → Parameter Extraction → API Call → Response Generation → Output
   ```

### Step 5: Test Integration

1. **Deploy Application:**
   - Click "Deploy" button
   - Wait for deployment to complete

2. **Test with Sample Queries:**
   ```
   "I need sample size for a two-group comparison with 0.5 difference, 
   SD of 1.0, and 80% power"
   
   "What sample size do I need for a chi-squared test with effect size 
   0.3, 1 degree of freedom, and 90% power?"
   ```

## ☁️ Cloud Platform Deployment

### Google Cloud Platform

1. **Install Google Cloud CLI:**
   ```bash
   # Download and install gcloud CLI
   curl https://sdk.cloud.google.com | bash
   exec -l $SHELL
   gcloud init
   ```

2. **Deploy Backend:**
   ```bash
   cd backend
   gcloud run deploy powergpt-backend \
     --source . \
     --platform managed \
     --region us-central1 \
     --memory 2Gi \
     --cpu 2 \
     --allow-unauthenticated
   ```

3. **Deploy Frontend:**
   ```bash
   cd ../frontend
   gcloud run deploy powergpt-frontend \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

### AWS Deployment

1. **Install AWS CLI:**
   ```bash
   pip install awscli
   aws configure
   ```

2. **Deploy with ECS:**
   ```bash
   # Create ECS cluster
   aws ecs create-cluster --cluster-name powergpt-cluster
   
   # Deploy services
   aws ecs create-service \
     --cluster powergpt-cluster \
     --service-name powergpt-backend \
     --task-definition powergpt-backend:1 \
     --desired-count 2
   ```

### Azure Deployment

1. **Install Azure CLI:**
   ```bash
   curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
   az login
   ```

2. **Deploy to Container Instances:**
   ```bash
   az container create \
     --resource-group powergpt-rg \
     --name powergpt-backend \
     --image your-registry/powergpt-backend:latest \
     --ports 5000 \
     --environment-variables R_LIBS_USER=/usr/local/lib/R/site-library
   ```

## 🔍 Troubleshooting

### Common Issues and Solutions

#### 1. R Package Installation Failures

**Problem:** R packages fail to install during Docker build

**Solution:**
```bash
# Update Dockerfile with proper R installation
RUN apt-get update && apt-get install -y \
    r-base \
    r-base-dev \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    && rm -rf /var/lib/apt/lists/*

# Install R packages with error handling
RUN R -e "install.packages(c('pwr', 'survival', 'stats'), repos='https://cran.rstudio.com/', dependencies=TRUE)"
```

#### 2. Port Conflicts

**Problem:** Services fail to start due to port conflicts

**Solution:**
```bash
# Check port usage
lsof -i :5000
lsof -i :8000

# Kill conflicting processes
sudo kill -9 <PID>

# Or use different ports
docker-compose up -p 5001:5000 -p 8001:8000
```

#### 3. Memory Issues

**Problem:** R computations fail due to insufficient memory

**Solution:**
```bash
# Increase Docker memory allocation
docker run --memory=4g powergpt-backend

# Or set R memory limit
export R_MAX_MEM_SIZE=4G
```

#### 4. API Connection Errors

**Problem:** Dify cannot connect to PowerGPT API

**Solution:**
```bash
# Verify API is accessible
curl -X POST "https://your-backend-url.com/api/v1/two_sample_t_test" \
  -H "Content-Type: application/json" \
  -d '{"delta": 0.5, "sd": 1.0, "power": 0.8}'

# Check CORS configuration
# Add to backend/app.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Debug Mode

**Enable Debug Logging:**
```bash
# Set debug environment variable
export LOG_LEVEL=DEBUG

# Run with debug output
python app.py --debug
```

**Check Service Logs:**
```bash
# Docker logs
docker-compose logs powergpt-backend
docker-compose logs powergpt-frontend

# Real-time logs
docker-compose logs -f powergpt-backend
```

### Performance Monitoring

**Monitor Resource Usage:**
```bash
# Docker stats
docker stats

# System resources
htop
free -h
df -h
```

**API Performance:**
```bash
# Test API response time
time curl -X POST "http://localhost:5000/api/v1/two_sample_t_test" \
  -H "Content-Type: application/json" \
  -d '{"delta": 0.5, "sd": 1.0, "power": 0.8}'
```

## 📊 Success Metrics

### Deployment Verification Checklist

- [ ] Backend API responds to health check
- [ ] Frontend loads without errors
- [ ] Statistical calculations return correct results
- [ ] Dify integration works end-to-end
- [ ] Docker containers are healthy
- [ ] Logs show no errors
- [ ] Performance meets requirements

### Performance Benchmarks

**Expected Response Times:**
- API health check: < 100ms
- Statistical calculation: < 2s
- Frontend page load: < 3s
- Dify integration: < 5s

**Resource Usage:**
- Backend memory: < 2GB
- Frontend memory: < 1GB
- CPU usage: < 50% under normal load

---

For additional support, please refer to our [Support Documentation](support.md) or contact our team. 