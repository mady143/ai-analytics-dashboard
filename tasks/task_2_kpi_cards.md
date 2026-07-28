# 📌 TASK 2 — Executive Warehouse KPI Summary Cards (`#kpi-grid`)

## 🖥️ Screen / Component Location
- **Component File:** [`frontend/src/components/KPICard.jsx`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/frontend/src/components/KPICard.jsx)
- **Parent File:** [`frontend/src/pages/Dashboard.jsx`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/frontend/src/pages/Dashboard.jsx)
- **API Endpoint:** `GET /api/charts/kpi?oerdte={oerdte}&target_db={target_db}`

---

## 🎯 Sub-Task Breakdown

### Sub-Task 2.1: 🏢 Total Warehouses KPI Card
- **Description:** Displays the distinct SQL count of active warehouses for the selected date.
- **SQL Logic:** `SELECT COUNT(DISTINCT oewhse) FROM sptn_sales_data WHERE oerdte = %s;`
- **Behavior:** Updates dynamically when changing target DB or date.

### Sub-Task 2.2: 📦 Cases Built KPI Card
- **Description:** Sum of `cases_built_qty` across active warehouses for the selected date.
- **SQL Logic:** `COALESCE(SUM(CAST(NULLIF(oeqtys, '') AS NUMERIC)), 0)`

### Sub-Task 2.3: 📋 Original Order Qty KPI Card
- **Description:** Sum of `original_order_qty` across active warehouses for the selected date.
- **SQL Logic:** `COALESCE(SUM(CAST(NULLIF(oeqtyo, '') AS NUMERIC)), 0)`

### Sub-Task 2.4: 📄 Invoices Processed KPI Card
- **Description:** Count of distinct invoice numbers (`oeinvo`) processed for the selected date.
- **SQL Logic:** `COUNT(DISTINCT oeinvo)`
