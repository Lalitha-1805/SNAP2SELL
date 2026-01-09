#!/bin/bash

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  AgriSmart - AI-Powered Agriculture E-Commerce Platform     ║"
echo "║                   Startup Script                             ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "✗ Python 3 not found. Please install Python 3.10+"
    exit 1
fi

# Create virtual environment if not exists
if [ ! -d "backend/venv" ]; then
    echo "Creating Python virtual environment..."
    cd backend
    python3 -m venv venv
    cd ..
fi

# Activate virtual environment
echo "Activating Python virtual environment..."
source backend/venv/bin/activate

# Install backend dependencies
echo "Installing backend dependencies..."
cd backend
pip install -r requirements.txt > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "✗ Failed to install backend dependencies"
    exit 1
fi
cd ..

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "✗ Node.js not found. Please install Node.js 16+"
    exit 1
fi

# Install frontend dependencies
echo "Installing frontend dependencies..."
cd frontend
if [ ! -d "node_modules" ]; then
    npm install > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "✗ Failed to install frontend dependencies"
        exit 1
    fi
fi
cd ..

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  ✓ Setup Complete! Starting servers...                       ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "Starting Backend Server (Port 5000)..."
echo "Starting Frontend Server (Port 5173)..."
echo ""
echo "Open in your browser:"
echo "- Frontend: http://localhost:5173"
echo "- Backend API: http://localhost:5000/api/info"
echo ""

# Start backend in background
cd backend
python app.py &
BACKEND_PID=$!
cd ..

# Wait a bit
sleep 3

# Start frontend
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✓ Both servers started successfully!"
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "Press Ctrl+C to stop the servers."
echo ""

# Wait for both processes
wait
