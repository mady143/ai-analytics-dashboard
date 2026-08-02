"""
Unit tests for Sidebar toggle button and Footer component integration.
"""

from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent


def test_sidebar_has_toggle_button():
    """Sidebar.jsx must contain the three-line toggle button element."""
    sidebar_path = ROOT_DIR / "frontend" / "src" / "components" / "Sidebar.jsx"
    assert sidebar_path.exists(), "Sidebar.jsx component file must exist"
    content = sidebar_path.read_text(encoding="utf-8")
    assert 'id="sidebar-toggle-btn"' in content
    assert 'toggleSidebar' in content
    assert 'collapsed' in content


def test_footer_component_exists():
    """Footer.jsx must exist and contain copyright information."""
    footer_path = ROOT_DIR / "frontend" / "src" / "components" / "Footer.jsx"
    assert footer_path.exists(), "Footer.jsx component file must exist"
    content = footer_path.read_text(encoding="utf-8")
    assert 'AI Analytics Dashboard' in content
    assert 'All rights reserved' in content
