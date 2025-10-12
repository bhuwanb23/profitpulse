const { query, body, param } = require('express-validator')

// Validation for AI analytics overview
const getAIAnalyticsOverviewValidation = [
  query('organization_id')
    .optional()
    .isUUID()
    .withMessage('Invalid organization ID format'),
  query('start_date')
    .optional()
    .isISO8601()
    .withMessage('Invalid start date format'),
  query('end_date')
    .optional()
    .isISO8601()
    .withMessage('Invalid end date format'),
  query('analysis_type')
    .optional()
    .isIn(['profitability', 'revenue_leak', 'budget_optimization', 'churn_prediction', 'demand_forecast'])
    .withMessage('Invalid analysis type')
]

// Validation for revenue leaks
const getRevenueLeaksValidation = [
  query('organization_id')
    .optional()
    .isUUID()
    .withMessage('Invalid organization ID format'),
  query('client_id')
    .optional()
    .isUUID()
    .withMessage('Invalid client ID format'),
  query('start_date')
    .optional()
    .isISO8601()
    .withMessage('Invalid start date format'),
  query('end_date')
    .optional()
    .isISO8601()
    .withMessage('Invalid end date format'),
  query('severity')
    .optional()
    .isIn(['low', 'medium', 'high', 'all'])
    .withMessage('Invalid severity level')
]

// Validation for profitability scores
const getProfitabilityScoresValidation = [
  query('organization_id')
    .optional()
    .isUUID()
    .withMessage('Invalid organization ID format'),
  query('client_id')
    .optional()
    .isUUID()
    .withMessage('Invalid client ID format'),
  query('start_date')
    .optional()
    .isISO8601()
    .withMessage('Invalid start date format'),
  query('end_date')
    .optional()
    .isISO8601()
    .withMessage('Invalid end date format'),
  query('min_score')
    .optional()
    .isFloat({ min: 0, max: 1 })
    .withMessage('Min score must be between 0 and 1'),
  query('max_score')
    .optional()
    .isFloat({ min: 0, max: 1 })
    .withMessage('Max score must be between 0 and 1')
]

// Validation for AI recommendations
const getAIRecommendationsValidation = [
  query('organization_id')
    .optional()
    .isUUID()
    .withMessage('Invalid organization ID format'),
  query('client_id')
    .optional()
    .isUUID()
    .withMessage('Invalid client ID format'),
  query('recommendation_type')
    .optional()
    .isIn(['pricing_adjustment', 'service_optimization', 'budget_reallocation', 'contract_renewal', 'upsell_opportunity'])
    .withMessage('Invalid recommendation type'),
  query('status')
    .optional()
    .isIn(['pending', 'accepted', 'rejected', 'implemented'])
    .withMessage('Invalid status'),
  query('min_impact_score')
    .optional()
    .isFloat({ min: 0, max: 1 })
    .withMessage('Min impact score must be between 0 and 1'),
  query('max_impact_score')
    .optional()
    .isFloat({ min: 0, max: 1 })
    .withMessage('Max impact score must be between 0 and 1'),
  query('sort_by')
    .optional()
    .isIn(['impact_score', 'created_at', 'estimated_savings', 'estimated_revenue_increase'])
    .withMessage('Invalid sort field'),
  query('sort_order')
    .optional()
    .isIn(['ASC', 'DESC'])
    .withMessage('Sort order must be ASC or DESC'),
  query('page')
    .optional()
    .isInt({ min: 1 })
    .withMessage('Page must be a positive integer'),
  query('limit')
    .optional()
    .isInt({ min: 1, max: 100 })
    .withMessage('Limit must be between 1 and 100')
]

// Validation for running AI analysis
const runAIAnalysisValidation = [
  body('organization_id')
    .isUUID()
    .withMessage('Valid organization ID is required'),
  body('analysis_type')
    .isIn(['profitability', 'revenue_leak', 'budget_optimization', 'churn_prediction', 'demand_forecast'])
    .withMessage('Valid analysis type is required'),
  body('client_id')
    .optional()
    .isUUID()
    .withMessage('Invalid client ID format'),
  body('parameters')
    .optional()
    .isObject()
    .withMessage('Parameters must be an object')
]

// Validation for analysis status
const getAnalysisStatusValidation = [
  param('id')
    .isUUID()
    .withMessage('Invalid analysis ID format')
]

module.exports = {
  getAIAnalyticsOverviewValidation,
  getRevenueLeaksValidation,
  getProfitabilityScoresValidation,
  getAIRecommendationsValidation,
  runAIAnalysisValidation,
  getAnalysisStatusValidation
}
