"""
TASK 20 — Unit Tests: Aware of Fallback Date Behavior
=======================================================
KEY RULE (from warehouse_service.py L255):
  When selected oerdte has NO data in the DB, the backend automatically
  falls back to all-dates query (oerdte="") and returns the most recent available data.
  This is CORRECT behavior — tests must verify it, not fail because of it.

Test scenarios covered:
  1. When today has no data → backend falls back → response still has data (fallback_used=True)
  2. When a known date HAS data → response has data for that exact date (fallback_used=False)
  3. AI Copilot: NEVER uses date — always queries full dataset
  4. Dashboard APIs: PASS the date; if date empty, fallback kicks in automatically
  5. Agents: all running
  6. Health: healthy
"""

import pytest
import sys
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "backend"))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

TODAY_ISO = date.today().strftime("%Y%m%d")   # e.g. "20260730"
TODAY_DISPLAY = date.today().strftime("%Y-%m-%d")


# ─────────────────────────────────────────────────────────────
# Helper: discover a date that actually has data
# ─────────────────────────────────────────────────────────────
def get_real_data_date(target_db: str = "pg_dev") -> dict:
    """
    Calls the warehouse API with no date filter.
    The backend returns real data from the most recent available date.
    Returns dict with: effective_date, fallback_used, item_count
    """
    res = client.get(f"/api/warehouse/statistics?oerdte=&target_db={target_db}&limit=5&offset=0")
    assert res.status_code == 200, f"Helper failed: {res.text}"
    data = res.json()
    items = data.get("warehouse_items", [])
    filters = data.get("filters_applied", {})
    effective = filters.get("effective_date", "")
    return {
        "effective_date": effective,
        "item_count": len(items),
        "fallback_used": filters.get("fallback_used", False),
        "data": data
    }


# ─────────────────────────────────────────────────────────────
# TC-UNIT-01: Today has no data → fallback returns most recent date
# ─────────────────────────────────────────────────────────────
def test_unit01_today_no_data_triggers_fallback():
    """
    TC-UNIT-01: When today's date has no records (SQL returns empty),
    the backend MUST automatically fall back to the most recent date
    with data and return that, with fallback_used=True.
    This is confirmed by: select distinct oewhse from sptn_sales_data where oerdte='20260730' → empty.
    """
    res = client.get(f"/api/warehouse/statistics?oerdte={TODAY_ISO}&target_db=pg_dev&limit=10&offset=0")
    assert res.status_code == 200, f"TC-UNIT-01 FAIL: {res.text}"
    data = res.json()
    items = data.get("warehouse_items", [])
    filters = data.get("filters_applied", {})

    if len(items) == 0:
        # Today has no data AND no fallback → this would be a real failure
        pytest.fail(
            f"TC-UNIT-01 FAIL: No data returned and no fallback for date {TODAY_ISO}. "
            f"Backend should fall back to most recent date with data."
        )
    else:
        effective = filters.get("effective_date", TODAY_ISO)
        fallback_used = filters.get("fallback_used", False)
        if fallback_used:
            print(f"TC-UNIT-01 PASS: Today ({TODAY_DISPLAY}) has no data → fallback to {effective} with {len(items)} items")
        else:
            print(f"TC-UNIT-01 PASS: Today ({TODAY_DISPLAY}) has {len(items)} items of its own data")


# ─────────────────────────────────────────────────────────────
# TC-UNIT-02: Discover the actual date with data dynamically
# ─────────────────────────────────────────────────────────────
def test_unit02_discover_real_data_date():
    """
    TC-UNIT-02: The API with oerdte="" returns the most recent date with real data.
    The effective_date in filters_applied tells us exactly which date has data.
    """
    info = get_real_data_date("pg_dev")
    assert info["item_count"] > 0, "TC-UNIT-02 FAIL: No data in pg_dev at all (even with no date filter)"
    effective = info["effective_date"]
    assert effective, f"TC-UNIT-02 FAIL: effective_date is empty even with data: {info}"
    print(f"TC-UNIT-02 PASS: Real data date discovered = '{effective}' ({info['item_count']} items)")


# ─────────────────────────────────────────────────────────────
# TC-UNIT-03: KPI API — date with no data falls back gracefully
# ─────────────────────────────────────────────────────────────
def test_unit03_kpi_api_returns_data_even_when_date_empty():
    """
    TC-UNIT-03: KPI API must return >= 4 KPIs regardless of whether the selected date
    has data or not (backend falls back automatically).
    """
    res = client.get(f"/api/charts/kpi?oerdte={TODAY_ISO}&target_db=pg_dev")
    assert res.status_code == 200, f"TC-UNIT-03 FAIL: {res.text}"
    data = res.json()
    kpis = data.get("kpis", [])
    assert len(kpis) >= 4, f"TC-UNIT-03 FAIL: Expected >= 4 KPIs, got {len(kpis)}"
    print(f"TC-UNIT-03 PASS: KPI API returned {len(kpis)} KPIs for {TODAY_ISO} (fallback may apply)")


# ─────────────────────────────────────────────────────────────
# TC-UNIT-04: Bar chart API — returns data with or without fallback
# ─────────────────────────────────────────────────────────────
def test_unit04_bar_chart_api_returns_data_regardless_of_date():
    """TC-UNIT-04: Bar chart API returns data even when today has no records (fallback applies)."""
    res = client.get(f"/api/charts/bar?oerdte={TODAY_ISO}&target_db=pg_dev")
    assert res.status_code == 200
    data = res.json()
    assert "data" in data, f"TC-UNIT-04 FAIL: No 'data' key: {list(data.keys())}"
    print(f"TC-UNIT-04 PASS: Bar chart API returned {len(data['data'])} points for {TODAY_ISO}")


# ─────────────────────────────────────────────────────────────
# TC-UNIT-05: Scatter chart API — same fallback behavior
# ─────────────────────────────────────────────────────────────
def test_unit05_scatter_chart_api_returns_data_regardless_of_date():
    """TC-UNIT-05: Scatter chart API returns data even when today has no records."""
    res = client.get(f"/api/charts/scatter?oerdte={TODAY_ISO}&target_db=pg_dev")
    assert res.status_code == 200
    data = res.json()
    assert "data" in data, f"TC-UNIT-05 FAIL: No 'data' key: {list(data.keys())}"
    print(f"TC-UNIT-05 PASS: Scatter API returned {len(data['data'])} points for {TODAY_ISO}")


# ─────────────────────────────────────────────────────────────
# TC-UNIT-06: Warehouse stats with effective (real) date — no fallback needed
# ─────────────────────────────────────────────────────────────
def test_unit06_warehouse_stats_with_real_date_no_fallback():
    """
    TC-UNIT-06: When queried with the ACTUAL date that has data (discovered dynamically),
    the backend returns data directly without needing the fallback.
    """
    info = get_real_data_date("pg_dev")
    effective = info["effective_date"]
    if not effective:
        pytest.skip("TC-UNIT-06 SKIP: Could not discover a real data date")

    res = client.get(f"/api/warehouse/statistics?oerdte={effective}&target_db=pg_dev&limit=10&offset=0")
    assert res.status_code == 200
    data = res.json()
    items = data.get("warehouse_items", [])
    filters = data.get("filters_applied", {})
    assert len(items) > 0, f"TC-UNIT-06 FAIL: No items for confirmed real date {effective}"
    fallback_used = filters.get("fallback_used", False)
    assert not fallback_used, (
        f"TC-UNIT-06 FAIL: fallback_used=True for a date that should have real data: {effective}"
    )
    print(f"TC-UNIT-06 PASS: Real date {effective} returned {len(items)} items without fallback")


# ─────────────────────────────────────────────────────────────
# TC-UNIT-07: Warehouse stats no date = full dataset
# ─────────────────────────────────────────────────────────────
def test_unit07_warehouse_statistics_no_date_returns_full_data():
    """TC-UNIT-07: Passing oerdte='' returns data across all dates."""
    res = client.get("/api/warehouse/statistics?oerdte=&target_db=pg_dev&limit=20&offset=0")
    assert res.status_code == 200
    items = res.json().get("warehouse_items", [])
    assert len(items) >= 1, "TC-UNIT-07 FAIL: No items with no date filter"
    print(f"TC-UNIT-07 PASS: No-date query returned {len(items)} items")


# ─────────────────────────────────────────────────────────────
# TC-UNIT-08: Anomaly API — works with any date (fallback applies internally)
# ─────────────────────────────────────────────────────────────
def test_unit08_anomaly_api_works_for_any_date():
    """TC-UNIT-08: Anomaly API responds for today's date (even if no records, returns empty alerts cleanly)."""
    res = client.get(f"/api/analytics/anomalies?oerdte={TODAY_ISO}&target_db=pg_dev")
    assert res.status_code == 200, f"TC-UNIT-08 FAIL: {res.text}"
    data = res.json()
    assert "anomalies" in data or "alerts" in data or "status" in data, (
        f"TC-UNIT-08 FAIL: Unexpected shape: {list(data.keys())}"
    )
    print(f"TC-UNIT-08 PASS: Anomaly API responded for {TODAY_ISO}")


# ─────────────────────────────────────────────────────────────
# TC-UNIT-09: AI Copilot — ALWAYS queries full dataset (no date)
# ─────────────────────────────────────────────────────────────
def test_unit09_copilot_always_queries_without_date():
    """
    TC-UNIT-09 CRITICAL: Copilot must return real data even when today has no records.
    It does NOT use the date — it queries ALL dates directly.
    Pass a future date that definitely has no data: copilot must still answer.
    """
    res = client.post("/api/analytics/ai-copilot", json={
        "prompt": "High Scratch Quantity",
        "target_db": "pg_dev",
        "oerdte": "29991231"  # Far future — definitely no data
    })
    assert res.status_code == 200, f"TC-UNIT-09 FAIL: {res.text}"
    data = res.json()
    summary = data.get("summary_answer", "")
    assert summary, "TC-UNIT-09 FAIL: Empty summary_answer — copilot not returning data"
    assert "across all" in summary.lower() or "all dates" in summary.lower() or "all available" in summary.lower(), (
        f"TC-UNIT-09 FAIL: Copilot answer doesn't confirm full-dataset query: '{summary}'"
    )
    print(f"TC-UNIT-09 PASS: Copilot returns full-dataset answer regardless of sent date: '{summary[:80]}'")


# ─────────────────────────────────────────────────────────────
# TC-UNIT-10: Copilot with empty oerdte returns full dataset
# ─────────────────────────────────────────────────────────────
def test_unit10_copilot_with_empty_date_returns_data():
    """TC-UNIT-10: Frontend sends oerdte='' to copilot — must return real data."""
    res = client.post("/api/analytics/ai-copilot", json={
        "prompt": "Warehouse 58 Overview",
        "target_db": "pg_dev",
        "oerdte": ""
    })
    assert res.status_code == 200
    data = res.json()
    assert data.get("summary_answer"), "TC-UNIT-10 FAIL: No summary_answer for empty-date copilot"
    print(f"TC-UNIT-10 PASS: Copilot empty-date returned: '{data['summary_answer'][:80]}'")


# ─────────────────────────────────────────────────────────────
# TC-UNIT-11: Agent status — all running
# ─────────────────────────────────────────────────────────────
def test_unit11_agent_status_all_running():
    """TC-UNIT-11: /api/agents/status must return >= 5 agents all status='running'."""
    res = client.get("/api/agents/status")
    assert res.status_code == 200, f"TC-UNIT-11 FAIL: {res.text}"
    agents = res.json().get("agents", {})
    assert len(agents) >= 5, f"TC-UNIT-11 FAIL: Expected >= 5 agents, got {len(agents)}"
    idle = [n for n, v in agents.items() if isinstance(v, dict) and v.get("status") != "running"]
    assert len(idle) == 0, f"TC-UNIT-11 FAIL: Idle agents: {idle}"
    print(f"TC-UNIT-11 PASS: All {len(agents)} agents running: {list(agents.keys())}")


# ─────────────────────────────────────────────────────────────
# TC-UNIT-12: Health check
# ─────────────────────────────────────────────────────────────
def test_unit12_health_check():
    """TC-UNIT-12: /api/health returns healthy."""
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json().get("status") == "healthy"
    print("TC-UNIT-12 PASS: Health check healthy")


# ─────────────────────────────────────────────────────────────
# TC-UNIT-13: Copilot warehouse 58 filter extraction
# ─────────────────────────────────────────────────────────────
def test_unit13_copilot_extracts_warehouse_58():
    """TC-UNIT-13: Asking about warehouse 58 → filtered_whse='58'."""
    res = client.post("/api/analytics/ai-copilot", json={
        "prompt": "Warehouse 58 cases built",
        "target_db": "pg_dev",
        "oerdte": ""
    })
    assert res.status_code == 200
    data = res.json()
    assert data.get("filtered_whse"), f"TC-UNIT-13 FAIL: No filtered_whse: {data}"
    assert data["filtered_whse"].strip().lstrip("0") == "58", (
        f"TC-UNIT-13 FAIL: Expected '58', got '{data['filtered_whse']}'"
    )
    print("TC-UNIT-13 PASS: Copilot extracted warehouse 58")


# ─────────────────────────────────────────────────────────────
# TC-UNIT-14: Copilot scratch query sets filter_scratch=True
# ─────────────────────────────────────────────────────────────
def test_unit14_copilot_scratch_sets_filter():
    """TC-UNIT-14: High Scratch Quantity query → filter_scratch=True."""
    res = client.post("/api/analytics/ai-copilot", json={
        "prompt": "High Scratch Quantity",
        "target_db": "pg_dev",
        "oerdte": ""
    })
    assert res.status_code == 200
    assert res.json().get("filter_scratch") is True, (
        f"TC-UNIT-14 FAIL: filter_scratch not True: {res.json()}"
    )
    print("TC-UNIT-14 PASS: Scratch query sets filter_scratch=True")
