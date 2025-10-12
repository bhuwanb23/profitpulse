const { query } = require('express-validator')

// Validation for revenue trends
const getRevenueTrendsValidation = [
  query('organization_id')
    .optional()
    .isUUID()
    .withMessage('Invalid organization ID format'),
  query('period')
    .optional()
    .isIn(['daily', 'weekly', 'monthly', 'quarterly', 'yearly'])
    .withMessage('Invalid period. Must be one of: daily, weekly, monthly, quarterly, yearly'),
  query('start_date')
    .optional()
    .isISO8601()
    .withMessage('Invalid start date format'),
  query('end_date')
    .optional()
    .isISO8601()
    .withMessage('Invalid end date format'),
  query('client_id')
    .optional()
    .isUUID()
    .withMessage('Invalid client ID format')
]

// Validation for payment status
const getPaymentStatusValidation = [
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
  query('client_id')
    .optional()
    .isUUID()
    .withMessage('Invalid client ID format')
]

// Validation for outstanding payments
const getOutstandingPaymentsValidation = [
  query('organization_id')
    .optional()
    .isUUID()
    .withMessage('Invalid organization ID format'),
  query('client_id')
    .optional()
    .isUUID()
    .withMessage('Invalid client ID format'),
  query('days_overdue')
    .optional()
    .isInt({ min: 0 })
    .withMessage('Days overdue must be a non-negative integer'),
  query('amount_min')
    .optional()
    .isFloat({ min: 0 })
    .withMessage('Amount minimum must be a positive number'),
  query('amount_max')
    .optional()
    .isFloat({ min: 0 })
    .withMessage('Amount maximum must be a positive number'),
  query('sort_by')
    .optional()
    .isIn(['due_date', 'total_amount', 'invoice_date', 'client_name'])
    .withMessage('Invalid sort field'),
  query('sort_order')
    .optional()
    .isIn(['ASC', 'DESC'])
    .withMessage('Sort order must be ASC or DESC')
]

// Validation for billing efficiency
const getBillingEfficiencyValidation = [
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
  query('client_id')
    .optional()
    .isUUID()
    .withMessage('Invalid client ID format')
]

// Validation for payment methods
const getPaymentMethodsValidation = [
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
  query('client_id')
    .optional()
    .isUUID()
    .withMessage('Invalid client ID format')
]

// Validation for revenue forecasting
const getRevenueForecastingValidation = [
  query('organization_id')
    .optional()
    .isUUID()
    .withMessage('Invalid organization ID format'),
  query('forecast_months')
    .optional()
    .isInt({ min: 1, max: 24 })
    .withMessage('Forecast months must be between 1 and 24'),
  query('confidence_level')
    .optional()
    .isFloat({ min: 0.1, max: 0.99 })
    .withMessage('Confidence level must be between 0.1 and 0.99')
]

module.exports = {
  getRevenueTrendsValidation,
  getPaymentStatusValidation,
  getOutstandingPaymentsValidation,
  getBillingEfficiencyValidation,
  getPaymentMethodsValidation,
  getRevenueForecastingValidation
}
