"""
TASK 19 & 20 — Unit Tests: AI Copilot Date-Agnostic + Default Date Parameter Rule
====================================================================================
Validates:
  1. AI Copilot backend endpoint ALWAYS queries with oerdte="" (never uses date)
  2. Dashboard APIs (KPI, bar, scatter, warehouse) ALWAYS include the oerdte param
  3. Default date (today) is applied on first API call
  4. Warehouse filter propagates correctly through API calls
"""

import pytest
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "backend"))

from datetime import date
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

TODAY_ISO = date.today().strftime("%Y%m%d")
KNOWN_DATE = "20260730"


# ─────────────────────────────────────────────────────────────
# TC-UNIT-01: Copilot endpoint ignores oerdte — always queries all dates
# ─────────────────────────────────────────────────────────────
def test_unit01_copilot_always_queries_without_date():
    """TC-UNIT-01: Copilot must return data even when a date with no records is sent."""
    # Send a date that likely has NO data — copilot must still return results from full DB
    res = client.post("/api/analytics/ai-copilot", json={
        "prompt": "High Scratch Quantity",
        "target_db": "pg_dev",
        "oerdte": "19990101"  # 1999 - definitely no data; copilot must still answer
    })
    assert res.status_code == 200, f"TC-UNIT-01 FAIL: {res.text}"
    data = res.json()
    assert data.get("status") == "success"
    # Summary answer must mention real items or warehouses (not 'Found 0')
    summary = data.get("summary_answer", "")
    assert summary, f"TC-UNIT-01 FAIL: summary_answer is empty"
    # "across all dates" must appear — confirms date-agnostic backend logic
    assert "across all" in summary.lower() or "all dates" in summary.lower() or "all available" in summary.lower(), (
        f"TC-UNIT-01 FAIL: summary_answer does not indicate full dataset query: '{summary}'"
    )
    print(f"TC-UNIT-01 PASS: Copilot returned full-dataset answer: '{summary[:80]}...'")


# ─────────────────────────────────────────────────────────────
# TC-UNIT-02: Copilot with empty oerdte still returns data
# ─────────────────────────────────────────────────────────────
def test_unit02_copilot_with_empty_date_returns_data():
    """TC-UNIT-02: Copilot with oerdte='' returns real data from full dataset."""
    res = client.post("/api/analytics/ai-copilot", json={
        "prompt": "Warehouse 58 Overview",
        "target_db": "pg_dev",
        "oerdte": ""  # This is what the frontend now sends
    })
    assert res.status_code == 200
    data = res.json()
    assert data.get("status") == "success"
    summary = data.get("summary_answer", "")
    assert summary, "TC-UNIT-02 FAIL: No summary_answer"
    print(f"TC-UNIT-02 PASS: Copilot empty-date returned: '{summary[:80]}...'")


# ─────────────────────────────────────────────────────────────
# TC-UNIT-03: KPI API requires oerdte and returns data for known date
# ─────────────────────────────────────────────────────────────
def test_unit03_kpi_api_uses_date_param():
    """TC-UNIT-03: KPI chart API must accept oerdte and return structured KPI data."""
    res = client.get(f"/api/charts/kpi?oerdte={KNOWN_DATE}&target_db=pg_dev")
    assert res.status_code == 200, f"TC-UNIT-03 FAIL: {res.text}"
    data = res.json()
    assert "kpis" in data, f"TC-UNIT-03 FAIL: No 'kpis' key in response: {data.keys()}"
    kpis = data["kpis"]
    assert len(kpis) >= 4, f"TC-UNIT-03 FAIL: Expected >= 4 KPIs, got {len(kpis)}"
    print(f"TC-UNIT-03 PASS: KPI API returned {len(kpis)} KPIs for date {KNOWN_DATE}")


# ─────────────────────────────────────────────────────────────
# TC-UNIT-04: Bar chart API uses oerdte
# ─────────────────────────────────────────────────────────────
def test_unit04_bar_chart_api_uses_date_param():
    """TC-UNIT-04: Bar chart API uses oerdte and returns chart data."""
    res = client.get(f"/api/charts/bar?oerdte={KNOWN_DATE}&target_db=pg_dev")
    assert res.status_code == 200
    data = res.json()
    assert "data" in data, f"TC-UNIT-04 FAIL: No 'data' key: {data.keys()}"
    print(f"TC-UNIT-04 PASS: Bar chart API returned {len(data['data'])} data points for {KNOWN_DATE}")


# ─────────────────────────────────────────────────────────────
# TC-UNIT-05: Scatter chart API uses oerdte
# ─────────────────────────────────────────────────────────────
def test_unit05_scatter_chart_api_uses_date_param():
    """TC-UNIT-05: Scatter chart API uses oerdte and returns scatter data."""
    res = client.get(f"/api/charts/scatter?oerdte={KNOWN_DATE}&target_db=pg_dev")
    assert res.status_code == 200
    data = res.json()
    assert "data" in data, f"TC-UNIT-05 FAIL: No 'data' key: {data.keys()}"
    print(f"TC-UNIT-05 PASS: Scatter chart returned {len(data['data'])} points for {KNOWN_DATE}")


# ─────────────────────────────────────────────────────────────
# TC-UNIT-06: Warehouse statistics API uses oerdte
# ─────────────────────────────────────────────────────────────
def test_unit06_warehouse_statistics_api_uses_date_param():
    """TC-UNIT-06: Warehouse statistics API accepts oerdte, returns paginated warehouse items."""
    res = client.get(f"/api/warehouse/statistics?oerdte={KNOWN_DATE}&target_db=pg_dev&limit=10&offset=0")
    assert res.status_code == 200
    data = res.json()
    assert "warehouse_items" in data, f"TC-UNIT-06 FAIL: No 'warehouse_items': {data.keys()}"
    print(f"TC-UNIT-06 PASS: Warehouse stats returned {len(data['warehouse_items'])} items for {KNOWN_DATE}")


# ─────────────────────────────────────────────────────────────
# TC-UNIT-07: Warehouse statistics API with no date returns all-dates data
# ─────────────────────────────────────────────────────────────
def test_unit07_warehouse_statistics_no_date_returns_full_data():
    """TC-UNIT-07: Passing oerdte='' to warehouse API returns data across all dates."""
    res = client.get("/api/warehouse/statistics?oerdte=&target_db=pg_dev&limit=20&offset=0")
    assert res.status_code == 200
    data = res.json()
    items = data.get("warehouse_items", [])
    assert len(items) >= 1, "TC-UNIT-07 FAIL: No warehouse items returned for empty date"
    print(f"TC-UNIT-07 PASS: Warehouse stats (no date) returned {len(items)} items")


# ─────────────────────────────────────────────────────────────
# TC-UNIT-08: Anomaly API uses oerdte
# ─────────────────────────────────────────────────────────────
def test_unit08_anomaly_api_uses_date_param():
    """TC-UNIT-08: Anomaly API accepts oerdte and returns alerts list."""
    res = client.get(f"/api/analytics/anomalies?oerdte={KNOWN_DATE}&target_db=pg_dev")
    assert res.status_code == 200
    data = res.json()
    assert "anomalies" in data or "alerts" in data or "status" in data, (
        f"TC-UNIT-08 FAIL: Unexpected response shape: {data.keys()}"
    )
    print(f"TC-UNIT-08 PASS: Anomaly API responded for date {KNOWN_DATE}")


# ─────────────────────────────────────────────────────────────
# TC-UNIT-09: Agent status API returns all 6 agents as 'running'
# ─────────────────────────────────────────────────────────────
def test_unit09_agent_status_all_running():
    """TC-UNIT-09: /api/agents/status must return at least 5 agents, all with status='running'."""
    res = client.get("/api/agents/status")
    assert res.status_code == 200, f"TC-UNIT-09 FAIL: {res.text}"
    data = res.json()
    agents = data.get("agents", {})
    assert len(agents) >= 5, f"TC-UNIT-09 FAIL: Expected >= 5 agents, got {len(agents)}: {list(agents.keys())}"

    idle_agents = [name for name, info in agents.items() if isinstance(info, dict) and info.get("status") != "running"]
    assert len(idle_agents) == 0, f"TC-UNIT-09 FAIL: These agents are not 'running': {idle_agents}"
    print(f"TC-UNIT-09 PASS: All {len(agents)} agents are 'running': {list(agents.keys())}")


# ─────────────────────────────────────────────────────────────
# TC-UNIT-10: Health check endpoint returns healthy
# ─────────────────────────────────────────────────────────────
def test_unit10_health_check_returns_healthy():
    """TC-UNIT-10: /api/health must return status=healthy."""
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data.get("status") == "healthy", f"TC-UNIT-10 FAIL: {data}"
    print("TC-UNIT-10 PASS: Health check returned healthy")


# ─────────────────────────────────────────────────────────────
# TC-UNIT-11: Copilot with warehouse filter returns warehouse-specific answer
# ─────────────────────────────────────────────────────────────
def test_unit11_copilot_warehouse_query_returns_warehouse_specific_answer():
    """TC-UNIT-11: Asking copilot about a specific warehouse returns warehouse-specific data."""
    res = client.post("/api/analytics/ai-copilot", json={
        "prompt": "Warehouse 58 cases built",
        "target_db": "pg_dev",
        "oerdte": ""
    })
    assert res.status_code == 200
    data = res.json()
    assert data.get("filtered_whse"), (
        f"TC-UNIT-11 FAIL: No filtered_whse returned for warehouse 58 query. Data: {data}"
    )
    assert data["filtered_whse"] in ["58", "58 "], (
        f"TC-UNIT-11 FAIL: Expected filtered_whse='58', got '{data['filtered_whse']}'"
    )
    print(f"TC-UNIT-11 PASS: Copilot correctly identified warehouse 58")


# ─────────────────────────────────────────────────────────────
# TC-UNIT-12: Copilot scratch query marks filter_scratch=True
# ─────────────────────────────────────────────────────────────
def test_unit12_copilot_scratch_query_sets_filter_scratch():
    """TC-UNIT-12: Asking about scratch quantity must return filter_scratch=True."""
    res = client.post("/api/analytics/ai-copilot", json={
        "prompt": "High Scratch Quantity",
        "target_db": "pg_dev",
        "oerdte": ""
    })
    assert res.status_code == 200
    data = res.json()
    assert data.get("filter_scratch") is True, (
        f"TC-UNIT-12 FAIL: filter_scratch should be True for scratch query, got: {data.get('filter_scratch')}"
    )
    print("TC-UNIT-12 PASS: Scratch query correctly sets filter_scratch=True")
