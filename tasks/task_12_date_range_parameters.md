# 📌 TASK 12 — Date Range Parameters Component (`#date-range-parameters`)

## 📋 Task Description & Architecture
- **Status:** Queued / Hidden from active UI layout (`Dashboard.jsx`) for sequential modular build.
- **Component File:** [`frontend/src/components/AiAnalyticsDashboardAddingDateParameter.jsx`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/frontend/src/components/AiAnalyticsDashboardAddingDateParameter.jsx)
- **Objective:** Add From-Date (`from_date`) and To-Date (`to_date`) range parameter selection to query historical trends across date ranges across all charts and warehouse statistics tables.

## 🛠️ Step-by-Step Implementation Roadmap
1. **Header Date Range Control:** Expand header controls to support Date Range Picker (`from_date` and `to_date` ISO selectors).
2. **Backend API Date Range Parameters:**
   - Update `/api/warehouse/statistics` to accept `from_date` and `to_date`.
   - Update `/api/charts/bar` and `/api/charts/scatter` to aggregate metrics across `oerdte BETWEEN from_date AND to_date`.
3. **UI Integration & State Sync:**
   - Synchronize global date range state with KPI Cards, Bar Chart, Scatter Plot, and Data Table.
4. **Verification & Testing:** Add automated pytest suite validating multi-date queries across PostgreSQL and Oracle databases.
