"""Unit tests for CopilotSearchFixes component."""
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent

def test_copilotsearchfixes_file_exists():
    file_path = ROOT_DIR / "frontend" / "src" / "components" / "CopilotSearchFixes.jsx"
    assert file_path.exists(), "CopilotSearchFixes.jsx should exist"

def test_copilotsearchfixes_structure():
    file_path = ROOT_DIR / "frontend" / "src" / "components" / "CopilotSearchFixes.jsx"
    content = file_path.read_text(encoding="utf-8")
    assert "Copilot search fixes" in content
