# 📌 TASK 20 — Full E2E + Unit Test Suite: Component Validation & Regression Prevention (`#full-e2e-testing`)

## 📋 Overview
This task specification governs the **Full Automated Testing Suite** (Pytest Unit Tests + Playwright Browser End-to-End Tests) for the AI Analytics Dashboard.

---

## 🧪 Section 1: Test Suite Specifications

### 1. Unit Test Suite (`tests/unit/`)
- **Execution Command:** `python -m pytest tests/unit/ -v --tb=short`
- **Total Test Cases:** 51 Unit Tests
- **Key Modules Tested:**
  - `test_analytics.py` — ML models, AI Copilot, Anomaly alerts
  - `test_charts.py` — KPI cards, Bar chart, Scatter plot, Heatmaps
  - `test_core_components.py` — Navbar, Warehouse Analytics components
  - `test_data_endpoints.py` — CSV ingestion, Health check, Summary stats
  - `test_task19_20_copilot_date_rules.py` — Date-agnostic Copilot & Date-strict Dashboard rules
  - `test_warehouse_db_filters.py` — PostgreSQL parameters & schema integrity

### 2. Playwright Browser E2E Suite (`tests/browser/`)
- **Execution Command:** `python -m pytest tests/browser/ -v --tb=short`
- **Total Test Cases:** 14 Interactive Browser Tests
- **Key Flow Validations:**
  - Default date auto-application on page load (`#global-date-picker`)
  - KPI card real number rendering
  - Date parameter submission & propagation
  - AI Copilot query submission & "Copilot Mode Active" banner
  - Multi-database engine toggle (`pg_dev` ↔ `oracle_dev`)
  - Excel test result sheet maintenance (`tests/TEST_CASES.xlsx`)

---

## 🚨 Section 2: Quality Gate Push Policy
- **100% Test Pass Rate Mandate:** No code commit or git push is permitted unless all unit tests and browser tests pass cleanly.
- **Zero Hardcoding Rule:** Dates and warehouse facility numbers MUST be computed dynamically — no static hardcoded test strings.
