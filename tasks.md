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

### 2. 60-Second Continuous Sprint Watcher Monitoring (ALWAYS RUNNING)
- **Schedule:** Runs continuously in background every **60 seconds** — ALWAYS ALLOWED, ALWAYS AUTO-RESTART:
  ```bash
  python scripts/run_sprint_watcher.py --interval 60
  ```
- **What it monitors:** Polls Plane workspace (`agentbuilder`) every **60 seconds** to detect:
  1. 🆕 **New tasks** — never-seen-before task IDs in any state
  2. 🔄 **State changes** — task state changes back to `unstarted` / `todo` (e.g. user resets a task)
  3. ✏️ **Content updates** — `updated_at` timestamp changed (user edited title, description, or details in Plane)
- **Fix Applied (2026-07-27):** Previous version only skipped tasks by ID once seen — it would **miss all subsequent updates**. Now uses `_last_seen_state` + `_last_seen_updated` dicts to detect *any change* and re-trigger the task lifecycle.
- **Update Detection Logic (in `agents/sprint_watcher_agent.py`):**
  - `is_new` → task ID never seen before → **PROCESS**
  - `state_changed` → `last_state != current_state` → **PROCESS**
  - `content_updated` → `last_updated_at != current_updated_at` → **PROCESS**
  - `done/completed` → skip (no action needed)
- **Mandatory Directive:** Must run **always**. If stopped for any reason, restart immediately without asking permission.
- **File References:**
  - [`scripts/run_sprint_watcher.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/scripts/run_sprint_watcher.py)
  - [`agents/sprint_watcher_agent.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/agents/sprint_watcher_agent.py)


---

### 3. Automatic Sprint Task Detection & Execution (Sprint Updates & New Tasks)
- **Mandatory Autonomous Directive:** Whenever the sprint is updated or a new task is added/updated in the sprint, the agent MUST automatically execute the full task lifecycle:
  1. 🛠️ **Work on the Task:** Pick up the task, transition Plane status to `In Progress`, extract all instructions/comments, and write/update the backend & frontend component code.
  2. 🧪 **Test the Code (Unit Tests):** Automatically generate and run unit tests (`pytest tests/unit/ -v`) to verify core component logic, endpoints, and ensure zero regression.
  3. 🌐 **Test in Browser (UI Automation):** Execute Playwright browser automation tests (`pytest tests/browser/ -v`) to test live rendering, charts, tables, KPI cards, and user interactions in a real browser environment.
  4. 🚀 **Deploy & Push:** Commit and push the tested changes to the remote Git repository (`mady143/ai-analytics-dashboard`), deploy the build, and mark the task status as `Done` / `Completed` in Plane.
- **Fix Applied (2026-07-27):** Sprint Watcher previously **did NOT poll comments** — it only watched task state changes. Added `list_comments()` to `plane_agent.py` and `_check_new_comments()` to `sprint_watcher_agent.py`. Every 60-second poll now also fetches comments on all open tasks and triggers the builder if any **new** (unseen) user comment is found.
- **Comment Detection Logic:**
  - On each 60s poll: `list_comments(project_id, task_id)` is called for every non-completed task
  - `_last_seen_comment_ids` tracks already-processed comment IDs per task
  - New human comments (not bot comments containing `🤖`) trigger `_handle_new_task()` with the comment injected into the task description
  - Bot-generated comments (`Sprint Watcher`, `🤖`) are automatically skipped to avoid infinite loops

---

### 3b. Open Requirements from Plane Comments (2026-07-27) — `Warehouse level statics`

These 3 instructions were added as comments by `manikantha.sekhar` in Plane and MUST be implemented:

#### ⚠️ Requirement 1 — Total Warehouse Count Mismatch + `batch_id` + Global Date Format
- **Issue:** Total warehouse count KPI value is mismatching actual data
- **Action:**
  1. Fix total warehouse count to show the correct distinct count from the database
  2. Add `batch_id` column to the `WarehouseSalesAnalytics` data table
  3. Add a **date format selector** at the top of the page — when the date format changes, it must apply to **all date fields across the entire page** (table rows, KPI cards, chart tooltips)

#### ⚠️ Requirement 2 — KPI Values Not Populating (Cases Built, Original Order Qty, Invoice Processed)
- **Issue:** These 3 KPI card values show `0` or are blank
- **Action:**
  1. `Cases Built` KPI — must show sum of `cases_built_qty` from the warehouse statistics API
  2. `Original Order Qty` KPI — must show sum of `original_order_qty`
  3. `Invoices Processed` KPI — must show the count of distinct invoice numbers

#### ⚠️ Requirement 3 — `batch_id` Not Visible in UI
- **Issue:** `batch_id` field exists in the database but is missing from the table display
- **Action:**
  1. Add `Batch ID` as a visible column in the `WarehouseSalesAnalytics` table
  2. Ensure `batch_id` is returned by the backend `GET /api/warehouse/statistics` endpoint
  3. Display it alongside `Invoice #`, `C&S Item Code`, etc.


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

### 7. Continuous Application Runtime & Auto-Restart Execution
- **Mandatory Directive (ALWAYS RUNNING & AUTO-RESTART):** The agent MUST continuously maintain the application in a running state. Never stop the backend or frontend servers.
  - **Auto-Detect & Auto-Reload:** If either server is not in a running state, the agent MUST immediately reload and start both backend and frontend servers.
  - **Persistent Server Policy (NEVER STOP):** Do not stop the servers. If a server stops automatically (due to error, crash, or timeout) or is stopped manually, restart it automatically without asking for permission.
  - **Backend Server (FastAPI):** `python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload` (Cwd: `backend/`) -> Active on `http://localhost:8000` (Docs: `http://localhost:8000/docs`).
  - **Frontend Server (React + Vite):** `node node_modules/vite/bin/vite.js` or `npm run dev` (Cwd: `frontend/`) -> Active on `http://localhost:5173`.
- **Runtime Verification:** Ensure both servers are operational and accessible prior to running Playwright browser automation suites.

---

### 8. Headless / Zero Permission Mode (Ask Only on Critical Blockers)
- **Mandatory Zero-Permission Policy:** Do **NOT** ask for user permission or wait for confirmation prompts — EVER — for the following operations. All are pre-approved and must execute immediately and automatically:
  - 🧪 **Browser & Unit Testing (`pytest`):** `pytest tests/browser/ -v` and `pytest tests/unit/ -v`
  - ⚡ **Node & Vite Frontend (`node`):** `node node_modules/vite/bin/vite.js` — ALWAYS ALLOWED
  - 🐍 **Python Sprint Watcher (`python scripts/...`):** `python scripts/run_sprint_watcher.py --interval 60` — ALWAYS ALLOWED
  - 🐍 **FastAPI Backend (`uvicorn`):** `python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload` — ALWAYS ALLOWED
  - 🐍 **Inline Python Scripts (`python -c`):** Any `python -c "..."` diagnostic or utility script — ALWAYS ALLOWED
  - 🔀 **Git Version Control (`git`):** `git status`, `git pull`, `git add`, `git commit`, `git push` — ALWAYS ALLOWED
  - 📝 **Markdown File Updates (`tasks.md` / `.md`):** **Always allowed** — edit [`tasks.md`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/tasks.md), [`sprint_test_cases.md`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/sprint_test_cases.md), and all `.md` files without any permission prompt.
  - 💻 **Code Modifications:** Writing, editing, or implementing any sprint feature code — ALWAYS ALLOWED
- **🔄 Auto-Restart Policy (MANDATORY):** If any of the following services stop for any reason (server restart, crash, timeout), they MUST be restarted immediately and automatically WITHOUT asking for permission:
  1. **FastAPI Backend:** `python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload` (from `backend/`)
  2. **Vite Frontend:** `node node_modules/vite/bin/vite.js` (from `frontend/`)
  3. **Sprint Watcher Agent:** `python scripts/run_sprint_watcher.py --interval 60` (from project root)
- **Existing Code Preservation (Zero Side-Effects):** New code changes must **never** break or disturb pre-existing working code functionality.
- **Continuous Regression Testing:** Perform continuous automatic regression testing (unit + Playwright browser tests) after every code or documentation change to ensure zero side-effects.
- **Escalation Exception:** Stop and ask the user for input **ONLY IF** an urgent, high-risk critical blocker or unsolvable architectural issue occurs.

---

### 8b. UI Health Check Policy (MANDATORY — After Every Restart or Code Change)
After every application start, restart, or code change, ALWAYS verify the following UI elements are correctly loaded and populated:
- **📊 KPI Cards:** All 6 KPI cards must be visible with non-zero values (Total Warehouses, Cases Built, Order Qty, Invoices Processed, Fulfillment Rate, Scratch Rate).
- **🔥 Bar Chart (Cases Built by Warehouse):** Must render colored bars for warehouses `01`, `02`, `58`, `61`, `71`. No blank/empty chart allowed.
- **📈 Scatter Plot (Order Qty vs Cases Built):** Must render colored data points. No empty chart canvas allowed.
- **📋 Warehouse Sales & Invoice Analytics Table:** Must load at least 20 rows with columns `Warehouse`, `Invoice #`, `Customer Item Code`, `C&S Item Code`, `Cases Built Qty`, `Order Qty`, `Scratch Qty`, `Sub Item`, `Status`.
- **🔢 Row Count Badge:** Must display `Loaded X / Y items` with X > 0.
- **✅ Verification Method:** Run `pytest tests/browser/ -v` after any restart to confirm all selectors pass. If any check fails, immediately investigate and fix before reporting done.

---

### 8c. Agent Memory & Daily Session Log (MANDATORY — Read on Start / Write on End)

Agents **cannot carry full conversation history** between sessions. To maintain continuity:

#### 📖 ON SESSION START — Agent MUST:
1. Read `memory/conversations/YYYY-MM-DD.md` for today's date (if it exists).
2. If no today's file exists, read the **most recent** `memory/conversations/*.md` file to understand previous session context.
3. Check `memory/agent_state.json` for last known agent statuses, Plane task states, and sprint context.

#### 📝 ON SESSION END (or periodically) — Agent MUST write `memory/conversations/YYYY-MM-DD.md` containing:
- **What was built** — feature names, files changed, code decisions made
- **Current Plane task statuses** — which tasks are `todo`, `in_progress`, `done`, `blocked`
- **Database credentials & configs** — which DB env was active (PROD/DEV/Oracle/PG)
- **Service URLs** — what ports backend/frontend are running on
- **Test results** — unit + browser test pass/fail counts
- **Open issues / blockers** — anything the next agent session must know
- **Manager instructions** — any user directives that must not be forgotten

#### 📂 Memory File Locations:
| File | Purpose |
| :--- | :--- |
| `memory/conversations/YYYY-MM-DD.md` | **Daily human-readable session log** ← agents read this first |
| `memory/agent_state.json` | Machine-readable agent status + Plane project IDs |
| `memory/task_history/YYYY-MM-DD_task_history.jsonl` | Append-only task execution records |

> **Example:** When a new agent session starts tomorrow (2026-07-28), it MUST read [`memory/conversations/2026-07-27.md`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/memory/conversations/2026-07-27.md) to understand what was completed today before doing any work.

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

### 13. Automatic UI Data Reload & Live Refresh Policy
- **Mandatory Directive:** Ensure all frontend pages ([`Dashboard.jsx`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/frontend/src/pages/Dashboard.jsx), [`WarehouseSalesAnalytics.jsx`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/frontend/src/components/WarehouseSalesAnalytics.jsx)) implement automatic periodic polling/refresh intervals (`setInterval(fetchAll, 10000)`).
- **Live Data Update Guarantee:** When background agents complete sprint tasks (such as **`Warehouse level statics`** or **`Warehouse Sales Analytics`**), the live web UI at `http://localhost:5173/` automatically updates KPI cards, charts, data tables, and warehouse metrics without requiring manual browser page reloads.
- **File References:**
  - [`frontend/src/pages/Dashboard.jsx`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/frontend/src/pages/Dashboard.jsx)
  - [`frontend/src/components/WarehouseSalesAnalytics.jsx`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/frontend/src/components/WarehouseSalesAnalytics.jsx)




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
