"""
Test suite for Performance Reporting API endpoints
"""

import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_get_performance_summary():
    """Test getting performance summary for all models"""
    response = client.get("/api/reporting/performance/summary?days=30",
                         headers={"Authorization": "admin_key"})
    assert response.status_code == 200
    data = response.json()
    assert "period_start" in data
    assert "period_end" in data
    assert "total_models" in data
    assert "average_accuracy" in data


def test_get_detailed_performance_report():
    """Test getting detailed performance report for a specific model"""
    response = client.get("/api/reporting/performance/profitability_prediction?days=30",
                         headers={"Authorization": "admin_key"})
    assert response.status_code == 200
    data = response.json()
    assert "model_name" in data
    assert "version" in data
    assert "metrics" in data
    assert "period_start" in data
    assert "period_end" in data
    assert data["model_name"] == "profitability_prediction"


def test_get_performance_trends():
    """Test getting performance trends for a model"""
    response = client.get("/api/reporting/performance/profitability_prediction/trends?days=90",
                         headers={"Authorization": "admin_key"})
    assert response.status_code == 200
    data = response.json()
    assert "model_name" in data
    assert "period_start" in data
    assert "period_end" in data
    assert "metrics" in data
    assert data["model_name"] == "profitability_prediction"


def test_get_model_comparison():
    """Test comparing performance metrics across multiple models"""
    response = client.get("/api/reporting/performance/comparison?models=profitability_prediction,churn_prediction,demand_forecasting&metric=accuracy&days=30",
                         headers={"Authorization": "admin_key"})
    assert response.status_code == 200
    data = response.json()
    assert "metric" in data
    assert "models" in data
    assert "best_performing" in data
    assert "worst_performing" in data
    assert data["metric"] == "accuracy"


def test_get_model_comparison_invalid():
    """Test comparing models with no models specified"""
    response = client.get("/api/reporting/performance/comparison?metric=accuracy&days=30",
                         headers={"Authorization": "admin_key"})
    assert response.status_code == 422  # Validation error for missing models parameter


def test_get_drift_alerts():
    """Test getting recent data drift alerts"""
    response = client.get("/api/reporting/drift/alerts?days=7",
                         headers={"Authorization": "admin_key"})
    assert response.status_code == 200
    # Should return a list (even if empty or with mock data)
    assert isinstance(response.json(), list)


def test_get_prediction_analysis():
    """Test getting comprehensive prediction analysis"""
    response = client.get("/api/reporting/predictions/analysis?days=30",
                         headers={"Authorization": "admin_key"})
    assert response.status_code == 200
    data = response.json()
    assert "period_start" in data
    assert "period_end" in data
    assert "total_predictions" in data
    assert "prediction_rate_per_day" in data
    assert "system_performance" in data


if __name__ == "__main__":
    pytest.main([__file__])