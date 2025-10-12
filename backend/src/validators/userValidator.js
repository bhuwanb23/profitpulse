const { body, param, query } = require('express-validator')

// Validation for updating user profile
const updateUserValidation = [
  param('id').isUUID().withMessage('Invalid user ID format'),
  body('first_name')
    .optional()
    .isLength({ min: 2, max: 50 })
    .withMessage('First name must be between 2 and 50 characters')
    .matches(/^[a-zA-Z\s]+$/)
    .withMessage('First name can only contain letters and spaces'),
  body('last_name')
    .optional()
    .isLength({ min: 2, max: 50 })
    .withMessage('Last name must be between 2 and 50 characters')
    .matches(/^[a-zA-Z\s]+$/)
    .withMessage('Last name can only contain letters and spaces'),
  body('email')
    .optional()
    .isEmail()
    .withMessage('Invalid email format')
    .normalizeEmail(),
  body('role')
    .optional()
    .isIn(['user', 'admin', 'finance', 'ops'])
    .withMessage('Invalid role. Must be one of: user, admin, finance, ops'),
  body('is_active')
    .optional()
    .isBoolean()
    .withMessage('is_active must be a boolean value'),
  body('organization_id')
    .optional()
    .isUUID()
    .withMessage('Invalid organization ID format')
]

// Validation for changing password
const changePasswordValidation = [
  param('id').isUUID().withMessage('Invalid user ID format'),
  body('currentPassword')
    .notEmpty()
    .withMessage('Current password is required'),
  body('newPassword')
    .isLength({ min: 8 })
    .withMessage('New password must be at least 8 characters long')
    .matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/)
    .withMessage('New password must contain at least one uppercase letter, one lowercase letter, one number, and one special character')
]

// Validation for user ID parameter
const userIdValidation = [
  param('id').isUUID().withMessage('Invalid user ID format')
]

// Validation for query parameters
const getUsersValidation = [
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
  query('role')
    .optional()
    .isIn(['user', 'admin', 'finance', 'ops'])
    .withMessage('Invalid role filter'),
  query('isActive')
    .optional()
    .isIn(['true', 'false'])
    .withMessage('isActive must be true or false')
]

module.exports = {
  updateUserValidation,
  changePasswordValidation,
  userIdValidation,
  getUsersValidation
}
