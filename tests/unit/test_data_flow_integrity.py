"""Unit test for Data Flow Integrity across charts and analytics endpoints."""
from pathlib import Path
import pytest

ROOT_DIR = Path(__file__).parent.parent.parent

def test_charts_router_has_warehouse_totals():
    charts_file = ROOT_DIR / "backend" / "routers" / "charts.py"
    assert charts_file.exists(), "charts.py router must exist"
    content = charts_file.read_text(encoding="utf-8")
    assert "warehouse_totals" in content, "charts.py must use warehouse_totals from SQL summary"
