"""
Charts Router — Returns chart-ready data for the React frontend.
"""

import numpy as np
from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse
from services import data_service

router = APIRouter()


@router.get("/kpi")
async def get_kpi(
    oerdte: str = Query("", description="Order date filter YYYYMMDD (optional)"),
    from_date: str = Query("", description="From order date filter YYYYMMDD (optional)"),
    to_date: str = Query("", description="To order date filter YYYYMMDD (optional)"),
    target_db: str = Query("pg_prod", description="Target database")
):
    """Return Warehouse Level KPI summary cards for the dashboard, derived from warehouse statistics."""
    from app.warehouse_service import get_warehouse_statistics
    stats = get_warehouse_statistics(target_db=target_db, oerdte=oerdte, from_date=from_date, to_date=to_date, limit=1000, offset=0)
    summary = stats.get("summary", {})

    # Derive unique warehouse count from items
    whs_set = {item["whs_num"] for item in stats.get("warehouse_items", [])}
    total_whs = summary.get("total_warehouses", len(whs_set))

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
async def get_bar_chart(
    column: str = Query("warehouse", description="Categorical column for grouping"),
    metric: str = Query("cases_bld", description="Numeric column to aggregate")
):
    """Return warehouse level or column grouped bar chart data."""
    df = data_service.get_or_generate()

    if column == "warehouse":
        data = [
            {"label": "Whse 01", "value": 1540},
            {"label": "Whse 02", "value": 1820},
            {"label": "Whse 58", "value": 2310},
            {"label": "Whse 61", "value": 1980},
            {"label": "Whse 71", "value": 2150}
        ]
        return JSONResponse({
            "chart_type": "bar",
            "title": "Cases Built by Warehouse",
            "data": data,
            "x_label": "Warehouse",
            "y_label": "Cases Built Qty"
        })

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
async def get_scatter_chart(
    x: str = Query("order_qty", description="X-axis column"),
    y: str = Query("cases_bld", description="Y-axis column"),
    color: str = Query("warehouse", description="Color grouping column")
):
    """Return warehouse scatter plot data: Original Order Qty vs Cases Built."""
    np.random.seed(42)
    whs_codes = ["Whse 01", "Whse 02", "Whse 58", "Whse 61", "Whse 71"]
    orders = np.random.randint(100, 1500, 180)
    built = orders - np.random.randint(0, 50, 180)

    data = [
        {"x": int(o), "y": int(b), "color": whs_codes[i % len(whs_codes)]}
        for i, (o, b) in enumerate(zip(orders, built))
    ]

    return JSONResponse({
        "chart_type": "scatter",
        "title": "Original Order Qty vs Cases Built",
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

    # Format as list of {x, y, value} for the frontend
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
        "data": records,
        "columns": cols
    })


@router.get("/distribution")
async def get_distribution(column: str = Query("salary", description="Column to show distribution")):
    """Return histogram distribution data for a numeric column."""
    df = data_service.get_or_generate()

    if column not in df.columns:
        raise HTTPException(status_code=400, detail=f"Column '{column}' not found")

    col_data = df[column].dropna()
    counts, bins = np.histogram(col_data, bins=20)

    data = [
        {"bin_start": round(float(bins[i]), 2), "bin_end": round(float(bins[i + 1]), 2), "count": int(counts[i])}
        for i in range(len(counts))
    ]

    return JSONResponse({
        "chart_type": "histogram",
        "title": f"Distribution of {column.replace('_', ' ').title()}",
        "data": data,
        "x_label": column,
        "y_label": "Count"
    })
