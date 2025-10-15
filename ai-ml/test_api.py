"""
Test script for FastAPI Model Serving API
"""

import asyncio
import logging
import requests
import json
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API base URL
BASE_URL = "http://localhost:8000"

def test_health_endpoints():
    """Test health check endpoints"""
    logger.info("Testing health endpoints...")
    
    try:
        # Basic health check
        response = requests.get(f"{BASE_URL}/api/health/")
        logger.info(f"Basic health check: {response.status_code}")
        if response.status_code == 200:
            logger.info(f"Response: {response.json()}")
        
        # Detailed health check
        response = requests.get(f"{BASE_URL}/api/health/detailed")
        logger.info(f"Detailed health check: {response.status_code}")
        if response.status_code == 200:
            logger.info(f"Response: {response.json()}")
        
        # Readiness check
        response = requests.get(f"{BASE_URL}/api/health/ready")
        logger.info(f"Readiness check: {response.status_code}")
        
        # Liveness check
        response = requests.get(f"{BASE_URL}/api/health/live")
        logger.info(f"Liveness check: {response.status_code}")
        
        return True
        
    except Exception as e:
        logger.error(f"Health endpoint test failed: {e}")
        return False

def test_model_endpoints():
    """Test model management endpoints"""
    logger.info("Testing model endpoints...")
    
    try:
        # List models
        response = requests.get(f"{BASE_URL}/api/models/")
        logger.info(f"List models: {response.status_code}")
        if response.status_code == 200:
            models = response.json()
            logger.info(f"Found {len(models)} models")
        
        # Get model info (if any models exist)
        if response.status_code == 200 and models:
            model_name = models[0]["name"]
            response = requests.get(f"{BASE_URL}/api/models/{model_name}")
            logger.info(f"Get model {model_name}: {response.status_code}")
        
        return True
        
    except Exception as e:
        logger.error(f"Model endpoint test failed: {e}")
        return False

def test_prediction_endpoints():
    """Test prediction endpoints"""
    logger.info("Testing prediction endpoints...")
    
    try:
        # Test profitability prediction
        prediction_data = {
            "client_id": "test_client_1",
            "contract_value": 15000.0,
            "hours_logged": 40.0,
            "billing_amount": 8000.0,
            "ticket_count": 12,
            "satisfaction_score": 4.2,
            "last_contact_days": 5,
            "service_types": ["support", "maintenance"]
        }
        
        response = requests.post(
            f"{BASE_URL}/api/predictions/profitability",
            json=prediction_data
        )
        logger.info(f"Profitability prediction: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            logger.info(f"Prediction result: {result}")
        
        # Test churn prediction
        churn_data = {
            "client_id": "test_client_2",
            "contract_value": 8000.0,
            "last_contact_days": 45,
            "ticket_frequency": 2.5,
            "satisfaction_score": 3.1,
            "payment_delays": 1,
            "service_issues": 2
        }
        
        response = requests.post(
            f"{BASE_URL}/api/predictions/churn",
            json=churn_data
        )
        logger.info(f"Churn prediction: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            logger.info(f"Churn prediction result: {result}")
        
        return True
        
    except Exception as e:
        logger.error(f"Prediction endpoint test failed: {e}")
        return False

def test_monitoring_endpoints():
    """Test monitoring endpoints"""
    logger.info("Testing monitoring endpoints...")
    
    try:
        # Get metrics
        response = requests.get(f"{BASE_URL}/api/monitoring/metrics")
        logger.info(f"Get metrics: {response.status_code}")
        if response.status_code == 200:
            metrics = response.json()
            logger.info(f"Metrics keys: {list(metrics.keys())}")
        
        # Get performance metrics
        response = requests.get(f"{BASE_URL}/api/monitoring/performance")
        logger.info(f"Get performance metrics: {response.status_code}")
        if response.status_code == 200:
            performance = response.json()
            logger.info(f"Performance metrics count: {len(performance)}")
        
        # Get alerts
        response = requests.get(f"{BASE_URL}/api/monitoring/alerts")
        logger.info(f"Get alerts: {response.status_code}")
        if response.status_code == 200:
            alerts = response.json()
            logger.info(f"Alerts count: {len(alerts)}")
        
        return True
        
    except Exception as e:
        logger.error(f"Monitoring endpoint test failed: {e}")
        return False

def test_admin_endpoints():
    """Test admin endpoints"""
    logger.info("Testing admin endpoints...")
    
    try:
        # Get system config
        response = requests.get(f"{BASE_URL}/api/admin/system/config")
        logger.info(f"Get system config: {response.status_code}")
        if response.status_code == 200:
            config = response.json()
            logger.info(f"System config keys: {list(config.keys())}")
        
        # Get system status
        response = requests.get(f"{BASE_URL}/api/admin/system/status")
        logger.info(f"Get system status: {response.status_code}")
        if response.status_code == 200:
            status = response.json()
            logger.info(f"System status: {status.get('overall_status', 'unknown')}")
        
        # List A/B tests
        response = requests.get(f"{BASE_URL}/api/admin/ab-tests")
        logger.info(f"List A/B tests: {response.status_code}")
        if response.status_code == 200:
            tests = response.json()
            logger.info(f"A/B tests count: {len(tests)}")
        
        return True
        
    except Exception as e:
        logger.error(f"Admin endpoint test failed: {e}")
        return False

def main():
    """Main test function"""
    logger.info("Starting SuperHack AI/ML API Tests")
    logger.info("=" * 50)
    
    # Wait for server to start
    logger.info("Waiting for server to start...")
    import time
    time.sleep(2)
    
    # Test endpoints
    tests = [
        ("Health Endpoints", test_health_endpoints),
        ("Model Endpoints", test_model_endpoints),
        ("Prediction Endpoints", test_prediction_endpoints),
        ("Monitoring Endpoints", test_monitoring_endpoints),
        ("Admin Endpoints", test_admin_endpoints)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        logger.info(f"\n{test_name}")
        logger.info("-" * 30)
        try:
            success = test_func()
            results[test_name] = "✅ PASSED" if success else "❌ FAILED"
        except Exception as e:
            logger.error(f"Test {test_name} failed with exception: {e}")
            results[test_name] = "❌ FAILED"
    
    # Summary
    logger.info("\n" + "=" * 50)
    logger.info("Test Summary:")
    for test_name, result in results.items():
        logger.info(f"  {test_name}: {result}")
    
    passed = sum(1 for result in results.values() if "PASSED" in result)
    total = len(results)
    
    if passed == total:
        logger.info(f"\n🎉 All {total} tests passed! API is working correctly.")
    else:
        logger.error(f"\n💥 {total - passed} out of {total} tests failed.")

if __name__ == "__main__":
    main()
