const { query } = require('express-validator')

// Validation for revenue forecasting
const getRevenueForecastingValidation = [
  query('organization_id')
    .optional()
    .isUUID()
    .withMessage('Invalid organization ID format'),
  query('client_id')
    .optional()
    .isUUID()
    .withMessage('Invalid client ID format'),
  query('forecast_period')
    .optional()
    .isInt({ min: 1, max: 24 })
    .withMessage('Forecast period must be between 1 and 24 months'),
  query('confidence_level')
    .optional()
    .isFloat({ min: 0.1, max: 0.99 })
    .withMessage('Confidence level must be between 0.1 and 0.99'),
  query('include_seasonality')
    .optional()
    .isBoolean()
    .withMessage('include_seasonality must be a boolean'),
  query('include_trends')
    .optional()
    .isBoolean()
    .withMessage('include_trends must be a boolean')
]

// Validation for churn prediction
const getChurnPredictionValidation = [
  query('organization_id')
    .optional()
    .isUUID()
    .withMessage('Invalid organization ID format'),
  query('prediction_horizon')
    .optional()
    .isInt({ min: 30, max: 365 })
    .withMessage('Prediction horizon must be between 30 and 365 days'),
  query('risk_threshold')
    .optional()
    .isFloat({ min: 0, max: 1 })
    .withMessage('Risk threshold must be between 0 and 1'),
  query('include_factors')
    .optional()
    .isBoolean()
    .withMessage('include_factors must be a boolean')
]

// Validation for demand forecasting
const getDemandForecastingValidation = [
  query('organization_id')
    .optional()
    .isUUID()
    .withMessage('Invalid organization ID format'),
  query('service_id')
    .optional()
    .isUUID()
    .withMessage('Invalid service ID format'),
  query('forecast_period')
    .optional()
    .isInt({ min: 1, max: 24 })
    .withMessage('Forecast period must be between 1 and 24 months'),
  query('include_seasonality')
    .optional()
    .isBoolean()
    .withMessage('include_seasonality must be a boolean'),
  query('include_growth_trends')
    .optional()
    .isBoolean()
    .withMessage('include_growth_trends must be a boolean')
]

// Validation for budget optimization
const getBudgetOptimizationValidation = [
  query('organization_id')
    .optional()
    .isUUID()
    .withMessage('Invalid organization ID format'),
  query('budget_id')
    .optional()
    .isUUID()
    .withMessage('Invalid budget ID format'),
  query('optimization_horizon')
    .optional()
    .isInt({ min: 1, max: 24 })
    .withMessage('Optimization horizon must be between 1 and 24 months'),
  query('include_scenarios')
    .optional()
    .isBoolean()
    .withMessage('include_scenarios must be a boolean'),
  query('risk_tolerance')
    .optional()
    .isFloat({ min: 0, max: 1 })
    .withMessage('Risk tolerance must be between 0 and 1')
]

// Validation for market trend analysis
const getMarketTrendAnalysisValidation = [
  query('organization_id')
    .optional()
    .isUUID()
    .withMessage('Invalid organization ID format'),
  query('analysis_period')
    .optional()
    .isInt({ min: 1, max: 24 })
    .withMessage('Analysis period must be between 1 and 24 months'),
  query('include_competitors')
    .optional()
    .isBoolean()
    .withMessage('include_competitors must be a boolean'),
  query('include_industry_trends')
    .optional()
    .isBoolean()
    .withMessage('include_industry_trends must be a boolean')
]

// Validation for growth opportunities
const getGrowthOpportunitiesValidation = [
  query('organization_id')
    .optional()
    .isUUID()
    .withMessage('Invalid organization ID format'),
  query('opportunity_type')
    .optional()
    .isIn(['client_expansion', 'service_diversification', 'revenue_optimization', 'market_penetration', 'technology_innovation'])
    .withMessage('Invalid opportunity type'),
  query('min_impact_score')
    .optional()
    .isFloat({ min: 0, max: 1 })
    .withMessage('Min impact score must be between 0 and 1'),
  query('include_implementation_plan')
    .optional()
    .isBoolean()
    .withMessage('include_implementation_plan must be a boolean')
]

module.exports = {
  getRevenueForecastingValidation,
  getChurnPredictionValidation,
  getDemandForecastingValidation,
  getBudgetOptimizationValidation,
  getMarketTrendAnalysisValidation,
  getGrowthOpportunitiesValidation
}
