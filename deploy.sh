#!/bin/bash

# PowerGPT Deployment Script
echo "🚀 PowerGPT Deployment Script"
echo "=============================="

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "❌ Please don't run as root"
    exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command_exists python3; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

if ! command_exists R; then
    echo "❌ R is required but not installed"
    exit 1
fi

if ! command_exists pip; then
    echo "❌ pip is required but not installed"
    exit 1
fi

echo "✅ Prerequisites check passed"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt

# Install R packages
echo "📦 Installing R packages..."
export R_LIBS_USER=~/R/library
mkdir -p ~/R/library
R -e "install.packages(c('pwr', 'survival', 'stats', 'MASS'), repos='https://cran.rstudio.com/', dependencies=TRUE, lib='~/R/library')"

# Set environment variables
echo "🔧 Setting environment variables..."
export R_LIBS_USER=~/R/library
export PYTHONPATH="${PYTHONPATH}:$(pwd)/backend:$(pwd)/frontend)"

# Check OpenAI API key
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  Warning: OPENAI_API_KEY not set"
    echo "   Set it with: export OPENAI_API_KEY='your-api-key-here'"
    echo "   AI features may not work without this key"
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cat > .env << EOF
# PowerGPT Environment Variables
OPENAI_API_KEY=${OPENAI_API_KEY:-your-api-key-here}
R_LIBS_USER=~/R/library
PYTHONPATH=${PYTHONPATH}
POWERGPT_BASE_URL=http://localhost:5001
EOF
    echo "✅ .env file created"
fi

# Make startup script executable
chmod +x start_powergpt.sh

# Test the installation
echo "🧪 Testing installation..."
cd backend
python3 -c "import app; print('✅ Backend imports successfully')" || {
    echo "❌ Backend test failed"
    exit 1
}
cd ../frontend
python3 -c "import main; print('✅ Frontend imports successfully')" || {
    echo "❌ Frontend test failed"
    exit 1
}
cd ..

echo ""
echo "🎉 Deployment completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Set your OpenAI API key:"
echo "   export OPENAI_API_KEY='your-api-key-here'"
echo ""
echo "2. Start PowerGPT:"
echo "   ./start_powergpt.sh"
echo ""
echo "3. Access the application:"
echo "   Main Interface: http://localhost:8000"
echo "   AI Chat: http://localhost:8000/ai-chat"
echo "   API Docs: http://localhost:5001/docs"
echo ""
echo "📚 For more information:"
echo "   - Quick Guide: QUICK_DEPLOYMENT.md"
echo "   - Full Guide: DEPLOYMENT_GUIDE.md"
echo "   - Documentation: README.md"
echo ""
echo "🚀 PowerGPT is ready to deploy!" 