# PowerGPT Quick Deployment Guide

## 🚀 **5-Minute Setup**

### **1. Install Dependencies**
```bash
# Python packages
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt

# R packages
export R_LIBS_USER=~/R/library
mkdir -p ~/R/library
R -e "install.packages(c('pwr', 'survival', 'stats', 'MASS'), repos='https://cran.rstudio.com/', dependencies=TRUE, lib='~/R/library')"
```

### **2. Set Environment**
```bash
export R_LIBS_USER=~/R/library
export PYTHONPATH="${PYTHONPATH}:$(pwd)/backend:$(pwd)/frontend"
export OPENAI_API_KEY="your-api-key-here"
```

### **3. Run PowerGPT**
```bash
# Option A: Startup script (recommended)
./start_powergpt.sh

# Option B: Manual start
cd backend && python -c "import uvicorn; uvicorn.run('app:app', host='0.0.0.0', port=5001)" &
cd frontend && python -c "import uvicorn; uvicorn.run('main:app', host='0.0.0.0', port=8000)" &
```

### **4. Access**
- **Main**: http://localhost:8000
- **AI Chat**: http://localhost:8000/ai-chat
- **API Docs**: http://localhost:5001/docs

---

## 🐳 **Docker Quick Start**
```bash
docker-compose up -d
```

---

## ☁️ **Cloud Quick Deploy**

### **AWS EC2**
```bash
# Launch Ubuntu 20.04 LTS instance
# SSH and run:
sudo apt update && sudo apt install -y python3 python3-pip r-base r-base-dev nginx
git clone https://github.com/your-username/powergpt.git
cd powergpt
# Follow steps 1-3 above
```

### **Google Cloud**
```bash
# Create VM instance
gcloud compute instances create powergpt --zone=us-central1-a --machine-type=e2-medium --image-family=ubuntu-2004-lts
# SSH and follow AWS steps
```

---

## 🧪 **Quick Test**
```bash
# Health check
curl -s http://localhost:5001/ai/health | python3 -m json.tool

# AI test
curl -s http://localhost:5001/ai/query -X POST -H "Content-Type: application/json" \
  -d '{"query": "two sample t test with delta 0.5, sd 1.0, power 0.8"}' | python3 -m json.tool
```

---

## 🚨 **Quick Fixes**

### **Port Issues**
```bash
pkill -f uvicorn
./start_powergpt.sh
```

### **R Issues**
```bash
export R_LIBS_USER=~/R/library
R -e "install.packages(c('pwr', 'survival', 'stats', 'MASS'), repos='https://cran.rstudio.com/', dependencies=TRUE, lib='~/R/library')"
```

### **API Issues**
```bash
export OPENAI_API_KEY="your-api-key-here"
```

---

## 📞 **Need Help?**
- **Full Guide**: `DEPLOYMENT_GUIDE.md`
- **Documentation**: `README.md`
- **Validation**: `NATURE_SUBMISSION_PACKAGE/validation_script.py`

**PowerGPT is ready in 5 minutes!** ⚡ 