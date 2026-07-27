"""Unit tests for AiAnalyticsDahsboardDateParaemeter component."""
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent

def test_aianalyticsdahsboarddateparaemeter_file_exists():
    file_path = ROOT_DIR / "frontend" / "src" / "components" / "AiAnalyticsDahsboardDateParaemeter.jsx"
    assert file_path.exists(), "AiAnalyticsDahsboardDateParaemeter.jsx should exist"

def test_aianalyticsdahsboarddateparaemeter_structure():
    file_path = ROOT_DIR / "frontend" / "src" / "components" / "AiAnalyticsDahsboardDateParaemeter.jsx"
    content = file_path.read_text(encoding="utf-8")
    assert "AI Analytics Dahsboard Date Paraemeter" in content
