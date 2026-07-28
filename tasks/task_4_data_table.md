# 📌 TASK 4 — Warehouse Item Level & Procurement Data Table (`#warehouse-table-container`)

## 🖥️ Screen / Component Location
- **Component File:** [`frontend/src/components/WarehouseSalesAnalytics.jsx`](file:///c:/Users/manik/Downloads/c&s/mani_personal/ai_analytics_dashboard/frontend/src/components/WarehouseSalesAnalytics.jsx)
- **API Endpoint:** `GET /api/warehouse/statistics?target_db={target_db}&oerdte={oerdte}&batch_id={batch_id}&oewhse={oewhse}&oeinv={oeinv}&limit=20&offset=0`

---

## 🎯 Sub-Task Breakdown

### Sub-Task 4.1: 📋 Line Items Data Grid
- **Columns:**
  1. `Warehouse #` (`whs_num`)
  2. `Batch ID` (`batch_id`) — Populated from `sptn_sales_data ssd`
  3. `Order Date` (`oerdte`)
  4. `Customer Item Code` (`cust_item_code`)
  5. `C&S Item Code` (`cs_item_code`)
  6. `Invoice #` (`invc_num_stg` / `oeinvo`)
  7. `Cases Built` (`cases_bld_stg` / `oeqtys`)
  8. `Order Qty` (`orgnl_ordr_qty_stg` / `oeqtyo`)
  9. `Scratch Qty` (`whs_scrtch_qty_stg` / `oeqscr`)
  10. `Fulfillment Status` (`procurement_transfer_status`)

### Sub-Task 4.2: 🔍 Table Level Parameters & Search Filters
- **Filter Inputs:**
  - `Warehouse #` filter (`#filter-whs`)
  - `Batch ID` filter (`#filter-batch`)
  - `Invoice #` filter (`#filter-invoice`)
- **Behavior:** Real-time query parameter filtering.

### Sub-Task 4.3: ♾️ Infinite Scroll & Pagination Batching
- **Description:** Infinite scroll loader batching line items 20 rows at a time for smooth performance.

### Sub-Task 4.4: 🔄 Submit Click Table Data Re-fetching Directive (2026-07-28)
- **Mandatory Behavior:**
  - When `globalDate` (`appliedDate`) or `globalTargetDb` (`appliedTargetDb`) changes in the header and the user clicks **🚀 Submit**, `WarehouseSalesAnalytics.jsx` MUST immediately reset offset to 0 and re-fetch `/api/warehouse/statistics`.
  - The table component MUST display a loading state ("Querying warehouse database..."), clear previous data, and populate the new matching line items for the selected target database and order date.
