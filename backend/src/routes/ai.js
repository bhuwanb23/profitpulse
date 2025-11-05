const express = require('express');
const router = express.Router();

const {
  healthCheck,
  predictProfitability,
  predictChurn,
  detectRevenueLeaks,
  getDynamicPricing,
  optimizeBudget,
  forecastDemand,
  detectAnomalies,
  getModelInfo,
  getModelHealth,
  batchPredict
} = require('../controllers/aiController');

const {
  validateProfitabilityPrediction,
  validateChurnPrediction,
  validateRevenueLeakDetection,
  validateDynamicPricing,
  validateBudgetOptimization,
  validateDemandForecasting,
  validateAnomalyDetection,
  validateModelInfo,
  validateModelHealth,
  validateBatchPrediction
} = require('../validators/aiValidator');

// Health check endpoint
router.get('/health', healthCheck);

// Profitability prediction endpoint
router.post('/profitability', validateProfitabilityPrediction, predictProfitability);

// Churn prediction endpoint
router.post('/churn', validateChurnPrediction, predictChurn);

// Revenue leak detection endpoint
router.post('/revenue-leaks', validateRevenueLeakDetection, detectRevenueLeaks);

// Dynamic pricing recommendation endpoint
router.post('/pricing', validateDynamicPricing, getDynamicPricing);

// Budget optimization endpoint
router.post('/budget', validateBudgetOptimization, optimizeBudget);

// Demand forecasting endpoint
router.post('/demand', validateDemandForecasting, forecastDemand);

// Anomaly detection endpoint
router.post('/anomalies', validateAnomalyDetection, detectAnomalies);

// Model information endpoint
router.get('/models/:model_name/info', validateModelInfo, getModelInfo);

// Model health endpoint
router.get('/models/:model_name/health', validateModelHealth, getModelHealth);

// Batch prediction endpoint
router.post('/batch', validateBatchPrediction, batchPredict);

module.exports = router;