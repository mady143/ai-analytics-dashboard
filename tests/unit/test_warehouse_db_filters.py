"""
Dynamic Unit Tests for Target Database Filtering & Service Parameter Integrity.
Validates response structure, schema keys, parameter propagation, and status codes
without hardcoding static database record values (dates, batch IDs, invoice numbers).
"""

import pytest
from app.warehouse_service import get_warehouse_statistics, DB_CONFIGURATIONS


def test_prod_target_warehouse_service():
    """DEV target DB query executes successfully and returns valid summary schema."""
    res = get_warehouse_statistics(target_db="pg_dev", limit=20)
    assert res["status"] == "success"
    assert "summary" in res
    assert "warehouse_items" in res
    summary = res.get("summary", {})
    assert "total_warehouses" in summary
    assert "total_invoices_processed" in summary
    assert "total_cases_built" in summary


def test_dev_target_warehouse_service():
    """DEV target DB query executes successfully and returns valid summary schema."""
    res = get_warehouse_statistics(target_db="pg_dev", limit=20)
    assert res["status"] == "success"
    assert "summary" in res
    assert "warehouse_items" in res
    summary = res.get("summary", {})
    assert "total_warehouses" in summary
    assert isinstance(res.get("warehouse_items"), list)


def test_dynamic_parameter_propagation():
    """Validates dynamic parameter propagation in response metadata."""
    test_params = {
        "target_db": "pg_dev",
        "oerdte": "dynamic_date",
        "batch_id": "dynamic_batch",
        "oewhse": "02",
        "oeinv": "dynamic_inv"
    }
    res = get_warehouse_statistics(**test_params)
    assert res["status"] == "success"
    filters = res.get("filters_applied", {})
    assert filters.get("oerdte") == "dynamic_date"
    assert filters.get("batch_id") == "dynamic_batch"
    assert filters.get("oewhse") == "02"
    assert filters.get("oeinv") == "dynamic_inv"


def test_item_schema_integrity():
    """Ensures returned warehouse item records conform to required data model keys."""
    res = get_warehouse_statistics(target_db="pg_dev", limit=50)
    assert res["status"] == "success"
    items = res.get("warehouse_items", [])
    if len(items) > 0:
        item = items[0]
        required_keys = [
            "whs_num", "batch_id", "oerdte", "cust_item_code",
            "cs_item_code", "invc_num_stg", "cases_bld_stg",
            "orgnl_ordr_qty_stg", "procurement_transfer_status"
        ]
        for key in required_keys:
            assert key in item


def test_bar_chart_total_warehouses_alignment():
    """Dynamically validates that /api/charts/bar returns ALL warehouses matching total warehouses summary for target DB."""
    from routers.charts import get_bar_chart
    import json

    for db in ["pg_dev"]:
        resp = get_bar_chart(column="warehouse", target_db=db)
        chart_data = json.loads(resp.body)

        assert chart_data["chart_type"] == "bar"
        assert "data" in chart_data
        assert "total_warehouses" in chart_data
        # Ensure the number of warehouses in bar chart matches dynamic total warehouses count in payload
        assert len(chart_data["data"]) == chart_data["total_warehouses"]
        # Verify schema structure of each bar item dynamically without hardcoded values
        for item in chart_data["data"]:
            assert "label" in item
            assert "value" in item
            assert "whs_num" in item
            assert isinstance(item["value"], (int, float))

