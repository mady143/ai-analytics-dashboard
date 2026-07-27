"""
pytest configuration — adds the backend directory to sys.path
so tests can import FastAPI app modules.
"""
import sys
from pathlib import Path

# Make backend importable in all tests
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
