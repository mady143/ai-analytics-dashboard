#!/usr/bin/env bash
# AI Analytics Dashboard — Autonomous Agent & Deployment Fleet (Linux/macOS)

set -e

APP_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$APP_ROOT"

echo "========================================================================="
echo "⚡ AI Analytics Dashboard — Autonomous Deployment Launcher (Linux/macOS)"
echo "========================================================================="

echo "[1/5] 📦 Installing Python Dependencies..."
pip install -r requirements.txt

echo "[2/5] 🟢 Installing Node.js Frontend Dependencies..."
cd "$APP_ROOT/frontend"
if [ ! -d "node_modules" ]; then
    npm install
fi
cd "$APP_ROOT"

echo "[3/5] 🎭 Installing Playwright Browser Binaries..."
python3 -m playwright install chromium

echo "[4/5] 🔀 Synchronizing Git Repository..."
git pull origin main || true

echo "[5/5] 🚀 Launching All Background Agent Fleet Services..."

# Run FastAPI backend in background
cd "$APP_ROOT/backend"
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Run Vite frontend in background
cd "$APP_ROOT/frontend"
npm run dev -- --host 0.0.0.0 &
FRONTEND_PID=$!

# Run Sprint Watcher agent loop in background
cd "$APP_ROOT"
python3 scripts/run_sprint_watcher.py --interval 60 &
WATCHER_PID=$!

# Run Orchestrator agent
python3 agents/orchestrator_agent.py &
ORCH_PID=$!

echo "========================================================================="
echo "🎉 Autonomous Agent Fleet Fully Deployed & Operational!"
echo "Backend PID:  $BACKEND_PID (http://localhost:8000)"
echo "Frontend PID: $FRONTEND_PID (http://localhost:5173)"
echo "Watcher PID:  $WATCHER_PID (60s poll interval)"
echo "========================================================================="

wait
