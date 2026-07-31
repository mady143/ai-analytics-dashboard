"""
Charts Router — Returns chart-ready data for the React frontend matching selected Target DB & Order Date.
"""

from typing import Any
import numpy as np
from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse
from services import data_service

router = APIRouter()


def _clean_param(val: Any, default: str = "") -> str:
    if hasattr(val, "default"):
        val = val.default
    s = str(val or "").strip()
    if s.startswith("annotation=") or "Query" in str(type(val)):
        return default
    return s


@router.get("/kpi")
def get_kpi(
    oerdte: str = Query("", description="Order date filter YYYYMMDD (optional)"),
    from_date: str = Query("", description="From order date filter YYYYMMDD (optional)"),
    to_date: str = Query("", description="To order date filter YYYYMMDD (optional)"),
    target_db: str = Query("pg_dev", description="Target database"),
    oewhse: str = Query("", description="Warehouse filter (optional)"),
    batch_id: str = Query("", description="Batch ID filter (optional)"),
    oeinv: str = Query("", description="Invoice number filter (optional)"),
    only_scratches: bool = Query(False, description="Only scratches filter (optional)")
):
    """Return Warehouse Level KPI summary cards for the dashboard, derived from warehouse statistics."""
    oerdte_clean = _clean_param(oerdte, "")
    target_db_clean = _clean_param(target_db, "pg_dev")
    from_date_clean = _clean_param(from_date, "")
    to_date_clean = _clean_param(to_date, "")
    oewhse_clean = _clean_param(oewhse, "")
    batch_clean = _clean_param(batch_id, "")
    oeinv_clean = _clean_param(oeinv, "")

    from app.warehouse_service import get_warehouse_statistics
    stats = get_warehouse_statistics(
        target_db=target_db_clean, oerdte=oerdte_clean, oewhse=oewhse_clean,
        batch_id=batch_clean, oeinv=oeinv_clean, only_scratches=only_scratches,
        from_date=from_date_clean, to_date=to_date_clean, limit=1000, offset=0
    )
    summary = stats.get("summary", {})

    total_whs = summary.get("total_warehouses", 0)
    total_built = summary.get("total_cases_built", 0)
    total_order = summary.get("total_original_order_qty", 0)
    total_invoices = summary.get("total_invoices_processed", 0)
    fulfillment = summary.get("procurement_fulfillment_rate", "0%")

    scratch_qty = total_order - total_built if total_order > total_built else 0
    scratch_rate = f"{(scratch_qty / total_order * 100):.1f}%" if total_order > 0 else "0%"

    kpis = [
        {
            "title": "TOTAL WAREHOUSES",
            "value": str(total_whs),
            "unit": "Facilities",
            "trend": 0.0,
            "trend_direction": "up",
            "color": "#7C3AED"
        },
        {
            "title": "CASES BUILT (cases_bld)",
            "value": f"{total_built:,}",
            "unit": "Cases",
            "trend": 8.4,
            "trend_direction": "up",
            "color": "#06B6D4"
        },
        {
            "title": "ORIGINAL ORDER QTY",
            "value": f"{total_order:,}",
            "unit": "Cases",
            "trend": 6.2,
            "trend_direction": "up",
            "color": "#F59E0B"
        },
        {
            "title": "INVOICES PROCESSED",
            "value": str(total_invoices),
            "unit": "Invoices",
            "trend": 4.1,
            "trend_direction": "up",
            "color": "#10B981"
        },
        {
            "title": "FULFILLMENT RATE",
            "value": fulfillment,
            "unit": "Target 95%",
            "trend": 2.1,
            "trend_direction": "up",
            "color": "#34D399"
        },
        {
            "title": "SCRATCH RATE",
            "value": scratch_rate,
            "unit": f"{scratch_qty:,} Cases",
            "trend": -1.5,
            "trend_direction": "down",
            "color": "#EF4444"
        }
    ]

    return JSONResponse({"kpis": kpis, "total_warehouses": total_whs, "selected_oerdte": oerdte})


@router.get("/bar")
def get_bar_chart(
    column: str = Query("warehouse", description="Categorical column for grouping"),
    metric: str = Query("cases_bld", description="Numeric column to aggregate"),
    target_db: str = Query("pg_dev", description="Target database"),
    oerdte: str = Query("", description="Order date filter YYYYMMDD"),
    oewhse: str = Query("", description="Warehouse filter (optional)"),
    batch_id: str = Query("", description="Batch ID filter (optional)"),
    oeinv: str = Query("", description="Invoice number filter (optional)"),
    only_scratches: bool = Query(False, description="Only scratches filter (optional)")
):
    target_db_clean = _clean_param(target_db, "pg_dev")
    oerdte_clean = _clean_param(oerdte, "")
    oewhse_clean = _clean_param(oewhse, "")
    batch_clean = _clean_param(batch_id, "")
    oeinv_clean = _clean_param(oeinv, "")

    col_val = str(column) if not hasattr(column, 'default') else (column.default or "warehouse")
    if col_val == "warehouse" or column == "warehouse":
        from app.warehouse_service import get_warehouse_statistics
        stats = get_warehouse_statistics(
            target_db=target_db_clean, oerdte=oerdte_clean, oewhse=oewhse_clean,
            batch_id=batch_clean, oeinv=oeinv_clean, only_scratches=only_scratches,
            limit=1000, offset=0
        )
        items = stats.get("warehouse_items", [])

        whs_totals_map = stats.get("summary", {}).get("warehouse_totals", {})
        distinct_whs = stats.get("summary", {}).get("distinct_warehouses", [])
        if not distinct_whs and whs_totals_map:
            distinct_whs = sorted(list(whs_totals_map.keys()))

        data = []
        for w in distinct_whs:
            w_totals = whs_totals_map.get(w, {}) or {}
            val = w_totals.get("cases_built", 0)
            data.append({"label": f"Whse {w}", "value": val, "whs_num": w})

        return JSONResponse({
            "chart_type": "bar",
            "title": f"Cases Built by Warehouse ({target_db_clean.upper()})",
            "data": data,
            "x_label": "Warehouse",
            "y_label": "Cases Built Qty",
            "total_warehouses": len(distinct_whs)
        })

    df = data_service.get_or_generate()
    if column not in df.columns:
        raise HTTPException(status_code=400, detail=f"Column '{column}' not found")

    metric_col = metric if metric in df.columns else df.select_dtypes(include=np.number).columns[0]
    grouped = df.groupby(column)[metric_col].mean().reset_index()
    grouped[metric_col] = grouped[metric_col].round(2)
    grouped.columns = ["label", "value"]

    return JSONResponse({
        "chart_type": "bar",
        "title": f"Average {metric_col.replace('_', ' ').title()} by {column.replace('_', ' ').title()}",
        "data": grouped.to_dict(orient="records"),
        "x_label": column,
        "y_label": f"Avg {metric_col}"
    })


@router.get("/scatter")
def get_scatter_chart(
    x: str = Query("order_qty", description="X-axis column"),
    y: str = Query("cases_bld", description="Y-axis column"),
    color: str = Query("warehouse", description="Color grouping column"),
    target_db: str = Query("pg_dev", description="Target database"),
    oerdte: str = Query("", description="Order date filter YYYYMMDD"),
    oewhse: str = Query("", description="Warehouse filter (optional)"),
    batch_id: str = Query("", description="Batch ID filter (optional)"),
    oeinv: str = Query("", description="Invoice number filter (optional)"),
    only_scratches: bool = Query(False, description="Only scratches filter (optional)")
):
    """Return warehouse scatter plot data: Original Order Qty vs Cases Built matching selected DB."""
    target_db_clean = _clean_param(target_db, "pg_dev")
    oerdte_clean = _clean_param(oerdte, "")
    oewhse_clean = _clean_param(oewhse, "")
    batch_clean = _clean_param(batch_id, "")
    oeinv_clean = _clean_param(oeinv, "")

    from app.warehouse_service import get_warehouse_statistics
    stats = get_warehouse_statistics(
        target_db=target_db_clean, oerdte=oerdte_clean, oewhse=oewhse_clean,
        batch_id=batch_clean, oeinv=oeinv_clean, only_scratches=only_scratches,
        limit=200, offset=0
    )
    items = stats.get("warehouse_items", [])

    data = [
        {
            "x": item.get("orgnl_ordr_qty_stg", 0),
            "y": item.get("cases_bld_stg", 0),
            "color": f"Whse {item.get('whs_num', '00')}"
        }
        for item in items
    ]

    return JSONResponse({
        "chart_type": "scatter",
        "title": f"Original Order Qty vs Cases Built ({target_db.upper()})",
        "data": data,
        "x_label": "Original Order Qty",
        "y_label": "Cases Built Qty"
    })


@router.get("/heatmap")
async def get_heatmap():
    """Return correlation heatmap data for numeric columns."""
    df = data_service.get_or_generate()
    numeric_df = df.select_dtypes(include=np.number)
    corr = numeric_df.corr().round(3)

    records = []
    cols = corr.columns.tolist()
    for i, row_label in enumerate(cols):
        for j, col_label in enumerate(cols):
            records.append({
                "x": col_label,
                "y": row_label,
                "value": float(corr.iloc[i, j])
            })

    return JSONResponse({
        "chart_type": "heatmap",
        "title": "Feature Correlation Matrix",
        "columns": cols,
        "data": records
    })


@router.get("/distribution")
async def get_distribution(column: str = Query("order_qty", description="Numeric column for distribution")):
    """Return histogram distribution data for numeric columns."""
    df = data_service.get_or_generate()
    if column not in df.columns or not np.issubdtype(df[column].dtype, np.number):
        column = df.select_dtypes(include=np.number).columns[0]

    counts, bin_edges = np.histogram(df[column].dropna(), bins=20)
    bins_data = [
        {
            "bin": f"{int(bin_edges[i])}-{int(bin_edges[i+1])}",
            "bin_start": float(bin_edges[i]),
            "bin_end": float(bin_edges[i+1]),
            "count": int(counts[i])
        }
        for i in range(len(counts))
    ]

    return JSONResponse({
        "chart_type": "histogram",
        "title": f"Distribution of {column.replace('_', ' ').title()}",
        "data": bins_data,
        "column": column
    })
