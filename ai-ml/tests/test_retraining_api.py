"""
Test suite for Model Retraining API endpoints
"""

import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_create_retraining_trigger():
    """Test creating a retraining trigger"""
    trigger_data = {
        "model_name": "profitability_prediction",
        "trigger_type": "performance",
        "trigger_condition": {"metric": "accuracy", "threshold": 0.8},
        "enabled": True
    }
    
    response = client.post("/api/retraining/triggers", json=trigger_data,
                          headers={"Authorization": "admin_key"})
    assert response.status_code == 200
    data = response.json()
    assert "trigger_id" in data
    assert "message" in data
    assert "trigger_details" in data
    assert data["message"] == "Retraining trigger created successfully"


def test_create_invalid_retraining_trigger():
    """Test creating an invalid retraining trigger"""
    trigger_data = {
        "model_name": "profitability_prediction",
        "trigger_type": "invalid_type",
        "trigger_condition": {"metric": "accuracy", "threshold": 0.8},
        "enabled": True
    }
    
    response = client.post("/api/retraining/triggers", json=trigger_data,
                          headers={"Authorization": "admin_key"})
    assert response.status_code == 400


def test_list_retraining_triggers():
    """Test listing retraining triggers for a model"""
    response = client.get("/api/retraining/triggers/profitability_prediction",
                         headers={"Authorization": "admin_key"})
    assert response.status_code == 200
    # Should return a list (even if empty in mock implementation)
    assert isinstance(response.json(), list)


def test_update_retraining_trigger():
    """Test updating a retraining trigger"""
    # First create a trigger to update
    trigger_data = {
        "model_name": "profitability_prediction",
        "trigger_type": "performance",
        "trigger_condition": {"metric": "accuracy", "threshold": 0.8},
        "enabled": True
    }
    
    create_response = client.post("/api/retraining/triggers", json=trigger_data,
                                 headers={"Authorization": "admin_key"})
    assert create_response.status_code == 200
    trigger_id = create_response.json()["trigger_id"]
    
    # Now update the trigger
    updated_data = {
        "model_name": "profitability_prediction",
        "trigger_type": "data_drift",
        "trigger_condition": {"metric": "drift_score", "threshold": 0.1},
        "enabled": False
    }
    
    response = client.put(f"/api/retraining/triggers/{trigger_id}", json=updated_data,
                         headers={"Authorization": "admin_key"})
    assert response.status_code == 200
    data = response.json()
    assert "trigger_id" in data
    assert data["trigger_id"] == trigger_id


def test_delete_retraining_trigger():
    """Test deleting a retraining trigger"""
    # In a real test, we would first create a trigger, then delete it
    # For now, we'll just test the endpoint exists and returns a response
    response = client.delete("/api/retraining/triggers/trigger_123",
                            headers={"Authorization": "admin_key"})
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "trigger_id" in data


def test_trigger_manual_retraining():
    """Test triggering manual model retraining"""
    retraining_data = {
        "model_name": "profitability_prediction",
        "parameters": {"epochs": 100, "learning_rate": 0.001}
    }
    
    response = client.post("/api/retraining/jobs", json=retraining_data,
                          headers={"Authorization": "admin_key"})
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert "message" in data
    assert "job_details" in data
    assert data["message"] == "Retraining job initiated successfully"


def test_get_retraining_job_status():
    """Test getting retraining job status"""
    response = client.get("/api/retraining/jobs/job_123",
                         headers={"Authorization": "admin_key"})
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "model_name" in data
    assert "status" in data


def test_get_retraining_history():
    """Test getting retraining history for a model"""
    response = client.get("/api/retraining/jobs/profitability_prediction/history?limit=10",
                         headers={"Authorization": "admin_key"})
    assert response.status_code == 200
    # Should return a list (even if empty in mock implementation)
    assert isinstance(response.json(), list)


if __name__ == "__main__":
    pytest.main([__file__])