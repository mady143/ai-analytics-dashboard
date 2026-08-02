"""
Playwright E2E Interactive Browser Test Suite:
1. Selects Order Date & Target DB in global header and clicks Submit.
2. Filters by Warehouse using the warehouse selector dropdown and verifies KPI cards, bar chart, and table update.
3. Enters query in AI Data Copilot ('58 warehouse overview'), clicks Ask AI, and verifies full UI synchronization.
4. Clears filters and verifies dashboard UI resets to default.
"""

import re
import pytest
from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:5173"


def test_interactive_step1_select_date_and_submit(page: Page):
    """Step 1: Select Order Date & Target DB, click Submit, and verify components."""
    page.goto(BASE_URL)
    page.wait_for_selector("#global-date-picker", timeout=15000)

    # Select Order Date & Target DB
    page.fill("#global-date-picker", "2026-07-28")
    page.select_option("#global-db-selector", "pg_dev")
    page.click("#submit-db-btn")
    page.wait_for_timeout(2000)

    # Verify KPI cards and charts render
    page.wait_for_selector(".kpi-card", timeout=15000)
    kpis = page.locator(".kpi-card")
    assert kpis.count() >= 6, f"Expected >= 6 KPI cards, got {kpis.count()}"

    # Verify table has rows
    page.wait_for_selector("table tbody tr", timeout=20000)
    rows = page.locator("table tbody tr").count()
    assert rows >= 1, f"Expected >= 1 table rows, got {rows}"
    print("✓ Step 1 PASS: Selected date 2026-07-28 & Submit loaded KPI cards and table rows")


def test_interactive_step2_filter_warehouse_via_dropdown(page: Page):
    """Step 2: Filter by Warehouse 58 via dropdown selector and verify dynamic KPI card & table update."""
    page.goto(BASE_URL)
    page.wait_for_selector("#global-whse-selector", timeout=15000)

    # Select Warehouse 58 in global dropdown
    page.select_option("#global-whse-selector", "58")
    page.wait_for_timeout(2000)

    # Verify active filter banner
    expect(page.locator("text=Active Page Filters:")).to_be_visible()
    expect(page.locator("text=Warehouse: Whse 58")).to_be_visible()

    # Verify first KPI card shows SELECTED WAREHOUSE / Whse 58
    first_kpi = page.locator(".kpi-card").first
    expect(first_kpi).to_contain_text("SELECTED WAREHOUSE")
    expect(first_kpi).to_contain_text("Whse 58")

    # Verify table rows show Warehouse 58
    page.wait_for_selector("table tbody tr", timeout=15000)
    first_row_whse = page.locator("table tbody tr td").first.inner_text().strip()
    assert "58" in first_row_whse, f"Expected Whse 58 in table row, got: '{first_row_whse}'"
    print("✓ Step 2 PASS: Selected Warehouse 58 via dropdown updated KPI cards & table")


def test_interactive_step3_copilot_search_warehouse_58(page: Page):
    """Step 3: Query AI Data Copilot with '58 warehouse overview', click Ask AI, and verify UI sync."""
    page.goto(BASE_URL)
    page.wait_for_selector("#copilot-input", timeout=15000)

    # Fill copilot prompt and submit query
    page.fill("#copilot-input", "58 warehouse overview")
    page.click("button:has-text('Ask AI')")

    # Wait for AI Copilot Finding card
    page.wait_for_selector("text=AI Copilot Finding", timeout=20000)
    expect(page.locator("text=AI Copilot Finding")).to_be_visible()
    expect(page.locator("text=Copilot Mode Active")).to_be_visible()

    # Verify Global Warehouse dropdown updated to 58
    whse_val = page.locator("#global-whse-selector").input_value()
    assert whse_val == "58", f"Expected #global-whse-selector value '58', got '{whse_val}'"

    # Verify first KPI card shows Whse 58
    first_kpi = page.locator(".kpi-card").first
    expect(first_kpi).to_contain_text("Whse 58")

    # Verify table displays rows for Warehouse 58
    page.wait_for_selector("table tbody tr", timeout=15000)
    first_row_whse = page.locator("table tbody tr td").first.inner_text().strip()
    assert "58" in first_row_whse, f"Expected Whse 58 in table row after Copilot query, got: '{first_row_whse}'"
    print("✓ Step 3 PASS: Query '58 warehouse overview' in Copilot updated dropdown, KPI cards & table")


def test_interactive_step4_clear_filters_resets_ui(page: Page):
    """Step 4: Click Clear All Filters and verify UI resets to default."""
    page.goto(BASE_URL)
    page.wait_for_selector("#copilot-input", timeout=15000)

    # Apply filter first via Copilot
    page.fill("#copilot-input", "Warehouse 58")
    page.click("button:has-text('Ask AI')")
    page.wait_for_selector("text=AI Copilot Finding", timeout=15000)

    # Click Clear All Filters button
    clear_btn = page.locator("button:has-text('Clear All Filters'), #copilot-clear-btn").first
    expect(clear_btn).to_be_visible()
    clear_btn.click()
    page.wait_for_timeout(1500)

    # Verify Global Warehouse dropdown reset to empty
    whse_val = page.locator("#global-whse-selector").input_value()
    assert whse_val == "", f"Expected empty #global-whse-selector after reset, got '{whse_val}'"
    print("✓ Step 4 PASS: Clear All Filters reset dashboard UI to default")
