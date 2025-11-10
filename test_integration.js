/**
 * Integration Test Script
 * Tests the integration between Backend (Node.js) and AI/ML (Python FastAPI) services
 */

const axios = require('axios');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

// Configuration
const BACKEND_URL = 'http://localhost:3000';
const AI_ML_URL = 'http://localhost:8000';
const AI_ML_API_KEY = 'admin_key';

// Colors for console output
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m'
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

// Test results
const testResults = {
  passed: 0,
  failed: 0,
  errors: []
};

// Wait for service to be ready
async function waitForService(url, serviceName, maxAttempts = 30) {
  log(`\n⏳ Waiting for ${serviceName} to start...`, 'cyan');
  
  for (let i = 0; i < maxAttempts; i++) {
    try {
      const response = await axios.get(url, { timeout: 2000 });
      if (response.status === 200) {
        log(`✅ ${serviceName} is ready!`, 'green');
        return true;
      }
    } catch (error) {
      // Service not ready yet
      process.stdout.write('.');
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  }
  
  log(`\n❌ ${serviceName} failed to start after ${maxAttempts} attempts`, 'red');
  return false;
}

// Test function
async function testEndpoint(name, method, url, data = null, headers = {}) {
  try {
    const config = {
      method,
      url,
      headers: {
        'Content-Type': 'application/json',
        ...headers
      },
      timeout: 10000
    };
    
    if (data) {
      config.data = data;
    }
    
    const response = await axios(config);
    
    if (response.status >= 200 && response.status < 300) {
      testResults.passed++;
      log(`✅ ${name} - Status: ${response.status}`, 'green');
      return { success: true, data: response.data };
    } else {
      testResults.failed++;
      testResults.errors.push(`${name}: Unexpected status ${response.status}`);
      log(`❌ ${name} - Status: ${response.status}`, 'red');
      return { success: false, error: `Status ${response.status}` };
    }
  } catch (error) {
    testResults.failed++;
    const errorMsg = error.response 
      ? `${name}: ${error.response.status} - ${error.response.data?.message || error.message}`
      : `${name}: ${error.message}`;
    testResults.errors.push(errorMsg);
    log(`❌ ${name} - Error: ${error.message}`, 'red');
    return { success: false, error: error.message };
  }
}

// Main test suite
async function runTests() {
  log('\n' + '='.repeat(60), 'cyan');
  log('🧪 SuperHack Integration Test Suite', 'cyan');
  log('='.repeat(60), 'cyan');
  
  // Test 1: Backend Health Check
  log('\n📋 Test 1: Backend Health Check', 'blue');
  await testEndpoint('Backend Health', 'GET', `${BACKEND_URL}/health`);
  
  // Test 2: AI/ML Health Check
  log('\n📋 Test 2: AI/ML Health Check', 'blue');
  await testEndpoint('AI/ML Root', 'GET', `${AI_ML_URL}/`, null, {
    'Authorization': `Bearer ${AI_ML_API_KEY}`
  });
  
  await testEndpoint('AI/ML Health', 'GET', `${AI_ML_URL}/api/health`, null, {
    'Authorization': `Bearer ${AI_ML_API_KEY}`
  });
  
  // Test 3: Backend → AI/ML Integration (via Backend health endpoint)
  log('\n📋 Test 3: Backend → AI/ML Integration', 'blue');
  await testEndpoint('Backend AI Health', 'GET', `${BACKEND_URL}/api/ai/health`, null, {
    'Authorization': 'Bearer test_token'
  });
  
  // Test 4: AI/ML Profitability Prediction
  log('\n📋 Test 4: AI/ML Profitability Prediction', 'blue');
  const profitabilityData = {
    client_id: 'test-client-1',
    financial_metrics: {
      monthly_revenue: 5000,
      total_revenue: 60000,
      profit_margin: 0.25
    },
    operational_metrics: {
      ticket_count: 10,
      avg_resolution_time: 2.5,
      sla_compliance: 0.95
    },
    client_characteristics: {
      contract_value: 60000,
      service_tier: 'premium',
      tenure_months: 12
    },
    historical_data: {
      revenue_trend: 'increasing',
      satisfaction_score: 4.5
    },
    prediction_options: {
      forecast_horizon: 6,
      include_confidence: true
    }
  };
  
  await testEndpoint('Profitability Prediction', 'POST', 
    `${AI_ML_URL}/api/profitability/`, 
    profitabilityData,
    { 'Authorization': `Bearer ${AI_ML_API_KEY}` }
  );
  
  // Test 5: AI/ML Churn Prediction
  log('\n📋 Test 5: AI/ML Churn Prediction', 'blue');
  const churnData = {
    client_id: 'test-client-1',
    contract_value: 60000,
    last_contact_days: 5,
    ticket_frequency: 2,
    satisfaction_score: 4.5,
    payment_delays: 0,
    service_issues: 1
  };
  
  await testEndpoint('Churn Prediction', 'POST',
    `${AI_ML_URL}/api/churn/predict`,
    churnData,
    { 'Authorization': `Bearer ${AI_ML_API_KEY}` }
  );
  
  // Test 6: AI/ML Revenue Leak Detection
  log('\n📋 Test 6: AI/ML Revenue Leak Detection', 'blue');
  const revenueLeakData = {
    billing_data: {
      invoices: [
        { amount: 5000, status: 'paid', date: '2024-01-01' },
        { amount: 4500, status: 'pending', date: '2024-01-15' }
      ]
    },
    service_data: {
      services_delivered: 10,
      services_billed: 8
    },
    time_period_days: 30
  };
  
  await testEndpoint('Revenue Leak Detection', 'POST',
    `${AI_ML_URL}/api/revenue-leak/detect`,
    revenueLeakData,
    { 'Authorization': `Bearer ${AI_ML_API_KEY}` }
  );
  
  // Test 7: Backend AI Insights (should call AI/ML)
  log('\n📋 Test 7: Backend AI Insights Endpoint', 'blue');
  await testEndpoint('Backend Profitability Genome', 'GET',
    `${BACKEND_URL}/api/ai/insights/profitability-genome?organization_id=test-org`,
    null,
    { 'Authorization': 'Bearer test_token' }
  );
  
  // Test 8: Backend Predictive Analytics
  log('\n📋 Test 8: Backend Predictive Analytics', 'blue');
  await testEndpoint('Backend Churn Prediction', 'GET',
    `${BACKEND_URL}/api/ai/predictions/churn?client_id=test-client`,
    null,
    { 'Authorization': 'Bearer test_token' }
  );
  
  // Test 9: AI/ML Models List
  log('\n📋 Test 9: AI/ML Models List', 'blue');
  await testEndpoint('AI/ML Models', 'GET',
    `${AI_ML_URL}/api/models`,
    null,
    { 'Authorization': `Bearer ${AI_ML_API_KEY}` }
  );
  
  // Test 10: AI/ML Monitoring
  log('\n📋 Test 10: AI/ML Monitoring', 'blue');
  await testEndpoint('AI/ML Monitoring Metrics', 'GET',
    `${AI_ML_URL}/api/monitoring/metrics`,
    null,
    { 'Authorization': `Bearer ${AI_ML_API_KEY}` }
  );
  
  // Print summary
  log('\n' + '='.repeat(60), 'cyan');
  log('📊 Test Summary', 'cyan');
  log('='.repeat(60), 'cyan');
  log(`✅ Passed: ${testResults.passed}`, 'green');
  log(`❌ Failed: ${testResults.failed}`, 'red');
  
  if (testResults.errors.length > 0) {
    log('\n❌ Errors:', 'red');
    testResults.errors.forEach((error, index) => {
      log(`  ${index + 1}. ${error}`, 'yellow');
    });
  }
  
  log('\n' + '='.repeat(60), 'cyan');
  
  return testResults.failed === 0;
}

// Main execution
async function main() {
  log('\n🚀 Starting Integration Tests...', 'cyan');
  
  // Check if services are running
  log('\n🔍 Checking if services are running...', 'cyan');
  
  const backendReady = await waitForService(`${BACKEND_URL}/health`, 'Backend');
  const aiMlReady = await waitForService(`${AI_ML_URL}/`, 'AI/ML');
  
  if (!backendReady || !aiMlReady) {
    log('\n❌ Services are not running. Please start them first:', 'red');
    log('  Backend: cd backend && npm start', 'yellow');
    log('  AI/ML: cd ai-ml && python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000', 'yellow');
    process.exit(1);
  }
  
  // Run tests
  const success = await runTests();
  
  // Exit with appropriate code
  process.exit(success ? 0 : 1);
}

// Run if executed directly
if (require.main === module) {
  main().catch(error => {
    log(`\n❌ Fatal error: ${error.message}`, 'red');
    console.error(error);
    process.exit(1);
  });
}

module.exports = { runTests, testEndpoint };

