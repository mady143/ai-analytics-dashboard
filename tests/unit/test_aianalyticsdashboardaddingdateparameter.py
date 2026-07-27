"""Unit tests for AiAnalyticsDashboardAddingDateParameter component."""
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent

def test_aianalyticsdashboardaddingdateparameter_file_exists():
    file_path = ROOT_DIR / "frontend" / "src" / "components" / "AiAnalyticsDashboardAddingDateParameter.jsx"
    assert file_path.exists(), "AiAnalyticsDashboardAddingDateParameter.jsx should exist"

def test_aianalyticsdashboardaddingdateparameter_structure():
    file_path = ROOT_DIR / "frontend" / "src" / "components" / "AiAnalyticsDashboardAddingDateParameter.jsx"
    content = file_path.read_text(encoding="utf-8")
    assert "AI Analytics Dashboard Adding Date Parameter" in content
