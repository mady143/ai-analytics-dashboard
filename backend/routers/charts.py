"""
Charts Router — Returns chart-ready data for the React frontend.
"""

import numpy as np
from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse
from services import data_service

router = APIRouter()


@router.get("/kpi")
async def get_kpi():
    """Return Warehouse Level KPI summary cards for the dashboard."""
    kpis = [
        {
            "title": "TOTAL WAREHOUSES",
            "value": "2",
            "unit": "Facilities",
            "trend": 0.0,
            "trend_direction": "up",
            "color": "#7C3AED"
        },
        {
            "title": "CASES BUILT (cases_bld)",
            "value": "4,760",
            "unit": "Cases",
            "trend": 8.4,
            "trend_direction": "up",
            "color": "#06B6D4"
        },
        {
            "title": "ORIGINAL ORDER QTY",
            "value": "4,900",
            "unit": "Cases",
            "trend": 6.2,
            "trend_direction": "up",
            "color": "#F59E0B"
        },
        {
            "title": "INVOICES PROCESSED",
            "value": "384",
            "unit": "Invoices",
            "trend": 4.1,
            "trend_direction": "up",
            "color": "#10B981"
        },
        {
            "title": "FULFILLMENT RATE",
            "value": "97.1%",
            "unit": "Target 95%",
            "trend": 2.1,
            "trend_direction": "up",
            "color": "#34D399"
        },
        {
            "title": "SCRATCH RATE",
            "value": "2.9%",
            "unit": "140 Cases",
            "trend": -1.5,
            "trend_direction": "down",
            "color": "#EF4444"
        }
    ]

    return JSONResponse({"kpis": kpis})


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
