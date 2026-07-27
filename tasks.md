# 📋 System Task Specification & Architecture (`tasks.md`)

This document outlines the mandatory operational requirements, daily tasks, component implementation details, and workspace file paths for the **AI Analytics Dashboard Autonomous Agent Network**.

---

## 🚨 Section 1: Mandatory Tasks (Autonomous Execution)

The system is configured to perform all mandatory tasks autonomously **without asking for permission prompts**:

### 1. Daily Git Synchronization (Morning & Evening)
- **Morning (Start of Day):** Run `python scripts/start_of_day.py` to execute `git pull origin main` and pull remote changes before work begins.
- **Evening (End of Day & Task Completion):** Run `python scripts/end_of_day.py` or automated `git_agent.eod_push()` to stage, commit, and push updated code to GitHub (`mady143/ai-analytics-dashboard`).
- **File References:**
  - [`scripts/start_of_day.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/scripts/start_of_day.py)
  - [`scripts/end_of_day.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/scripts/end_of_day.py)
  - [`agents/git_agent.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/agents/git_agent.py)

---

### 2. 60-Second Continuous Sprint Watcher Monitoring
- **Schedule:** Runs continuously in background every **60 seconds**:
  ```bash
  python scripts/run_sprint_watcher.py --interval 60
  ```
- **What it monitors:** Polls Plane workspace (`agentbuilder`) every 60 seconds to check if any task is in `unstarted`, `to-do`, or `in-progress` state.
- **File References:**
  - [`scripts/run_sprint_watcher.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/scripts/run_sprint_watcher.py)
  - [`agents/sprint_watcher_agent.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/agents/sprint_watcher_agent.py)

---

### 3. Automatic Sprint Task Detection & Execution
- **Flow:** When a new task is detected on Plane:
  1. Sets status on Plane to `In Progress`.
  2. Invokes [`builder_agent.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/agents/builder_agent.py) to write/update component code.
  3. Generates new test cases automatically.
  4. Runs full regression test suite.
  5. Updates status on Plane to `Completed` with execution duration & timestamps.
- **File References:**
  - [`agents/plane_agent.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/agents/plane_agent.py)

---

### 4. Code Modification & Zero Regression Rule
- **Rule:** When adding new code or features, existing functionality **must never be broken**.
- **Enforcement:** The system runs both unit tests and browser tests prior to finalizing any task. If any existing test fails, the task is marked `FAILED` and flagged for correction.

---

### 5. Automated Test Case Generation (`sprint_test_cases.md`)
- **Requirement:** For every new sprint task, the system automatically prepares unit test cases in `tests/unit/` and records test documentation in [`sprint_test_cases.md`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/sprint_test_cases.md).
- **File References:**
  - [`sprint_test_cases.md`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/sprint_test_cases.md)
  - [`tests/unit/test_navbar.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/tests/unit/test_navbar.py)

---

### 6. Full Playwright Browser Automation Testing
- **Execution:** Headless Chromium browser automation tests verify UI rendering, routes, KPI cards, and components on the live web app.
- **Command:** `pytest tests/browser/ -v`
- **File References:**
  - [`tests/browser/test_dashboard_loads.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/tests/browser/test_dashboard_loads.py)

---

### 7. Continuous Application Runtime
- **Backend (FastAPI):** Active on `http://localhost:8000` (Docs: `http://localhost:8000/docs`)
- **Frontend (React + Vite):** Active on `http://localhost:5173`

---

### 8. Headless / Zero Permission Mode
- All tasks in Section 1 execute automatically without interrupting the user for confirmation.

---

### 9. Plane Task State Transitions (`Unstarted` ➔ `In Progress` ➔ `Done`)
- **State Mapping:**
  - Initial Task State: `Todo` / `Unstarted`
  - Active Development: `In Progress` / `Started`
  - Completion & Verification: `Done` / `Completed`
- **Execution:** Once Builder code implementation and Playwright/pytest test suites pass 100%, the agent automatically maps and patches the task state to **`Done`** in Plane.

---

## 🧹 Section 2: Daily & Regular Tasks

1. **Code Cleanup & Architecture Review:**
   - Regularly prune temporary artifacts and verify clean code formatting.
2. **Sprint & Backlog Check:**
   - Continuously poll for newly added sprint cycles and backlog items in Plane.
3. **User Approval Escalation:**
   - **Rule:** Ask for user permission **ONLY** if an urgent, high-risk breaking change or core structural change is needed. Otherwise, handle updates automatically.

---

## 🧩 Section 3: Component & Module Implementation Details

| Module / File Path | Description & Purpose |
|---|---|
| [`agents/sprint_watcher_agent.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/agents/sprint_watcher_agent.py) | Main autonomous loop. Monitors Plane every 60s, coordinates Builder & Tester agents, logs end-to-end execution time, and triggers Git push. |
| [`agents/builder_agent.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/agents/builder_agent.py) | Code generation agent. Builds frontend/backend code components and automatically creates matching unit test files. |
| [`agents/tester_agent.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/agents/tester_agent.py) | Runs unit test suite (`pytest tests/unit/`) and browser suite (`pytest tests/browser/`), generating HTML reports under `reports/`. |
| [`agents/git_agent.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/agents/git_agent.py) | Git automation engine. Stages changes, builds structured commit messages with task details, and pushes to `origin/main`. |
| [`agents/plane_agent.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/agents/plane_agent.py) | Integration client for Plane REST API (`app.plane.so`). Manages project issues, cycles/sprints, statuses, and task comments. |
| [`agents/memory_manager.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/agents/memory_manager.py) | Manages persistent JSONL task logs in `memory/task_history/` and tracks agent status in `memory/agent_state.json`. |
| [`frontend/src/components/Navbar.jsx`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/frontend/src/components/Navbar.jsx) | Top navigation bar component built for the dashboard UI. |
| [`frontend/src/App.jsx`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/frontend/src/App.jsx) | Core React routing and layout container. |
| [`frontend/index.html`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/frontend/index.html) | HTML entry point mounted to `#root` with title `AI Analytics Dashboard`. |
| [`AI_Agents_and_MCP_Presentation.pptx`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/AI_Agents_and_MCP_Presentation.pptx) | Widescreen PowerPoint presentation deck covering AI Agents & Model Context Protocol architecture. |
