#!/bin/bash

# PowerGPT Startup Script
echo "🚀 Starting PowerGPT..."

# Set environment variables
export R_LIBS_USER=~/R/library
export PYTHONPATH="${PYTHONPATH}:$(pwd)/backend:$(pwd)/frontend"

# Check if OpenAI API key is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  Warning: OPENAI_API_KEY not set. AI features may not work."
    echo "   Set it with: export OPENAI_API_KEY='your-api-key-here'"
fi

# Kill any existing processes
pkill -f uvicorn 2>/dev/null

# Start backend server
echo "📊 Starting Backend Server (port 5001)..."
cd backend
python -c "import uvicorn; uvicorn.run('app:app', host='0.0.0.0', port=5001, log_level='info')" &
BACKEND_PID=$!

# Wait a moment
sleep 3

# Start frontend server
echo "🌐 Starting Frontend Server (port 8000)..."
cd ../frontend
python -c "import uvicorn; uvicorn.run('main:app', host='0.0.0.0', port=8000, log_level='info')" &
FRONTEND_PID=$!

# Wait for servers to start
sleep 5

# Test the application
echo "🧪 Testing application..."
if curl -s http://localhost:5001/ai/health > /dev/null; then
    echo "✅ Backend is running at http://localhost:5001"
else
    echo "❌ Backend failed to start"
fi

if curl -s http://localhost:8000 > /dev/null; then
    echo "✅ Frontend is running at http://localhost:8000"
else
    echo "❌ Frontend failed to start"
fi

echo ""
echo "🎉 PowerGPT is ready!"
echo "📱 Main Interface: http://localhost:8000"
echo "🤖 AI Chat Interface: http://localhost:8000/ai-chat"
echo "📚 API Documentation: http://localhost:5001/docs"
echo ""
echo "Press Ctrl+C to stop the servers"

# Wait for user to stop
wait 