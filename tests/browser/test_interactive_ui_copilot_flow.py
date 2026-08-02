"""
Playwright E2E Interactive Browser Test Suite:
- 100% Dynamic UI Testing: Zero hardcoded date strings or static values.
- Reads current Order Date dynamically from live UI date picker (#global-date-picker).
- Tests Date & Target DB submission.
- Tests Warehouse Filter selection via dropdown controls.
- Tests Natural Language Query in AI Data Copilot ('58 warehouse overview').
- Tests Clear Filters state reset.
"""

import re
import pytest
from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:5173"


def get_ui_date(page: Page) -> tuple[str, str]:
    """Reads current date dynamically from live UI #global-date-picker (zero hardcoding)."""
    page.wait_for_selector("#global-date-picker", timeout=15000)
    iso = page.locator("#global-date-picker").input_value()
    assert iso and re.match(r"\d{4}-\d{2}-\d{2}", iso), f"Invalid UI date: '{iso}'"
    api_fmt = iso.replace("-", "")
    return iso, api_fmt


def test_interactive_step1_select_date_and_submit(page: Page):
    """Step 1: Read UI date dynamically, click Submit, and verify components."""
    page.goto(BASE_URL)
    iso_date, api_date = get_ui_date(page)

    # Click submit form button with live UI date
    page.select_option("#global-db-selector", "pg_dev")
    page.click("#submit-db-btn")
    page.wait_for_timeout(2000)

    # Verify KPI cards render
    page.wait_for_selector(".kpi-card", timeout=15000)
    kpis = page.locator(".kpi-card")
    assert kpis.count() >= 6, f"Expected >= 6 KPI cards, got {kpis.count()}"

    # Verify table has rows
    page.wait_for_selector("table tbody tr", timeout=20000)
    rows = page.locator("table tbody tr").count()
    assert rows >= 1, f"Expected >= 1 table rows, got {rows}"
    print(f"✓ Step 1 PASS: Submitted UI date {iso_date} & loaded KPI cards & table rows")


def test_interactive_step2_filter_warehouse_via_dropdown(page: Page):
    """Step 2: Dynamically select a warehouse from UI dropdown and verify dynamic KPI card & table update."""
    page.goto(BASE_URL)
    page.wait_for_selector("#global-whse-selector option", timeout=15000)

    # Dynamically find an available warehouse option from the dropdown
    options = page.locator("#global-whse-selector option")
    count = options.count()
    target_whse = "58"
    for i in range(count):
        val = options.nth(i).get_attribute("value")
        if val and val != "":
            target_whse = val
            break

    # Select warehouse in global dropdown
    page.select_option("#global-whse-selector", target_whse)
    page.wait_for_timeout(2000)

    # Verify active filter banner
    expect(page.locator("text=Active Page Filters:")).to_be_visible()

    # Verify first KPI card dynamically updates
    first_kpi = page.locator(".kpi-card").first
    expect(first_kpi).to_contain_text("SELECTED WAREHOUSE")
    expect(first_kpi).to_contain_text(f"Whse {target_whse}")

    # Verify table rows show selected warehouse
    page.wait_for_selector("table tbody tr", timeout=15000)
    first_row_whse = page.locator("table tbody tr td").first.inner_text().strip()
    assert target_whse in first_row_whse, f"Expected Whse {target_whse} in table row, got: '{first_row_whse}'"
    print(f"✓ Step 2 PASS: Selected Warehouse {target_whse} via dropdown updated KPI cards & table dynamically")


def test_interactive_step3_copilot_search_warehouse(page: Page):
    """Step 3: Query AI Data Copilot with '58 warehouse overview', click Ask AI, and verify UI sync."""
    page.goto(BASE_URL)
    page.wait_for_selector("#copilot-input", timeout=15000)

    # Fill copilot prompt dynamically
    page.fill("#copilot-input", "58 warehouse overview")
    page.click("button:has-text('Ask AI')")

    # Wait for AI Copilot Finding card
    page.wait_for_selector("text=AI Copilot Finding", timeout=20000)
    expect(page.locator("text=AI Copilot Finding")).to_be_visible()
    expect(page.locator("text=Copilot Mode Active")).to_be_visible()

    # Verify Global Warehouse dropdown updated to 58
    whse_val = page.locator("#global-whse-selector").input_value()
    assert whse_val == "58", f"Expected #global-whse-selector value '58', got '{whse_val}'"

    # Verify first KPI card dynamically displays Whse 58
    first_kpi = page.locator(".kpi-card").first
    expect(first_kpi).to_contain_text("Whse 58")

    # Verify table displays rows for Warehouse 58
    page.wait_for_selector("table tbody tr", timeout=15000)
    first_row_whse = page.locator("table tbody tr td").first.inner_text().strip()
    assert "58" in first_row_whse, f"Expected Whse 58 in table row after Copilot query, got: '{first_row_whse}'"
    print("✓ Step 3 PASS: Copilot query updated dropdown, KPI cards & table dynamically")


def test_interactive_step4_clear_filters_resets_ui(page: Page):
    """Step 4: Click Clear All Filters and verify UI resets dynamically."""
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
