"""
Comprehensive API Test Script
Tests all API endpoints between Backend and AI/ML services
"""

import requests
import json
import time
import sys
from typing import Dict, Any, Optional

# Configuration
BACKEND_URL = "http://localhost:3000"
AI_ML_URL = "http://localhost:8000"
AI_ML_API_KEY = "admin_key"

# Test results
test_results = {
    "passed": 0,
    "failed": 0,
    "errors": []
}

# Colors for output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

def log(message: str, color: str = Colors.RESET):
    print(f"{color}{message}{Colors.RESET}")

def test_endpoint(name: str, method: str, url: str, data: Optional[Dict] = None, 
                 headers: Optional[Dict] = None, expected_status: int = 200) -> bool:
    """Test an API endpoint"""
    try:
        if headers is None:
            headers = {}
        
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers, timeout=10)
        elif method.upper() == 'POST':
            response = requests.post(url, json=data, headers=headers, timeout=10)
        elif method.upper() == 'PUT':
            response = requests.put(url, json=data, headers=headers, timeout=10)
        elif method.upper() == 'DELETE':
            response = requests.delete(url, headers=headers, timeout=10)
        else:
            log(f"❌ {name} - Unsupported method: {method}", Colors.RED)
            test_results["failed"] += 1
            return False
        
        if response.status_code == expected_status or (200 <= response.status_code < 300):
            test_results["passed"] += 1
            log(f"✅ {name} - Status: {response.status_code}", Colors.GREEN)
            return True
        else:
            test_results["failed"] += 1
            error_msg = f"{name}: Status {response.status_code}"
            test_results["errors"].append(error_msg)
            log(f"❌ {name} - Status: {response.status_code}", Colors.RED)
            try:
                log(f"   Response: {json.dumps(response.json(), indent=2)}", Colors.YELLOW)
            except:
                log(f"   Response: {response.text[:200]}", Colors.YELLOW)
            return False
            
    except requests.exceptions.ConnectionError:
        test_results["failed"] += 1
        error_msg = f"{name}: Connection refused - Service not running"
        test_results["errors"].append(error_msg)
        log(f"❌ {name} - Connection refused", Colors.RED)
        return False
    except Exception as e:
        test_results["failed"] += 1
        error_msg = f"{name}: {str(e)}"
        test_results["errors"].append(error_msg)
        log(f"❌ {name} - Error: {str(e)}", Colors.RED)
        return False

def wait_for_service(url: str, service_name: str, max_attempts: int = 30) -> bool:
    """Wait for a service to be ready"""
    log(f"\n⏳ Waiting for {service_name} to start...", Colors.CYAN)
    
    for i in range(max_attempts):
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                log(f"✅ {service_name} is ready!", Colors.GREEN)
                return True
        except:
            pass
        print(".", end="", flush=True)
        time.sleep(1)
    
    log(f"\n❌ {service_name} failed to start after {max_attempts} attempts", Colors.RED)
    return False

def run_tests():
    """Run all API tests"""
    log("\n" + "="*60, Colors.CYAN)
    log("🧪 SuperHack Comprehensive API Test Suite", Colors.CYAN)
    log("="*60, Colors.CYAN)
    
    # Check services
    log("\n🔍 Checking services...", Colors.BLUE)
    backend_ready = wait_for_service(f"{BACKEND_URL}/health", "Backend")
    ai_ml_ready = wait_for_service(f"{AI_ML_URL}/", "AI/ML")
    
    if not backend_ready or not ai_ml_ready:
        log("\n❌ Services are not running!", Colors.RED)
        log("   Please start them first:", Colors.YELLOW)
        log("   Backend: cd backend && npm start", Colors.YELLOW)
        log("   AI/ML: cd ai-ml && python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000", Colors.YELLOW)
        return False
    
    # Test Backend Health
    log("\n📋 Testing Backend Endpoints", Colors.BLUE)
    test_endpoint("Backend Health", "GET", f"{BACKEND_URL}/health")
    test_endpoint("Backend Database Health", "GET", f"{BACKEND_URL}/health/database")
    
    # Test AI/ML Health
    log("\n📋 Testing AI/ML Health Endpoints", Colors.BLUE)
    test_endpoint("AI/ML Root", "GET", f"{AI_ML_URL}/", 
                 headers={"Authorization": f"Bearer {AI_ML_API_KEY}"})
    test_endpoint("AI/ML Health", "GET", f"{AI_ML_URL}/api/health",
                 headers={"Authorization": f"Bearer {AI_ML_API_KEY}"})
    
    # Test AI/ML Profitability
    log("\n📋 Testing AI/ML Profitability Endpoint", Colors.BLUE)
    profitability_data = {
        "client_id": "test-client-1",
        "financial_metrics": {
            "monthly_revenue": 5000,
            "total_revenue": 60000,
            "profit_margin": 0.25
        },
        "operational_metrics": {
            "ticket_count": 10,
            "avg_resolution_time": 2.5,
            "sla_compliance": 0.95
        },
        "client_characteristics": {
            "contract_value": 60000,
            "service_tier": "premium",
            "tenure_months": 12
        },
        "historical_data": {
            "revenue_trend": "increasing",
            "satisfaction_score": 4.5
        },
        "prediction_options": {
            "forecast_horizon": 6,
            "include_confidence": True
        }
    }
    test_endpoint("Profitability Prediction", "POST", 
                 f"{AI_ML_URL}/api/profitability/",
                 data=profitability_data,
                 headers={"Authorization": f"Bearer {AI_ML_API_KEY}"})
    
    # Test AI/ML Churn
    log("\n📋 Testing AI/ML Churn Endpoint", Colors.BLUE)
    churn_data = {
        "client_id": "test-client-1",
        "contract_value": 60000,
        "last_contact_days": 5,
        "ticket_frequency": 2,
        "satisfaction_score": 4.5,
        "payment_delays": 0,
        "service_issues": 1
    }
    test_endpoint("Churn Prediction", "POST",
                 f"{AI_ML_URL}/api/churn/predict",
                 data=churn_data,
                 headers={"Authorization": f"Bearer {AI_ML_API_KEY}"})
    
    # Test AI/ML Revenue Leak
    log("\n📋 Testing AI/ML Revenue Leak Endpoint", Colors.BLUE)
    revenue_leak_data = {
        "billing_data": {
            "invoices": [
                {"amount": 5000, "status": "paid", "date": "2024-01-01"},
                {"amount": 4500, "status": "pending", "date": "2024-01-15"}
            ]
        },
        "service_data": {
            "services_delivered": 10,
            "services_billed": 8
        },
        "time_period_days": 30
    }
    test_endpoint("Revenue Leak Detection", "POST",
                 f"{AI_ML_URL}/api/revenue-leak/detect",
                 data=revenue_leak_data,
                 headers={"Authorization": f"Bearer {AI_ML_API_KEY}"})
    
    # Test AI/ML Pricing
    log("\n📋 Testing AI/ML Pricing Endpoint", Colors.BLUE)
    pricing_data = {
        "client_profile": {
            "client_id": "test-client-1",
            "contract_value": 60000,
            "service_tier": "premium"
        },
        "service_type": "managed_services",
        "market_conditions": {
            "competitor_avg_price": 5500,
            "market_demand": "high"
        },
        "competitor_data": {
            "prices": [5000, 5500, 6000]
        }
    }
    test_endpoint("Dynamic Pricing", "POST",
                 f"{AI_ML_URL}/api/pricing/recommend",
                 data=pricing_data,
                 headers={"Authorization": f"Bearer {AI_ML_API_KEY}"})
    
    # Test AI/ML Budget
    log("\n📋 Testing AI/ML Budget Endpoint", Colors.BLUE)
    budget_data = {
        "current_budget": {
            "total": 100000,
            "allocated": 80000
        },
        "departments": [
            {"name": "IT", "current": 40000, "required": 45000},
            {"name": "Sales", "current": 30000, "required": 35000}
        ],
        "constraints": {
            "max_total": 120000,
            "min_department": 20000
        },
        "optimization_method": "linear_programming"
    }
    test_endpoint("Budget Optimization", "POST",
                 f"{AI_ML_URL}/api/budget/optimize",
                 data=budget_data,
                 headers={"Authorization": f"Bearer {AI_ML_API_KEY}"})
    
    # Test AI/ML Demand
    log("\n📋 Testing AI/ML Demand Endpoint", Colors.BLUE)
    demand_data = {
        "historical_data": {
            "periods": [
                {"month": "2024-01", "demand": 100},
                {"month": "2024-02", "demand": 110},
                {"month": "2024-03", "demand": 105}
            ]
        },
        "forecast_horizon": 6,
        "seasonality": True,
        "method": "prophet"
    }
    test_endpoint("Demand Forecasting", "POST",
                 f"{AI_ML_URL}/api/demand/forecast",
                 data=demand_data,
                 headers={"Authorization": f"Bearer {AI_ML_API_KEY}"})
    
    # Test AI/ML Anomaly
    log("\n📋 Testing AI/ML Anomaly Endpoint", Colors.BLUE)
    anomaly_data = {
        "data": [
            {"timestamp": "2024-01-01", "value": 100},
            {"timestamp": "2024-01-02", "value": 105},
            {"timestamp": "2024-01-03", "value": 200}  # Anomaly
        ],
        "stream_type": "revenue",
        "detection_method": "isolation_forest",
        "window_size": 10
    }
    test_endpoint("Anomaly Detection", "POST",
                 f"{AI_ML_URL}/api/anomaly/detect",
                 data=anomaly_data,
                 headers={"Authorization": f"Bearer {AI_ML_API_KEY}"})
    
    # Test AI/ML Models
    log("\n📋 Testing AI/ML Model Management", Colors.BLUE)
    test_endpoint("List Models", "GET",
                 f"{AI_ML_URL}/api/models",
                 headers={"Authorization": f"Bearer {AI_ML_API_KEY}"})
    
    # Test AI/ML Monitoring
    log("\n📋 Testing AI/ML Monitoring", Colors.BLUE)
    test_endpoint("Monitoring Metrics", "GET",
                 f"{AI_ML_URL}/api/monitoring/metrics",
                 headers={"Authorization": f"Bearer {AI_ML_API_KEY}"})
    
    # Test Backend AI Integration
    log("\n📋 Testing Backend AI Integration Endpoints", Colors.BLUE)
    # Note: These may require authentication tokens
    test_endpoint("Backend AI Health", "GET",
                 f"{BACKEND_URL}/api/ai/health",
                 expected_status=200)  # May be 401 without auth
    
    # Print summary
    log("\n" + "="*60, Colors.CYAN)
    log("📊 Test Summary", Colors.CYAN)
    log("="*60, Colors.CYAN)
    log(f"✅ Passed: {test_results['passed']}", Colors.GREEN)
    log(f"❌ Failed: {test_results['failed']}", Colors.RED)
    
    if test_results["errors"]:
        log("\n❌ Errors:", Colors.RED)
        for i, error in enumerate(test_results["errors"], 1):
            log(f"  {i}. {error}", Colors.YELLOW)
    
    log("\n" + "="*60, Colors.CYAN)
    
    return test_results["failed"] == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)

