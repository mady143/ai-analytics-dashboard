# 📌 TASK 10 — Interactive Browser Parameter Combination Testing & Strict Quality Gate Push Policy (`#interactive-testing-pipeline`)

## 🖥️ Location & File References
- **Test File:** [`tests/browser/test_dashboard_loads.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/tests/browser/test_dashboard_loads.py)
- **Unit Test Directory:** [`tests/unit/`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/tests/unit/)
- **Frontend File:** [`frontend/src/pages/Dashboard.jsx`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/frontend/src/pages/Dashboard.jsx)
- **Backend File:** [`backend/app/warehouse_service.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/backend/app/warehouse_service.py)

---

## 🎯 Sub-Task Breakdown

### Sub-Task 10.1: 🌐 Interactive Browser Form & Parameter Testing
- **Browser Automation Flow:**
  1. Launch Playwright browser (`pytest tests/browser/`).
  2. Navigate to `http://localhost:5173`.
  3. Select different Order Dates (`#global-date-picker`).
  4. Select different Target DBs (`#global-db-selector`: `pg_prod`, `pg_dev`, `oracle_dev`, `oracle_f1`, `oracle_prod`).
  5. Click **🚀 Submit** button (`#submit-db-btn`).
  6. Verify UI reloads and pulls fresh data from backend APIs.
  7. Verify data populates correctly across:
     - 🏢 KPI Cards (Total Warehouses, Cases Built, Order Qty, Invoices)
     - 📊 Cases Built Bar Chart
     - 📈 Order Qty vs Cases Built Scatter Plot
     - 📋 Warehouse Line Items Data Table
  8. If any parameter combination fails, hangs, or shows blank data inappropriately:
     - Diagnose root cause in `backend/` or `frontend/`.
     - Implement code fix in respective source files.
     - Re-test immediately until 100% PASS rate is achieved.

### Sub-Task 10.2: 🔄 Automatic Server Restart & Browser Reload Pipeline
- **Behavior:** Whenever backend Python (`backend/`) or React UI (`frontend/`) code is modified:
  1. Restart/reload FastAPI server (`uvicorn main:app` at `:8000`) and Vite server (`npm run dev` at `:5173`).
  2. Execute unit test suite (`pytest tests/unit/`).
  3. Reload Playwright browser and run end-to-end UI tests (`pytest tests/browser/`).

### Sub-Task 10.3: 🛡️ Strict Quality Gate Push Policy (Zero Push Until Verified)
- **Mandatory Quality Gate:**
  - Code MUST NOT be pushed to remote Git (`git push origin main`) until:
    1. All unit tests pass 100% (`pytest tests/unit/`).
    2. All browser UI tests pass 100% (`pytest tests/browser/`).
    3. Interactive parameter switching (Date + DB dropdown + Submit click) is verified populated with real data.
