@echo off
TITLE AI Analytics Dashboard & Background Agent Fleet
echo ========================================================
echo 🚀 Launching Production/Deployment Fleet Services...
echo ========================================================

echo 1. Starting FastAPI Backend Server on port 8000...
start "FastAPI Backend" cmd /k "cd /d %~dp0\..\backend && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

echo 2. Starting Vite Frontend Dev Server on port 5173...
start "Vite Frontend" cmd /k "cd /d %~dp0\..\frontend && npm run dev -- --host 0.0.0.0"

echo 3. Starting Sprint Watcher Continuous Loop...
start "Sprint Watcher Agent" cmd /k "cd /d %~dp0\.. && python scripts/run_sprint_watcher.py --interval 60"

echo ========================================================
echo 🎉 All 3 services deployed & running autonomously!
echo Backend:  http://localhost:8000 (Swagger docs at /docs)
echo Frontend: http://localhost:5173
echo Watcher:  Monitoring Plane every 60 seconds
echo ========================================================
