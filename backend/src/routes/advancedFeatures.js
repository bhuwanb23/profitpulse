const express = require('express');
const { body, param, query } = require('express-validator');
const router = express.Router();
const {
  getHistoricalAnalysis,
  getTrendAnalysis,
  getPerformanceReport,
  getModelMetrics,
  triggerRetraining,
  getRetrainingStatus,
  listRetrainingJobs,
  getDashboardMetrics
} = require('../controllers/advancedFeaturesController');
const { authenticateToken } = require('../middleware/auth');

// Validation middleware
const validateHistoricalAnalysis = [
  body('model_type')
    .isIn(['profitability', 'churn', 'revenue_leak', 'pricing', 'budget', 'demand', 'anomaly'])
    .withMessage('Invalid model type'),
  body('organization_id')
    .isUUID()
    .withMessage('Invalid organization ID'),
  body('start_date')
    .isISO8601()
    .withMessage('Invalid start date format'),
  body('end_date')
    .isISO8601()
    .withMessage('Invalid end date format'),
  body('analysis_type')
    .optional()
    .isIn(['trend', 'performance', 'comparison'])
    .withMessage('Invalid analysis type'),
  body('parameters')
    .optional()
    .isObject()
    .withMessage('Parameters must be an object')
];

const validateTrendAnalysis = [
  body('model_type')
    .isIn(['profitability', 'churn', 'revenue_leak', 'pricing', 'budget', 'demand', 'anomaly'])
    .withMessage('Invalid model type'),
  body('organization_id')
    .isUUID()
    .withMessage('Invalid organization ID'),
  body('time_period')
    .optional()
    .isIn(['7d', '30d', '90d', '1y'])
    .withMessage('Invalid time period'),
  body('metrics')
    .optional()
    .isArray()
    .withMessage('Metrics must be an array'),
  body('granularity')
    .optional()
    .isIn(['hourly', 'daily', 'weekly', 'monthly'])
    .withMessage('Invalid granularity')
];

const validatePerformanceReport = [
  body('organization_id')
    .isUUID()
    .withMessage('Invalid organization ID'),
  body('model_type')
    .optional()
    .isIn(['profitability', 'churn', 'revenue_leak', 'pricing', 'budget', 'demand', 'anomaly'])
    .withMessage('Invalid model type'),
  body('report_type')
    .optional()
    .isIn(['summary', 'detailed', 'comparison'])
    .withMessage('Invalid report type'),
  body('time_range')
    .optional()
    .isIn(['7d', '30d', '90d', '1y'])
    .withMessage('Invalid time range'),
  body('metrics')
    .optional()
    .isArray()
    .withMessage('Metrics must be an array')
];

const validateRetrainingTrigger = [
  body('model_type')
    .isIn(['profitability', 'churn', 'revenue_leak', 'pricing', 'budget', 'demand', 'anomaly'])
    .withMessage('Invalid model type'),
  body('organization_id')
    .isUUID()
    .withMessage('Invalid organization ID'),
  body('trigger_type')
    .optional()
    .isIn(['performance', 'schedule', 'manual'])
    .withMessage('Invalid trigger type'),
  body('threshold_metrics')
    .optional()
    .isObject()
    .withMessage('Threshold metrics must be an object'),
  body('parameters')
    .optional()
    .isObject()
    .withMessage('Parameters must be an object')
];

const validateJobId = [
  param('jobId')
    .isUUID()
    .withMessage('Invalid job ID format')
];

const validateModelMetricsQuery = [
  query('model_type')
    .optional()
    .isIn(['profitability', 'churn', 'revenue_leak', 'pricing', 'budget', 'demand', 'anomaly'])
    .withMessage('Invalid model type'),
  query('organization_id')
    .optional()
    .isUUID()
    .withMessage('Invalid organization ID')
];

// Historical Data Analysis Routes

/**
 * @route POST /api/advanced/historical/analysis
 * @desc Get historical analysis for a specific model
 * @access Private
 */
router.post('/historical/analysis', 
  authenticateToken, 
  validateHistoricalAnalysis, 
  getHistoricalAnalysis
);

/**
 * @route POST /api/advanced/trends/analysis
 * @desc Get trend analysis for model performance
 * @access Private
 */
router.post('/trends/analysis', 
  authenticateToken, 
  validateTrendAnalysis, 
  getTrendAnalysis
);

// Performance Reporting Routes

/**
 * @route POST /api/advanced/performance/report
 * @desc Generate comprehensive performance report
 * @access Private
 */
router.post('/performance/report', 
  authenticateToken, 
  validatePerformanceReport, 
  getPerformanceReport
);

/**
 * @route GET /api/advanced/performance/metrics
 * @desc Get real-time model performance metrics
 * @access Private
 */
router.get('/performance/metrics', 
  authenticateToken, 
  validateModelMetricsQuery, 
  getModelMetrics
);

// Model Retraining Routes

/**
 * @route POST /api/advanced/retraining/trigger
 * @desc Trigger model retraining based on performance thresholds
 * @access Private
 */
router.post('/retraining/trigger', 
  authenticateToken, 
  validateRetrainingTrigger, 
  triggerRetraining
);

/**
 * @route GET /api/advanced/retraining/status/:jobId
 * @desc Get status of a retraining job
 * @access Private
 */
router.get('/retraining/status/:jobId', 
  authenticateToken, 
  validateJobId, 
  getRetrainingStatus
);

/**
 * @route GET /api/advanced/retraining/jobs
 * @desc List retraining jobs with optional filtering
 * @access Private
 */
router.get('/retraining/jobs', 
  authenticateToken, 
  [
    query('model_type')
      .optional()
      .isIn(['profitability', 'churn', 'revenue_leak', 'pricing', 'budget', 'demand', 'anomaly'])
      .withMessage('Invalid model type'),
    query('organization_id')
      .optional()
      .isUUID()
      .withMessage('Invalid organization ID'),
    query('status')
      .optional()
      .isIn(['pending', 'running', 'completed', 'failed', 'cancelled'])
      .withMessage('Invalid status')
  ], 
  listRetrainingJobs
);

// Dashboard and Alerting Routes

/**
 * @route GET /api/advanced/dashboard/metrics
 * @desc Get comprehensive dashboard metrics with alerts
 * @access Private
 */
router.get('/dashboard/metrics', 
  authenticateToken, 
  [
    query('organization_id')
      .isUUID()
      .withMessage('Invalid organization ID')
  ], 
  getDashboardMetrics
);

// Model-specific convenience routes

/**
 * @route POST /api/advanced/profitability/historical
 * @desc Get historical analysis for profitability model
 * @access Private
 */
router.post('/profitability/historical', authenticateToken, [
  body('organization_id').isUUID().withMessage('Invalid organization ID'),
  body('start_date').isISO8601().withMessage('Invalid start date format'),
  body('end_date').isISO8601().withMessage('Invalid end date format')
], async (req, res) => {
  req.body.model_type = 'profitability';
  return getHistoricalAnalysis(req, res);
});

/**
 * @route POST /api/advanced/churn/trends
 * @desc Get trend analysis for churn model
 * @access Private
 */
router.post('/churn/trends', authenticateToken, [
  body('organization_id').isUUID().withMessage('Invalid organization ID'),
  body('time_period').optional().isIn(['7d', '30d', '90d', '1y']).withMessage('Invalid time period')
], async (req, res) => {
  req.body.model_type = 'churn';
  return getTrendAnalysis(req, res);
});

/**
 * @route POST /api/advanced/revenue-leak/performance
 * @desc Get performance report for revenue leak model
 * @access Private
 */
router.post('/revenue-leak/performance', authenticateToken, [
  body('organization_id').isUUID().withMessage('Invalid organization ID'),
  body('time_range').optional().isIn(['7d', '30d', '90d', '1y']).withMessage('Invalid time range')
], async (req, res) => {
  req.body.model_type = 'revenue_leak';
  return getPerformanceReport(req, res);
});

/**
 * @route POST /api/advanced/pricing/retrain
 * @desc Trigger retraining for pricing model
 * @access Private
 */
router.post('/pricing/retrain', authenticateToken, [
  body('organization_id').isUUID().withMessage('Invalid organization ID'),
  body('threshold_metrics').optional().isObject().withMessage('Threshold metrics must be an object')
], async (req, res) => {
  req.body.model_type = 'pricing';
  return triggerRetraining(req, res);
});

/**
 * @route POST /api/advanced/budget/retrain
 * @desc Trigger retraining for budget model
 * @access Private
 */
router.post('/budget/retrain', authenticateToken, [
  body('organization_id').isUUID().withMessage('Invalid organization ID'),
  body('threshold_metrics').optional().isObject().withMessage('Threshold metrics must be an object')
], async (req, res) => {
  req.body.model_type = 'budget';
  return triggerRetraining(req, res);
});

/**
 * @route POST /api/advanced/demand/retrain
 * @desc Trigger retraining for demand forecasting model
 * @access Private
 */
router.post('/demand/retrain', authenticateToken, [
  body('organization_id').isUUID().withMessage('Invalid organization ID'),
  body('threshold_metrics').optional().isObject().withMessage('Threshold metrics must be an object')
], async (req, res) => {
  req.body.model_type = 'demand';
  return triggerRetraining(req, res);
});

/**
 * @route POST /api/advanced/anomaly/retrain
 * @desc Trigger retraining for anomaly detection model
 * @access Private
 */
router.post('/anomaly/retrain', authenticateToken, [
  body('organization_id').isUUID().withMessage('Invalid organization ID'),
  body('threshold_metrics').optional().isObject().withMessage('Threshold metrics must be an object')
], async (req, res) => {
  req.body.model_type = 'anomaly';
  return triggerRetraining(req, res);
});

module.exports = router;
