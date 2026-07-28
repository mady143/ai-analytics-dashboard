# 🚀 AI Analytics Dashboard

> An agentic, AI-powered Data Analytics Dashboard built with **FastAPI + React**, managed and tested by **Autonomous AI agents**.

---

## ✨ Features

- 📊 **Interactive Dashboard** — KPI cards, bar charts, scatter plots, heatmaps, and warehouse analytics
- 🏭 **Warehouse Sales & Invoice Analytics** — Real-time PostgreSQL (`sptn_sales_data`) item & invoice statistics
- 🗄️ **Multi-Target DB Architecture** — Strict parameter-driven querying across `pg_prod`, `pg_dev`, `oracle_dev`, `oracle_f1`, `oracle_prod`
- 🤖 **Continuous Autonomous Agent Network** — 5 background agents (`Sprint Watcher`, `Orchestrator`, `Builder`, `Tester`, `Git Agent`) running continuously
- 💾 **Persistent Memory** — All agent conversations stored in `memory/` as JSONL
- 🏃 **Sprint Watcher** — Continuous 60s background polling of Plane tasks and comment updates
- 🧪 **Auto Testing** — pytest unit tests + Playwright browser automation tests
- 🔀 **Git Automation** — Automatic pull, stage, commit, PR creation, and push to GitHub
- 🔌 **MCP Integration** — Plane, GitHub, Memory, Browser MCP servers

---

## 🗂️ Project Structure

```
ai_analytics_dashboard/
├── agents/          # AI agents (Orchestrator, Builder, Tester, Plane, Git, Memory, Sprint Watcher)
├── backend/         # FastAPI backend (data, analytics, charts, warehouse_service)
├── frontend/        # React + Vite dashboard (Dashboard, WarehouseSalesAnalytics, KPICard)
├── tests/           # pytest unit tests + Playwright browser tests
├── memory/          # Persistent agent memory (conversations + task history)
├── mcp_servers/     # MCP server configurations (plane, github, memory, browser)
├── config/          # Agent and Plane configuration
├── scripts/         # setup.py, start_of_day.py, end_of_day.py, run_sprint_watcher.py, run_tests.py
└── reports/         # Auto-generated test reports
```

---

## 🚀 Quick Start & Continuous Operations

### 1. Continuous Background Services
- **Frontend Dashboard:** [http://localhost:5173](http://localhost:5173) (`npm run dev`)
- **Backend API:** [http://127.0.0.1:8000](http://127.0.0.1:8000) (`python -m uvicorn main:app`)
- **Sprint Watcher Agent:** `python scripts/run_sprint_watcher.py --interval 60`

### 2. Autonomous Testing Suite
```bash
# Unit test suite
pytest tests/unit/ -v

# Playwright browser end-to-end test suite
pytest tests/browser/ -v
```

---

## 📋 API Endpoints

| Endpoint | Method | Parameters | Description |
|---|---|---|---|
| `/api/health` | GET | None | Health check |
| `/api/warehouse/statistics` | GET | `target_db`, `oerdte`, `batch_id`, `oewhse`, `oeinv` | Direct PostgreSQL query for warehouse item/invoice stats |
| `/api/charts/kpi` | GET | `oerdte`, `target_db` | Returns KPI cards (Total Warehouses, Cases Built, Order Qty, Invoices) |
| `/api/charts/bar` | GET | `oerdte`, `target_db` | Returns cases built breakdown per warehouse |
| `/api/charts/scatter` | GET | `oerdte`, `target_db` | Returns order quantity vs cases built scatter plot |
| `/api/charts/heatmap` | GET | None | Correlation heatmap matrix |
| `/api/charts/distribution` | GET | `column` | Numeric distribution histogram |

---

## 📁 Memory System

Agent conversations are stored in `memory/conversations/` as JSONL files:
```
memory/
├── conversations/
│   └── 2026-07-28_orchestrator.jsonl
├── task_history/
│   └── 2026-07-28_task_history.jsonl
└── agent_state.json
```

---

*Built with ❤️ by AI agents — managed by Antigravity*
