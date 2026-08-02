"""
Unit tests for Plane sprint reading and task endpoint.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "backend"))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_sprint_tasks_endpoint():
    """GET /api/sprints/tasks should return live Plane sprint metadata and task lists."""
    response = client.get("/api/sprints/tasks")
    assert response.status_code == 200
    data = response.json()
    assert "sprint" in data
    assert "tasks" in data
    assert data["sprint"]["total_tasks"] >= 18
    assert len(data["tasks"]["all"]) >= 18
    assert "todo" in data["tasks"]
    assert "in_progress" in data["tasks"]
    assert "completed" in data["tasks"]
