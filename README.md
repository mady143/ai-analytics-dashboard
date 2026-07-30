# 🚀 AI Analytics Dashboard

> An agentic, AI-powered Data Analytics Dashboard built with **FastAPI + React**, managed and tested by **Autonomous AI Agents & Watchdog Supervisor**.

---

## ✨ Features

- 📊 **Interactive Dashboard** — KPI cards, bar charts, scatter plots, heatmaps, and warehouse analytics
- 🏭 **Warehouse Sales & Invoice Analytics** — Real-time PostgreSQL (`sptn_sales_data`) item & invoice statistics
- 🗄️ **Multi-Target DB Architecture** — Strict parameter-driven querying across `pg_prod`, `pg_dev`, `oracle_dev`, `oracle_f1`, `oracle_prod`
- 🤖 **Autonomous Agent Fleet & Watchdog** — 6 background agents (`Sprint Watcher`, `Orchestrator`, `Builder`, `Tester`, `Memory Agent`, `Git Agent`) supervised by `scripts/agent_watchdog.py`
- 🛡️ **Auto-Restart Watchdog Engine** — Continuously monitors servers (`:8000`, `:5173`) and agents (`sprint_watcher`, `builder`, `tester`, `memory`, `git_agent`), automatically restarting them if downtime or idle failure is detected
- 💾 **Persistent Memory & Taxonomy** — Agent state (`memory/agent_state.json`) and online NLP taxonomy (`memory/nlp_taxonomy.json`)
- 🏃 **Sprint Watcher** — Continuous 60s background polling of Plane tasks and comment updates with automated Git push hooks
- 🧪 **Auto Testing** — pytest unit tests + Playwright browser automation tests
- 🔀 **Git Automation & EOD Push** — Automatic pull, stage, commit, and push to GitHub (`mady143/ai-analytics-dashboard`)
- 🔌 **MCP Integration** — Plane, GitHub, Memory, Browser MCP servers

---

## 🗂️ Project Structure

```
ai_analytics_dashboard/
├── agents/          # AI agents (Orchestrator, Builder, Tester, Plane, Git, Memory, Sprint Watcher)
├── backend/         # FastAPI backend (data, analytics, charts, warehouse_service)
├── frontend/        # React + Vite dashboard (Dashboard, WarehouseSalesAnalytics, KPICard)
├── tests/           # pytest unit tests + Playwright browser tests
├── memory/          # Persistent agent memory & online NLP taxonomy
├── mcp_servers/     # MCP server configurations (plane, github, memory, browser)
├── config/          # Agent and Plane configuration
├── scripts/         # start_all_services.bat, start_all_services.sh, agent_watchdog.py, end_of_day.py, run_sprint_watcher.py
└── reports/         # Auto-generated test reports
```

---

## 🚀 1-Click Launchers & Continuous Operations

### 1-Click Launch (Zero Approval Prompts)
* **Windows Launcher:** `scripts\start_all_services.bat`
* **Linux/macOS Launcher:** `bash scripts/start_all_services.sh`

### Individual Agent & Service Commands
```bash
# 1. FastAPI Backend Server (Port 8000)
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 2. Vite Frontend Dev Server (Port 5173)
cd frontend && npm run dev -- --host 0.0.0.0

# 3. Agent & Server Watchdog Supervisor
python scripts/agent_watchdog.py

# 4. Sprint Watcher Continuous Agent Loop (60s)
python scripts/run_sprint_watcher.py --interval 60

# 5. Git Agent & End-of-Day Auto-Push
python scripts/end_of_day.py
python -m agents.git_agent
```

---

## 🔀 Git Commands Reference

| Command | Description |
|---|---|
| `python scripts/end_of_day.py` | Staging, committing, and pushing all daily progress to remote `origin/main` |
| `python -m agents.git_agent` | Git MCP Server & Git Agent automation handler |
| `git pull origin main` | Synchronizes local workspace with latest remote commits |
| `git status --porcelain` | Used by agents to detect changed files in real time |
| `git push origin main` | Pushes staged commits to GitHub repository (`mady143/ai-analytics-dashboard`) |

---

## 📋 API Endpoints

| Endpoint | Method | Parameters | Description |
|---|---|---|---|
| `/api/health` | GET | None | Health check |
| `/api/warehouse/statistics` | GET | `target_db`, `oerdte`, `batch_id`, `oewhse`, `oeinv`, `only_scratches` | Direct PostgreSQL query for warehouse item/invoice stats |
| `/api/analytics/ai-copilot` | POST | `prompt`, `target_db`, `oerdte` | AI Data Copilot intent parser & table filter generator |
| `/api/charts/kpi` | GET | `oerdte`, `target_db` | Returns KPI cards (Total Warehouses, Cases Built, Order Qty, Invoices) |
| `/api/charts/bar` | GET | `oerdte`, `target_db` | Returns cases built breakdown per warehouse |
| `/api/charts/scatter` | GET | `oerdte`, `target_db` | Returns order quantity vs cases built scatter plot |

---

## 📁 Memory System

Agent conversations and dynamic state are stored in `memory/`:
```
memory/
├── conversations/
│   └── orchestrator_conversation.jsonl
├── task_history/
│   └── 2026-07-30_task_history.jsonl
├── nlp_taxonomy.json
└── agent_state.json
```

---

*Built with ❤️ by AI agents — managed by Antigravity*
