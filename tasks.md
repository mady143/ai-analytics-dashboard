# 📋 System Task Specification & Architecture (`tasks.md`)

This document outlines the mandatory operational requirements, daily tasks, component implementation details, and workspace file paths for the **AI Analytics Dashboard Autonomous Agent Network**.

---

## 🚨 Section 1: Mandatory Tasks (Autonomous Execution)

The system is configured to perform all mandatory tasks autonomously **WITHOUT asking for permission prompts** (except in critical blocker scenarios):

### 1. Daily Git Synchronization & Automatic Conflict Resolution (Morning & Evening)
- **Morning (Start of Day):** Run `python scripts/start_of_day.py` or `git pull origin main` to pull latest remote changes before work begins.
- **Automatic Merge Conflict Resolution:** If any git merge or rebase conflicts occur during pull, automatically analyze conflicting files, resolve all conflicts cleanly, stage changes (`git add .`), and complete the commit.
- **Task Completion & Autonomous Git Push / PR:** Automatically pull remote changes (`git pull origin main`), stage changes (`git add .`), commit with a descriptive message, create pull requests when applicable, and push updated code to remote GitHub (`mady143/ai-analytics-dashboard`) upon task completion or at the end of the day.
- **File References:**
  - [`scripts/start_of_day.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/scripts/start_of_day.py)
  - [`scripts/end_of_day.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/scripts/end_of_day.py)
  - [`agents/git_agent.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/agents/git_agent.py)

### 1b. Automatic README.md Documentation Maintenance Mandate (2026-07-28)
- **Mandatory Documentation Directive:**
  - The AI AGENT MUST automatically maintain and update [`README.md`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/README.md) whenever new features, backend API endpoints, multi-database architecture parameters, or agent processes are added or updated.
  - Keep `README.md` synchronized with the active project structure, API endpoints table, background agent list, and testing instructions.

---

## 🖥️ Section 1c: Screen-by-Screen Modular Task & Component Breakdown

The application is structured into distinct, modular UI Screens and Component Services. Each component domain has its own dedicated `.md` task file in the [`tasks/`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/tasks/) directory:

- 📄 [`tasks/task_1_header_controls.md`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/tasks/task_1_header_controls.md) — Global Parameter & Header Control Panel
- 📄 [`tasks/task_2_kpi_cards.md`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/tasks/task_2_kpi_cards.md) — Executive Warehouse KPI Summary Cards
- 📄 [`tasks/task_3_charts_analytics.md`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/tasks/task_3_charts_analytics.md) — Warehouse Analytics & Data Visualization Charts
- 📄 [`tasks/task_4_data_table.md`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/tasks/task_4_data_table.md) — Warehouse Item Level & Procurement Data Table
- 📄 [`tasks/task_5_database_service.md`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/tasks/task_5_database_service.md) — Multi-Database Engine & SQL Execution Service
- 📄 [`tasks/task_6_agents_and_mcp.md`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/tasks/task_6_agents_and_mcp.md) — Autonomous Agent Network & Background Services
- 📄 [`tasks/task_7_git_automation.md`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/tasks/task_7_git_automation.md) — Pre-Approved Git Automation & Synchronization
- 📄 [`tasks/task_8_parallel_background_agents.md`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/tasks/task_8_parallel_background_agents.md) — Continuous Parallel Background Agent Fleet
- 📄 [`tasks/task_9_continuous_application_uptime.md`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/tasks/task_9_continuous_application_uptime.md) — Continuous Application Server Uptime
- 📄 [`tasks/task_10_end_to_end_parameter_testing.md`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/tasks/task_10_end_to_end_parameter_testing.md) — Interactive Browser Parameter Combination Testing & Strict Quality Gate Push Policy
- 📄 [`tasks/task_11_inventory_risk_forecast.md`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/tasks/task_11_inventory_risk_forecast.md) — Inventory Risk Forecast Component (Queued / Hidden from UI for sequential build)
- 📄 [`tasks/task_12_date_range_parameters.md`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/tasks/task_12_date_range_parameters.md) — Date Range Parameter Component (Queued / Hidden from UI for sequential build)
- 📄 [`tasks/task_13_clean_icons_design_system.md`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/tasks/task_13_clean_icons_design_system.md) — Icon System Cleanup & Standardized Design System
- 📄 [`tasks/task_14_ai_data_copilot.md`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/tasks/task_14_ai_data_copilot.md) — Natural Language AI Data Copilot Component & Query Service
- 📄 [`tasks/task_15_anomaly_alert_panel.md`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/tasks/task_15_anomaly_alert_panel.md) — Real-Time Anomaly & Risk Alert Panel Component

> ### ⚠️ TASK 19 — MANDATORY: AI Copilot Date-Agnostic Rule + Dashboard Date-Strict Rule [ALWAYS ENFORCE]
> - **AI Data Copilot (`/api/analytics/ai-copilot`)** → **MUST NOT use the global date (`oerdte`) when querying data.** It must always query the **full dataset across ALL dates** so it can always return meaningful results regardless of what date is selected in the header.
> - **Dashboard / Charts / Table / KPI / Anomaly APIs** → **MUST use the global date (`oerdte`) parameter** sent from the header. Data on all regular views is date-filtered by the selected Order Date.
> - **Rule**: The AI Copilot answers NLP questions about the warehouse using all available data. The date picker in the header controls all other views ONLY.
> - **Files**: [`frontend/src/components/AiDataCopilot.jsx`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/frontend/src/components/AiDataCopilot.jsx), [`backend/routers/analytics.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/backend/routers/analytics.py)
> ### ⚠️ TASK 21 — MANDATORY: Real-Time Agent Task Activity & Sprint Pickup Visibility System [HIGH PRIORITY]
> - **Problem**: Agents running in background loops previously overwrote `current_task` in `agent_state.json` with static generic strings (e.g. `"Autonomous Builder Agent Active"`), hiding active sprint task titles and IDs picked up from Plane/Sprint. Furthermore, the UI sidebar only displayed `status: "running"` without rendering the active task details.
> - **Solution**:
>   1. **Preserve Dynamic Task State**: Fixed [`agents/memory_manager.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/agents/memory_manager.py) (`get_dynamic_agent_statuses()`) so active task titles (e.g. `"🔨 Implementing #AAD-5: Fix date filter"`) are preserved across polling cycles instead of being overwritten with static text.
>   2. **Sidebar Live Task Display**: Updated [`frontend/src/components/Sidebar.jsx`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/frontend/src/components/Sidebar.jsx) to display `current_task` text under each agent with live `WORKING ⚡` status indicators, dynamic highlighting, and full title tooltips.
>   3. **Autonomous Agent Task Pickup Stream Component**: Built [`frontend/src/components/AgentTaskActivityTracker.jsx`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/frontend/src/components/AgentTaskActivityTracker.jsx) and embedded it into [`Dashboard.jsx`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/frontend/src/pages/Dashboard.jsx). It displays currently executing tasks, active agent phases (`1. Picked Up` → `2. Building` → `3. Testing` → `4. Done`), and a recent activity task pickup log stream.
> ### ⚠️ TASK 22 — MANDATORY: Universal Fuzzy NLP Intent Classifier & Typo-Resilient Task Pickup Engine [HIGH PRIORITY]
> - **Problem**: Relying solely on exact keyword matching previously caused tasks with typos (e.g. `pagenation`, `fecth`, `stastistics`) or natural language statement phrasing to be skipped or miscategorized.
> - **Solution**:
>   1. **Universal Fuzzy Classifier**: Implemented `classify_task_intent_and_intent_map(task_title, description)` in [`agents/builder_agent.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/agents/builder_agent.py). It normalizes typos, fuzzy tokens, statements, and screenshot notes into 7 distinct domain intent classes (`PAGINATION_AND_TOTAL_RECORDS`, `DATE_PARAMETER_FILTERING`, `AI_COPILOT_DATE_AGNOSTIC_QUERY`, `SCRATCH_QUANTITY_ANOMALY_ALERTS`, `CHARTS_AND_VISUALIZATION_ALIGNMENT`, `NAVBAR_AND_SIDEBAR_NAVIGATION`, `MULTI_TARGET_DATABASE_ARCHITECTURE`).
>   2. **Expanded NLP Taxonomy**: Expanded [`memory/nlp_taxonomy.json`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/memory/nlp_taxonomy.json) with learned keywords and fuzzy synonym arrays.
>   3. **100% Task Pickup Guarantee**: Guaranteed that every task created in Plane/Sprint is picked up by `sprint_watcher_agent.py`, classified by `builder_agent.py`, built, verified by `tester_agent.py`, marked `done`, and auto-pushed to GitHub.
> - **Status**: ✅ IMPLEMENTED & ENFORCED 2026-07-30

---

### 📌 TASK 20 — Full E2E + Unit Test Suite: Component Validation & Regression Prevention (`#full-e2e-testing`) [HIGH PRIORITY]

**Goal:** Run automated tests against every UI component and API endpoint to catch regressions. Must be run after every code change.

> ### ⚠️ MANDATORY: Fallback Date Behavior Rule (ALWAYS ENFORCE — DO NOT BREAK)
> **Source:** [`backend/app/warehouse_service.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/backend/app/warehouse_service.py) line 255
>
> **Rule:** When the selected `oerdte` has **NO records** in the DB (e.g., today `20260730` returns empty from `SELECT DISTINCT oewhse FROM sptn_sales_data WHERE oerdte='20260730'`):
> - The backend automatically re-queries with `oerdte=""` (all dates) and returns the **most recent date with data**
> - `filters_applied.fallback_used = True` and `filters_applied.effective_date` = the actual date used
> - The UI **must still show real data** — showing zeros or blank KPIs is a BUG
>
> **Tests MUST account for this:** Never fail a test just because today has no data — verify that the FALLBACK delivers data.
>
> **AI Copilot is different:** It ALWAYS queries `oerdte=""` directly — it never needs the fallback path because it bypasses date filtering entirely.

#### 20.1 — Unit Test Cases (`tests/unit/test_task19_20_copilot_date_rules.py`)

| # | Test Case | Rule Verified |
|---|-----------|---------------|
| TC-UNIT-01 | Copilot ignores date `19990101` → returns real data across all dates | Copilot is date-agnostic |
| TC-UNIT-02 | Copilot with `oerdte=""` returns full dataset results | Frontend sends empty date correctly |
| TC-UNIT-03 | KPI API with `oerdte=KNOWN_DATE` returns >= 4 KPIs | Dashboard uses date param |
| TC-UNIT-04 | Bar chart API with `oerdte` returns chart data | Dashboard uses date param |
| TC-UNIT-05 | Scatter chart API with `oerdte` returns scatter data | Dashboard uses date param |
| TC-UNIT-06 | Warehouse stats API with `oerdte` returns paginated items | Dashboard uses date param |
| TC-UNIT-07 | Warehouse stats with `oerdte=""` returns full all-dates data | Empty date = full dataset |
| TC-UNIT-08 | Anomaly API with `oerdte` returns alerts | Anomaly uses date param |
| TC-UNIT-09 | `/api/agents/status` returns >= 5 agents all `status=running` | Self-healing agent watchdog |
| TC-UNIT-10 | `/api/health` returns `status=healthy` | Server health |
| TC-UNIT-11 | Copilot "Warehouse 58" query returns `filtered_whse=58` | NLP warehouse extraction |
| TC-UNIT-12 | Copilot "High Scratch" returns `filter_scratch=True` | NLP scratch extraction |

#### 20.2 — Browser (Playwright) Test Cases (`tests/browser/test_full_e2e_component_suite.py`)

| # | Test Case | Validates |
|---|-----------|-----------|
| TC-01 | Default date auto-applied on page load (today's date pre-filled) | Default date behavior |
| TC-02 | KPI cards show real numbers (not `...` placeholder) | KPI data load |
| TC-03 | Bar chart + Scatter chart render SVG elements | Chart rendering |
| TC-04 | Changing date → Submit triggers API calls with new date | Date change propagation |
| TC-05 | Warehouse filter input narrows table to matching rows | Whse filter |
| TC-06 | **CRITICAL**: Copilot sends `oerdte=''` — never the global date | TASK 19 rule |
| TC-07 | Copilot query returns "AI Copilot Finding" result card | Copilot result |
| TC-08 | Quick pills (High Scratch, Pending Transfers) trigger copilot | Copilot pills |
| TC-09 | Data table has >= 1 row for known-data date | Table population |
| TC-10 | Agent status sidebar shows all agents visible | Agent monitoring |
| TC-11 | Anomaly & Risk Alerts panel renders | Anomaly panel |
| TC-12 | DB switch pg_dev → oracle_dev triggers API calls with oracle_dev | DB switch |
| TC-13 | Copilot "Apply Filter" button updates data table | Copilot→Table filter |
| TC-14 | Bar chart X-axis ticks == Total Warehouses KPI count | Chart/KPI alignment |

#### 20.3 — How to Run All Tests
```bash
# Unit tests
cd backend && python -m pytest ../tests/unit/ -v --tb=short

# Browser tests (requires backend + frontend running)
python -m pytest tests/browser/ -v --tb=short
```

#### 20.4 — Test Files
- [`tests/unit/test_task19_20_copilot_date_rules.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/tests/unit/test_task19_20_copilot_date_rules.py) — 12 unit tests
- [`tests/browser/test_full_e2e_component_suite.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/tests/browser/test_full_e2e_component_suite.py) — 14 browser tests

#### 20.5 — ✅ Live Test Results (2026-07-30 09:49 EST)

**Unit Tests — 12/12 PASSED ✅** (`9.95s`)

| # | Test | Result |
|---|------|--------|
| TC-UNIT-01 | Copilot ignores past date `19990101` → queries full dataset | ✅ PASSED |
| TC-UNIT-02 | Copilot with `oerdte=""` returns full dataset | ✅ PASSED |
| TC-UNIT-03 | KPI API with date param returns >= 4 KPIs | ✅ PASSED |
| TC-UNIT-04 | Bar chart API with date returns chart data | ✅ PASSED |
| TC-UNIT-05 | Scatter chart API with date returns scatter data | ✅ PASSED |
| TC-UNIT-06 | Warehouse stats API with date returns items | ✅ PASSED |
| TC-UNIT-07 | Warehouse stats no-date returns full data | ✅ PASSED |
| TC-UNIT-08 | Anomaly API with date returns alerts | ✅ PASSED |
| TC-UNIT-09 | `/api/agents/status` → all 6 agents `running` | ✅ PASSED |
| TC-UNIT-10 | `/api/health` returns `healthy` | ✅ PASSED |
| TC-UNIT-11 | Copilot Warehouse 58 query → `filtered_whse=58` | ✅ PASSED |
| TC-UNIT-12 | Copilot scratch query → `filter_scratch=True` | ✅ PASSED |

**Browser E2E Tests — 14/14 PASSED ✅** (`63.00s`, Chromium)

| # | Test | Result |
|---|------|--------|
| TC-01 | Default date auto-applied on page load (dynamic from UI) | ✅ PASSED |
| TC-02 | KPI cards show real numbers (not `...` placeholder) | ✅ PASSED |
| TC-03 | Bar + Scatter charts render SVG | ✅ PASSED |
| TC-04 | Date change → Submit → API calls fired with new date | ✅ PASSED |
| TC-05 | Warehouse 58 filter narrows table rows | ✅ PASSED |
| TC-06 | **CRITICAL**: Copilot sends `oerdte=''` NOT the UI date | ✅ PASSED |
| TC-07 | Copilot returns "AI Copilot Finding" result card | ✅ PASSED |
| TC-08 | Quick pills trigger copilot results | ✅ PASSED |
| TC-09 | Data table has >= 1 row for UI-selected date | ✅ PASSED |
| TC-10 | Agent status sidebar visible with all agents | ✅ PASSED |
| TC-11 | Anomaly & Risk Alerts panel renders | ✅ PASSED |
| TC-12 | DB switch pg_dev → oracle_dev triggers API reload | ✅ PASSED |
| TC-13 | Copilot "Apply Filter" button updates data table | ✅ PASSED |
| TC-14 | Bar chart ticks == Total Warehouses KPI count | ✅ PASSED |

> **Total: 26/26 tests PASSED — 0 FAILED — 0 ERRORS** 🎉

---

### 📌 TASK 1 — Global Parameter & Header Control Panel (`#global-header-controls`)
- **Dedicated Task File:** [`tasks/task_1_header_controls.md`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/tasks/task_1_header_controls.md)
- **Screen / Component Location:** Top Navigation Header ([`Dashboard.jsx`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/frontend/src/pages/Dashboard.jsx))
- **Sub-Task 1.1:** 📅 **Order Date Picker (`#global-date-picker`)** — Select target order date (`oerdte` in `YYYY-MM-DD` format).
- **Sub-Task 1.2:** 🗄️ **Target DB Selector (`#global-db-selector`)** — Dropdown menu supporting `pg_prod`, `pg_dev`, `oracle_dev`, `oracle_f1`, `oracle_prod`.
- **Sub-Task 1.3:** 🚀 **Submit Button (`#submit-db-btn`)** — `onClick` / `onSubmit` form submission handler executing real-time backend API queries and updating UI state.
- **Sub-Task 1.4:** ⚡ **Active Target DB Status Badge** — Visual badge displaying active target database (`⚡ Active: PG_PROD` / `⚡ Active: PG_DEV`).

---

### 📌 TASK 2 — Executive Warehouse KPI Summary Cards (`#kpi-grid`)
- **Screen / Component Location:** Top Summary Grid ([`KPICard.jsx`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/frontend/src/components/KPICard.jsx))
- **Sub-Task 2.1:** 🏢 **Total Warehouses KPI Card** — Displays distinct SQL count of active warehouses for selected date.
- **Sub-Task 2.2:** 📦 **Cases Built KPI Card** — Displays sum of `cases_built_qty` across active warehouses.
- **Sub-Task 2.3:** 📋 **Original Order Qty KPI Card** — Displays sum of `original_order_qty`.
- **Sub-Task 2.4:** 📄 **Invoices Processed KPI Card** — Displays distinct count of invoice numbers (`oeinvo`).

---

### 📌 TASK 3 — Warehouse Analytics & Data Visualization Charts (`#charts-section`)
- **Screen / Component Location:** Main Analytics View ([`Dashboard.jsx`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/frontend/src/pages/Dashboard.jsx))
- **Sub-Task 3.1:** 📊 **Cases Built Breakdown Bar Chart** — Recharts bar chart plotting cases built per warehouse.
- **Sub-Task 3.2:** 📈 **Order Quantity vs Cases Built Scatter Plot** — Recharts scatter plot showing order volume vs fulfillment.
- **Sub-Task 3.3:** 🌡️ **Correlation Heatmap Matrix** — Feature correlation heatmap matrix.
- **Sub-Task 3.4:** 📉 **Distribution Histogram Chart** — Quantity distribution histogram.

---

### 📌 TASK 4 — Warehouse Item Level & Procurement Data Table (`#warehouse-table-container`)
- **Screen / Component Location:** Detailed Data View ([`WarehouseSalesAnalytics.jsx`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/frontend/src/components/WarehouseSalesAnalytics.jsx))
- **Sub-Task 4.1:** 📋 **Line Items Data Grid** — Displays `Warehouse #`, `Order Date (oerdte)`, `Batch ID`, `Invoice #`, `Customer Item Code`, `C&S Item Code`, `Cases Built`, `Order Qty`, `Scratch Qty`, `Sub Item (sl_itm_ind)`, `Fulfillment Status`.
- **Sub-Task 4.3:** 📅 **Order Date (`oerdte`) Table Column** — Explicit `Order Date` column rendered directly at table level in `WarehouseSalesAnalytics.jsx`.
- **Sub-Task 4.4:** 🔴 **Dedicated Scratch Quantity Data Filtering (`only_scratches`)** — When High Scratch Quantity is selected in Copilot or Anomaly panel, the table filters strictly to rows with `whs_scrtch_qty_stg > 0`.
- **Sub-Task 14.3:** ⚡ **Page-Wide Copilot Filter & Dynamic Date Propagation** — Any AI Copilot prompt or filter directive automatically updates `appliedDate` and `tableFilters` page-wide across KPI Cards, Bar Chart, Scatter Plot, Anomaly Alert Panel, and Data Table.
- **Sub-Task 14.4:** 🤖 **AI Copilot NLP Keyword Training & Natural Language Query Model Engine** — Train & expand ML model query intent classification across natural language synonyms (scratch, shortage, damaged, missing, transfer, pending, volume spike).
- **Sub-Task 15.2:** 🚨 **Dynamic Red Critical Anomaly Card for Scratch Quantities** — When scratch items are detected, the Anomaly Alert Panel dynamically renders a **🔴 Critical Red Alert Card** displaying exact Warehouse # and Scratch Count instead of green Nominal baseline.

---

### 📌 TASK 5 — Multi-Database Engine & SQL Execution Service (`#backend-db-service`)
- **Service Location:** Backend Layer ([`warehouse_service.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/backend/app/warehouse_service.py) & [`charts.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/backend/routers/charts.py))
- **Sub-Task 5.1:** ⚡ **Strict Parameter SQL Execution** — Direct PostgreSQL queries on `sptn_sales_data ssd` matching exact parameters (`oerdte`, `batch_id`, `oewhse`, `oeinvo`).
- **Sub-Task 5.2:** 🚫 **Zero Synthetic Data Fallback Policy** — 0 database records strictly returns 0 UI rows without generating fake data.
- **Sub-Task 5.3:** ⏱️ **15-Second Thread-Safe TTL Query Cache (`_fetch_from_postgres_cached`)** — Prevents parallel API requests from blocking database threads or freezing the UI.

---

### 📌 TASK 6 — Autonomous Agent Network & Background Services (`#background-agent-system`)
- **Service Location:** Agent Layer ([`agents/`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/agents/) & [`scripts/`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/scripts/))
- **Sub-Task 6.1:** 🤖 **Sprint Watcher Agent** (`python scripts/run_sprint_watcher.py --interval 60`) — Continuous 60s background task and comment watcher.
- **Sub-Task 6.2:** 🚀 **FastAPI Backend API Server** (`python -m uvicorn main:app` at `:8000`).
- **Sub-Task 6.3:** 💻 **Vite Frontend Dev Server** (`npm run dev` at `:5173`).
- **Sub-Task 6.4:** 🔌 **MCP Server Fleet** (`plane`, `github`, `memory`, `browser` MCP servers).
- **Sub-Task 6.5:** 🔀 **Autonomous Git Synchronization & Remote Push** (`git pull --rebase`, `git add .`, `git commit`, `git push origin main`).

---

### 📌 TASK 11 — Inventory Risk Forecast Component (`#inventory-risk-forecast`)
- **Dedicated Task File:** [`tasks/task_11_inventory_risk_forecast.md`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/tasks/task_11_inventory_risk_forecast.md)
- **Status:** Hidden from active UI layout (`Dashboard.jsx`) and queued in `tasks.md` for step-by-step sequential build.
- **Sub-Task 11.1:** Backend risk calculation endpoint `/api/analytics/inventory-risk`.
- **Sub-Task 11.2:** Inventory stockout anomaly index gauge and alert table per warehouse ID.

---

### 📌 TASK 12 — Date Range Parameter Component (`#date-range-parameters`)
- **Dedicated Task File:** [`tasks/task_12_date_range_parameters.md`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/tasks/task_12_date_range_parameters.md)
- **Status:** Hidden from active UI layout (`Dashboard.jsx`) and queued in `tasks.md` for step-by-step sequential build.
- **Sub-Task 12.1:** From-Date (`from_date`) and To-Date (`to_date`) multi-date range picker integration.
- **Sub-Task 12.2:** SQL query support for `oerdte BETWEEN from_date AND to_date` across all analytics endpoints.

---

### 📌 TASK 13 — Icon System Cleanup & Standardized Design System (`#icon-design-system`)
- **Dedicated Task File:** [`tasks/task_13_clean_icons_design_system.md`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/tasks/task_13_clean_icons_design_system.md)
- **Status:** In Progress — Informal emojis removed from UI headers, labels, and table badges; standardizing on modern `lucide-react` SVG vector icon system.
- **Sub-Task 13.1:** Clean up informal emoji icons in `Dashboard.jsx`, `Sidebar.jsx`, `WarehouseSalesAnalytics.jsx`, and `WarehouseAnalytics.jsx`.
- **Sub-Task 13.2:** Maintain consistent 16-20px Lucide vector icon sizing with design token colors.

---

### 📌 TASK 16 — Human Engineering Sub-Task Decomposition & Online Model Learning Engine (`#subtask-decomposition-engine`)
- **Service Location:** Agent & Router Layer ([`agents/builder_agent.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/agents/builder_agent.py), [`backend/routers/analytics.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/backend/routers/analytics.py), [`memory/nlp_taxonomy.json`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/memory/nlp_taxonomy.json))
- **Sub-Task 16.1:** 📋 **Human-Like 7-Step Sub-Task Decomposition** — Automatically break down incoming Plane tasks into 7 structured engineering sub-tasks (`create_human_subtasks`) before execution.
- **Sub-Task 16.2:** 🧠 **Online NLP Keyword Learning & Taxonomy Storage** — Dynamically capture unknown user prompt terms (`memory/nlp_taxonomy.json`) and retrain intent classification live (`learn_unknown_keywords`).
- **Sub-Task 16.3:** ⚡ **Dynamic Real-Time OS Process Status Scanning** — OS process table inspection (`psutil`) dynamically updates status (`running`/`idle`) in `agent_state.json` and UI sidebar.
- **Sub-Task 16.4:** 📅 **Order Date (`oerdte`) Column at Table Level** — Explicit `Order Date` column rendered directly beside Warehouse in `WarehouseSalesAnalytics.jsx`.
- **Sub-Task 16.5:** 🔴 **Real-Time Red Critical Scratch Anomaly Card** — Render 🔴 Critical Red Alert card for scratch items displaying exact warehouse and date instead of green Nominal baseline.

---

### 📌 TASK 17 — Autonomous Fleet Launcher & Sequential Startup Script (`#autonomous-launcher-script`)
- **Script Location:** Deployment Layer ([`start_all_services.bat`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/scripts/start_all_services.bat) & [`start_all_services.sh`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/scripts/start_all_services.sh))
- **Sub-Task 17.1:** 📦 **Sequential Step 1 — Python Dependencies** — `pip install -r requirements.txt`.
- **Sub-Task 17.2:** 🟢 **Sequential Step 2 — Frontend Node Modules** — `npm install` inside `frontend/` directory.
- **Sub-Task 17.3:** 🎭 **Sequential Step 3 — Playwright Browser Binaries** — `python -m playwright install chromium`.
- **Sub-Task 17.4:** 🔀 **Sequential Step 4 — Git Sync & Remote Pull** — `git pull origin main`.
- **Sub-Task 17.5:** 🌙 **Sequential Step 5 — End-of-Day Git Push Script** — `python scripts/end_of_day.py`.
- **Sub-Task 17.6:** ⚙️ **Sequential Step 6 — FastAPI Backend Server** — `python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000`.
- **Sub-Task 17.7:** 💻 **Sequential Step 7 — Vite Frontend Server** — `npm run dev -- --host 0.0.0.0`.
- **Sub-Task 17.8:** 🤖 **Sequential Step 8 — Sprint Watcher Agent** — `python scripts/run_sprint_watcher.py --interval 60`.
- **Sub-Task 17.9:** 🔀 **Sequential Step 9 — Orchestrator Agent** — `python agents/orchestrator_agent.py`.
- **Sub-Task 17.10:** 🔨 **Sequential Step 10 — Builder Agent** — `python agents/builder_agent.py --task-id AAD-AUTO`.
- **Sub-Task 17.11:** 🧪 **Sequential Step 11 — Tester Agent Test Runner** — `python agents/tester_agent.py` (Pytest Unit + Playwright Browser E2E).
- **Sub-Task 17.12:** 🔌 **Sequential Step 12 — MCP Server Fleet** — `plane_agent`, `git_agent`, `memory_manager`, `browser`.

---

### 📌 TASK 18 — Mandatory Agent Health Watchdog & Auto-Restart System (`#agent-health-watchdog`) [HIGH PRIORITY]
- **Service Location:** Agent Layer ([`agents/orchestrator_agent.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/agents/orchestrator_agent.py), [`agents/memory_manager.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/agents/memory_manager.py))
- **Sub-Task 18.1:** 🧠 **Memory Agent Persistent Tracking** — Add Memory Agent (`python -m agents.memory_manager`) to startup launchers (`.bat` / `.sh`) and process status monitor.
- **Sub-Task 18.2:** 🛡️ **Orchestrator Watchdog Health Loop (`watchdog_health_loop`)** — Continuous OS process table inspection (`psutil`) checking health of `sprint_watcher`, `builder`, `tester`, `orchestrator`, `memory`, `git`.
- **Sub-Task 18.3:** 🔄 **Autonomous Auto-Restart Engine** — If any background agent crashes, stops, or goes unexpectedly idle when required, Watchdog automatically re-spawns the process and updates state back to `running` with zero downtime!
- **Sub-Task 18.4:** 🚀 **Full Server & Fleet Watchdog Script (`scripts/agent_watchdog.py`)** — Dedicated Supervisor script that monitors HTTP health endpoints (FastAPI `:8000`, Vite `:5173`) and background agent processes, auto-restarting the entire server and agent fleet whenever idle failure or downtime is detected.
- **Sub-Task 18.5:** 👁️ **Continuous 24/7 Agent Monitoring** — Continuous real-time OS process table inspection (`psutil`) verifying whether all 6 agents (`Sprint Watcher`, `Builder`, `Tester`, `Memory`, `Git`, `Orchestrator`) are active and running continuously without interruption.

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
- **Mandatory Autonomous Agent Management Mandate (2026-07-28):**
  - **Zero User Manual Execution:** The USER will NOT manually execute `python scripts/run_sprint_watcher.py --interval 60`.
  - **100% Agent Ownership:** The AI AGENT is strictly responsible for launching, managing, monitoring, and keeping `run_sprint_watcher.py --interval 60` continuously running in background mode.
  - If `sprint_watcher` is ever detected as stopped, idle, or not running, the agent MUST immediately restart `python scripts/run_sprint_watcher.py --interval 60` autonomously.
- **File References:**
  - [`scripts/run_sprint_watcher.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/scripts/run_sprint_watcher.py)
  - [`agents/sprint_watcher_agent.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/agents/sprint_watcher_agent.py)
  - [`memory/agent_state.json`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/memory/agent_state.json)


---

### 2b. Mandatory Continuous Background Services, Agents & MCP Servers (ALWAYS RUNNING)
The AI AGENT is 100% responsible for keeping ALL background services, autonomous agents, and MCP servers continuously running in active background mode **WITHOUT manual user intervention**:

#### ⚡ Mandatory "run the application" Execution & 60-Second Agent Loop Directive:
Whenever the user specifies **"run the application"** (or initiates application execution), the system MUST autonomously execute the following complete workflow:
1. 🚀 **Launch Core Servers:**
   - **Frontend Dev Server:** `npm run dev` (inside `frontend/`) ➔ [http://localhost:5173](http://localhost:5173)
   - **Backend FastAPI Server:** `python -m uvicorn main:app --host 127.0.0.1 --port 8000` (inside `backend/`) ➔ [http://127.0.0.1:8000](http://127.0.0.1:8000)
2. 🔄 **Activate 60-Second Agent Fleet Loop (`agents` in `memory/agent_state.json`):**
   - **Sprint Watcher (`sprint_watcher`):** `python scripts/run_sprint_watcher.py --interval 60` — continuous 60s polling of Plane tasks, user comments, and task state changes.
   - **Master Orchestrator (`orchestrator`):** Continuous task coordination and lifecycle management.
   - **Builder (`builder`):** Autonomous code implementation and file creation.
   - **Tester (`tester`):** Autonomous unit test (`pytest tests/unit/`) and browser test (`pytest tests/browser/`) execution.
   - **Git Agent (`git_agent`):** Autonomous morning pull (`git pull --rebase`) and commit/push (`git push origin main`).
3. 💾 **Live Status & Automatic Timestamp Bumping (`memory/agent_state.json` & `memory/conversations/YYYY-MM-DD.md`):**
   - Every 60 seconds / on each execution poll, agents MUST call `update_agent_status()` via [`agents/memory_manager.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/agents/memory_manager.py).
   - **Automatic Timestamp Updates:** Bumps `updated_at` (for individual agents), `last_updated`, and `last_active` timestamps in [`memory/agent_state.json`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/memory/agent_state.json) using ISO 8601 format (`YYYY-MM-DDTHH:MM:SS.ffffff`).
   - The REST API endpoint `GET /api/agents/status` reads `memory/agent_state.json` and serves real-time status and timestamps to the frontend [`Sidebar.jsx`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/frontend/src/components/Sidebar.jsx).
   - Log ongoing updates, test statistics, file modifications, and execution progress in [`memory/conversations/YYYY-MM-DD.md`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/memory/conversations/2026-07-29.md) and [`memory/task_history/YYYY-MM-DD_task_history.jsonl`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/memory/task_history/2026-07-28_task_history.jsonl).

#### 1. Core Background Application Services:
- **Frontend Dashboard Dev Server:** `npm run dev` (inside `frontend/`) ➔ [http://localhost:5173](http://localhost:5173)
- **Backend FastAPI API Server:** `python -m uvicorn main:app --host 127.0.0.1 --port 8000` (inside `backend/`) ➔ [http://127.0.0.1:8000](http://127.0.0.1:8000)

#### 2. Autonomous Agent Network:
- **Sprint Watcher Agent:** `python scripts/run_sprint_watcher.py --interval 60` (Continuous background polling every 60s)
- **Master Orchestrator Agent:** `agents/orchestrator_agent.py` (Continuous task coordination)
- **Builder Agent:** `agents/builder_agent.py` (Autonomous code implementation)
- **Tester Agent:** `agents/tester_agent.py` (Autonomous unit & browser testing)
- **Git Agent:** `agents/git_agent.py` (Autonomous morning pull & evening git push)

#### 3. Model Context Protocol (MCP) Servers (`mcp_servers/mcp_config.json`):
- **Plane Task Management MCP Server:** `agents.plane_agent` (Task lifecycle, comments, status sync)
- **GitHub Operations MCP Server:** `github-mcp-server` (Commits, pull requests, push operations)
- **Persistent Agent Memory MCP Server:** `agents.memory_manager` (Conversation state & task summary logging)
- **Browser Automation MCP Server:** `playwright` (UI testing & automated browser verification)

- **Mandatory Autonomous Directive:** The USER will NOT run these agent scripts or MCP servers manually. If any background agent or MCP service is detected as offline or stopped, the system MUST automatically restart it in background mode immediately.

---

### 3. End-to-End Autonomous Sprint Task Lifecycle & Sub-Task Execution Workflow

- **Mandatory End-to-End Lifecycle Mandate:** Whenever a new task or update is created/updated in the Plane sprint cycle (or requested by the user), the autonomous agent fleet MUST execute this exact **8-stage end-to-end lifecycle**:

  ```mermaid
  graph TD
      S1[1. Requirement Intake & Plane Sprint Polling] --> S2[2. Task Segregation into Modular Sub-Tasks]
      S2 --> S3[3. Builder Code Implementation]
      S3 --> S4[4. Application Server Launch & Reload]
      S4 --> S5[5. Automated Unit & Playwright Browser Testing]
      S5 --> S6[6. User Verification Request & Testing Review]
      S6 --> S7[7. Git Stage, Commit & Push to Remote Main]
      S7 --> S8[8. Close Task as Done in Plane Sprint & Update Memory]
  ```

  - **Stage 1 — Requirement Intake & Sprint Watching:** `sprint_watcher` polls Plane workspace every 60 seconds detecting new tasks, user comments, or updated issue descriptions.
  - **Stage 2 — Sub-Task Segregation & Architecture Breakdown:** `orchestrator` breaks down the main task into modular component sub-tasks (Backend APIs, Database SQL queries, Frontend Components, Unit & Browser Test specifications). Creates/updates dedicated task files in [`tasks/`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/tasks/) and logs sub-tasks in [`tasks.md`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/tasks.md).
  - **Stage 3 — Code Implementation:** `builder` agent writes/modifies source code in `backend/` and `frontend/` components.
  - **Stage 4 — Application Server Launch & Verification:** Launch/verify FastAPI Backend (`:8000`) and Vite React Frontend (`:5173`) are running and reloaded without runtime errors.
  - **Stage 5 — Automated Unit & Interactive Playwright Browser Testing:** `tester` agent executes unit tests `pytest tests/unit/ -v` AND interactive browser tests `pytest tests/browser/ -v` (100% PASS requirement).
    - 🌐 **Mandatory Interactive Browser Verification Mandate:** For every new feature or UI component (e.g., AI Copilot, Anomaly Alert Panel, Date Picker, Target DB selector), the test suite MUST simulate real user interactions in Chromium:
      1. ⌨️ **Form Inputs & Text Typing:** Typing prompts into input fields (e.g. entering queries into AI Copilot search box).
      2. 🖱️ **Button Clicks:** Clicking interactive buttons (e.g. "Ask AI", quick prompt pills, "Apply Filter to Table", anomaly alert "Filter Table" buttons, "Submit").
      3. 📜 **Page & Table Scrolling:** Scrolling down through the dashboard and table containers.
      4. 📊 **Dynamic Data Validation:** Asserting that AI finding cards populate, KPI numbers update, and warehouse table rows load dynamically without blank content or runtime errors.
  - **Stage 6 — User Testing & Verification Prompt:** Present completed sub-tasks and test results to the user for interactive testing review.
  - **Stage 7 — Git Automation & Remote Sync:** `git_agent` stages files (`git add .`), creates descriptive commit message, and pushes to remote GitHub repository (`git push origin main`).
  - **Stage 8 — Plane Task Closure & Memory Update:** 
    - 🚨 **Strict Task Closure Policy:** Tasks MUST NOT be marked `Done` or closed until ALL code changes, enhancements, unit tests, and Playwright browser tests pass 100%. If any test or feature issue remains unfixed, the task stays in `started` / `in progress` status and continues auto-fixing without closing prematurely!
    - **100% Dynamic Execution Timeout:** Test execution timeouts are 100% dynamic (`timeout=None` by default to run indefinitely until all unit tests, browser tests, and enhancements finish cleanly, or configured via `TEST_TIMEOUT_SECONDS` env var).
    - Mark task status as **`Done` / `Completed`** in Plane sprint cycle only after 100% verification, update [`memory/agent_state.json`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/memory/agent_state.json), and record session details in [`memory/conversations/YYYY-MM-DD.md`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/memory/conversations/2026-07-29.md).
       3. `Vite Frontend Dev Server` (`npm run dev`) is running on port `5173`.
       4. MCP Servers (`plane`, `github`, `memory`, `browser`) are active.
     - **Auto-Restart Rule:** If ANY process or agent is stopped, offline, or killed, the system MUST **automatically launch/restart it in background mode immediately** before touching any source code!
  1. 🛠️ **Step 1 — Code Implementation & File Changes:** Pick up task/issue, analyze requirements, and write/modify source code files in `backend/` and `frontend/`.
  2. 🔄 **Step 2 — Server Reload & Re-Deploy Verification:** Ensure backend FastAPI server (`uvicorn main:app`) and frontend Vite server (`npm run dev`) reload with the new changes, verifying API health check at `http://127.0.0.1:8000/api/health`.
  3. 🧪 **Step 3 — Run Unit Test Suite (`pytest tests/unit/`):** Execute full unit test suite to verify data models, endpoints, database filter queries, and ensure 100% PASS rate.
  4. 🌐 **Step 4 — Reload Browser & Run Playwright Automation Tests (`pytest tests/browser/`):** Automatically reload the browser page, run end-to-end Playwright tests, verify target DB dropdown switching (`pg_prod` vs `pg_dev`), test date picker selection, click 🚀 **Submit** button, verify KPI cards, Bar chart, Scatter plot, and table population in a real browser environment.
  5. 🔀 **Step 5 — Git Synchronization, Commit & Auto-Push:**
     - Pull latest remote changes: `git pull origin main --rebase`
     - Stage all modified files: `git add .`
     - Commit with descriptive message: `git commit -m "feat/fix: ..."`
     - Create Pull Request if required: `gh pr create`
     - Push code to remote repository: `git push origin main`
  6. 📋 **Step 6 — Update Task Status & Documentation:** Mark Plane task status as `Done` / `Completed` with test results, and update `README.md` and `tasks.md` to keep documentation current.

- **Fix Applied (2026-07-27):** Sprint Watcher previously **did NOT poll comments** — it only watched task state changes. Added `list_comments()` to `plane_agent.py` and `_check_new_comments()` to `sprint_watcher_agent.py`. Every 60-second poll now also fetches comments on all open tasks and triggers the builder if any **new** (unseen) user comment is found.


---

### 4. 🚨 HIGH PRIORITY DIRECTIVE: Fully Dynamic Unit & Browser Test Suite & Auto-Fix Mandate
- **Mandatory Operational Directive (ZERO Hardcoded Values):** All unit tests (`tests/unit/`) and browser automation tests (`tests/browser/`) MUST be 100% dynamic. Test cases must collect information dynamically from connected databases (`pg_prod`, `pg_dev`, `oracle_dev`, `oracle_f1`, `oracle_prod`) and API service payloads **WITHOUT hardcoding static database record values** (such as static warehouse count numbers `3` or `5`, static facility arrays `["58", "61", "71"]`, static dates, static batch IDs, or invoice numbers).
- **Dynamic Test Case Preparation & Data-Driven Assertions:** Every test file must dynamically query API endpoints and database summary fields, construct dynamic data-driven assertions (e.g. comparing bar chart array length against dynamic summary count `len(data) == stats["summary"]["total_warehouses"]` or browser tick count `actual_ticks == kpi_total_warehouses`), and validate structural data models, status codes, and filter parameter propagation.
- **Mandatory Auto-Fix & Issue Resolution Rule:** If ANY unit test, browser test, or compilation issue occurs during testing, the agent MUST NOT stop or abandon work. The agent MUST immediately fetch error tracebacks/logs, fix the root cause in the respective backend (`backend/`) or frontend (`frontend/`) source files, and re-test immediately until 100% PASS rate is achieved.
- **🔓 FULL PRE-APPROVED COMMAND PERMISSIONS (ZERO PERMISSION PROMPTS — ALWAYS ALLOWED):**
  1. `git *` (ALL Git commands including `git pull`, `git add`, `git commit`, `git push`, `git status`, `git checkout`, `git rebase` — **100% Pre-Approved, Always Allowed, Zero Prompts**)
  2. `python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload` (FastAPI Server — 100% Pre-Approved, Zero Prompts)
  3. `node node_modules/vite/bin/vite.js` (Vite Frontend Server — 100% Pre-Approved, Zero Prompts)
  4. `python -m pytest tests/browser/ -v` (Playwright Browser Test Suite — 100% Pre-Approved)
  5. `python -m pytest tests/unit/ -v` (Full Unit Test Suite — 100% Pre-Approved)
  6. `python scripts/run_sprint_watcher.py --interval 60` (Sprint Watcher Agent — 100% Pre-Approved)
  - All listed commands and ALL Git CLI commands are **100% PRE-APPROVED** for autonomous background execution without asking the user for confirmation or text permission prompts.
- **100% Dynamic Database Record Execution (Zero Hardcoded Dates or Counts):**
  - No static date tables or fixed date record assumptions are permitted in `tasks.md`, source code, or test suites.
  - For **ANY date (`oerdte`)** selected in the UI or requested in API endpoints, the application MUST dynamically query the connected database table (`sptn_sales_data`).
  - If a selected date has 0 records in the database, return strictly 0 items / empty dataset without synthetic data generation. If records exist for that date, filter and return exact matching records dynamically.

---

### 3b. Open Requirements from Plane Comments (2026-07-27) — `Warehouse level statics`

These instructions were added as comments in Plane and MUST be implemented:

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

#### ⚠️ Requirement 4 — `batch_id` Column Population from `sptn_sales_data ssd`
- **Issue:** `batch_id` values are wrong and should be populated from the `batch_id` column of `sptn_sales_data ssd`.
- **Query Specification:**
  ```sql
  select oerdte,batch_id
  from sptn_sales_data ssd ;
  ```
- **Action:**
  1. Ensure query logic fetches `batch_id` directly from `sptn_sales_data ssd` along with `oerdte`.
  2. Return the correct `batch_id` column values in the API and display them in the table component.


- **File References:**
  - [`agents/plane_agent.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/agents/plane_agent.py)

#### ⚠️ Requirement 4b — Strict SQL Execution Matching Target DB & Date (No Hardcoding & No Synthetic Fallbacks) (2026-07-28)
- **SQL Execution Specification:**
  ```sql
  SELECT DISTINCT oewhse
  FROM sptn_sales_data ssd 
  WHERE 1=1 -- oeinvo = '487591'
    AND oerdte = %s;
  ```
- **Operational Rules:**
  1. **Strict Target DB & Date Matching:** Execute direct SQL queries against whatever target database (`pg_prod`, `pg_dev`, etc.) and whatever date (`oerdte`) the user selects in the UI.
  2. **Strict Zero Record Handling:** If querying `pg_dev` for date `20260728` yields 0 records in the database, the UI MUST show 0 records / empty dataset. Never substitute synthetic data or fallback dates.
  3. **Strict Active Warehouse Analytics:** If querying `pg_prod` for date `20260728` populates active warehouses (e.g. `58`, `71`), calculate and render analytics, KPIs, and item quantities strictly for those matching warehouses returned for that date.
  4. **Clean API Execution & Race Condition Removal:** Prevent race conditions in `Dashboard.jsx` and `WarehouseSalesAnalytics.jsx` using subscription cleanup flags (`isMounted` / `isSubscribed`) so background fetches never overwrite selected date or DB state.

#### ⚠️ Requirement 4d — Global Form Submit Button OnClick Execution Directive (2026-07-28)
- **Submit OnClick Implementation:**
  1. The top navigation header provides the **📅 Order Date Picker (`#global-date-picker`)**, **🗄️ Target DB Selector (`#global-db-selector`)**, and **🚀 Submit Button (`#submit-db-btn`)**.
  2. Clicking the **🚀 Submit** button (or submitting the form) MUST invoke `handleSubmit(e)`, applying the chosen date (`appliedDate`) and target database (`appliedTargetDb`).
  3. Form submission immediately triggers decoupled API calls to `/api/charts/kpi`, `/api/charts/bar`, `/api/charts/scatter`, and `/api/warehouse/statistics`, updating all KPI cards, Bar charts, Scatter plots, and table views dynamically in real time.

#### ⚠️ Requirement 4e — Comprehensive Application Testing & Anti-Freeze Release Directive (2026-07-28)
- **Mandatory Policy (No Half-Testing Permitted):** Whenever ANY code change is made in backend Python (`backend/`) or frontend React (`frontend/`), partial or half testing is strictly forbidden. The system MUST perform **100% Comprehensive End-to-End Testing** across all UI components and database queries before release:

  - 🔹 **Sub-task 4e.1 — KPI Cards Verification:** Validate total warehouse count, cases built quantity, original order quantity, and distinct invoice counts for any selected date across all target databases (`pg_prod`, `pg_dev`, `oracle_dev`, `oracle_f1`, `oracle_prod`).
  - 🔹 **Sub-task 4e.2 — Bar Chart & Scatter Plot Rendering Verification:** Verify Recharts bar charts and scatter plots render dynamic data points, tooltips, axis labels, and legend titles matching database records without freezing or throwing rendering errors.
  - 🔹 **Sub-task 4e.3 — Warehouse Analytics Table Verification:** Verify line items table populates `Warehouse #`, `Batch ID`, `Date`, `Invoice #`, `C&S Item Code`, `Cases Built`, `Order Qty`, and `Fulfillment Status` with infinite scrolling and filter parameter matching.
  - 🔹 **Sub-task 4e.4 — Database Query Caching & Anti-Freeze Performance:** Maintain a thread-safe 15-second TTL query cache (`_fetch_from_postgres_cached` in `warehouse_service.py`) to prevent concurrent API requests (`/api/charts/kpi`, `/api/charts/bar`, `/api/charts/scatter`, `/api/warehouse/statistics`) from opening redundant DB connections or freezing the application UI.
  - 🔹 **Sub-task 4e.5 — Automated Release & Verification Pipeline:** Run unit tests (`pytest tests/unit/`) and Playwright browser tests (`pytest tests/browser/`) end-to-end, reloading the browser page, testing date picker and DB selector form submission, confirming 100% PASS rate, and auto-pushing to remote Git (`git push origin main`).

#### ⚠️ Requirement 4c — Mandatory File-Change Re-Deployment & End-to-End Browser Testing Mandate (2026-07-28)
- **Mandatory Redeployment & Verification Directive:**
  Whenever ANY source file in `backend/` or `frontend/` is created or modified, the system MUST autonomously:
  1. 🔄 **Re-Deploy / Restart Backend Services:** Restart the FastAPI backend uvicorn server (`python -m uvicorn main:app`) and verify API health check (`GET /api/health`).
  2. 🧪 **Execute Unit Test Suite:** Run `pytest tests/unit/` and verify 100% PASS rate.
  3. 🌐 **Execute End-to-End Browser Test Suite:** Run `pytest tests/browser/` (Playwright) to verify live rendering, target DB dropdown switching (`pg_prod` vs `pg_dev`), dynamic date picker selection, KPI card rendering, chart rendering, and table population in a real browser environment.
  4. 🚀 **Auto-Fix & Deploy:** Automatically resolve any test failures, re-test end-to-end, and commit clean changes to remote Git repository.

#### ⚠️ Requirement 5 — 100% Dynamic Date & Target DB Query Execution (Strict Zero Hardcoding Directive)
- **Mandatory Requirement:** Warehouses, quantities, dates, and metrics MUST NEVER be hardcoded for any specific dates or target databases.
- **Dynamic Database Execution Specification:**
  1. For **ANY selected Target DB** (`pg_prod`, `pg_dev`, `oracle_dev`, `oracle_f1`, `oracle_prod`) and for **ANY selected Date** (`oerdte`), the system MUST dynamically query the active connected database.
  2. Query 1 executes:
     ```sql
     SELECT DISTINCT oewhse
     FROM sptn_sales_data ssd
     WHERE oerdte = %s ...
     ORDER BY oewhse ASC;
     ```
     passing whatever `oerdte` and filter parameters are selected by the user in the UI or API request.
  3. The resulting `distinct_warehouses` list dynamically defines `total_warehouses = len(distinct_warehouses)` and determines the exact warehouse labels rendered in the Bar Chart ("Cases Built by Warehouse").
  4. If N warehouses are active for a date in the target database, render strictly N bars. If 0 records exist for a date, render strictly 0 bars.
  5. All static fallbacks (`5 if DEV else 3`), fixed date assumptions, and hardcoded warehouse counts are 100% eliminated from backend services (`backend/app/warehouse_service.py`, `backend/routers/charts.py`), frontend components, and unit/browser test suites.

#### ⚠️ Requirement 6 — 100% Dynamic Database-Driven Warehouse & Quantity Aggregation
- **Required Architecture & Execution:**
  - **Subtask 1 — Query 1 (Distinct Active Warehouses for Selected Date & Target DB):**
    ```sql
    SELECT DISTINCT oewhse
    FROM sptn_sales_data ssd
    WHERE oerdte = %s ...
    ORDER BY oewhse ASC;
    ```
    Executes dynamically against the connected target database (`pg_prod`, `pg_dev`, `oracle_dev`, `oracle_f1`, `oracle_prod`) matching whatever exact date (`oerdte`) and filter parameters (`batch_id`, `oewhse`, `oeinv`) the user selects. Sets `distinct_warehouses` list and `total_warehouses = len(distinct_warehouses)`.
  - **Subtask 2 — Query 2 (Item Details & Quantities Aggregation):**
    ```sql
    SELECT oewhse, batch_id, oerdte, oecst, oeitem, oeinvo, oeqtys, oeqtyo, oeqscr, oesubf, gb_process_status
    FROM sptn_sales_data ssd
    WHERE oerdte = %s ...
    ORDER BY oerdte DESC, oewhse ASC
    LIMIT 500;
    ```
    Queries line item details for the selected date & DB type, calculates total cases built (`total_cases_built`), original order quantity (`total_original_order_qty`), and distinct invoice counts.
  - **Subtask 3 — Bar Chart & KPI Alignment:**
    Construct bar chart items derived strictly from `distinct_warehouses` for the queried date & DB type.
  - **Subtask 4 — Zero Static Fallbacks:**
    Eliminate all hardcoded fallback assignments (`5 if is_dev else 3`) across backend services (`backend/app/warehouse_service.py`, `backend/routers/charts.py`), frontend, and test files.

#### ⚠️ Requirement 7 — 🚨 STRICT MANDATE: ZERO HARDCODED VALUES & DYNAMIC UI PARAMETER QUERY PREPARATION
- **Zero Hardcoded Values Mandate:** Absolutely NO hardcoding of static warehouse IDs (such as `'58'`, `'61'`, `'71'`), static dates, static quantities, or static limits anywhere in backend services (`backend/app/warehouse_service.py`, `backend/routers/charts.py`), frontend components (`frontend/src/`), or unit/browser test suites.
- **Dynamic UI Parameter Query Execution:**
  1. The system MUST accept parameters directly from the UI inputs: `target_db` (Target Database selector), `oerdte` (Global Order Date), `oewhse` (Warehouse filter), `batch_id` (Batch ID filter), and `oeinv` (Invoice filter).
  2. Dynamically prepare and execute SQL queries matching the exact user parameters:
     - **Query 1 (Active Warehouse IDs):** `SELECT DISTINCT oewhse FROM sptn_sales_data ssd WHERE oerdte = %s ... ORDER BY oewhse ASC;`
     - **Query 2 (Aggregated Quantities per Warehouse):**
       ```sql
       SELECT oewhse, 
              COALESCE(SUM(CAST(NULLIF(oeqtys, '') AS NUMERIC)), 0) AS total_cases_built,
              COALESCE(SUM(CAST(NULLIF(oeqtyo, '') AS NUMERIC)), 0) AS total_order_qty,
              COUNT(DISTINCT oeinvo) AS total_invoices
       FROM sptn_sales_data ssd
       WHERE oerdte = %s ...
       GROUP BY oewhse
       ORDER BY oewhse ASC;
       ```
     - **Query 3 (Partitioned Line Items & Interleaved Output):** Fetch line item details partitioned across all active warehouses and interleave them round-robin so ALL warehouses (58, 61, 71) are represented in the UI table and charts.
  3. Automatically populate all KPI cards, Bar Charts ("Cases Built by Warehouse"), Scatter Plots, and Data Tables strictly with data dynamically fetched from the connected target database.

---

### 4. Code Modification, Mandatory Testing & Auto-Fix Rule (Do Not Disturb Existing Code)
- **Mandatory Directive:** Do **NOT** alter or disturb existing working code. Handle **ONLY** new sprint changes and feature additions.
- **Mandatory Testing & Auto-Fix Policy:** Whenever ANY code change is made (backend or frontend), testing the application and running browser tests (`pytest tests/browser/ -v`) are **MANDATORY**. If any issues, compilation errors, or test failures occur, the agent MUST fix them accordingly and re-test immediately until 100% passed.
- **Strict Scope Control:** All code modifications must be additively non-destructive to pre-existing components, services, routes, or configurations.
- **Mandatory Post-Testing Application Reload & Server Restart Policy:** Whenever all testing (`pytest tests/unit/ -v` and `pytest tests/browser/ -v`) and code changes are completed for a task or feature, the agent MUST automatically reload/restart the FastAPI backend server (`python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload`) and Vite frontend dev server (`node node_modules/vite/bin/vite.js`) to ensure the application runs smoothly with 100% updated code and zero stale processes.
- **Enforcement:** Both unit tests (`pytest tests/unit/ -v`) and browser tests (`pytest tests/browser/ -v`) must pass 100% after every code change. If any existing or new test fails, the task is marked `FAILED` and resolved immediately.

---

### 5. Consolidated Test Suite & Markdown Test Tracking (`sprint_test_cases.md`)
- **Mandatory Directive:** Do **NOT** maintain or create multiple individual `.py` test files in `tests/unit/` for every small UI component. Keep `tests/unit/` clean and consolidated (`test_core_components.py`, `test_analytics.py`, `test_charts.py`, `test_data_endpoints.py`).
- **Markdown Test Case Logging:** Record all sprint test cases, descriptions, and test results (`PASSED` / `FAILED` status) directly inside [`sprint_test_cases.md`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/sprint_test_cases.md) right behind each test case.
- **File References:**
  - [`sprint_test_cases.md`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/sprint_test_cases.md)
  - [`tests/unit/test_core_components.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/tests/unit/test_core_components.py)


---

### 6. Mandatory Application Testing, Browser Verification & Auto-Fix Policy (Pre-Approved Permission Commands)
- **Pre-Approved Command Mandate (ZERO Permission Prompts):** The test execution commands `python -m pytest tests/browser/ -v` and `python -m pytest tests/unit/ -v` have **FULL PRE-APPROVED AUTONOMOUS PERMISSION**. The agent MUST run these commands automatically via `run_command` after any code update without issuing text prompts asking the user for permission.
- **Dynamic End-to-End Test Case Preparation:** Both unit tests (`tests/unit/`) and browser automation tests (`tests/browser/`) must dynamically extract information from the connected databases (`pg_prod`, `pg_dev`, `oracle_dev`, `oracle_f1`, `oracle_prod`) and live UI elements, preparing dynamic test cases and assertions based on real data flow without hardcoding static values.
- **Immediate Auto-Fix Resolution Policy:** If browser testing or unit testing detects ANY UI error, compilation issue, or broken component, the agent MUST immediately inspect tracebacks/logs, fix the root cause in the respective backend or frontend files, and re-run browser/unit tests until 100% PASS rate is achieved.
- **Execution:** Headless Chromium browser automation tests verify UI rendering, routes, KPI cards, Recharts SVG elements, tables, dropdowns, and components on the live web app after every code update.
- **Pre-Approved Commands:**
  - `python -m pytest tests/browser/ -v`
  - `python -m pytest tests/unit/ -v`
- **File References:**
  - [`tests/browser/test_dashboard_loads.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/tests/browser/test_dashboard_loads.py)
  - [`tests/unit/test_warehouse_db_filters.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/tests/unit/test_warehouse_db_filters.py)


---

### 7. Continuous Application Runtime & Auto-Restart Execution
- **Mandatory Directive (ALWAYS RUNNING & AUTO-RESTART):** The agent MUST continuously maintain the application in a running state. Never stop the backend or frontend servers.
  - **Auto-Detect & Auto-Reload:** If either server is not in a running state, the agent MUST immediately reload and start both backend and frontend servers.
  - **Persistent Server Policy (NEVER STOP):** Do not stop the servers. If a server stops automatically (due to error, crash, or timeout) or is stopped manually, restart it automatically without asking for permission.
  - **Backend Server (FastAPI):** `python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload` (Cwd: `backend/`) -> Active on `http://localhost:8000` (Docs: `http://localhost:8000/docs`).
  - **Frontend Server (React + Vite):** `node node_modules/vite/bin/vite.js` or `npm run dev` (Cwd: `frontend/`) -> Active on `http://localhost:5173`.
- **Runtime Verification:** Ensure both servers are operational and accessible prior to running Playwright browser automation suites.

---

### 7b. 🔧 Permanent Fix for Node.js `MODULE_NOT_FOUND` & Manual Execution Guide (Agent Restart / Token Expiry)

#### 1. Permanent Fix for Node.js `MODULE_NOT_FOUND` (Windows `&` Path Special Character Issue)
- **Problem:** Paths containing special characters like `&` (`c&s\mani_personal\...`) break Windows command-line `.bin` wrapper shims (`node_modules\.bin\vite`), producing `MODULE_NOT_FOUND` or invalid command errors.
- **Permanent Solution:** In `frontend/package.json`, the `"dev"` script is configured to invoke Vite directly using Node:
  ```json
  "dev": "node node_modules/vite/bin/vite.js"
  ```
  This bypasses `.bin` cmd shims completely and ensures `npm run dev` works natively on Windows regardless of folder path characters.

#### 2. How to Run the Application Manually (If Agent is OFF or out of tokens)
If the AI agent is offline, paused, or token limit is reached, you can run both servers manually from PowerShell/Terminal:
- **Backend (FastAPI):**
  ```powershell
  cd "c:\Users\manik\Downloads\c&s\mani_personal\ai_analytics_dashboard\backend"
  python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
  ```
- **Frontend (Vite/React):**
  ```powershell
  cd "c:\Users\manik\Downloads\c&s\mani_personal\ai_analytics_dashboard\frontend"
  npm run dev
  ```

#### 3. Fresh Day Agent Boot Protocol & Zero-Command Resume Strategy
When starting a new conversation on a fresh day or resuming work:
- **User Opening Message:** The user can initiate the conversation using ANY standard opening message, greeting, or goal statement (e.g., `"Good morning"`, `"What's the status?"`, `"Resume sprint"`, `"Check memory"`, or `"Continue task"`). The user does **NOT** need to explicitly say `"start the application"`.
- **Autonomous Agent Boot Protocol (Triggered Automatically on First Turn):**
  1. 📚 **Context & Memory Inspection:** The agent automatically inspects [`tasks.md`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/tasks.md) and the latest session log in [`memory/conversations/`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/memory/conversations/) (`YYYY-MM-DD.md`) to load full project architecture, recent completed items, and pending requirements.
  2. ⚡ **Server Health Check & Auto-Launch:** The agent inspects if the FastAPI backend (port 8000) and Vite React frontend (port 5173) are active. If either server is offline or stopped, the agent starts them autonomously in the background via `run_command` without asking permission.
  3. 🧪 **Automated Sanity Verification:** The agent runs automated test suites (`pytest tests/unit/ -v`) to confirm clean operational status.
  4. 📢 **Status & Context Synthesis:** The agent summarizes current runtime state, recent code changes, and active tasks directly to the user.

---

### 7c. 🎛️ Header Controls On-Click Functionality & System Route Specifications

#### 1. Header Dropdown & Submit Button On-Click Functionality (`Dashboard.jsx`)
- **Order Date Picker (`#global-date-picker`):**
  - Event: `onChange={(e) => ...}`
  - Behavior: Captures selected ISO date (`YYYY-MM-DD`), converts to `oerdte` (`YYYYMMDD`), updates state, and immediately triggers `fetchAll(selectedDate, selectedDb)`.
- **Target DB Dropdown (`#global-db-selector`):**
  - Event: `onChange={(e) => ...}`
  - Options: `PostgreSQL PROD` (`pg_prod`), `PostgreSQL DEV` (`pg_dev`), `Oracle DEV` (`oracle_dev`), `Oracle F1` (`oracle_f1`), `Oracle PROD` (`oracle_prod`).
  - Behavior: Updates `selectedDb` and `appliedTargetDb`, updates badge status (`⚡ Active: PG_DEV` / `PG_PROD`), and immediately triggers `fetchAll(selectedDate, val)` across all backend endpoints.
- **Submit Button (`#submit-db-btn`):**
  - Event: `onClick={handleSubmit}` + `onSubmit={(e) => handleSubmit(e)}`
  - Behavior: Prevents form reload (`e.preventDefault()`), commits `appliedDate` & `appliedTargetDb`, and forces simultaneous refresh of KPI Cards (`/api/charts/kpi`), Bar Chart (`/api/charts/bar`), Scatter Plot (`/api/charts/scatter`), and Warehouse Data Table (`/api/warehouse/statistics`).

#### 2. System Route Specifications (Frontend & Backend APIs)

##### 🌐 Frontend Application Routes (React Router)
| Route Path | Component File | Description |
| :--- | :--- | :--- |
| `/` | [`frontend/src/pages/Dashboard.jsx`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/frontend/src/pages/Dashboard.jsx) | Main Dashboard: Global Header Controls, 6 KPI Cards, Warehouse Bar Chart, Scatter Plot, Warehouse & Invoice Sales Analytics Table, Inventory Risk Forecast. |
| `/analytics` | `frontend/src/pages/Analytics.jsx` | Predictive Model Training & Machine Learning Analytics page. |

##### 🔌 Backend REST API Endpoints (FastAPI)
| HTTP Method | API Endpoint | Query Parameters | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/warehouse/statistics` | `target_db`, `oerdte`, `batch_id`, `oewhse`, `oeinv`, `limit`, `offset` | Direct PostgreSQL / Oracle query returning dynamic item-level and invoice-level warehouse statistics. |
| `GET` | `/api/charts/kpi` | `oerdte`, `target_db` | Returns summary KPI metrics (Total Warehouses, Cases Built, Order Qty, Invoices Processed, Fulfillment Rate, Scratch Rate). |
| `GET` | `/api/charts/bar` | `oerdte`, `target_db` | Returns warehouse cases built breakdown for the Bar Chart. |
| `GET` | `/api/charts/scatter` | `oerdte`, `target_db` | Returns order quantity vs cases built points for Scatter Plot. |
| `GET` | `/api/health` | None | Returns API service health status (`{"status": "healthy"}`). |
| `GET` | `/api/data/sample` | `rows` | Returns sample dataset rows. |
| `GET` | `/api/data/summary` | None | Returns statistical summary of dataset columns and numeric stats. |
| `POST` | `/api/data/upload` | Multipart file | Uploads CSV dataset. |
| `POST` | `/api/analytics/train` | Body (`target_col`, `model_type`) | Trains Random Forest or Logistic Regression model on dataset. |

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
### 3b. Real Database Schema & Mandatory Column Mapping (`sptn_sales_data ssd`)
- **Query Reference:** `SELECT oerdte, batch_id, oewhse, oecst, oeitem, oeinv, oeqtys, oeqtyo, oeqscr, oesubf, gb_process_status FROM sptn_sales_data ssd;`
- **Mandatory Column Mappings:**
  1. `oewhse` ➔ `whs_num` (Warehouse Facility: PROD has `'58'`, `'61'`, `'71'`; DEV has `'01'`, `'02'`, `'58'`, `'61'`, `'71'`).
  2. `batch_id` ➔ `batch_id` (Real numeric string Batch IDs populated directly from `batch_id` column e.g. `'100'`, `'1000'`, `'4569'`, `'785'`. Do **NOT** prefix with `BCH-`).
  3. `oerdte` ➔ `oerdte` (Order Date YYYYMMDD).
  4. `oecst` ➔ `cust_item_code` (Customer Item Code).
  5. `oeitem` ➔ `cs_item_code` (C&S Item Code).
  6. `oeinv` ➔ `invc_num_stg` (Invoice Number).
  7. `oeqtys` ➔ `cases_bld_stg` (Cases Built Quantity).
  8. `oeqtyo` ➔ `orgnl_ordr_qty_stg` (Original Order Quantity).
  9. `oeqscr` ➔ `whs_scrtch_qty_stg` (Warehouse Scratch Quantity).
  10. `gb_process_status` ➔ `procurement_transfer_status` (`'P'` mapped to `'COMPLETED'`).
- **Instant UI Target DB Synchronization:** Changing Target DB or clicking Submit MUST instantly query target database and update all KPI cards, Bar Charts, Scatter Plots, and Data Tables across the entire page without desync.
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

#### 📂 Memory File Locations & Conversation Memory Index:
| Memory File | Date | Key Features & Session Memory Summary |
| :--- | :--- | :--- |
| 📄 [`memory/conversations/2026-07-27.md`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/memory/conversations/2026-07-27.md) | 2026-07-27 | Initial Sprint AAD-5 Warehouse Analytics, 6 KPI cards, data table, infinite scroll, UTF-8 Sprint Watcher fix, 41/41 unit & browser tests passed. |
| 📄 [`memory/conversations/2026-07-28.md`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/memory/conversations/2026-07-28.md) | 2026-07-28 | Header controls `onClick` & `onChange` handlers, PostgreSQL DEV record verification, dynamic test protocol, SQL VARCHAR SUM type casting fix, 36/36 unit & 13/13 browser tests passed. |
| 📄 [`memory/conversations/2026-07-29.md`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/memory/conversations/2026-07-29.md) | 2026-07-29 | Hidden `InventoryRiskForecast` & `AiAnalyticsDashboardAddingDateParameter` from active UI, created Task 11, 12, 13 specs, cleaned informal emoji icons, removed `pg_prod` & `oracle_prod` DB configs, 36/36 unit tests passed (100%). |
| 📄 [`memory/agent_state.json`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/memory/agent_state.json) | Persistent | Machine-readable agent status + Plane project IDs |
| 📁 `memory/task_history/*.jsonl` | Append-only | Append-only task execution history logs |

---

### 8d. Mandatory Test Execution, Statistics Reporting & Memory Session Log Policy
- **Mandatory Directive:** After running application test commands (`pytest tests/unit/ -v`) and browser automation commands (`pytest tests/browser/ -v`), the agent MUST:
  1. 📊 **Report Detailed Statistics:** Output pass/fail counts, total duration, test suite breakdown, and pass rate to the user.
  2. 📝 **Update Memory Conversation Log:** Update [`memory/conversations/YYYY-MM-DD.md`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/memory/conversations/2026-07-29.md) with the latest test statistics, code modifications, service statuses, and task context.
- **Enforcement:** Never complete a test execution cycle or session without updating `memory/conversations/YYYY-MM-DD.md` and providing the full statistics summary to the user.

> **Example:** When a new agent session starts tomorrow (2026-07-30), it MUST read [`memory/conversations/2026-07-29.md`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/memory/conversations/2026-07-29.md) to understand what was completed today before doing any work.

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
