"""
Unit tests for Task AAD-20 — Nav Bar Hide Toggle Button and Footer Copyright Notice.
"""

from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent


def test_sidebar_has_hide_toggle_button():
    """Sidebar.jsx should contain a 3-line hamburger hide toggle button."""
    sidebar_file = ROOT_DIR / "frontend" / "src" / "components" / "Sidebar.jsx"
    assert sidebar_file.exists(), "Sidebar.jsx file must exist"
    content = sidebar_file.read_text(encoding="utf-8")
    assert "nav-bar-toggle-btn" in content
    assert "Menu" in content


def test_app_has_collapsed_toggle_and_footer():
    """App.jsx should contain collapsed sidebar state, enable toggle, and Footer component."""
    app_file = ROOT_DIR / "frontend" / "src" / "App.jsx"
    assert app_file.exists(), "App.jsx file must exist"
    content = app_file.read_text(encoding="utf-8")
    assert "sidebarCollapsed" in content
    assert "nav-bar-enable-btn" in content
    assert "Footer" in content


def test_footer_has_copyright_notice():
    """Footer.jsx should contain default copyright notice."""
    footer_file = ROOT_DIR / "frontend" / "src" / "components" / "Footer.jsx"
    assert footer_file.exists(), "Footer.jsx file must exist"
    content = footer_file.read_text(encoding="utf-8")
    assert "AI Analytics Dashboard. All rights reserved." in content
