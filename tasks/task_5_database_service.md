# 📌 TASK 5 — Multi-Database Engine & SQL Execution Service (`#backend-db-service`)

## 🖥️ Backend Service Location
- **Service Files:**
  - [`backend/app/warehouse_service.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/backend/app/warehouse_service.py)
  - [`backend/routers/charts.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/backend/routers/charts.py)

---

## 🎯 Sub-Task Breakdown

### Sub-Task 5.1: ⚡ Strict Parameter SQL Execution
- **Database Table:** `sptn_sales_data ssd`
- **SQL Logic:**
  ```sql
  SELECT DISTINCT oewhse
  FROM sptn_sales_data ssd
  WHERE 1=1
    AND oerdte = %s;
  ```
- **Strict Matching:** Queries execute direct SQL against whichever target database (`pg_prod`, `pg_dev`, etc.) and date (`oerdte`) selected in UI.

### Sub-Task 5.2: 🚫 Zero Synthetic Data Fallback Policy
- **Rule:** If 0 records exist in database for selected date, return strictly 0 items / empty dataset without generating fake or synthetic data.

### Sub-Task 5.3: ⏱️ 15-Second Thread-Safe TTL Query Cache (`_fetch_from_postgres_cached`)
- **Function:** `_fetch_from_postgres_cached(config, oerdte, batch_id, oewhse, oeinv, limit)`
- **Behavior:** Caches query result in memory for 15 seconds to prevent parallel API requests (`/api/charts/kpi`, `/api/charts/bar`, `/api/charts/scatter`, `/api/warehouse/statistics`) from blocking database threads or freezing the UI.
