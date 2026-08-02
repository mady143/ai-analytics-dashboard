"""
Playwright E2E Browser Test — Sidebar Three-Line Toggle Button & Footer
Verifies clicking the hamburger button collapses/expands the nav bar and footer displays copyright info.
"""

import pytest
from playwright.sync_api import Page, expect


def test_sidebar_toggle_and_footer_rendering(page: Page):
    """Test three-line toggle button collapses/expands navbar and footer renders copyright."""
    page.goto("http://localhost:5173/")
    page.wait_for_timeout(2000)

    # 1. Verify three-line toggle button exists
    toggle_btn = page.locator("#sidebar-toggle-btn")
    expect(toggle_btn).to_be_visible()

    # 2. Click toggle button to collapse/disable nav bar
    toggle_btn.click()
    page.wait_for_timeout(1000)

    # Verify sidebar is collapsed
    sidebar = page.locator("aside.sidebar")
    expect(sidebar).to_have_class(pytest.PytestRegex(".*collapsed.*"))

    # 3. Click toggle button again to expand/enable nav bar
    toggle_btn.click()
    page.wait_for_timeout(1000)
    expect(sidebar).not_to_have_class(pytest.PytestRegex(".*collapsed.*"))

    # 4. Verify Footer renders copyright
    footer = page.locator("#app-footer")
    expect(footer).to_be_visible()
    expect(footer).to_contain_text("AI Analytics Dashboard")
    expect(footer).to_contain_text("All rights reserved")
