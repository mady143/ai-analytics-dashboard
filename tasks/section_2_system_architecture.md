# 🖥️ Section 2: System Architecture & Data Flow

This document details the core architecture, framework dependencies, and data flow pipelines of the **AI Analytics Dashboard**.

---

## 1. Stack Architecture
- **Frontend**: React + Vite (ESBuild), TailwindCSS / Vanilla CSS, Lucide Icons, Recharts, Framer Motion.
- **Backend API**: Python 3.10 FastAPI (`backend/main.py`), Uvicorn on `http://localhost:8000`.
- **Database Layer**: PostgreSQL (`sptnintgdb`), Oracle DEV/F1, and CSV Mock Fallback.
- **Plane PM Integration**: Plane REST API (`plane_agent.py`) synchronized with `SprintWatcherAgent`.

---

## 2. Dynamic Data Flow Rules
1. **Header Date & Database Selectors**: Header controls (`#global-date-picker`, `#global-db-selector`) propagate parameters across Dashboard API calls (`/api/charts/kpi`, `/api/charts/bar`, `/api/charts/scatter`, `/api/warehouse/statistics`).
2. **Date-Agnostic Copilot Rule**: AI Copilot (`/api/analytics/ai-copilot`) MUST query the full dataset across ALL dates to answer user questions, bypassing the header date filter.
3. **Single Warehouse Filtering Rule**: When a warehouse filter is active, Bar Chart and Scatter Plot display data ONLY for that selected warehouse facility.
