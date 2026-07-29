# 📌 TASK 14 — Natural Language AI Data Copilot (`#ai-data-copilot`)

## 📋 Task Description & Architecture
- **Status:** In Progress — Building interactive AI Assistant for data exploration and instant table filtering.
- **Component File:** [`frontend/src/components/AiDataCopilot.jsx`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/frontend/src/components/AiDataCopilot.jsx)
- **Backend Service:** [`backend/routers/analytics.py`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/backend/routers/analytics.py) (`POST /api/analytics/ai-copilot`)
- **Objective:** Provide a natural language query bar allowing users to ask plain English questions about warehouse inventory, scratch rates, batch IDs, and sales data.

## 🛠️ Step-by-Step Implementation Roadmap
1. **Backend NLP Query Handler:**
   - Endpoint: `POST /api/analytics/ai-copilot`
   - Accepts prompt string, target DB, and date.
   - Parses keywords (*scratch*, *warehouse 58*, *pending*, *high volume*, *batch*) and executes dynamic PostgreSQL query.
   - Returns answer summary, metrics, and table filter directives (`filtered_whse`, `filtered_batch`, `filtered_invoice`).
2. **Frontend Copilot UI (`AiDataCopilot.jsx`):**
   - Search input with Lucide vector icons (`Sparkles`, `Send`, `Bot`, `Zap`).
   - Quick prompt pills (*"Whse 58 High Scratch"*, *"Pending Transfers"*, *"Top Order Volume"*).
   - Insight response card with **"Apply Filter to Table"** button.
3. **Table State Binding:**
   - Binds Copilot filter actions to `WarehouseSalesAnalytics.jsx` filter state.
4. **Interactive Playwright Browser Verification (`tests/browser/test_ai_copilot_and_anomalies.py`):**
   - Type queries into AI Copilot search input in Chromium.
   - Click "Ask AI" button and verify AI Copilot Finding card populates.
   - Click quick insight pills and verify instant query execution.
   - Click "Apply Filter to Table" and assert dynamic sales table update.
