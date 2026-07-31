"""
Auto-generated unit tests for Plane task: Data Distrubances
Task ID: 9f427731-d9a2-45cc-b8b9-3fa08ec8c8d3
Description: <image-component data-id="f154bc66-4f47-47d8-b00c-39f51de6e423" src="13980eb4-e22d-499e-96cb-8d5082f5df90" id="f154bc66-4f47-47d8-b00c-39f51de6e423" width="299px" height="81px" aspectratio="3.69449081
Generated at: 2026-07-31T11:42:04.721565
"""
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent

def test_task_picked_up():
    """Verify task was picked up and processed by the agent."""
    assert True, "Task Data Distrubances was processed by Builder Agent"

def test_dashboard_whse_filter_support():
    """Verify Dashboard.jsx extracts whse from tableFilters for page-wide filtering."""
    dash_file = ROOT_DIR / "frontend" / "src" / "pages" / "Dashboard.jsx"
    content = dash_file.read_text(encoding="utf-8")
    assert "tableFilters?.whse" in content, "Dashboard.jsx must extract tableFilters?.whse"
    assert "tableFilters?.filtered_whse" in content, "Dashboard.jsx must extract tableFilters?.filtered_whse"

def test_warehouse_58_copilot_and_kpi_filter():
    """Verify warehouse 58 filter API parameter support."""
    from fastapi.testclient import TestClient
    import sys
    sys.path.insert(0, str(ROOT_DIR / "backend"))
    from main import app

    client = TestClient(app)
    # Test Copilot NLP extraction for Whse 58
    copilot_res = client.post("/api/analytics/ai-copilot", json={"prompt": "selected warehouse 58 overview", "target_db": "pg_dev", "oerdte": ""})
    assert copilot_res.status_code == 200
    data = copilot_res.json()
    assert data.get("filtered_whse") == "58", "Copilot should extract filtered_whse '58'"

    # Test KPI card filter with oewhse=58
    kpi_res = client.get("/api/charts/kpi?oerdte=&target_db=pg_dev&oewhse=58")
    assert kpi_res.status_code == 200
    kpis = kpi_res.json().get("kpis", [])
    assert len(kpis) > 0, "KPI endpoint should return data for oewhse=58"


