const { query, body } = require('express-validator')

// Validation for profitability genome
const getProfitabilityGenomeValidation = [
  query('organization_id')
    .optional()
    .isUUID()
    .withMessage('Invalid organization ID format'),
  query('client_id')
    .optional()
    .isUUID()
    .withMessage('Invalid client ID format'),
  query('include_dna_analysis')
    .optional()
    .isBoolean()
    .withMessage('include_dna_analysis must be a boolean'),
  query('include_genetic_factors')
    .optional()
    .isBoolean()
    .withMessage('include_genetic_factors must be a boolean'),
  query('include_evolution_tracking')
    .optional()
    .isBoolean()
    .withMessage('include_evolution_tracking must be a boolean')
]

// Validation for service optimization
const getServiceOptimizationValidation = [
  query('organization_id')
    .optional()
    .isUUID()
    .withMessage('Invalid organization ID format'),
  query('service_id')
    .optional()
    .isUUID()
    .withMessage('Invalid service ID format'),
  query('optimization_focus')
    .optional()
    .isIn(['efficiency', 'quality', 'cost', 'all'])
    .withMessage('optimization_focus must be one of: efficiency, quality, cost, all'),
  query('include_automation')
    .optional()
    .isBoolean()
    .withMessage('include_automation must be a boolean'),
  query('include_scaling')
    .optional()
    .isBoolean()
    .withMessage('include_scaling must be a boolean')
]

// Validation for pricing recommendations
const getPricingRecommendationsValidation = [
  query('organization_id')
    .optional()
    .isUUID()
    .withMessage('Invalid organization ID format'),
  query('service_id')
    .optional()
    .isUUID()
    .withMessage('Invalid service ID format'),
  query('pricing_strategy')
    .optional()
    .isIn(['competitive', 'value_based', 'cost_plus', 'all'])
    .withMessage('pricing_strategy must be one of: competitive, value_based, cost_plus, all'),
  query('include_market_analysis')
    .optional()
    .isBoolean()
    .withMessage('include_market_analysis must be a boolean'),
  query('include_client_segmentation')
    .optional()
    .isBoolean()
    .withMessage('include_client_segmentation must be a boolean')
]

// Validation for market analysis
const getMarketAnalysisValidation = [
  query('organization_id')
    .optional()
    .isUUID()
    .withMessage('Invalid organization ID format'),
  query('analysis_depth')
    .optional()
    .isIn(['basic', 'standard', 'comprehensive'])
    .withMessage('analysis_depth must be one of: basic, standard, comprehensive'),
  query('include_competitors')
    .optional()
    .isBoolean()
    .withMessage('include_competitors must be a boolean'),
  query('include_trends')
    .optional()
    .isBoolean()
    .withMessage('include_trends must be a boolean'),
  query('include_opportunities')
    .optional()
    .isBoolean()
    .withMessage('include_opportunities must be a boolean')
]

// Validation for competitive intelligence
const getCompetitiveIntelligenceValidation = [
  query('organization_id')
    .optional()
    .isUUID()
    .withMessage('Invalid organization ID format'),
  query('competitor_focus')
    .optional()
    .isIn(['direct', 'indirect', 'all'])
    .withMessage('competitor_focus must be one of: direct, indirect, all'),
  query('analysis_type')
    .optional()
    .isIn(['basic', 'detailed', 'comprehensive'])
    .withMessage('analysis_type must be one of: basic, detailed, comprehensive'),
  query('include_swot')
    .optional()
    .isBoolean()
    .withMessage('include_swot must be a boolean'),
  query('include_positioning')
    .optional()
    .isBoolean()
    .withMessage('include_positioning must be a boolean')
]

// Validation for accept recommendation
const acceptRecommendationValidation = [
  body('recommendation_id')
    .isUUID()
    .withMessage('Invalid recommendation ID format'),
  body('organization_id')
    .isUUID()
    .withMessage('Invalid organization ID format'),
  body('acceptance_notes')
    .optional()
    .isString()
    .isLength({ min: 10, max: 1000 })
    .withMessage('Acceptance notes must be between 10 and 1000 characters'),
  body('implementation_plan')
    .optional()
    .isString()
    .isLength({ min: 20, max: 2000 })
    .withMessage('Implementation plan must be between 20 and 2000 characters'),
  body('expected_outcomes')
    .optional()
    .isString()
    .isLength({ min: 20, max: 1000 })
    .withMessage('Expected outcomes must be between 20 and 1000 characters')
]

module.exports = {
  getProfitabilityGenomeValidation,
  getServiceOptimizationValidation,
  getPricingRecommendationsValidation,
  getMarketAnalysisValidation,
  getCompetitiveIntelligenceValidation,
  acceptRecommendationValidation
}
