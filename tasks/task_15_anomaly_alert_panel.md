# 📌 TASK 15 — Real-Time Anomaly & Risk Alert Panel (`#anomaly-alert-panel`)

## 📋 Task Description & Architecture
- **Status:** In Progress — Building real-time automated anomaly detector and risk alert widget.
- **Component File:** [`frontend/src/components/AnomalyAlertPanel.jsx`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/frontend/src/components/AnomalyAlertPanel.jsx)
- **Backend Service:** [`backend/routers/analytics.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/backend/routers/analytics.py) (`GET /api/analytics/anomalies`)
- **Objective:** Automatically scan connected database records for fulfillment anomalies (high scratch rates, pending transfer status, order volume spikes) and display actionable color-coded risk alerts.

## 🛠️ Step-by-Step Implementation Roadmap
1. **Backend Anomaly Engine:**
   - Endpoint: `GET /api/analytics/anomalies`
   - Scans PostgreSQL `sptn_sales_data` for matching date & target DB.
   - Categorizes findings:
     - 🚨 **Critical**: Scratch Quantity > 0 / Scratch Rate > 15%
     - ⚠️ **Warning**: Pending Procurement Transfers (`procurement_transfer_status == 'PENDING'`)
     - ℹ️ **Info**: High Volume Order Spikes (`original_order_qty > 500`)
2. **Frontend Alert Widget (`AnomalyAlertPanel.jsx`):**
   - Severity-styled cards with Lucide vector icons (`AlertTriangle`, `AlertCircle`, `Info`, `Filter`).
   - 1-click **"Filter Table"** buttons for each anomaly card.
3. **Table Filter Synchronization:**
   - Immediately updates `WarehouseSalesAnalytics.jsx` search inputs on click.
