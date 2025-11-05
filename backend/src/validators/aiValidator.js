const { body, param, query } = require('express-validator');

const validateProfitabilityPrediction = [
  body('client_id').notEmpty().withMessage('Client ID is required'),
  body('financial_data').isObject().withMessage('Financial data must be an object'),
  body('operational_data').optional().isObject().withMessage('Operational data must be an object'),
  query('model_version').optional().isString().withMessage('Model version must be a string'),
  query('return_confidence').optional().isBoolean().withMessage('Return confidence must be a boolean'),
  query('return_explanation').optional().isBoolean().withMessage('Return explanation must be a boolean')
];

const validateChurnPrediction = [
  body('client_id').notEmpty().withMessage('Client ID is required'),
  body('features').isObject().withMessage('Features must be an object'),
  body('timeframe_days').optional().isInt({ min: 1 }).withMessage('Timeframe days must be a positive integer'),
  query('model_version').optional().isString().withMessage('Model version must be a string')
];

const validateRevenueLeakDetection = [
  body('billing_data').isArray().withMessage('Billing data must be an array'),
  body('service_data').isArray().withMessage('Service data must be an array'),
  body('time_period_days').optional().isInt({ min: 1 }).withMessage('Time period days must be a positive integer'),
  query('model_version').optional().isString().withMessage('Model version must be a string')
];

const validateDynamicPricing = [
  body('client_profile').isObject().withMessage('Client profile must be an object'),
  body('service_type').notEmpty().withMessage('Service type is required'),
  body('market_conditions').optional().isObject().withMessage('Market conditions must be an object'),
  body('competitor_data').optional().isArray().withMessage('Competitor data must be an array'),
  query('model_version').optional().isString().withMessage('Model version must be a string')
];

const validateBudgetOptimization = [
  body('current_budget').isFloat({ min: 0 }).withMessage('Current budget must be a positive number'),
  body('departments').isArray().withMessage('Departments must be an array'),
  body('constraints').optional().isObject().withMessage('Constraints must be an object'),
  body('optimization_method').optional().isString().withMessage('Optimization method must be a string'),
  query('model_version').optional().isString().withMessage('Model version must be a string')
];

const validateDemandForecasting = [
  body('historical_data').isArray().withMessage('Historical data must be an array'),
  body('forecast_horizon').optional().isInt({ min: 1 }).withMessage('Forecast horizon must be a positive integer'),
  body('seasonality').optional().isBoolean().withMessage('Seasonality must be a boolean'),
  body('method').optional().isString().withMessage('Method must be a string'),
  query('model_version').optional().isString().withMessage('Model version must be a string')
];

const validateAnomalyDetection = [
  body('data').isArray().withMessage('Data must be an array'),
  body('stream_type').optional().isString().withMessage('Stream type must be a string'),
  body('detection_method').optional().isString().withMessage('Detection method must be a string'),
  body('window_size').optional().isInt({ min: 1 }).withMessage('Window size must be a positive integer'),
  query('model_version').optional().isString().withMessage('Model version must be a string')
];

const validateModelInfo = [
  param('model_name').notEmpty().withMessage('Model name is required')
];

const validateModelHealth = [
  param('model_name').notEmpty().withMessage('Model name is required')
];

const validateBatchPrediction = [
  body('model_name').notEmpty().withMessage('Model name is required'),
  body('data').isArray().withMessage('Data must be an array'),
  query('model_version').optional().isString().withMessage('Model version must be a string')
];

module.exports = {
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
};