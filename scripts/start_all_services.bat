@echo off
TITLE AI Analytics Dashboard — Autonomous Agent & Deployment Fleet
echo =========================================================================
echo ⚡ AI Analytics Dashboard — Comprehensive Autonomous Deployment Launcher
echo =========================================================================

set APP_ROOT=%~dp0..
cd /d "%APP_ROOT%"

echo.
echo [STEP 1/5] 📦 Checking & Installing Python Dependencies...
pip install -r requirements.txt

echo.
echo [STEP 2/5] 🟢 Checking & Installing Node.js Frontend Dependencies...
cd /d "%APP_ROOT%\frontend"
if not exist "node_modules" (
    echo Installing node_modules...
    npm install
) else (
    echo node_modules verified!
)
cd /d "%APP_ROOT%"

echo.
echo [STEP 3/5] 🎭 Installing Playwright E2E Browser Testing Binaries...
python -m playwright install chromium

echo.
echo [STEP 4/5] 🔀 Synchronizing Git Repository...
git pull origin main

echo.
echo [STEP 5/5] 🚀 Launching All Autonomous Fleet Services & Agent Loops...

echo 1. Launching FastAPI Backend API Server (Port 8000)...
start "FastAPI Backend Server" cmd /k "cd /d %APP_ROOT%\backend && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

echo 2. Launching Vite Frontend Dev Server (Port 5173)...
start "Vite Frontend Dev Server" cmd /k "cd /d %APP_ROOT%\frontend && npm run dev -- --host 0.0.0.0"

echo 3. Launching Sprint Watcher Continuous Agent Loop (60s Interval)...
start "Sprint Watcher Agent" cmd /k "cd /d %APP_ROOT% && python scripts/run_sprint_watcher.py --interval 60"

echo 4. Launching Orchestrator Agent State Coordinator...
start "Orchestrator Agent" cmd /k "cd /d %APP_ROOT% && python agents/orchestrator_agent.py"

echo =========================================================================
echo 🎉 Autonomous Agent Fleet Fully Deployed & Operational!
echo -------------------------------------------------------------------------
echo 🌐 Frontend UI:     http://localhost:5173
echo ⚙️ Backend API:     http://localhost:8000 (Swagger docs: http://localhost:8000/docs)
echo 🤖 Active Agents:   Sprint Watcher (60s), Builder Agent, Tester Agent, Orchestrator
echo 🔄 Auto-Git Push:   Enabled background auto-commit & push to origin/main
echo =========================================================================
pause
