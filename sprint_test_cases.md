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
