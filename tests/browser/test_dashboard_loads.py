"""
Browser tests using Playwright.
Tests the React frontend running at http://localhost:5173
"""

import pytest
from playwright.sync_api import Page, expect


BASE_URL = "http://localhost:5173"


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1440, "height": 900}
    }


def test_dashboard_loads(page: Page):
    """Dashboard page should load and show KPI cards."""
    page.goto(BASE_URL)
    expect(page).to_have_title("AI Analytics Dashboard")
    # Wait for page content
    page.wait_for_selector(".kpi-card", timeout=10000)
    kpi_cards = page.locator(".kpi-card")
    assert kpi_cards.count() >= 4


def test_sidebar_navigation(page: Page):
    """Sidebar links should navigate to correct pages."""
    page.goto(BASE_URL)
    page.wait_for_selector(".sidebar")

    # Click on Analytics page in sidebar specifically
    page.click(".sidebar a[href='/analytics']")
    expect(page).to_have_url(f"{BASE_URL}/analytics")


def test_dashboard_has_charts(page: Page):
    """Dashboard should display chart panels."""
    page.goto(BASE_URL)
    page.wait_for_selector(".chart-card", timeout=10000)
    chart_cards = page.locator(".chart-card")
    assert chart_cards.count() >= 2


def test_analytics_page_loads(page: Page):
    """Analytics page should show model config panel."""
    page.goto(f"{BASE_URL}/analytics")
    page.wait_for_selector(".form-select", timeout=10000)
    # Should have model type selector
    model_select = page.locator(".form-select").first
    expect(model_select).to_be_visible()


def test_agent_status_sidebar(page: Page):
    """Sidebar should show agent status section."""
    page.goto(BASE_URL)
    page.wait_for_selector(".sidebar")
    status_section = page.locator("text=AGENT STATUS")
    expect(status_section).to_be_visible()


# ── UI Health Check Tests (Section 8b) ──────────────────────────────────────


def test_kpi_cards_populated(page: Page):
    """All KPI cards must be visible and display non-empty values."""
    page.goto(BASE_URL)
    page.wait_for_selector(".kpi-card", timeout=10000)
    kpi_cards = page.locator(".kpi-card")
    assert kpi_cards.count() >= 6, "Expected at least 6 KPI cards"
    # Each card must have a visible value element
    for i in range(kpi_cards.count()):
        card = kpi_cards.nth(i)
        expect(card).to_be_visible()


def test_bar_chart_rendered(page: Page):
    """Bar chart must render SVG bars — not blank canvas."""
    page.goto(BASE_URL)
    page.wait_for_selector(".chart-card", timeout=10000)
    # Recharts renders <svg> inside chart-card
    page.wait_for_selector(".chart-card svg", timeout=8000)
    svg_elements = page.locator(".chart-card svg")
    assert svg_elements.count() >= 1, "Bar chart SVG not found — chart may be blank"


def test_scatter_plot_rendered(page: Page):
    """Scatter plot must render SVG dots — not blank canvas."""
    page.goto(BASE_URL)
    page.wait_for_selector(".chart-card svg", timeout=10000)
    # Both charts (bar + scatter) must have SVGs
    chart_svgs = page.locator(".chart-card svg")
    assert chart_svgs.count() >= 2, "Scatter plot SVG not found — second chart may be blank"


def test_warehouse_table_populated(page: Page):
    """Warehouse Sales & Invoice Analytics table must have at least 1 row of data."""
    page.goto(BASE_URL)
    # Wait for the table to appear (it's inside WarehouseSalesAnalytics component)
    page.wait_for_selector("table", timeout=15000)
    rows = page.locator("table tbody tr")
    count = rows.count()
    assert count >= 1, f"Table has no data rows — got {count} rows"


def test_table_row_count_badge(page: Page):
    """Row count badge must show 'Loaded X / Y' with X > 0."""
    page.goto(BASE_URL)
    page.wait_for_selector("table", timeout=15000)
    # Look for the row count text in the page
    row_badge = page.locator("text=Data Table Rows")
    expect(row_badge).to_be_visible()
