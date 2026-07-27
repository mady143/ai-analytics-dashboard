# 🚀 AI Analytics Dashboard

> An agentic, AI-powered Data Analytics Dashboard built with **FastAPI + React**, managed and tested by **Claude-powered AI agents**.

---

## ✨ Features

- 📊 **Interactive Dashboard** — KPI cards, bar charts, scatter plots, heatmaps
- 🤖 **ML Analytics** — Train Random Forest & Logistic Regression, visualize results
- 🧠 **AI Agent System** — 5 agents (Orchestrator, Builder, Tester, Plane, Git) work autonomously
- 💾 **Persistent Memory** — All agent conversations stored in `memory/` as JSONL
- 🏃 **Sprint Management** — Automatic Plane task creation and status updates
- 🧪 **Auto Testing** — pytest unit tests + Playwright browser tests
- 🔀 **Git Automation** — End-of-day auto-commit and push to GitHub
- 🔌 **MCP Integration** — Plane, GitHub, Memory, Browser MCP servers

---

## 🗂️ Project Structure

```
ai_analytics_dashboard/
├── agents/          # AI agents (Orchestrator, Builder, Tester, Plane, Git, Memory)
├── backend/         # FastAPI backend (data, analytics, charts)
├── frontend/        # React + Vite dashboard
├── tests/           # pytest unit tests + Playwright browser tests
├── memory/          # Persistent agent memory (conversations + task history)
├── mcp_servers/     # MCP server configurations
├── config/          # Agent and Plane configuration
├── scripts/         # setup.py, run_agents.py, end_of_day.py, run_tests.py
└── reports/         # Auto-generated test reports
```

---

## 🚀 Quick Start

### 1. Run Setup (First Time Only)
```bash
python scripts/setup.py
```
This will:
- Create `.env` from your API keys
- Install Python dependencies
- Install Playwright browsers
- Initialize git
- Set up Plane project + sprints

### 2. Start the Backend
```bash
cd backend
uvicorn main:app --reload
# API available at: http://localhost:8000
# Docs at: http://localhost:8000/docs
```

### 3. Start the Frontend
```bash
cd frontend
npm run dev
# Dashboard at: http://localhost:5173
```

### 4. Run AI Agents
```bash
python scripts/run_agents.py
```

### 5. Run Tests
```bash
python scripts/run_tests.py
```

### 6. End-of-Day Push
```bash
python scripts/end_of_day.py
```

---

## 🔑 Required API Keys

| Key | Where to Get |
|---|---|
| `ANTHROPIC_API_KEY` | [console.anthropic.com](https://console.anthropic.com) |
| `PLANE_API_TOKEN` | app.plane.so → Settings → API Tokens |
| `PLANE_WORKSPACE_SLUG` | Your workspace URL slug |
| `GITHUB_TOKEN` | github.com → Settings → Developer Settings → PAT |

---

## 🤖 Agent System

| Agent | Role | Model |
|---|---|---|
| **Orchestrator** | Master coordinator | claude-opus-4-5 |
| **Builder** | Code writer | claude-opus-4-5 |
| **Tester** | pytest + Playwright | claude-sonnet-4-5 |
| **Plane Agent** | Task management | claude-haiku-4-5 |
| **Git Agent** | EOD git operations | claude-haiku-4-5 |

---

## 📋 API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/api/health` | GET | Health check |
| `/api/data/sample` | GET | Sample dataset |
| `/api/data/upload` | POST | Upload CSV |
| `/api/data/summary` | GET | Statistical summary |
| `/api/analytics/train` | POST | Train ML model |
| `/api/analytics/results` | GET | Get model results |
| `/api/analytics/predict` | POST | Make prediction |
| `/api/charts/kpi` | GET | KPI cards data |
| `/api/charts/bar` | GET | Bar chart data |
| `/api/charts/scatter` | GET | Scatter plot data |
| `/api/charts/heatmap` | GET | Correlation heatmap |
| `/api/charts/distribution` | GET | Histogram data |

---

## 🧪 Testing

```bash
# Unit tests only
pytest tests/unit/ -v

# Browser tests (requires frontend running at :5173)
pytest tests/browser/ -v

# Full suite with HTML reports
python scripts/run_tests.py
```

---

## 📁 Memory System

Agent conversations are stored in `memory/conversations/` as JSONL files:
```
memory/
├── conversations/
│   └── 2026-07-27_09-00-00_orchestrator.jsonl
├── task_history/
│   └── 2026-07-27_task_history.jsonl
└── agent_state.json
```

---

*Built with ❤️ by AI agents — managed by Claude*
