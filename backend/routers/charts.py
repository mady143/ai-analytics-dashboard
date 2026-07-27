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
    """Return KPI summary cards for the dashboard."""
    df = data_service.get_or_generate()

    kpis = [
        {
            "title": "Total Employees",
            "value": len(df),
            "unit": None,
            "trend": 5.2,
            "trend_direction": "up",
            "color": "#7C3AED"
        },
        {
            "title": "Avg Salary",
            "value": f"${df['salary'].mean():,.0f}" if "salary" in df.columns else "N/A",
            "unit": None,
            "trend": 3.1,
            "trend_direction": "up",
            "color": "#06B6D4"
        },
        {
            "title": "Avg Performance",
            "value": round(df["performance_score"].mean(), 2) if "performance_score" in df.columns else "N/A",
            "unit": "/ 5.0",
            "trend": -0.5,
            "trend_direction": "down",
            "color": "#F59E0B"
        },
        {
            "title": "Attrition Rate",
            "value": f"{df['attrition'].mean() * 100:.1f}%" if "attrition" in df.columns else "N/A",
            "unit": None,
            "trend": -2.3,
            "trend_direction": "down",
            "color": "#EF4444"
        },
        {
            "title": "Avg Satisfaction",
            "value": round(df["satisfaction_score"].mean(), 1) if "satisfaction_score" in df.columns else "N/A",
            "unit": "/ 10",
            "trend": 1.8,
            "trend_direction": "up",
            "color": "#10B981"
        },
        {
            "title": "Promotion Rate",
            "value": f"{df['promoted'].mean() * 100:.1f}%" if "promoted" in df.columns else "N/A",
            "unit": None,
            "trend": 0.7,
            "trend_direction": "up",
            "color": "#8B5CF6"
        }
    ]

    return JSONResponse({"kpis": kpis})


@router.get("/bar")
async def get_bar_chart(
    column: str = Query("department", description="Categorical column for grouping"),
    metric: str = Query("salary", description="Numeric column to aggregate")
):
    """Return bar chart data: avg metric per category."""
    df = data_service.get_or_generate()

    if column not in df.columns:
        raise HTTPException(status_code=400, detail=f"Column '{column}' not found")
    if metric not in df.columns:
        raise HTTPException(status_code=400, detail=f"Metric '{metric}' not found")

    grouped = df.groupby(column)[metric].mean().reset_index()
    grouped[metric] = grouped[metric].round(2)
    grouped.columns = ["label", "value"]

    return JSONResponse({
        "chart_type": "bar",
        "title": f"Average {metric.replace('_', ' ').title()} by {column.replace('_', ' ').title()}",
        "data": grouped.to_dict(orient="records"),
        "x_label": column,
        "y_label": f"Avg {metric}"
    })


@router.get("/scatter")
async def get_scatter_chart(
    x: str = Query("experience_years", description="X-axis column"),
    y: str = Query("salary", description="Y-axis column"),
    color: str = Query("department", description="Color grouping column")
):
    """Return scatter plot data."""
    df = data_service.get_or_generate()

    for col in [x, y]:
        if col not in df.columns:
            raise HTTPException(status_code=400, detail=f"Column '{col}' not found")

    # Limit to 300 points for performance
    sample_df = df[[x, y, color]].dropna().sample(min(300, len(df)), random_state=42)
    data = sample_df.rename(columns={x: "x", y: "y", color: "color"}).to_dict(orient="records")

    return JSONResponse({
        "chart_type": "scatter",
        "title": f"{y.replace('_', ' ').title()} vs {x.replace('_', ' ').title()}",
        "data": data,
        "x_label": x.replace("_", " ").title(),
        "y_label": y.replace("_", " ").title()
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
