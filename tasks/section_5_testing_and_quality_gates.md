# 🧪 Section 5: Testing & Quality Gates

This document defines the automated testing procedures, Playwright browser testing tasks, Quality Gate push policies, and regression validation steps.

---

## 📄 Dedicated Testing Task Files
- 📄 [`tasks/task_10_end_to_end_parameter_testing.md`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/tasks/task_10_end_to_end_parameter_testing.md) — Interactive Browser Parameter Combination Testing & Quality Gate Push Policy
- 📄 [`tasks/task_20_full_e2e_component_suite.md`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/tasks/task_20_full_e2e_component_suite.md) — Full E2E + Unit Test Suite Component Validation & Regression Prevention

---

## 🧪 1. Pytest Unit Testing Suite
- **Execution Command:** `python -m pytest tests/unit/ -v --tb=short`
- **Total Test Cases:** 51 Unit Tests
- **Coverage:** ML models, AI Copilot, Anomaly alerts, KPI cards, Bar chart, Scatter plot, Heatmaps, FastAPI endpoints, Database filters.

---

## 🎭 2. Playwright Browser E2E Testing Suite
- **Execution Command:** `python -m pytest tests/browser/ -v --tb=short`
- **Total Test Cases:** 14 Interactive Browser Tests
- **Test File:** [`tests/browser/test_full_e2e_component_suite.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/tests/browser/test_full_e2e_component_suite.py)

### Key Playwright Browser Test Scenarios:
1. **TC-01: Default Date Auto-Load** — Verifies default date pre-fills in `#global-date-picker`.
2. **TC-02: KPI Card Data Load** — Verifies KPI cards render real metrics (not placeholders).
3. **TC-03: Chart SVG Rendering** — Verifies Bar Chart and Scatter Plot render SVG elements.
4. **TC-04: Date Change & Form Submit** — Verifies date change triggers API reload across widgets.
5. **TC-05: Warehouse Filter** — Verifies selecting a warehouse filters table rows and charts.
6. **TC-06: Copilot Date-Agnostic Query** — Verifies AI Copilot queries full dataset with `oerdte=''`.
7. **TC-07: Copilot Result Card** — Verifies Copilot displays "AI Copilot Finding" card.
8. **TC-08: Quick Pills Trigger** — Verifies clicking quick filter pills populates Copilot results.
9. **TC-10: Agent Monitor Sidebar** — Verifies all 6 autonomous agents are visible in sidebar.
10. **TC-12: Multi-DB Switch** — Verifies switching `pg_dev` ↔ `oracle_dev` reloads metrics.
11. **TC-14: Chart/KPI Alignment** — Verifies Bar Chart X-axis warehouse count equals KPI count.

---

## 🚨 3. Mandatory Quality Gate Push Policy
- **100% Pass Rate Mandate:** No code commit or git push is permitted unless all unit tests and browser tests pass cleanly.
- **Zero Hardcoding Directive:** All dates and warehouse facility numbers MUST be extracted dynamically from live DOM or API responses — no static hardcoded strings.
