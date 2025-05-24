#!/usr/bin/env bash

set -e

# Funktion für Logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Funktion für Fehlerbehandlung
handle_error() {
    log "ERROR: Installation failed at step: $1"
    log "Error details: $2"
    exit 1
}

# Install backend dependencies
log "Starting backend setup..."
cd backend || handle_error "cd backend" "Could not change to backend directory"

log "Creating Python virtual environment..."
python3 -m venv .venv || handle_error "venv creation" "Failed to create virtual environment"

log "Activating virtual environment..."
source .venv/bin/activate || handle_error "venv activation" "Failed to activate virtual environment"

log "System information:"
log "Python version: $(python3 --version)"
log "Pip version: $(pip --version)"
log "Memory info: $(free -h)"
log "Disk space: $(df -h .)"

log "Upgrading pip..."
pip install --upgrade pip || handle_error "pip upgrade" "Failed to upgrade pip"

log "Installing opencv-python-headless (pre-compiled version)..."
pip install --no-cache-dir opencv-python-headless || handle_error "opencv install" "Failed to install opencv"

log "Installing other requirements..."
pip install -v --no-cache-dir -r requirements.txt || handle_error "requirements install" "Failed to install requirements"

cd ..

# Install frontend dependencies
log "Starting frontend setup..."
cd frontend || handle_error "cd frontend" "Could not change to frontend directory"

log "Node information:"
log "Node version: $(node --version)"
log "NPM version: $(npm --version)"

log "Installing npm packages..."
npm install --verbose --no-audit --no-fund || handle_error "npm install" "Failed to install npm packages"

cd ..

# Start backend (in background)
log "Starting backend server..."
cd backend
source .venv/bin/activate
PYTHONPATH=src python3 main.py &
BACKEND_PID=$!
cd ..

# Start frontend (in background)
log "Starting frontend server..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

log "Setup completed successfully!"
log "Backend PID: $BACKEND_PID"
log "Frontend PID: $FRONTEND_PID"
log "Stop this script with Ctrl+C. The servers are running in the background."

wait $FRONTEND_PID $BACKEND_PID 