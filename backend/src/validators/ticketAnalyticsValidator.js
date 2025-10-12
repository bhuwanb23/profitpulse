const { query } = require('express-validator')

// Common validation for analytics endpoints
const analyticsValidation = [
  query('organization_id')
    .optional()
    .isUUID()
    .withMessage('Invalid organization ID format'),
  query('period')
    .optional()
    .isIn(['7d', '30d', '90d', '1y'])
    .withMessage('Invalid period. Must be one of: 7d, 30d, 90d, 1y'),
  query('start_date')
    .optional()
    .isISO8601()
    .withMessage('Start date must be a valid ISO 8601 date'),
  query('end_date')
    .optional()
    .isISO8601()
    .withMessage('End date must be a valid ISO 8601 date')
]

// Validation for volume trends
const volumeTrendsValidation = [
  ...analyticsValidation
]

// Validation for resolution time analytics
const resolutionTimeValidation = [
  ...analyticsValidation
]

// Validation for category breakdown
const categoryBreakdownValidation = [
  ...analyticsValidation
]

// Validation for technician performance
const technicianPerformanceValidation = [
  ...analyticsValidation
]

// Validation for SLA compliance
const slaComplianceValidation = [
  ...analyticsValidation
]

// Validation for customer satisfaction
const customerSatisfactionValidation = [
  ...analyticsValidation
]

module.exports = {
  volumeTrendsValidation,
  resolutionTimeValidation,
  categoryBreakdownValidation,
  technicianPerformanceValidation,
  slaComplianceValidation,
  customerSatisfactionValidation
}
