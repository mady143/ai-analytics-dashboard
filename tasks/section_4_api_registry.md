# 🔌 Section 4: API Endpoint Registry & Database Schemas

This document lists all active FastAPI backend routes and database schemas.

---

## 1. Active FastAPI Endpoints

| Endpoint | Method | Router | Description |
|----------|--------|--------|-------------|
| `/api/data/health` | GET | `data.py` | Core health check |
| `/api/data/summary` | GET | `data.py` | Data summary metrics |
| `/api/charts/kpi` | GET | `charts.py` | Warehouse KPI statistics |
| `/api/charts/bar` | GET | `charts.py` | Warehouse Bar Chart totals |
| `/api/charts/scatter` | GET | `charts.py` | Warehouse Scatter Plot points |
| `/api/warehouse/statistics` | GET | `main.py` | Item-level invoice & procurement stats |
| `/api/analytics/ai-copilot` | GET/POST | `analytics.py` | Natural Language Copilot Search |
| `/api/sprints/tasks` | GET | `sprints.py` | Plane Sprint tasks & Auto-Watcher trigger |
| `/api/agents/status` | GET | `main.py` | Dynamic Agent Process Monitor |

---

## 2. PostgreSQL Table Schema (`sptn_sales_data`)

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| `oewhse` | VARCHAR / TEXT | Warehouse Facility Number (e.g. `'01'`, `'58'`) |
| `oerdte` | VARCHAR / DATE | Order Date (`YYYYMMDD` / `YYYY-MM-DD`) |
| `oeinvo` | VARCHAR / TEXT | Invoice Number |
| `batch_id` | VARCHAR | Batch Identifier |
| `oeqtys` | NUMERIC | Cases Built / Shipped Quantity |
| `oeqtyo` | NUMERIC | Original Order Quantity |
| `oeqscr` | NUMERIC | Warehouse Scratch Quantity |
