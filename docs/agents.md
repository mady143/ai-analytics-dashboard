# 🤖 Agents — Complete Module Documentation

> Every agent in `agents/` is a **focused, single-responsibility AI worker**.  
> They communicate via shared memory (`memory/agent_state.json`) and Plane's REST API.

---

## Agent Architecture Overview

```
                  ┌─────────────────────────────┐
                  │      Plane (Sprint Board)    │
                  │  Tasks / Cycles / Projects   │
                  └──────────┬──────────────────┘
                             │ REST API
                             ▼
              ┌──────────────────────────────────┐
              │     sprint_watcher_agent.py       │  ← NEW
              │  Polls Plane every N seconds      │
              │  Detects new/completed tasks      │
              └──────┬──────────────┬────────────┘
                     │              │
          New task   │              │  Tests passed
                     ▼              ▼
           ┌──────────────┐   ┌──────────────┐
           │ builder_agent│   │  tester_agent│
           │ Writes code  │──►│ pytest +     │
           │ via Claude   │   │ Playwright   │
           └──────────────┘   └──────┬───────┘
                                     │
                     ┌───────────────┘
                     ▼
           ┌──────────────────┐   ┌──────────────┐
           │  plane_agent.py  │   │  git_agent.py │
           │  Mark task Done/ │   │  EOD commit + │
           │  Failed + comment│   │  push to GitHub│
           └──────────────────┘   └──────┬───────┘
                                         │
                     ┌───────────────────┘
                     ▼
           ┌──────────────────────────────────────┐
           │        scripts/agent_watchdog.py      │
           │  Supervisor: Monitors servers & ALL   │
           │  6 agents (incl. git_agent), auto-   │
           │  restarts on downtime/idle failure    │
           └──────────────────────────────────────┘
                     ▲
           ┌──────────────────────────────────────┐
           │      orchestrator_agent.py            │
           │  Master coordinator — reads state,    │
           │  decides which agent runs next        │
           └──────────────────────────────────────┘
                     ▲
           ┌──────────────────────────────────────┐
           │       memory_manager.py               │
           │  Persists all conversations, task     │
           │  logs, and agent state to disk        │
           └──────────────────────────────────────┘
```

---

## 1. `sprint_watcher_agent.py` ⭐ NEW

**File:** `agents/sprint_watcher_agent.py`  
**Run:** `python scripts/run_sprint_watcher.py`

### What it does
The Sprint Watcher is the **heartbeat of the agent system**. It runs in a continuous loop, polling Plane for sprint task changes and driving the full build-test-close lifecycle autonomously.

### Task Lifecycle it manages

```
[Plane] Todo
    │
    ▼
[sprint_watcher] Detects new task
    │
    ├─► Updates Plane → "In Progress"
    │
    ├─► Calls builder_agent.py (writes/updates code)
    │
    ├─► Calls tester_agent.py (pytest + playwright)
    │
    ├── PASS ──► Updates Plane → "Done"  ✅
    │            Adds test result comment
    │
    └── FAIL ──► Updates Plane → "Failed" ❌
                 Adds error comment
                 Re-queues for next cycle
```

### Configuration
| Parameter | Default | Description |
|---|---|---|
| `--interval` | 120s | How often to poll Plane |
| `--cycles` | 0 (∞) | Max poll cycles (0 = run forever) |

### Example Usage
```bash
# Watch every 2 minutes, forever
python scripts/run_sprint_watcher.py

# Quick test: 3 cycles, 30 second interval
python scripts/run_sprint_watcher.py --interval 30 --cycles 3
```

### Key Methods
| Method | Description |
|---|---|
| `watch(max_cycles)` | Main poll loop |
| `_handle_new_task(task)` | Full lifecycle for one task |
| `_run_builder(...)` | Subprocess call to builder_agent.py |
| `_run_tests()` | Subprocess call to pytest |
| `_finalize_task(...)` | Update Plane + log to memory |
| `_sync_completed_tasks(...)` | Sync already-completed tasks to memory |

---

## 2. `orchestrator_agent.py`

**File:** `agents/orchestrator_agent.py`  
**Run:** `python scripts/run_agents.py`

### What it does
The Orchestrator is the **master coordinator**. It:
- Loads the current state from `memory/agent_state.json`
- Pulls the current sprint task list from Plane
- Uses **Claude (claude-opus-4-5)** to reason about what should be done next
- Restores conversation history from `memory/conversations/` for continuity
- Initializes git and Plane on first run
- Saves memory after each session

### When to use it
Run the Orchestrator at the **start of each work session** to get a status report and a Claude-generated plan for the day.

### Key Methods
| Method | Description |
|---|---|
| `run_daily_session()` | Full session: status → plan → save memory |
| `_call_claude(message)` | Sends message to Claude, appends to history |
| `_build_context()` | Builds rich context from state + Plane tasks |
| `_load_memory()` | Restores last conversation on startup |
| `mark_task_done(task_id)` | Updates Plane + logs to memory |

---

## 3. `builder_agent.py`

**File:** `agents/builder_agent.py`  
**Called by:** `sprint_watcher_agent.py`

### What it does
The Builder is the **code-writing agent**. Given a task title and description, it:
- Uses Claude to generate or modify Python/React code
- Writes files directly to the project
- Logs all file changes to `memory/task_history/`
- Updates Plane task to "In Progress" when it starts

### Interface (CLI arguments when called by Sprint Watcher)
```bash
python agents/builder_agent.py \
  --task-id    "abc123" \
  --task-title "Create chart endpoint" \
  --description "Add GET /api/charts/pie endpoint" \
  --priority   "high"
```

> **Note:** `builder_agent.py` is a skeleton that needs to be fleshed out with your specific Claude API calls. The Sprint Watcher handles it gracefully if it's not yet implemented.

---

## 4. `tester_agent.py`

**File:** `agents/tester_agent.py`  
**Run:** `python agents/tester_agent.py`  
**Called by:** `sprint_watcher_agent.py` after Builder completes

### What it does
The Tester runs **automated tests** after every code change:
- **Unit tests** via `pytest tests/unit/` with HTML report
- **Browser tests** via Playwright + `pytest tests/browser/`
- Saves `reports/unit_test_report.html` and `reports/browser_test_report.html`
- Updates `memory/agent_state.json` with latest test results
- Logs pass/fail to `memory/task_history/`

### Test Suites it manages
| Suite | Location | What it tests |
|---|---|---|
| Unit — Data | `tests/unit/test_data_endpoints.py` | Upload, sample, summary endpoints |
| Unit — Analytics | `tests/unit/test_analytics.py` | ML training, prediction, columns |
| Unit — Charts | `tests/unit/test_charts.py` | KPI, bar, scatter, heatmap, distribution |
| Browser | `tests/browser/test_dashboard_loads.py` | Frontend UI loading and navigation |

### Key Methods
| Method | Description |
|---|---|
| `run_unit_tests()` | Runs pytest on `tests/unit/`, returns results dict |
| `run_browser_tests()` | Runs Playwright tests, returns results dict |
| `run_all_tests()` | Runs both, combines results, updates state |

---

## 5. `plane_agent.py`

**File:** `agents/plane_agent.py`  
**Called by:** All other agents for Plane API operations

### What it does
The Plane Agent is a **thin API wrapper** around Plane's REST API. It is not an AI agent — it's a utility module that all other agents import.

### Functions
| Function | Description |
|---|---|
| `get_or_create_project()` | Returns project ID, creates project if first run |
| `create_sprint(name, desc, weeks)` | Creates a Plane cycle (sprint) |
| `list_sprints(project_id)` | Returns all sprint cycles |
| `create_task(title, desc, priority, pts)` | Creates a Plane issue |
| `create_subtask(parent_id, title)` | Creates a child issue |
| `update_task_status(issue_id, status)` | Moves task to new state |
| `add_comment(issue_id, text)` | Posts a comment on an issue |
| `list_tasks(project_id)` | Returns all issues in project |
| `get_states(project_id)` | Returns workflow states |
| `setup_all_sprints(project_id)` | Creates all 5 sprints from config |
| `setup_initial_tasks(project_id, sprint_id)` | Seeds Sprint 1 with initial tasks |

### Plane → Sprint mapping
```
Plane Terminology    ↔    This Project
─────────────────────────────────────
Issue                ↔    Task / Sub-task
Cycle                ↔    Sprint
State: "unstarted"   ↔    To Do
State: "started"     ↔    In Progress
State: "completed"   ↔    Done ✅
State: "cancelled"   ↔    Failed ❌
```

---

## 6. `git_agent.py`

**File:** `agents/git_agent.py`  
**Run:** `python scripts/end_of_day.py`

### What it does
The Git Agent handles **end-of-day version control**:
- Discovers all changed files (`git status --porcelain`)
- Stages everything (`git add .`)
- Generates a **meaningful commit message** from today's task history
- Commits and pushes to the GitHub remote

### Commit message format
```
EOD 2026-07-27 @ 18:00 — Daily agent commit

## Tasks Completed
- ✅ Create chart endpoint
- ✅ Add CSV upload validation

## Files Changed
- backend/routers/charts.py
- tests/unit/test_charts.py

🤖 Auto-committed by Git Agent at 18:00
```

### Key Functions
| Function | Description |
|---|---|
| `init_repo()` | Initialize git repo if not exists |
| `setup_git_config()` | Set agent name/email for commits |
| `get_changed_files()` | List of modified/new files |
| `eod_push(tasks, summary)` | Full stage → commit → push workflow |
| `generate_commit_message(...)` | Build descriptive commit from task history |

---

## 7. `memory_manager.py`

**File:** `agents/memory_manager.py`  
**Used by:** All agents (imported as utility module)

### What it does
The Memory Manager provides **persistent storage** across agent sessions. It stores:

| Storage | Location | Format |
|---|---|---|
| Agent state | `memory/agent_state.json` | JSON |
| Conversation history | `memory/conversations/YYYY-MM-DD_HH-MM-SS_agentname.jsonl` | JSONL |
| Task history | `memory/task_history/YYYY-MM-DD_task_history.jsonl` | JSONL |

### Why JSONL?
JSONL (JSON Lines) allows **append-only writes** — each conversation turn or task result is one line. This avoids file corruption and allows streaming reads.

### Key Functions
| Function | Description |
|---|---|
| `load_state()` | Load `agent_state.json` |
| `save_state(state)` | Write updated state to disk |
| `update_agent_status(name, status, task)` | Set agent running/idle/error |
| `save_conversation(agent, messages)` | Write session to JSONL |
| `load_last_conversation(agent)` | Restore last N messages for context |
| `log_task_result(task_id, ...)` | Append task result to today's history |
| `get_todays_summary()` | Summary dict of today's activity |
| `cleanup_old_memory(days)` | Delete files older than retention period |

---

## Running All Agents Together

```bash
# Terminal 1 — Backend API
cd backend && uvicorn main:app --reload

# Terminal 2 — Frontend
cd frontend && node node_modules/vite/bin/vite.js

# Terminal 3 — Sprint Watcher (core autonomous loop)
python scripts/run_sprint_watcher.py --interval 120

# Terminal 4 — Orchestrator (daily planning session)
python scripts/run_agents.py

# Terminal 5 — EOD push (run manually or schedule at 6pm)
python scripts/end_of_day.py
```
