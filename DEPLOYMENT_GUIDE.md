# PowerGPT Deployment Guide

## 🚀 Quick Start Deployment

### **Prerequisites**
- Python 3.9+
- R 4.4.2+
- OpenAI API key (for AI features)
- Git

### **Step 1: Clone and Setup**
```bash
# Clone the repository
git clone https://github.com/your-username/powergpt.git
cd powergpt

# Install Python dependencies
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt

# Install R packages
export R_LIBS_USER=~/R/library
mkdir -p ~/R/library
R -e "install.packages(c('pwr', 'survival', 'stats', 'MASS'), repos='https://cran.rstudio.com/', dependencies=TRUE, lib='~/R/library')"
```

### **Step 2: Set Environment Variables**
```bash
# Set R library path
export R_LIBS_USER=~/R/library

# Set Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/backend:$(pwd)/frontend"

# Set OpenAI API key (required for AI features)
export OPENAI_API_KEY="your-openai-api-key-here"
```

### **Step 3: Run PowerGPT**
```bash
# Option A: Use the startup script (recommended)
./start_powergpt.sh

# Option B: Manual start
cd backend && python -c "import uvicorn; uvicorn.run('app:app', host='0.0.0.0', port=5001)" &
cd frontend && python -c "import uvicorn; uvicorn.run('main:app', host='0.0.0.0', port=8000)" &
```

### **Step 4: Access the Application**
- **Main Interface**: http://localhost:8000
- **AI Chat Interface**: http://localhost:8000/ai-chat
- **API Documentation**: http://localhost:5001/docs

---

## 🐳 Docker Deployment

### **Prerequisites**
- Docker
- Docker Compose

### **Step 1: Build and Run with Docker**
```bash
# Build the images
docker-compose build

# Run the services
docker-compose up -d

# Check status
docker-compose ps
```

### **Step 2: Access the Application**
- **Main Interface**: http://localhost:8000
- **AI Chat Interface**: http://localhost:8000/ai-chat
- **API Documentation**: http://localhost:5001/docs

---

## ☁️ Cloud Deployment

### **AWS EC2 Deployment**

#### **Step 1: Launch EC2 Instance**
```bash
# Connect to your EC2 instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3 python3-pip r-base r-base-dev nginx
```

#### **Step 2: Install PowerGPT**
```bash
# Clone repository
git clone https://github.com/your-username/powergpt.git
cd powergpt

# Install Python dependencies
pip3 install -r backend/requirements.txt
pip3 install -r frontend/requirements.txt

# Install R packages
export R_LIBS_USER=~/R/library
mkdir -p ~/R/library
R -e "install.packages(c('pwr', 'survival', 'stats', 'MASS'), repos='https://cran.rstudio.com/', dependencies=TRUE, lib='~/R/library')"
```

#### **Step 3: Configure Environment**
```bash
# Create environment file
cat > .env << EOF
OPENAI_API_KEY=your-openai-api-key-here
R_LIBS_USER=~/R/library
PYTHONPATH=/home/ubuntu/powergpt/backend:/home/ubuntu/powergpt/frontend
EOF

# Source environment
source .env
```

#### **Step 4: Set Up Systemd Services**
```bash
# Create backend service
sudo tee /etc/systemd/system/powergpt-backend.service > /dev/null << EOF
[Unit]
Description=PowerGPT Backend
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/powergpt/backend
Environment=R_LIBS_USER=/home/ubuntu/R/library
Environment=PYTHONPATH=/home/ubuntu/powergpt/backend:/home/ubuntu/powergpt/frontend
Environment=OPENAI_API_KEY=your-openai-api-key-here
ExecStart=/usr/bin/python3 -c "import uvicorn; uvicorn.run('app:app', host='0.0.0.0', port=5001)"
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Create frontend service
sudo tee /etc/systemd/system/powergpt-frontend.service > /dev/null << EOF
[Unit]
Description=PowerGPT Frontend
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/powergpt/frontend
Environment=PYTHONPATH=/home/ubuntu/powergpt/backend:/home/ubuntu/powergpt/frontend
ExecStart=/usr/bin/python3 -c "import uvicorn; uvicorn.run('main:app', host='0.0.0.0', port=8000)"
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Enable and start services
sudo systemctl daemon-reload
sudo systemctl enable powergpt-backend
sudo systemctl enable powergpt-frontend
sudo systemctl start powergpt-backend
sudo systemctl start powergpt-frontend
```

#### **Step 5: Configure Nginx**
```bash
# Create nginx configuration
sudo tee /etc/nginx/sites-available/powergpt > /dev/null << EOF
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /api/ {
        proxy_pass http://localhost:5001;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/powergpt /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### **Step 6: Configure Firewall**
```bash
# Allow HTTP and HTTPS
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow 22
sudo ufw enable
```

### **Google Cloud Platform Deployment**

#### **Step 1: Create VM Instance**
```bash
# Create instance
gcloud compute instances create powergpt \
  --zone=us-central1-a \
  --machine-type=e2-medium \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --tags=http-server,https-server

# Allow HTTP traffic
gcloud compute firewall-rules create allow-http \
  --allow tcp:80 \
  --target-tags=http-server \
  --description="Allow HTTP traffic"
```

#### **Step 2: Install PowerGPT**
```bash
# SSH into instance
gcloud compute ssh powergpt --zone=us-central1-a

# Follow the same installation steps as AWS EC2
```

### **Azure Deployment**

#### **Step 1: Create VM**
```bash
# Create resource group
az group create --name powergpt-rg --location eastus

# Create VM
az vm create \
  --resource-group powergpt-rg \
  --name powergpt-vm \
  --image UbuntuLTS \
  --size Standard_B2s \
  --admin-username azureuser \
  --generate-ssh-keys

# Open port 80
az vm open-port --port 80 --resource-group powergpt-rg --name powergpt-vm
```

#### **Step 2: Install PowerGPT**
```bash
# SSH into VM
ssh azureuser@your-vm-ip

# Follow the same installation steps as AWS EC2
```

---

## 🔧 Production Configuration

### **Environment Variables**
```bash
# Required
OPENAI_API_KEY=your-openai-api-key-here
R_LIBS_USER=/path/to/r/library

# Optional
POWERGPT_BASE_URL=http://your-domain.com
LOG_LEVEL=info
PORT_BACKEND=5001
PORT_FRONTEND=8000
```

### **SSL/HTTPS Setup**
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### **Monitoring and Logging**
```bash
# Check service status
sudo systemctl status powergpt-backend
sudo systemctl status powergpt-frontend

# View logs
sudo journalctl -u powergpt-backend -f
sudo journalctl -u powergpt-frontend -f

# Monitor resources
htop
df -h
free -h
```

---

## 🧪 Testing Deployment

### **Health Checks**
```bash
# Test backend
curl -s http://localhost:5001/ai/health | python3 -m json.tool

# Test frontend
curl -s http://localhost:8000 | head -5

# Test AI functionality
curl -s http://localhost:5001/ai/query -X POST -H "Content-Type: application/json" \
  -d '{"query": "two sample t test with delta 0.5, sd 1.0, power 0.8"}' | python3 -m json.tool
```

### **Validation Script**
```bash
# Run comprehensive tests
cd NATURE_SUBMISSION_PACKAGE
python3 validation_script.py
```

---

## 🚨 Troubleshooting

### **Common Issues**

#### **Port Already in Use**
```bash
# Find process using port
sudo lsof -i :5001
sudo lsof -i :8000

# Kill process
sudo kill -9 <PID>
```

#### **R Package Issues**
```bash
# Reinstall R packages
export R_LIBS_USER=~/R/library
R -e "install.packages(c('pwr', 'survival', 'stats', 'MASS'), repos='https://cran.rstudio.com/', dependencies=TRUE, lib='~/R/library')"
```

#### **OpenAI API Issues**
```bash
# Check API key
echo $OPENAI_API_KEY

# Test API connection
curl -H "Authorization: Bearer $OPENAI_API_KEY" https://api.openai.com/v1/models
```

#### **Permission Issues**
```bash
# Fix file permissions
chmod +x start_powergpt.sh
chmod -R 755 backend/
chmod -R 755 frontend/
```

### **Log Analysis**
```bash
# Check application logs
tail -f backend/logs/app.log
tail -f frontend/logs/app.log

# Check system logs
sudo journalctl -u powergpt-backend --since "1 hour ago"
sudo journalctl -u powergpt-frontend --since "1 hour ago"
```

---

## 📊 Performance Optimization

### **Resource Requirements**
- **Minimum**: 2GB RAM, 1 CPU core
- **Recommended**: 4GB RAM, 2 CPU cores
- **Production**: 8GB RAM, 4 CPU cores

### **Scaling Options**
```bash
# Horizontal scaling with load balancer
# Use multiple instances behind nginx

# Vertical scaling
# Increase VM size for more resources
```

---

## 🔒 Security Considerations

### **Firewall Configuration**
```bash
# Allow only necessary ports
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw deny 5001   # Backend (internal only)
sudo ufw deny 8000   # Frontend (internal only)
```

### **API Key Security**
```bash
# Store API keys securely
echo $OPENAI_API_KEY | sudo tee /etc/environment
# Or use AWS Secrets Manager / Azure Key Vault
```

---

## 📞 Support

### **Documentation**
- **README.md**: Main project documentation
- **NATURE_SUBMISSION_PACKAGE/**: Complete submission package
- **API Documentation**: http://localhost:5001/docs

### **Contact**
- **Issues**: GitHub Issues
- **Documentation**: Project README
- **Validation**: NATURE_SUBMISSION_PACKAGE/validation_script.py

---

## ✅ Deployment Checklist

- [ ] Prerequisites installed (Python, R, dependencies)
- [ ] Environment variables set
- [ ] OpenAI API key configured
- [ ] Services started successfully
- [ ] Health checks passing
- [ ] SSL certificate configured (production)
- [ ] Firewall configured
- [ ] Monitoring set up
- [ ] Backup strategy implemented
- [ ] Documentation updated

**PowerGPT is now deployed and ready for use!** 🎉 