"""Unit tests for WarehouseAnalytics component."""
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent

def test_warehouse_file_exists():
    file_path = ROOT_DIR / "frontend" / "src" / "components" / "WarehouseAnalytics.jsx"
    assert file_path.exists(), "WarehouseAnalytics.jsx should exist"

def test_warehouse_structure():
    file_path = ROOT_DIR / "frontend" / "src" / "components" / "WarehouseAnalytics.jsx"
    content = file_path.read_text(encoding="utf-8")
    assert "Warehouse Level Statistics" in content
