const { body, param, query } = require('express-validator')

// Validation for creating service
const createServiceValidation = [
  body('name')
    .notEmpty()
    .withMessage('Service name is required')
    .isLength({ min: 2, max: 100 })
    .withMessage('Service name must be between 2 and 100 characters'),
  body('description')
    .optional()
    .isLength({ min: 10, max: 1000 })
    .withMessage('Description must be between 10 and 1000 characters'),
  body('category')
    .optional()
    .isLength({ min: 2, max: 50 })
    .withMessage('Category must be between 2 and 50 characters'),
  body('type')
    .optional()
    .isIn(['basic', 'premium', 'enterprise', 'custom'])
    .withMessage('Invalid service type. Must be one of: basic, premium, enterprise, custom'),
  body('status')
    .optional()
    .isIn(['active', 'inactive', 'suspended', 'terminated'])
    .withMessage('Invalid status. Must be one of: active, inactive, suspended, terminated'),
  body('base_price')
    .optional()
    .isFloat({ min: 0 })
    .withMessage('Base price must be a positive number'),
  body('monthly_cost')
    .optional()
    .isFloat({ min: 0 })
    .withMessage('Monthly cost must be a positive number'),
  body('billing_type')
    .optional()
    .isIn(['hourly', 'monthly', 'per-user', 'per-device'])
    .withMessage('Invalid billing type. Must be one of: hourly, monthly, per-user, per-device'),
  body('organization_id')
    .isUUID()
    .withMessage('Invalid organization ID format'),
  body('client_id')
    .optional()
    .isUUID()
    .withMessage('Invalid client ID format')
]

// Validation for updating service
const updateServiceValidation = [
  param('id').isUUID().withMessage('Invalid service ID format'),
  body('name')
    .optional()
    .isLength({ min: 2, max: 100 })
    .withMessage('Service name must be between 2 and 100 characters'),
  body('description')
    .optional()
    .isLength({ min: 10, max: 1000 })
    .withMessage('Description must be between 10 and 1000 characters'),
  body('category')
    .optional()
    .isLength({ min: 2, max: 50 })
    .withMessage('Category must be between 2 and 50 characters'),
  body('type')
    .optional()
    .isIn(['basic', 'premium', 'enterprise', 'custom'])
    .withMessage('Invalid service type. Must be one of: basic, premium, enterprise, custom'),
  body('status')
    .optional()
    .isIn(['active', 'inactive', 'suspended', 'terminated'])
    .withMessage('Invalid status. Must be one of: active, inactive, suspended, terminated'),
  body('base_price')
    .optional()
    .isFloat({ min: 0 })
    .withMessage('Base price must be a positive number'),
  body('monthly_cost')
    .optional()
    .isFloat({ min: 0 })
    .withMessage('Monthly cost must be a positive number'),
  body('billing_type')
    .optional()
    .isIn(['hourly', 'monthly', 'per-user', 'per-device'])
    .withMessage('Invalid billing type. Must be one of: hourly, monthly, per-user, per-device'),
  body('client_id')
    .optional()
    .isUUID()
    .withMessage('Invalid client ID format')
]

// Validation for service ID parameter
const serviceIdValidation = [
  param('id').isUUID().withMessage('Invalid service ID format')
]

// Validation for query parameters
const getServicesValidation = [
  query('page')
    .optional()
    .isInt({ min: 1 })
    .withMessage('Page must be a positive integer'),
  query('limit')
    .optional()
    .isInt({ min: 1, max: 100 })
    .withMessage('Limit must be between 1 and 100'),
  query('search')
    .optional()
    .isLength({ min: 1, max: 100 })
    .withMessage('Search term must be between 1 and 100 characters'),
  query('category')
    .optional()
    .isLength({ min: 1, max: 50 })
    .withMessage('Category filter must be between 1 and 50 characters'),
  query('type')
    .optional()
    .isIn(['basic', 'premium', 'enterprise', 'custom'])
    .withMessage('Invalid service type filter'),
  query('status')
    .optional()
    .isIn(['active', 'inactive', 'suspended', 'terminated'])
    .withMessage('Invalid status filter'),
  query('is_active')
    .optional()
    .isIn(['true', 'false'])
    .withMessage('is_active must be true or false'),
  query('organization_id')
    .optional()
    .isUUID()
    .withMessage('Invalid organization ID format'),
  query('client_id')
    .optional()
    .isUUID()
    .withMessage('Invalid client ID format'),
  query('sort_by')
    .optional()
    .isIn(['name', 'category', 'type', 'status', 'base_price', 'monthly_cost', 'created_at', 'updated_at'])
    .withMessage('Invalid sort field'),
  query('sort_order')
    .optional()
    .isIn(['ASC', 'DESC', 'asc', 'desc'])
    .withMessage('Sort order must be ASC or DESC')
]

// Validation for assigning service to client
const assignServiceValidation = [
  param('id').isUUID().withMessage('Invalid service ID format'),
  body('client_id')
    .isUUID()
    .withMessage('Invalid client ID format')
]

// Validation for updating service pricing
const updatePricingValidation = [
  param('id').isUUID().withMessage('Invalid service ID format'),
  body('base_price')
    .optional()
    .isFloat({ min: 0 })
    .withMessage('Base price must be a positive number'),
  body('monthly_cost')
    .optional()
    .isFloat({ min: 0 })
    .withMessage('Monthly cost must be a positive number'),
  body('billing_type')
    .optional()
    .isIn(['hourly', 'monthly', 'per-user', 'per-device'])
    .withMessage('Invalid billing type. Must be one of: hourly, monthly, per-user, per-device')
]

module.exports = {
  createServiceValidation,
  updateServiceValidation,
  serviceIdValidation,
  getServicesValidation,
  assignServiceValidation,
  updatePricingValidation
}
