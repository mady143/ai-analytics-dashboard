# 📋 System Task Specification & Architecture (`tasks.md`)

This document outlines the mandatory operational requirements, daily tasks, component implementation details, and workspace file paths for the **AI Analytics Dashboard Autonomous Agent Network**.

---

## 🚨 Section 1: Mandatory Tasks (Autonomous Execution)

The system is configured to perform all mandatory tasks autonomously **WITHOUT asking for permission prompts** (except in critical blocker scenarios):

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
- **Mandatory Directive:** Must run continuously every 60 seconds without manual intervention.
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

### 4. Code Modification & Zero Regression Rule (Do Not Disturb Existing Code)
- **Mandatory Directive:** Do **NOT** alter or disturb existing working code. Handle **ONLY** new sprint changes and feature additions.
- **Strict Scope Control:** All code modifications must be additively non-destructive to pre-existing components, services, routes, or configurations.
- **Enforcement:** Both unit tests and browser tests must pass 100%. If any existing or new test fails, the task is marked `FAILED` and flagged for immediate resolution.

---

### 5. Consolidated Test Suite & Markdown Test Tracking (`sprint_test_cases.md`)
- **Mandatory Directive:** Do **NOT** maintain or create multiple individual `.py` test files in `tests/unit/` for every small UI component. Keep `tests/unit/` clean and consolidated (`test_core_components.py`, `test_analytics.py`, `test_charts.py`, `test_data_endpoints.py`).
- **Markdown Test Case Logging:** Record all sprint test cases, descriptions, and test results (`PASSED` / `FAILED` status) directly inside [`sprint_test_cases.md`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/sprint_test_cases.md) right behind each test case.
- **File References:**
  - [`sprint_test_cases.md`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/sprint_test_cases.md)
  - [`tests/unit/test_core_components.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/tests/unit/test_core_components.py)


---

### 6. Full Playwright Browser Automation Testing (Zero Permission Prompting)
- **Mandatory Directive:** Run `pytest tests/browser/ -v` and all testing/build commands autonomously **WITHOUT asking for permission prompts**. Never pause or ask confirmation to run browser tests or shell commands.
- **Execution:** Headless Chromium browser automation tests verify UI rendering, routes, KPI cards, and components on the live web app.
- **Command:** `pytest tests/browser/ -v`
- **File References:**
  - [`tests/browser/test_dashboard_loads.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/tests/browser/test_dashboard_loads.py)


---

### 7. Continuous Application Runtime & Execution
- **Mandatory Directive:** Automatically launch and maintain the live application runtime whenever developing, building, or testing:
  - **Backend Server (FastAPI):** Run `python -m uvicorn main:app --host 127.0.0.1 --port 8000` (Cwd: `backend/`) -> Active on `http://localhost:8000` (Docs: `http://localhost:8000/docs`).
  - **Frontend Server (React + Vite):** Run `node node_modules/vite/bin/vite.js` or `npx vite` (Cwd: `frontend/`) -> Active on `http://localhost:5173`.
- **Runtime Verification:** Ensure both servers are operational and accessible prior to running Playwright browser automation suites.

---

### 8. Headless / Zero Permission Mode (Ask Only on Critical Blockers)
- **Mandatory Zero-Permission Policy:** Do **NOT** ask for user permission or wait for confirmation prompts for standard development operations:
  - 🧪 **Browser & Unit Testing (`pytest`):** Running `pytest tests/browser/ -v` and `pytest tests/unit/ -v` autonomously without permission popups.
  - ⚡ **Node & NPM Operations (`npm` / `node`):** Running `node node_modules/vite/bin/vite.js`, `npm run dev`, `npm run build`, and `npm install` without permission popups.
  - 🐍 **Python & Server Runtimes (`python` / `uvicorn`):** Running 60-second Sprint Watcher Agent (`python scripts/run_sprint_watcher.py --interval 60`), starting FastAPI backend server (`python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload`), running inline python scripts (`python -c ...`), and executing pytest test suites without permission popups.
  - 🔀 **Git Version Control (`git`):** Executing `git status`, `git pull`, `git add`, `git commit`, and `git push` without permission popups.
  - 📝 **Markdown Documentation Updates (`tasks.md` / `.md`):** **Always allow modifying, editing, and updating [`tasks.md`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/tasks.md)**, [`sprint_test_cases.md`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/sprint_test_cases.md), and all markdown files completely autonomously without permission popups.
  - 💻 **Code Modifications:** Writing, editing, or implementing new sprint feature code.
- **Existing Code Preservation (Zero Side-Effects):** New code changes must **never** break or disturb pre-existing working code functionality.
- **Continuous Regression Testing:** Perform continuous automatic regression testing (unit + Playwright browser tests) after every code or documentation change to ensure zero side-effects.
- **Escalation Exception:** Stop and ask the user for input **ONLY IF** an urgent, high-risk critical blocker or unsolvable architectural issue occurs.



---

### 9. Plane Task State Transitions (`Unstarted` ➔ `In Progress` ➔ `Done`)
- **State Mapping:**
  - Initial Task State: `Todo` / `Unstarted`
  - Active Development: `In Progress` / `Started`
  - Completion & Verification: `Done` / `Completed`
- **Execution:** Once Builder code implementation and Playwright/pytest test suites pass 100%, the agent automatically maps and patches the task state to **`Done`** in Plane.

---

### 10. Autonomous Sprint Context & Issue Tracking (Sprint ID, Title & Description)
- **Mandatory Directive:** Whenever the user is unavailable to guide code updates, the system must autonomously check and manage all sprint metadata, specifically:
  - **Sprint ID**
  - **Sprint Title**
  - **Sprint Description**
- **Autonomous Execution & Verification:** Inspect sprint specifications, run tests, verify endpoints, and update components to fulfill sprint requirements completely.
- **Escalation Policy:** If any blocking ambiguity or unsolvable failure occurs, immediately pause execution and ask the user for guidance until unstuck.

---

### 11. Autonomous Workflow Execution & Full-Stack Testing Checklist
- **Proactive Autonomous Execution (Zero Waiting):** Do **NOT** wait for user requests to run the application server, read sprint specifications, or make code updates. Trigger all steps automatically end-to-end.
- **Do Not Disturb Existing Code:** Existing functionality must remain untouched and fully working. Only add/update code strictly necessary for the new sprint.
- **Full-Spectrum Testing (Existing + New Features):** Mandatory validation across both existing features and newly added features:
  - Unit Tests: `pytest tests/unit/ -v` (100% pass requirement for existing + new code)
  - Browser Automation: `pytest tests/browser/ -v` (100% pass requirement for full UI rendering & interactions)
- **Mandatory Task Execution Checklist:**
  - [ ] 1. Read Sprint Metadata (Sprint ID, Sprint Title, Sprint Description).
  - [ ] 2. Preserve existing codebase without altering unrelated pre-existing features.
  - [ ] 3. Implement new sprint requirements additively.
  - [ ] 4. Ensure active Sprint feature (e.g. Warehouse Sales & Invoice Analytics) is positioned prominently at the top of the main Dashboard page.
  - [ ] 5. Launch/verify application runtime (Backend on `:8000`, Frontend on `:5173`).
  - [ ] 6. Test full functionality: run unit & browser tests for BOTH existing and newly added features.
  - [ ] 7. Push verified status to Plane and commit/push to Git.

---

### 12. Primary Dashboard Layout Alignment with Active Sprint Specification
- **Mandatory Directive:** Whenever a sprint defines a new feature component (such as Sprint `AAD-5`: **Warehouse Sales & Invoice Analytics**), the primary user interface (`http://localhost:5173`) must display the target sprint feature **prominently at the top of the page above the fold**.
- **Sprint Specification Reading Rule:** Read and analyze the **Sprint ID**, **Sprint Title**, and **Sprint Description** thoroughly. Do not place active sprint components below secondary or generic fallback components (such as default HR/Employee cards). Ensure the primary dashboard header and top view reflect the active sprint topic.




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
