# 📌 TASK 9 — Continuous Application Server Uptime (`#application-uptime`)

## 🖥️ Server Configurations & Endpoints
- **Backend API Server:**
  - **Command:** `python -m uvicorn main:app --host 127.0.0.1 --port 8000` (inside `backend/`)
  - **URL:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
  - **Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
  - **Health Check:** `GET /api/health`
- **Frontend Dashboard Dev Server:**
  - **Command:** `npm run dev` (inside `frontend/`)
  - **URL:** [http://localhost:5173](http://localhost:5173)

---

## 🎯 Sub-Task Breakdown

### Sub-Task 9.1: 🚀 Backend FastAPI Server Continuous Background Execution
- **Behavior:** Runs continuously in the background on port `8000`. Exposes REST API endpoints for KPI cards, bar charts, scatter plots, correlation heatmaps, and PostgreSQL warehouse sales analytics.

### Sub-Task 9.2: 💻 Frontend Vite Dev Server Continuous Background Execution
- **Behavior:** Runs continuously in the background on port `5173`. Serves the React + Vite dashboard UI with real-time parameter controls, KPI cards, charts, and warehouse data table.

### Sub-Task 9.3: 🩺 Continuous Uptime Monitoring & Auto-Restart Directive
- **Rule:** The USER will NOT start servers manually. The system MUST keep both frontend and backend servers continuously active. If either server goes offline or crashes, the agent MUST automatically relaunch it in background mode immediately.
