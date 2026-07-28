# 📌 TASK 3 — Warehouse Analytics & Data Visualization Charts (`#charts-section`)

## 🖥️ Screen / Component Location
- **Component Location:** [`frontend/src/pages/Dashboard.jsx`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/frontend/src/pages/Dashboard.jsx)
- **API Endpoints:**
  - `GET /api/charts/bar?oerdte={oerdte}&target_db={target_db}`
  - `GET /api/charts/scatter?oerdte={oerdte}&target_db={target_db}`

---

## 🎯 Sub-Task Breakdown

### Sub-Task 3.1: 📊 Cases Built Breakdown Bar Chart
- **Description:** Recharts Bar Chart plotting cases built quantity (`cases_built`) per active warehouse.
- **X-Axis:** Warehouse Number (`Warehouse 58`, `Warehouse 71`, etc.)
- **Y-Axis:** Total Cases Built (`cases_built`)

### Sub-Task 3.2: 📈 Order Quantity vs Cases Built Scatter Plot
- **Description:** Recharts Scatter Plot showing order volume (`order_qty`) vs cases built (`cases_built`).
- **Data Points:** Individual warehouse fulfillment data points with interactive tooltips.

### Sub-Task 3.3: 🌡️ Correlation Heatmap Matrix
- **Description:** Interactive correlation heatmap analyzing procurement feature relationships.

### Sub-Task 3.4: 📉 Distribution Histogram Chart
- **Description:** Quantity distribution histogram chart rendering value spread.
