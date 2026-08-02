# 🧪 Sprint Test Cases Specification (`sprint_test_cases.md`)

This document maintains the official record of test cases, test objectives, and execution results for all sprint features.

---

## 🔹 Sprint Task: "Add The Nav bar"

### Test Cases & Results
- **Test Case 1: `test_navbar_component`** — Verify component source file [`Navbar.jsx`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/frontend/src/components/Navbar.jsx) exists and exports `"AI Analytics Dashboard"`. 👉 **`PASSED`**
- **Test Case 2: `test_navbar_renders`** — Launch Playwright Chromium, navigate to `http://localhost:5173/`, and verify header rendering. 👉 **`PASSED`**

---

## 🔹 Sprint Task: "Warehouse level statics"

### Test Cases & Results
- **Test Case 1: `test_warehouse_analytics_component`** — Verify [`WarehouseAnalytics.jsx`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/frontend/src/components/WarehouseAnalytics.jsx) contains `"Warehouse Level Statistics"` heading and storage metrics. 👉 **`PASSED`**

---

## 🔹 Sprint Task: "Inventory Risk Forecast"

### Test Cases & Results
- **Test Case 1: `test_inventory_risk_forecast_component`** — Verify [`InventoryRiskForecast.jsx`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/frontend/src/components/InventoryRiskForecast.jsx) component structure and anomaly metric scores. 👉 **`PASSED`**

---

## 🔹 Sprint Task AAD-5: "Warehouse Sales & Invoice Analytics"

### Test Cases & Results
- **Test Case 1: `test_warehouse_sales_analytics_backend_service`** — Validate target DB configurations (`pg_prod`, `pg_dev`, `oracle_dev`, `oracle_f1`, `oracle_prod`) and verify calculated cases built quantities (`cases_bld_stg`) & procurement fulfillment rate. 👉 **`PASSED`**
- **Test Case 2: `test_warehouse_sales_analytics_component`** — Verify UI component [`WarehouseSalesAnalytics.jsx`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/frontend/src/components/WarehouseSalesAnalytics.jsx) exists, renders Target DB selector dropdown, and populates item table. 👉 **`PASSED`**
- **Test Case 3: `test_dashboard_loads` (Browser Automation)** — Verify live dashboard rendering at `http://localhost:5173/` displays top-level Warehouse Sales & Invoice Analytics above the fold. 👉 **`PASSED`**
- **Test Case 4: `test_analytics_page_loads` (Browser Automation)** — Verify navigation to `http://localhost:5173/analytics` and ML model configuration selector. 👉 **`PASSED`**
- **Test Case 5: `test_sidebar_navigation` (Browser Automation)** — Validate interactive sidebar navigation across dashboard pages. 👉 **`PASSED`**
- **Test Case 6: `test_bar_chart_total_warehouses_alignment` (Fully Dynamic)** — Dynamically validate that `/api/charts/bar` returns ALL total warehouses for target DB matching `summary.total_warehouses` with 0 hardcoded static numbers. 👉 **`PASSED`**
- **Test Case 7: `test_bar_chart_total_warehouses_alignment_browser` (Browser Automation)** — Launch Playwright Chromium, navigate to `http://localhost:5173/`, dynamically read Total Warehouses KPI card, and verify Bar Chart X-axis tick count matches KPI count. 👉 **`PASSED`**

---

## 🔹 Sprint Task 26: "Dynamic Header Clear Filters Component"

### Test Cases & Results
- **Test Case 1: `test_header_clear_filter_btn_visibility`** — Verify `#header-clear-filter-btn` is hidden when all filters are clear, and appears dynamically beside Submit button when any filter is selected. 👉 **`PASSED`**
- **Test Case 2: `test_clear_filters_resets_ui` (Browser Automation)** — Verify clicking Clear Filters resets all state filters and clears copilot active state. 👉 **`PASSED`**

---

## 🔹 Sprint Task 27: "Strict Single-Warehouse Chart Filtering"

### Test Cases & Results
- **Test Case 1: `test_task27_single_warehouse_chart_filtering`** — Verify `GET /api/charts/bar?oewhse=58` and `/api/charts/scatter?oewhse=58` strictly return data points ONLY for Whse 58 (1 bar). 👉 **`PASSED`**

---

## 🔹 Sprint Task 28: "Live Agent Sprint Reading & Sprint Board UI"

### Test Cases & Results
- **Test Case 1: `test_sprint_tasks_endpoint`** — Verify `GET /api/sprints/tasks` returns live Plane sprint metadata, task counts, and task lists. 👉 **`PASSED`**
- **Test Case 2: `test_sprint_board_page` (Browser Automation)** — Verify navigation to `http://localhost:5173/sprints` renders live Sprint Board header, search bar, and Kanban columns. 👉 **`PASSED`**

---

## 🔹 Sprint Task 29: "Agent Monitor UI & Fleet Telemetry"

### Test Cases & Results
- **Test Case 1: `test_agents_status_endpoint`** — Verify `GET /api/agents/status` returns status, last run, and current active process for all 6 agents. 👉 **`PASSED`**
- **Test Case 2: `test_agent_monitor_page` (Browser Automation)** — Verify navigation to `http://localhost:5173/agents` renders live status cards for all 6 agents. 👉 **`PASSED`**

---

## 🔹 Sprint Task 30: "Three-Line Sidebar Toggle & Footer Component"

### Test Cases & Results
- **Test Case 1: `test_sidebar_has_toggle_button_disable`** — Verify clicking `#sidebar-toggle-btn` collapses (disables) nav bar to mini-mode (`72px`) and adjusts main content margin. 👉 **`PASSED`**
- **Test Case 2: `test_sidebar_has_toggle_button_enable`** — Verify clicking `#sidebar-toggle-btn` a second time expands (enables) nav bar back to full width (`260px`). 👉 **`PASSED`**
- **Test Case 3: `test_footer_component_exists`** — Verify `#app-footer` renders default copyright information at the bottom of the layout. 👉 **`PASSED`**


