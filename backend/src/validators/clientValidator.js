const { body, param, query } = require('express-validator')

// Validation for creating client
const createClientValidation = [
  body('name')
    .notEmpty()
    .withMessage('Client name is required')
    .isLength({ min: 2, max: 100 })
    .withMessage('Client name must be between 2 and 100 characters'),
  body('email')
    .isEmail()
    .withMessage('Invalid email format')
    .normalizeEmail(),
  body('phone')
    .optional()
    .isLength({ min: 10, max: 20 })
    .withMessage('Phone number must be between 10 and 20 characters')
    .matches(/^[\+]?[1-9][\d]{0,15}$/)
    .withMessage('Invalid phone number format'),
  body('company')
    .optional()
    .isLength({ min: 2, max: 100 })
    .withMessage('Company name must be between 2 and 100 characters'),
  body('contact_person')
    .optional()
    .isLength({ min: 2, max: 100 })
    .withMessage('Contact person name must be between 2 and 100 characters'),
  body('address')
    .optional()
    .isLength({ min: 5, max: 200 })
    .withMessage('Address must be between 5 and 200 characters'),
  body('city')
    .optional()
    .isLength({ min: 2, max: 50 })
    .withMessage('City must be between 2 and 50 characters'),
  body('state')
    .optional()
    .isLength({ min: 2, max: 50 })
    .withMessage('State must be between 2 and 50 characters'),
  body('zip_code')
    .optional()
    .isLength({ min: 3, max: 20 })
    .withMessage('ZIP code must be between 3 and 20 characters'),
  body('country')
    .optional()
    .isLength({ min: 2, max: 50 })
    .withMessage('Country must be between 2 and 50 characters'),
  body('industry')
    .optional()
    .isIn(['technology', 'healthcare', 'finance', 'retail', 'manufacturing', 'education', 'government', 'nonprofit', 'other'])
    .withMessage('Invalid industry. Must be one of: technology, healthcare, finance, retail, manufacturing, education, government, nonprofit, other'),
  body('status')
    .optional()
    .isIn(['active', 'inactive', 'suspended', 'terminated'])
    .withMessage('Invalid status. Must be one of: active, inactive, suspended, terminated'),
  body('contract_start_date')
    .optional()
    .isISO8601()
    .withMessage('Contract start date must be a valid date'),
  body('contract_end_date')
    .optional()
    .isISO8601()
    .withMessage('Contract end date must be a valid date'),
  body('monthly_budget')
    .optional()
    .isFloat({ min: 0 })
    .withMessage('Monthly budget must be a positive number'),
  body('organization_id')
    .optional()
    .isUUID()
    .withMessage('Invalid organization ID format')
]

// Validation for updating client
const updateClientValidation = [
  param('id').isUUID().withMessage('Invalid client ID format'),
  body('name')
    .optional()
    .isLength({ min: 2, max: 100 })
    .withMessage('Client name must be between 2 and 100 characters'),
  body('email')
    .optional()
    .isEmail()
    .withMessage('Invalid email format')
    .normalizeEmail(),
  body('phone')
    .optional()
    .isLength({ min: 10, max: 20 })
    .withMessage('Phone number must be between 10 and 20 characters')
    .matches(/^[\+]?[1-9][\d]{0,15}$/)
    .withMessage('Invalid phone number format'),
  body('company')
    .optional()
    .isLength({ min: 2, max: 100 })
    .withMessage('Company name must be between 2 and 100 characters'),
  body('contact_person')
    .optional()
    .isLength({ min: 2, max: 100 })
    .withMessage('Contact person name must be between 2 and 100 characters'),
  body('address')
    .optional()
    .isLength({ min: 5, max: 200 })
    .withMessage('Address must be between 5 and 200 characters'),
  body('city')
    .optional()
    .isLength({ min: 2, max: 50 })
    .withMessage('City must be between 2 and 50 characters'),
  body('state')
    .optional()
    .isLength({ min: 2, max: 50 })
    .withMessage('State must be between 2 and 50 characters'),
  body('zip_code')
    .optional()
    .isLength({ min: 3, max: 20 })
    .withMessage('ZIP code must be between 3 and 20 characters'),
  body('country')
    .optional()
    .isLength({ min: 2, max: 50 })
    .withMessage('Country must be between 2 and 50 characters'),
  body('industry')
    .optional()
    .isIn(['technology', 'healthcare', 'finance', 'retail', 'manufacturing', 'education', 'government', 'nonprofit', 'other'])
    .withMessage('Invalid industry. Must be one of: technology, healthcare, finance, retail, manufacturing, education, government, nonprofit, other'),
  body('status')
    .optional()
    .isIn(['active', 'inactive', 'suspended', 'terminated'])
    .withMessage('Invalid status. Must be one of: active, inactive, suspended, terminated'),
  body('contract_start_date')
    .optional()
    .isISO8601()
    .withMessage('Contract start date must be a valid date'),
  body('contract_end_date')
    .optional()
    .isISO8601()
    .withMessage('Contract end date must be a valid date'),
  body('monthly_budget')
    .optional()
    .isFloat({ min: 0 })
    .withMessage('Monthly budget must be a positive number'),
  body('organization_id')
    .optional()
    .isUUID()
    .withMessage('Invalid organization ID format')
]

// Validation for client ID parameter
const clientIdValidation = [
  param('id').isUUID().withMessage('Invalid client ID format')
]

// Validation for query parameters
const getClientsValidation = [
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
  query('industry')
    .optional()
    .isIn(['technology', 'healthcare', 'finance', 'retail', 'manufacturing', 'education', 'government', 'nonprofit', 'other'])
    .withMessage('Invalid industry filter'),
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
  query('sort_by')
    .optional()
    .isIn(['name', 'email', 'company', 'created_at', 'updated_at', 'monthly_budget'])
    .withMessage('Invalid sort field'),
  query('sort_order')
    .optional()
    .isIn(['ASC', 'DESC', 'asc', 'desc'])
    .withMessage('Sort order must be ASC or DESC')
]

// Validation for client services query
const getClientServicesValidation = [
  param('id').isUUID().withMessage('Invalid client ID format'),
  query('page')
    .optional()
    .isInt({ min: 1 })
    .withMessage('Page must be a positive integer'),
  query('limit')
    .optional()
    .isInt({ min: 1, max: 100 })
    .withMessage('Limit must be between 1 and 100'),
  query('status')
    .optional()
    .isIn(['active', 'inactive', 'suspended', 'terminated'])
    .withMessage('Invalid status filter'),
  query('type')
    .optional()
    .isIn(['basic', 'premium', 'enterprise', 'custom'])
    .withMessage('Invalid service type filter')
]

// Validation for client analytics query
const getClientAnalyticsValidation = [
  param('id').isUUID().withMessage('Invalid client ID format'),
  query('period')
    .optional()
    .isIn(['7d', '30d', '90d', '1y'])
    .withMessage('Invalid period. Must be one of: 7d, 30d, 90d, 1y')
]

// Validation for client profitability query
const getClientProfitabilityValidation = [
  param('id').isUUID().withMessage('Invalid client ID format'),
  query('period')
    .optional()
    .isIn(['7d', '30d', '90d', '1y'])
    .withMessage('Invalid period. Must be one of: 7d, 30d, 90d, 1y')
]

module.exports = {
  createClientValidation,
  updateClientValidation,
  clientIdValidation,
  getClientsValidation,
  getClientServicesValidation,
  getClientAnalyticsValidation,
  getClientProfitabilityValidation
}
