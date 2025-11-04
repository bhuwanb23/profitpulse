"""
Test script for Scheduled Runs API endpoints
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


def test_scheduled_endpoints():
    """Test scheduled runs endpoints"""
    logger.info("Testing scheduled runs endpoints...")
    
    try:
        # Test creating a scheduled run
        scheduled_data = {
            "model_name": "client_profitability",
            "schedule": "0 0 * * *",  # Daily at midnight
            "parameters": {
                "return_confidence": True,
                "batch_size": 100
            },
            "enabled": True
        }
        
        response = requests.post(
            f"{BASE_URL}/api/scheduled/",
            json=scheduled_data,
            headers={"Authorization": "admin_key"}
        )
        logger.info(f"Create scheduled run: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            logger.info(f"Create scheduled run result: {result}")
            run_id = result.get("run_id")
        else:
            logger.error(f"Error response: {response.text}")
            return False
        
        # Test getting the scheduled run
        response = requests.get(
            f"{BASE_URL}/api/scheduled/{run_id}",
            headers={"Authorization": "admin_key"}
        )
        logger.info(f"Get scheduled run: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            logger.info(f"Get scheduled run result: {result}")
        else:
            logger.error(f"Error response: {response.text}")
            return False
        
        # Test listing scheduled runs
        response = requests.get(
            f"{BASE_URL}/api/scheduled/",
            headers={"Authorization": "admin_key"}
        )
        logger.info(f"List scheduled runs: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            logger.info(f"List scheduled runs count: {len(result)}")
        else:
            logger.error(f"Error response: {response.text}")
            return False
        
        # Test updating the scheduled run
        update_data = {
            "model_name": "client_churn",
            "schedule": "0 12 * * *",  # Daily at noon
            "parameters": {
                "return_confidence": False,
                "timeframe_days": 30
            },
            "enabled": False
        }
        
        response = requests.put(
            f"{BASE_URL}/api/scheduled/{run_id}",
            json=update_data,
            headers={"Authorization": "admin_key"}
        )
        logger.info(f"Update scheduled run: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            logger.info(f"Update scheduled run result: {result}")
        else:
            logger.error(f"Error response: {response.text}")
            return False
        
        # Test triggering the scheduled run
        response = requests.post(
            f"{BASE_URL}/api/scheduled/{run_id}/trigger",
            headers={"Authorization": "admin_key"}
        )
        logger.info(f"Trigger scheduled run: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            logger.info(f"Trigger scheduled run result: {result}")
        else:
            logger.error(f"Error response: {response.text}")
            return False
        
        # Test deleting the scheduled run
        response = requests.delete(
            f"{BASE_URL}/api/scheduled/{run_id}",
            headers={"Authorization": "admin_key"}
        )
        logger.info(f"Delete scheduled run: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            logger.info(f"Delete scheduled run result: {result}")
        else:
            logger.error(f"Error response: {response.text}")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"Scheduled runs endpoint test failed: {e}")
        return False


def main():
    """Main test function"""
    logger.info("Starting SuperHack AI/ML Scheduled Runs API Tests")
    logger.info("=" * 50)
    
    # Wait for server to start
    logger.info("Waiting for server to start...")
    import time
    time.sleep(2)
    
    # Test endpoints
    tests = [
        ("Scheduled Runs Endpoints", test_scheduled_endpoints),
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
        logger.info(f"\n🎉 All {total} tests passed! Scheduled Runs API is working correctly.")
    else:
        logger.error(f"\n💥 {total - passed} out of {total} tests failed.")

if __name__ == "__main__":
    main()