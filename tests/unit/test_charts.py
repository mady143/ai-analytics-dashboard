"""
Unit tests for chart data endpoints.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "backend"))

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_kpi_endpoint():
    """KPI endpoint should return list of KPI cards."""
    response = client.get("/api/charts/kpi")
    assert response.status_code == 200
    data = response.json()
    assert "kpis" in data
    assert len(data["kpis"]) >= 4
    for kpi in data["kpis"]:
        assert "title" in kpi
        assert "value" in kpi
        assert "color" in kpi


def test_bar_chart_default():
    """Bar chart should return data grouped by department."""
    response = client.get("/api/charts/bar")
    assert response.status_code == 200
    data = response.json()
    assert data["chart_type"] == "bar"
    assert "data" in data
    assert len(data["data"]) > 0
    assert "label" in data["data"][0]
    assert "value" in data["data"][0]


def test_bar_chart_custom_column():
    """Bar chart should work with custom column and metric."""
    response = client.get("/api/charts/bar?column=region&metric=performance_score")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) > 0


def test_bar_chart_invalid_column():
    """Bar chart with invalid column should return 400."""
    response = client.get("/api/charts/bar?column=nonexistent")
    assert response.status_code == 400


def test_scatter_chart():
    """Scatter chart should return x, y, color data."""
    response = client.get("/api/charts/scatter")
    assert response.status_code == 200
    data = response.json()
    assert data["chart_type"] == "scatter"
    assert "data" in data


def test_task27_single_warehouse_chart_filtering():
    """Task 27: When oewhse is provided, bar chart and scatter plot must strictly return ONLY data for that warehouse."""
    bar_res = client.get("/api/charts/bar?target_db=pg_dev&oewhse=58")
    assert bar_res.status_code == 200
    bar_json = bar_res.json()
    assert len(bar_json["data"]) == 1
    assert bar_json["data"][0]["whs_num"] == "58"

    scatter_res = client.get("/api/charts/scatter?target_db=pg_dev&oewhse=58")
    assert scatter_res.status_code == 200
    scatter_json = scatter_res.json()
    assert len(scatter_json["data"]) > 0
    for point in scatter_json["data"]:
        assert point["color"] == "Whse 58"

    assert len(data["data"]) > 0
    assert "x" in data["data"][0]
    assert "y" in data["data"][0]


def test_heatmap():
    """Heatmap should return correlation matrix data."""
    response = client.get("/api/charts/heatmap")
    assert response.status_code == 200
    data = response.json()
    assert data["chart_type"] == "heatmap"
    assert "columns" in data
    assert len(data["data"]) > 0


def test_distribution():
    """Distribution endpoint should return histogram bins."""
    response = client.get("/api/charts/distribution?column=salary")
    assert response.status_code == 200
    data = response.json()
    assert data["chart_type"] == "histogram"
    assert len(data["data"]) == 20  # 20 bins
    for bin_item in data["data"]:
        assert "bin_start" in bin_item
        assert "bin_end" in bin_item
        assert "count" in bin_item
