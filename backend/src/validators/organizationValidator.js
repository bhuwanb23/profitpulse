const { body, param, query } = require('express-validator')

// Validation for creating organization
const createOrganizationValidation = [
  body('name')
    .notEmpty()
    .withMessage('Organization name is required')
    .isLength({ min: 2, max: 100 })
    .withMessage('Organization name must be between 2 and 100 characters')
    .matches(/^[a-zA-Z0-9\s\-&.,()]+$/)
    .withMessage('Organization name can only contain letters, numbers, spaces, and basic punctuation'),
  body('domain')
    .optional()
    .isLength({ min: 3, max: 100 })
    .withMessage('Domain must be between 3 and 100 characters')
    .matches(/^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/)
    .withMessage('Invalid domain format'),
  body('subscription_plan')
    .optional()
    .isIn(['basic', 'professional', 'enterprise', 'custom'])
    .withMessage('Invalid subscription plan. Must be one of: basic, professional, enterprise, custom'),
  body('is_active')
    .optional()
    .isBoolean()
    .withMessage('is_active must be a boolean value')
]

// Validation for updating organization
const updateOrganizationValidation = [
  param('id').isUUID().withMessage('Invalid organization ID format'),
  body('name')
    .optional()
    .isLength({ min: 2, max: 100 })
    .withMessage('Organization name must be between 2 and 100 characters')
    .matches(/^[a-zA-Z0-9\s\-&.,()]+$/)
    .withMessage('Organization name can only contain letters, numbers, spaces, and basic punctuation'),
  body('domain')
    .optional()
    .isLength({ min: 3, max: 100 })
    .withMessage('Domain must be between 3 and 100 characters')
    .matches(/^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/)
    .withMessage('Invalid domain format'),
  body('subscription_plan')
    .optional()
    .isIn(['basic', 'professional', 'enterprise', 'custom'])
    .withMessage('Invalid subscription plan. Must be one of: basic, professional, enterprise, custom'),
  body('is_active')
    .optional()
    .isBoolean()
    .withMessage('is_active must be a boolean value')
]

// Validation for organization ID parameter
const organizationIdValidation = [
  param('id').isUUID().withMessage('Invalid organization ID format')
]

// Validation for query parameters
const getOrganizationsValidation = [
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
  query('subscription_plan')
    .optional()
    .isIn(['basic', 'professional', 'enterprise', 'custom'])
    .withMessage('Invalid subscription plan filter'),
  query('is_active')
    .optional()
    .isIn(['true', 'false'])
    .withMessage('is_active must be true or false')
]

// Validation for adding organization member
const addMemberValidation = [
  param('id').isUUID().withMessage('Invalid organization ID format'),
  body('user_id')
    .isUUID()
    .withMessage('Invalid user ID format'),
  body('role')
    .optional()
    .isIn(['user', 'admin', 'finance', 'ops'])
    .withMessage('Invalid role. Must be one of: user, admin, finance, ops')
]

// Validation for removing organization member
const removeMemberValidation = [
  param('id').isUUID().withMessage('Invalid organization ID format'),
  param('userId').isUUID().withMessage('Invalid user ID format')
]

module.exports = {
  createOrganizationValidation,
  updateOrganizationValidation,
  organizationIdValidation,
  getOrganizationsValidation,
  addMemberValidation,
  removeMemberValidation
}
