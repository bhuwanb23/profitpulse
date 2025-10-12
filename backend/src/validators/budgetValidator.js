const { body, param, query } = require('express-validator')

// Validation for getting budgets
const getBudgetsValidation = [
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
  query('budget_type')
    .optional()
    .isIn(['monthly', 'quarterly', 'annual', 'project'])
    .withMessage('Invalid budget type. Must be one of: monthly, quarterly, annual, project'),
  query('organization_id')
    .optional()
    .isUUID()
    .withMessage('Invalid organization ID format'),
  query('is_active')
    .optional()
    .isBoolean()
    .withMessage('is_active must be a boolean'),
  query('start_date')
    .optional()
    .isISO8601()
    .withMessage('Invalid start date format'),
  query('end_date')
    .optional()
    .isISO8601()
    .withMessage('Invalid end date format'),
  query('sort_by')
    .optional()
    .isIn(['created_at', 'updated_at', 'name', 'total_amount', 'start_date', 'end_date'])
    .withMessage('Invalid sort field'),
  query('sort_order')
    .optional()
    .isIn(['ASC', 'DESC'])
    .withMessage('Sort order must be ASC or DESC')
]

// Validation for creating budget
const createBudgetValidation = [
  body('organization_id')
    .isUUID()
    .withMessage('Valid organization ID is required'),
  body('name')
    .notEmpty()
    .withMessage('Budget name is required')
    .isLength({ min: 2, max: 255 })
    .withMessage('Budget name must be between 2 and 255 characters'),
  body('description')
    .optional()
    .isLength({ max: 1000 })
    .withMessage('Description must not exceed 1000 characters'),
  body('budget_type')
    .optional()
    .isIn(['monthly', 'quarterly', 'annual', 'project'])
    .withMessage('Invalid budget type. Must be one of: monthly, quarterly, annual, project'),
  body('total_amount')
    .isFloat({ min: 0.01 })
    .withMessage('Total amount must be greater than 0'),
  body('start_date')
    .isISO8601()
    .withMessage('Valid start date is required'),
  body('end_date')
    .isISO8601()
    .withMessage('Valid end date is required'),
  body('categories')
    .optional()
    .isArray()
    .withMessage('Categories must be an array'),
  body('categories.*.name')
    .if(body('categories').isArray())
    .notEmpty()
    .withMessage('Category name is required'),
  body('categories.*.amount')
    .if(body('categories').isArray())
    .isFloat({ min: 0.01 })
    .withMessage('Category amount must be greater than 0'),
  body('alert_thresholds')
    .optional()
    .isObject()
    .withMessage('Alert thresholds must be an object'),
  body('created_by')
    .optional()
    .isUUID()
    .withMessage('Invalid created by user ID format'),
  body('notes')
    .optional()
    .isLength({ max: 1000 })
    .withMessage('Notes must not exceed 1000 characters')
]

// Validation for getting budget by ID
const getBudgetByIdValidation = [
  param('id').isUUID().withMessage('Invalid budget ID format')
]

// Validation for updating budget
const updateBudgetValidation = [
  param('id').isUUID().withMessage('Invalid budget ID format'),
  body('name')
    .optional()
    .isLength({ min: 2, max: 255 })
    .withMessage('Budget name must be between 2 and 255 characters'),
  body('description')
    .optional()
    .isLength({ max: 1000 })
    .withMessage('Description must not exceed 1000 characters'),
  body('budget_type')
    .optional()
    .isIn(['monthly', 'quarterly', 'annual', 'project'])
    .withMessage('Invalid budget type. Must be one of: monthly, quarterly, annual, project'),
  body('total_amount')
    .optional()
    .isFloat({ min: 0.01 })
    .withMessage('Total amount must be greater than 0'),
  body('start_date')
    .optional()
    .isISO8601()
    .withMessage('Invalid start date format'),
  body('end_date')
    .optional()
    .isISO8601()
    .withMessage('Invalid end date format'),
  body('categories')
    .optional()
    .isArray()
    .withMessage('Categories must be an array'),
  body('alert_thresholds')
    .optional()
    .isObject()
    .withMessage('Alert thresholds must be an object'),
  body('is_active')
    .optional()
    .isBoolean()
    .withMessage('is_active must be a boolean'),
  body('notes')
    .optional()
    .isLength({ max: 1000 })
    .withMessage('Notes must not exceed 1000 characters')
]

// Validation for deleting budget
const deleteBudgetValidation = [
  param('id').isUUID().withMessage('Invalid budget ID format')
]

// Validation for getting budget categories
const getBudgetCategoriesValidation = [
  param('id').isUUID().withMessage('Invalid budget ID format')
]

// Validation for adding budget category
const addBudgetCategoryValidation = [
  param('id').isUUID().withMessage('Invalid budget ID format'),
  body('name')
    .notEmpty()
    .withMessage('Category name is required')
    .isLength({ min: 2, max: 100 })
    .withMessage('Category name must be between 2 and 100 characters'),
  body('amount')
    .isFloat({ min: 0.01 })
    .withMessage('Category amount must be greater than 0'),
  body('description')
    .optional()
    .isLength({ max: 500 })
    .withMessage('Description must not exceed 500 characters')
]

// Validation for getting budget expenses
const getBudgetExpensesValidation = [
  param('id').isUUID().withMessage('Invalid budget ID format'),
  query('page')
    .optional()
    .isInt({ min: 1 })
    .withMessage('Page must be a positive integer'),
  query('limit')
    .optional()
    .isInt({ min: 1, max: 100 })
    .withMessage('Limit must be between 1 and 100'),
  query('category')
    .optional()
    .isLength({ min: 1, max: 100 })
    .withMessage('Category must be between 1 and 100 characters'),
  query('start_date')
    .optional()
    .isISO8601()
    .withMessage('Invalid start date format'),
  query('end_date')
    .optional()
    .isISO8601()
    .withMessage('Invalid end date format'),
  query('sort_by')
    .optional()
    .isIn(['expense_date', 'amount', 'category', 'created_at'])
    .withMessage('Invalid sort field'),
  query('sort_order')
    .optional()
    .isIn(['ASC', 'DESC'])
    .withMessage('Sort order must be ASC or DESC')
]

// Validation for getting budget alerts
const getBudgetAlertsValidation = [
  param('id').isUUID().withMessage('Invalid budget ID format')
]

module.exports = {
  getBudgetsValidation,
  createBudgetValidation,
  getBudgetByIdValidation,
  updateBudgetValidation,
  deleteBudgetValidation,
  getBudgetCategoriesValidation,
  addBudgetCategoryValidation,
  getBudgetExpensesValidation,
  getBudgetAlertsValidation
}
