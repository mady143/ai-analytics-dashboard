# 📐 Architecture — Full System Documentation

> End-to-end documentation of the AI Analytics Dashboard system.

---

## System Components

```
┌──────────────────────────────────────────────────────────────────────┐
│                         Developer / You                              │
│         Adds tasks to Plane sprint board (or via app.plane.so)      │
└──────────────────────────┬───────────────────────────────────────────┘
                           │ REST API
                           ▼
┌──────────────────────────────────────────────────────────────────────┐
│                        PLANE (Sprint Board)                          │
│    Project: AI Analytics Dashboard                                   │
│    Sprints: Sprint 1 → Sprint 5                                      │
│    Tasks:   Todo | In Progress | Done | Failed                       │
└──────────────────────────┬───────────────────────────────────────────┘
                           │  Polled by Sprint Watcher (every 2 min)
                           ▼
┌──────────────────────────────────────────────────────────────────────┐
│                     AGENT SYSTEM (Python)                            │
│                                                                      │
│  ┌─────────────────┐    ┌──────────────────┐    ┌────────────────┐  │
│  │ sprint_watcher  │───►│  builder_agent   │───►│ tester_agent   │  │
│  │ (poll loop)     │    │  (Claude writes  │    │ (pytest +      │  │
│  │                 │    │   code)          │    │  Playwright)   │  │
│  └────────┬────────┘    └──────────────────┘    └───────┬────────┘  │
│           │                                             │            │
│           ▼                                             ▼            │
│  ┌─────────────────┐    ┌──────────────────┐    ┌────────────────┐  │
│  │ orchestrator    │    │  plane_agent     │    │  git_agent     │  │
│  │ (daily planner) │    │  (Plane REST API)│    │  (EOD push)    │  │
│  └─────────────────┘    └──────────────────┘    └────────────────┘  │
│                                    ▲                                 │
│                        ┌───────────┴───────────┐                    │
│                        │   memory_manager       │                    │
│                        │   (JSONL persistence)  │                    │
│                        └───────────────────────┘                    │
└──────────────────────────┬───────────────────────────────────────────┘
                           │ HTTP (localhost:8000)
                           ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI, Python)                         │
│                                                                      │
│   /api/data/*       →  data_service.py  (CSV, sample data)          │
│   /api/analytics/*  →  ml_service.py   (sklearn models)             │
│   /api/charts/*     →  charts.py       (chart-ready JSON)           │
└──────────────────────────┬───────────────────────────────────────────┘
                           │ HTTP (localhost:5173)
                           ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    FRONTEND (React + Vite)                           │
│                                                                      │
│   /           →  Dashboard.jsx    (KPIs + charts)                   │
│   /analytics  →  Analytics.jsx   (ML training UI)                   │
│   /charts     →  ChartsExplorer  (interactive charts)               │
│   /agents     →  AgentMonitor    (live agent status)                │
│   /sprints    →  SprintBoard     (Plane sprint view)                │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow

### 1. Adding a Task (Manual or via API)
```
You add task in Plane
    → Sprint Watcher detects it on next poll
    → Marks "In Progress"
    → Builder Agent writes code (via Claude)
    → Tester Agent runs tests
    → PASS: Plane → "Done", comment added, memory logged
    → FAIL: Plane → "Failed", error logged, re-queued next cycle
```

### 2. Dashboard Viewing
```
Browser opens localhost:5173
    → React fetches from FastAPI (localhost:8000)
    → FastAPI reads from in-memory Pandas DataFrame
    → Charts rendered with Recharts
```

### 3. CSV Upload + ML Training
```
User drops CSV on Analytics page
    → POST /api/data/upload → stored in _dataframe_store
    → POST /api/analytics/train → sklearn fits model
    → GET results → accuracy, confusion matrix, feature importance
    → Charts rendered in UI
```

### 4. End of Day
```
python scripts/end_of_day.py
    → memory_manager.get_todays_summary()
    → git_agent.eod_push(tasks_completed)
    → git add . → git commit (with task summary) → git push
    → Plane sprint notes updated
```

---

## Technology Decisions

| Decision | Choice | Reason |
|---|---|---|
| Backend framework | FastAPI | Async, auto-docs, Pydantic validation |
| Frontend framework | React + Vite | Fast HMR, JSX, great ecosystem |
| Chart library | Recharts | React-native, responsive, simple API |
| AI SDK | Anthropic (Claude) | Best coding agent capabilities |
| Task management | Plane | Open-source, free tier, REST API |
| Testing — unit | pytest + httpx | De facto Python standard |
| Testing — browser | Playwright | Fast, reliable, Chromium headless |
| Memory storage | JSONL files | Append-only, no DB required, portable |
| ML library | scikit-learn | Proven, fast, well-documented |
| Animations | Framer Motion | Smooth declarative React animations |

---

## Environment Variables Reference

| Variable | Used by | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | Orchestrator, Builder | Claude API access |
| `PLANE_API_TOKEN` | plane_agent, sprint_watcher | Plane REST API |
| `PLANE_WORKSPACE_SLUG` | plane_agent | Your Plane workspace URL slug |
| `PLANE_PROJECT_ID` | Auto-filled after setup | Plane project ID |
| `GITHUB_TOKEN` | git_agent | GitHub Personal Access Token |
| `GITHUB_REPO` | git_agent | `username/repo` for push |
| `BACKEND_PORT` | main.py | Default: 8000 |
| `FRONTEND_URL` | main.py (CORS) | Default: http://localhost:5173 |
| `AGENT_MODEL` | All AI agents | Default: claude-opus-4-5 |
| `EOD_PUSH_TIME` | git_agent | Default: 18:00 |

---

## Port Map

| Service | Port | URL |
|---|---|---|
| FastAPI Backend | 8000 | http://localhost:8000 |
| Swagger API Docs | 8000 | http://localhost:8000/docs |
| React Frontend | 5173 | http://localhost:5173 |
| Plane (cloud) | — | https://app.plane.so |

---

## File Count Summary

| Area | Files |
|---|---|
| Agents | 7 Python files |
| Backend | 7 Python files |
| Frontend | 8 JSX/JS files |
| Tests | 5 Python files |
| Config | 4 JSON files |
| Scripts | 5 Python files |
| Docs | 4 Markdown files |
| **Total** | **~40 files** |
