"""Unit tests for InventoryRiskForecast component."""
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent

def test_inventoryriskforecast_file_exists():
    file_path = ROOT_DIR / "frontend" / "src" / "components" / "InventoryRiskForecast.jsx"
    assert file_path.exists(), "InventoryRiskForecast.jsx should exist"

def test_inventoryriskforecast_structure():
    file_path = ROOT_DIR / "frontend" / "src" / "components" / "InventoryRiskForecast.jsx"
    content = file_path.read_text(encoding="utf-8")
    assert "Inventory Risk Forecast" in content
