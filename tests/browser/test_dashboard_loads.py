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

