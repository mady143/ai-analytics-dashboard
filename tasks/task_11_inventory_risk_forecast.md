# 📌 TASK 11 — Inventory Risk Forecast Component (`#inventory-risk-forecast`)

## 📋 Task Description & Architecture
- **Status:** Queued / Hidden from active UI layout (`Dashboard.jsx`) for sequential modular build.
- **Component File:** [`frontend/src/components/InventoryRiskForecast.jsx`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/frontend/src/components/InventoryRiskForecast.jsx)
- **Objective:** Build real-time risk assessment, stock anomaly scoring, and predictive inventory risk breakdown by warehouse.

## 🛠️ Step-by-Step Implementation Roadmap
1. **Backend Endpoint Integration:** Create `/api/analytics/inventory-risk` endpoint returning anomaly scores, stockout probability, and risk tiers (Low, Medium, High, Critical).
2. **UI Card & Metrics Layout:**
   - Risk Index Gauge / Progress Bar
   - Predicted Out-of-Stock Items Count
   - Anomaly Alert Table per Warehouse ID (`oewhse`)
3. **Interactive Filter Controls:** Allow filtering risk metrics by Warehouse and Date Range.
4. **Verification & Testing:** Add unit test in `tests/unit/test_inventory_risk.py` and Playwright browser test when unhidden.
