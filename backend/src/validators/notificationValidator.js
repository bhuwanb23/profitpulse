const { body, query, param } = require('express-validator')

// Validation for get notifications
const getNotificationsValidation = [
  query('organization_id')
    .optional()
    .isUUID()
    .withMessage('Invalid organization ID format'),
  query('user_id')
    .optional()
    .isUUID()
    .withMessage('Invalid user ID format'),
  query('type')
    .optional()
    .isIn(['info', 'warning', 'error', 'success', 'alert'])
    .withMessage('Type must be one of: info, warning, error, success, alert'),
  query('category')
    .optional()
    .isIn(['system', 'ticket', 'invoice', 'budget', 'report', 'ai', 'integration'])
    .withMessage('Category must be one of: system, ticket, invoice, budget, report, ai, integration'),
  query('is_read')
    .optional()
    .isBoolean()
    .withMessage('Is read must be a boolean'),
  query('priority')
    .optional()
    .isIn(['low', 'medium', 'high', 'urgent'])
    .withMessage('Priority must be one of: low, medium, high, urgent'),
  query('limit')
    .optional()
    .isInt({ min: 1, max: 100 })
    .withMessage('Limit must be between 1 and 100'),
  query('offset')
    .optional()
    .isInt({ min: 0 })
    .withMessage('Offset must be a non-negative integer')
]

// Validation for mark notification as read
const markNotificationAsReadValidation = [
  param('id')
    .isUUID()
    .withMessage('Invalid notification ID format')
]

// Validation for update notification preferences
const updateNotificationPreferencesValidation = [
  body('organization_id')
    .isUUID()
    .withMessage('Invalid organization ID format'),
  body('user_id')
    .optional()
    .isUUID()
    .withMessage('Invalid user ID format'),
  body('preferences')
    .isArray()
    .withMessage('Preferences must be an array'),
  body('preferences.*.category')
    .isIn(['system', 'ticket', 'invoice', 'budget', 'report', 'ai', 'integration'])
    .withMessage('Category must be one of: system, ticket, invoice, budget, report, ai, integration'),
  body('preferences.*.type')
    .isIn(['info', 'warning', 'error', 'success', 'alert'])
    .withMessage('Type must be one of: info, warning, error, success, alert'),
  body('preferences.*.enabled')
    .isBoolean()
    .withMessage('Enabled must be a boolean'),
  body('preferences.*.email_enabled')
    .isBoolean()
    .withMessage('Email enabled must be a boolean'),
  body('preferences.*.push_enabled')
    .isBoolean()
    .withMessage('Push enabled must be a boolean'),
  body('preferences.*.sms_enabled')
    .isBoolean()
    .withMessage('SMS enabled must be a boolean'),
  body('preferences.*.webhook_enabled')
    .isBoolean()
    .withMessage('Webhook enabled must be a boolean'),
  body('preferences.*.webhook_url')
    .optional()
    .isURL()
    .withMessage('Webhook URL must be a valid URL'),
  body('preferences.*.frequency')
    .isIn(['immediate', 'hourly', 'daily', 'weekly'])
    .withMessage('Frequency must be one of: immediate, hourly, daily, weekly'),
  body('preferences.*.quiet_hours_start')
    .optional()
    .matches(/^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$/)
    .withMessage('Quiet hours start must be in HH:MM format'),
  body('preferences.*.quiet_hours_end')
    .optional()
    .matches(/^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$/)
    .withMessage('Quiet hours end must be in HH:MM format'),
  body('preferences.*.timezone')
    .optional()
    .isString()
    .isLength({ min: 1, max: 50 })
    .withMessage('Timezone must be between 1 and 50 characters')
]

// Validation for get email settings
const getEmailSettingsValidation = [
  query('organization_id')
    .optional()
    .isUUID()
    .withMessage('Invalid organization ID format')
]

// Validation for update email settings
const updateEmailSettingsValidation = [
  body('organization_id')
    .isUUID()
    .withMessage('Invalid organization ID format'),
  body('smtp_host')
    .optional()
    .isString()
    .isLength({ min: 1, max: 255 })
    .withMessage('SMTP host must be between 1 and 255 characters'),
  body('smtp_port')
    .optional()
    .isInt({ min: 1, max: 65535 })
    .withMessage('SMTP port must be between 1 and 65535'),
  body('smtp_secure')
    .optional()
    .isBoolean()
    .withMessage('SMTP secure must be a boolean'),
  body('smtp_username')
    .optional()
    .isString()
    .isLength({ min: 1, max: 255 })
    .withMessage('SMTP username must be between 1 and 255 characters'),
  body('smtp_password')
    .optional()
    .isString()
    .isLength({ min: 1, max: 255 })
    .withMessage('SMTP password must be between 1 and 255 characters'),
  body('from_email')
    .isEmail()
    .withMessage('From email must be a valid email address'),
  body('from_name')
    .isString()
    .isLength({ min: 1, max: 255 })
    .withMessage('From name must be between 1 and 255 characters'),
  body('reply_to_email')
    .optional()
    .isEmail()
    .withMessage('Reply to email must be a valid email address'),
  body('reply_to_name')
    .optional()
    .isString()
    .isLength({ min: 1, max: 255 })
    .withMessage('Reply to name must be between 1 and 255 characters'),
  body('is_active')
    .optional()
    .isBoolean()
    .withMessage('Is active must be a boolean'),
  body('daily_limit')
    .optional()
    .isInt({ min: 1, max: 10000 })
    .withMessage('Daily limit must be between 1 and 10000'),
  body('hourly_limit')
    .optional()
    .isInt({ min: 1, max: 1000 })
    .withMessage('Hourly limit must be between 1 and 1000'),
  body('template_settings')
    .optional()
    .isObject()
    .withMessage('Template settings must be an object')
]

// Validation for get dashboard alerts
const getDashboardAlertsValidation = [
  query('organization_id')
    .optional()
    .isUUID()
    .withMessage('Invalid organization ID format'),
  query('user_id')
    .optional()
    .isUUID()
    .withMessage('Invalid user ID format')
]

// Validation for test notification
const testNotificationValidation = [
  body('organization_id')
    .isUUID()
    .withMessage('Invalid organization ID format'),
  body('user_id')
    .optional()
    .isUUID()
    .withMessage('Invalid user ID format'),
  body('type')
    .optional()
    .isIn(['info', 'warning', 'error', 'success', 'alert'])
    .withMessage('Type must be one of: info, warning, error, success, alert'),
  body('category')
    .optional()
    .isIn(['system', 'ticket', 'invoice', 'budget', 'report', 'ai', 'integration'])
    .withMessage('Category must be one of: system, ticket, invoice, budget, report, ai, integration'),
  body('title')
    .optional()
    .isString()
    .isLength({ min: 1, max: 255 })
    .withMessage('Title must be between 1 and 255 characters'),
  body('message')
    .optional()
    .isString()
    .isLength({ min: 1, max: 1000 })
    .withMessage('Message must be between 1 and 1000 characters'),
  body('test_email')
    .optional()
    .isEmail()
    .withMessage('Test email must be a valid email address'),
  body('test_phone')
    .optional()
    .isString()
    .matches(/^\+?[1-9]\d{1,14}$/)
    .withMessage('Test phone must be a valid phone number')
]

module.exports = {
  getNotificationsValidation,
  markNotificationAsReadValidation,
  updateNotificationPreferencesValidation,
  getEmailSettingsValidation,
  updateEmailSettingsValidation,
  getDashboardAlertsValidation,
  testNotificationValidation
}
