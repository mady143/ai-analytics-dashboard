"""
Unit tests for ML analytics endpoints.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "backend"))

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_columns():
    """Columns endpoint should return column lists."""
    response = client.get("/api/analytics/columns")
    assert response.status_code == 200
    data = response.json()
    assert "all_columns" in data
    assert "numeric_columns" in data
    assert "categorical_columns" in data
    assert len(data["all_columns"]) > 0


def test_train_random_forest():
    """Should successfully train a Random Forest model."""
    response = client.post("/api/analytics/train", json={
        "target_column": "target",
        "model_type": "random_forest",
        "n_estimators": 10,  # Small for test speed
        "test_size": 0.2
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["results"]) == 1
    result = data["results"][0]
    assert result["model_name"] == "Random Forest"
    assert 0.0 <= result["accuracy"] <= 1.0
    assert result["confusion_matrix"] is not None


def test_train_logistic_regression():
    """Should successfully train a Logistic Regression model."""
    response = client.post("/api/analytics/train", json={
        "target_column": "promoted",
        "model_type": "logistic_regression",
        "lr_max_iter": 200
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    result = data["results"][0]
    assert result["model_name"] == "Logistic Regression"
    assert 0.0 <= result["accuracy"] <= 1.0


def test_train_both_models():
    """Should train both models when type is 'both'."""
    response = client.post("/api/analytics/train", json={
        "target_column": "target",
        "model_type": "both",
        "n_estimators": 10
    })
    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) == 2


def test_train_invalid_target():
    """Should return 400 for unknown target column."""
    response = client.post("/api/analytics/train", json={
        "target_column": "nonexistent_column_xyz",
        "model_type": "random_forest"
    })
    assert response.status_code == 400


def test_get_results_without_training():
    """Should return data about trained models."""
    # Train first
    client.post("/api/analytics/train", json={
        "target_column": "target",
        "model_type": "random_forest",
        "n_estimators": 10
    })
    response = client.get("/api/analytics/results")
    assert response.status_code == 200
    data = response.json()
    assert "trained_models" in data


def test_ai_copilot_endpoint():
    """Should process natural language AI copilot queries."""
    response = client.post("/api/analytics/ai-copilot", json={
        "prompt": "Show Warehouse 58 scratch items",
        "target_db": "pg_dev",
        "oerdte": "20260729"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "summary_answer" in data
    assert "suggested_actions" in data


def test_anomalies_endpoint():
    """Should return real-time anomaly risk evaluations."""
    response = client.get("/api/analytics/anomalies?target_db=pg_dev")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "anomalies" in data
    assert len(data["anomalies"]) > 0

