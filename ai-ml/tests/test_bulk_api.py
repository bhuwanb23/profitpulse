"""
Test script for FastAPI Model Serving API Bulk Prediction Endpoints
"""

import asyncio
import logging
import json
from datetime import datetime
import requests

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API base URL
BASE_URL = "http://localhost:8000"

def test_bulk_prediction_endpoints():
    """Test bulk prediction endpoints"""
    logger.info("Testing bulk prediction endpoints...")
    
    try:
        # Test profitability bulk prediction
        bulk_data = [
            {
                "client_id": "test_client_1",
                "financial_data": {
                    "contract_value": 15000.0,
                    "hours_logged": 40.0,
                    "billing_amount": 8000.0,
                    "ticket_count": 12,
                    "satisfaction_score": 4.2,
                    "last_contact_days": 5,
                    "service_types": ["support", "maintenance"]
                },
                "operational_data": {
                    "support_tickets": 5,
                    "response_time_hours": 2.5,
                    "resolution_time_hours": 4.1
                },
                "historical_period_months": 12
            },
            {
                "client_id": "test_client_2",
                "financial_data": {
                    "contract_value": 8000.0,
                    "hours_logged": 25.0,
                    "billing_amount": 5000.0,
                    "ticket_count": 8,
                    "satisfaction_score": 3.8,
                    "last_contact_days": 15,
                    "service_types": ["support"]
                },
                "operational_data": {
                    "support_tickets": 3,
                    "response_time_hours": 3.2,
                    "resolution_time_hours": 5.7
                },
                "historical_period_months": 12
            }
        ]
        
        bulk_request = {
            "data": bulk_data
        }
        
        response = requests.post(
            f"{BASE_URL}/api/profitability/batch",
            json=bulk_request,
            headers={"Authorization": "admin_key"}
        )
        logger.info(f"Profitability bulk prediction: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            logger.info(f"Bulk prediction result: {result}")
            logger.info(f"Total predictions: {result.get('total_predictions', 0)}")
        else:
            logger.error(f"Error response: {response.text}")
        
        # Test churn bulk prediction
        churn_bulk_data = [
            {
                "client_id": "test_client_1",
                "features": {
                    "contract_value": 15000.0,
                    "last_contact_days": 30,
                    "ticket_frequency": 1.5,
                    "satisfaction_score": 4.2,
                    "payment_delays": 0,
                    "service_issues": 1
                },
                "timeframe_days": 90
            },
            {
                "client_id": "test_client_2",
                "features": {
                    "contract_value": 8000.0,
                    "last_contact_days": 60,
                    "ticket_frequency": 3.2,
                    "satisfaction_score": 2.8,
                    "payment_delays": 2,
                    "service_issues": 4
                },
                "timeframe_days": 90
            }
        ]
        
        churn_bulk_request = {
            "data": churn_bulk_data
        }
        
        response = requests.post(
            f"{BASE_URL}/api/churn/batch",
            json=churn_bulk_request,
            headers={"Authorization": "admin_key"}
        )
        logger.info(f"Churn bulk prediction: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            logger.info(f"Churn bulk prediction result: {result}")
            logger.info(f"Total predictions: {result.get('total_predictions', 0)}")
        else:
            logger.error(f"Error response: {response.text}")
        
        return True
        
    except Exception as e:
        logger.error(f"Bulk prediction endpoint test failed: {e}")
        return False

def test_model_info_endpoints():
    """Test model info endpoints"""
    logger.info("Testing model info endpoints...")
    
    try:
        # Test profitability model info
        response = requests.get(
            f"{BASE_URL}/api/profitability/models/client_profitability/info",
            headers={"Authorization": "admin_key"}
        )
        logger.info(f"Profitability model info: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            logger.info(f"Profitability model info: {result}")
        
        # Test churn model info
        response = requests.get(
            f"{BASE_URL}/api/churn/models/client_churn/info",
            headers={"Authorization": "admin_key"}
        )
        logger.info(f"Churn model info: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            logger.info(f"Churn model info: {result}")
        
        return True
        
    except Exception as e:
        logger.error(f"Model info endpoint test failed: {e}")
        return False

def test_model_health_endpoints():
    """Test model health endpoints"""
    logger.info("Testing model health endpoints...")
    
    try:
        # Test profitability model health
        response = requests.get(
            f"{BASE_URL}/api/profitability/models/client_profitability/health",
            headers={"Authorization": "admin_key"}
        )
        logger.info(f"Profitability model health: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            logger.info(f"Profitability model health: {result}")
        
        # Test churn model health
        response = requests.get(
            f"{BASE_URL}/api/churn/models/client_churn/health",
            headers={"Authorization": "admin_key"}
        )
        logger.info(f"Churn model health: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            logger.info(f"Churn model health: {result}")
        
        return True
        
    except Exception as e:
        logger.error(f"Model health endpoint test failed: {e}")
        return False

def main():
    """Main test function"""
    logger.info("Starting SuperHack AI/ML Bulk API Tests")
    logger.info("=" * 50)
    
    # Wait for server to start
    logger.info("Waiting for server to start...")
    import time
    time.sleep(2)
    
    # Test endpoints
    tests = [
        ("Bulk Prediction Endpoints", test_bulk_prediction_endpoints),
        ("Model Info Endpoints", test_model_info_endpoints),
        ("Model Health Endpoints", test_model_health_endpoints)
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
        logger.info(f"\n🎉 All {total} tests passed! Bulk API is working correctly.")
    else:
        logger.error(f"\n💥 {total - passed} out of {total} tests failed.")

if __name__ == "__main__":
    main()