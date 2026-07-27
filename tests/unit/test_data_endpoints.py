"""
Unit tests for the data endpoints.
"""

import sys
from pathlib import Path

# Add backend to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "backend"))

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check():
    """API health endpoint should return 200 with status healthy."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_get_sample_data_default():
    """Sample data endpoint should return 100 rows by default."""
    response = client.get("/api/data/sample")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "columns" in data
    assert "total_rows" in data
    assert len(data["data"]) <= 100
    assert data["total_rows"] > 0


def test_get_sample_data_custom_rows():
    """Sample data endpoint should respect the rows parameter."""
    response = client.get("/api/data/sample?rows=20")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) <= 20


def test_get_summary():
    """Summary endpoint should return statistical info."""
    response = client.get("/api/data/summary")
    assert response.status_code == 200
    data = response.json()
    assert "rows" in data
    assert "columns" in data
    assert "numeric_stats" in data
    assert data["rows"] > 0
    assert data["columns"] > 0


def test_upload_invalid_file():
    """Uploading a non-CSV file should return 400."""
    response = client.post(
        "/api/data/upload",
        files={"file": ("test.txt", b"hello world", "text/plain")}
    )
    assert response.status_code == 400


def test_upload_valid_csv():
    """Uploading a valid CSV should succeed."""
    csv_content = b"name,age,salary\nAlice,30,50000\nBob,25,45000\n"
    response = client.post(
        "/api/data/upload",
        files={"file": ("test.csv", csv_content, "text/csv")}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["rows"] == 2
    assert "name" in data["column_names"]


def test_root_endpoint():
    """Root endpoint should return API info."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
