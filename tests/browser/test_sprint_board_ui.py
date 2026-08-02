"""
Playwright Browser Test — Sprint Board UI Integration
Verifies that navigating to /sprints renders the live Plane Sprint Board with tasks.
"""

import pytest
from playwright.sync_api import Page, expect


def test_sprint_board_page(page: Page):
    """Navigate to /sprints and verify live Plane sprint tasks are displayed."""
    page.goto("http://localhost:5173/sprints")
    page.wait_for_timeout(3000)

    # Verify Sprint Header is present
    expect(page.locator("h1")).to_contain_text("Sprint")

    # Verify Search and Priority Filters are present
    expect(page.locator("input[placeholder*='Filter sprint tasks']")).to_be_visible()

    # Verify Kanban columns exist
    expect(page.get_by_text("To Do / Backlog")).to_be_visible()
    expect(page.get_by_text("In Progress")).to_be_visible()
    expect(page.get_by_text("Completed")).to_be_visible()

    # Verify task cards are rendered
    task_cards = page.locator("div").filter(has_text="pts")
    expect(task_cards.first).to_be_visible()
