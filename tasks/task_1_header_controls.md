# 📌 TASK 1 — Global Parameter & Header Control Panel (`#global-header-controls`)

## 🖥️ Screen / Component Location
- **Component File:** [`frontend/src/pages/Dashboard.jsx`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/frontend/src/pages/Dashboard.jsx)
- **UI Placement:** Top Navigation Header Control Bar

---

## 🎯 Sub-Task Breakdown

### Sub-Task 1.1: 📅 Order Date Picker (`#global-date-picker`)
- **Element ID:** `#global-date-picker`
- **Description:** Allows user to select target order date (`oerdte` in `YYYY-MM-DD` format).
- **Behavior:** `onChange` updates `selectedDate` state in React.

### Sub-Task 1.2: 🗄️ Target Database Selector (`#global-db-selector`)
- **Element ID:** `#global-db-selector`
- **Description:** Dropdown menu supporting 5 target databases:
  1. `pg_prod` — PostgreSQL Production (`gc-ue4-psql-sni-prd01.prod.gcp.cswg.com`)
  2. `pg_dev` — PostgreSQL Development (`gc-ue4-psql-sni-dev01.nonprod.gcp.cswg.com`)
  3. `oracle_dev` — Oracle Development
  4. `oracle_f1` — Oracle F1
  5. `oracle_prod` — Oracle Production
- **Behavior:** `onChange` updates `selectedDb` state in React.

### Sub-Task 1.3: 🚀 Submit Button (`#submit-db-btn`)
- **Element ID:** `#submit-db-btn`
- **Description:** Form submission button triggering real-time API fetches.
- **Behavior:** Clicking **🚀 Submit** (or pressing Enter) invokes `handleSubmit(e)`, sets `appliedDate` and `appliedTargetDb`, AND immediately calls `fetchAll(selectedDate, selectedDb)` to update all KPI cards, Bar charts, Scatter plots, and Table components.

### Sub-Task 1.4: ⚡ Active Target DB Status Badge
- **Description:** Visual status badge displaying active target database.
- **Example:** `⚡ Active: PG_PROD` or `⚡ Active: PG_DEV`.

### Sub-Task 1.5: 🔄 Date & DB Change Submit Reload Verification Directive (2026-07-28)
- **Mandatory Directive:**
  - When the user selects a new Order Date (`#global-date-picker`) or changes the Target DB (`#global-db-selector`) and clicks **🚀 Submit**, all data components MUST immediately pull fresh backend data from `/api/charts/kpi`, `/api/charts/bar`, `/api/charts/scatter`, and `/api/warehouse/statistics`.
  - The UI MUST NOT remain stuck on stale data or ignore the Submit click.
- **Verification Rule:** Test end-to-end in browser by changing date/DB, clicking **🚀 Submit**, and verifying that API request logs show new network calls with updated `oerdte` and `target_db` query parameters.
