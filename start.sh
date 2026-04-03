#!/bin/bash

echo "========================================="
echo "Starting OMS Application"
echo "========================================="

if ! command -v python3 &> /dev/null
then
    echo "Error: Python3 is not installed. Please install Python3 to continue."
    exit 1
fi

if ! command -v node &> /dev/null
then
    echo "Error: Node.js is not installed. Please install Node.js to continue."
    exit 1
fi

echo ""
echo "Setting up Backend..."
cd api

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing backend dependencies..."
pip install -q -r requirements.txt

cd ..

echo ""
echo "Setting up Frontend..."
cd client

if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
else
    echo "Frontend dependencies already installed"
fi

cd ..

echo ""
echo "========================================="
echo "Starting Servers..."
echo "========================================="
echo "Backend will run on: http://localhost:8000"
echo "Frontend will run on: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both servers"
echo "========================================="

export PYTHONPATH="${PYTHONPATH}:$(pwd)"

cd api
source venv/bin/activate
cd ..

uvicorn api.app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

cd client
npm start &
FRONTEND_PID=$!

wait $BACKEND_PID $FRONTEND_PID
