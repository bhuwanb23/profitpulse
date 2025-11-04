"""
Test suite for Historical Data Analysis API endpoints
"""

import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_get_historical_predictions():
    """Test getting historical predictions for a model"""
    response = client.get("/api/historical/predictions/profitability_prediction?days=7&limit=100", 
                         headers={"Authorization": "admin_key"})
    assert response.status_code == 200
    # Since we're returning an empty list in the mock implementation, we check for a list
    assert isinstance(response.json(), list)


def test_get_prediction_statistics():
    """Test getting prediction statistics for a model"""
    response = client.get("/api/historical/predictions/profitability_prediction/stats?days=30",
                         headers={"Authorization": "admin_key"})
    assert response.status_code == 200
    data = response.json()
    assert "model_name" in data
    assert "period_days" in data
    assert data["model_name"] == "profitability_prediction"


def test_get_model_performance_report():
    """Test getting model performance report"""
    response = client.get("/api/historical/performance/profitability_prediction?days=30",
                         headers={"Authorization": "admin_key"})
    assert response.status_code == 200
    data = response.json()
    assert "model_name" in data
    assert "version" in data
    assert "metrics" in data
    assert "period_start" in data
    assert "period_end" in data
    assert data["model_name"] == "profitability_prediction"


def test_get_drift_analysis():
    """Test getting drift analysis for a model"""
    response = client.get("/api/historical/drift/profitability_prediction?days=30",
                         headers={"Authorization": "admin_key"})
    assert response.status_code == 200
    data = response.json()
    assert "model_name" in data
    assert "analysis_period_days" in data
    assert "data_drift_detected" in data
    assert "concept_drift_detected" in data
    assert data["model_name"] == "profitability_prediction"


if __name__ == "__main__":
    pytest.main([__file__])