#!/usr/bin/env bash

set -e

# Install backend dependencies
echo "[SETUP] Installing backend dependencies..."
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd ..

# Install frontend dependencies
echo "[SETUP] Installing frontend dependencies..."
cd frontend
npm install
cd ..

# Start backend (in background)
echo "[START] Starting backend..."
cd backend
source .venv/bin/activate
PYTHONPATH=src python3 main.py &
BACKEND_PID=$!
cd ..

# Start frontend (in background)
echo "[START] Starting frontend..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..



echo "[INFO] Stop this script with Ctrl+C. The servers are running in the background."
wait $FRONTEND_PID $BACKEND_PID 