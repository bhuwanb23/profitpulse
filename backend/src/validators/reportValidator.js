const { body, query, param } = require('express-validator')

// Validation for get report templates
const getReportTemplatesValidation = [
  query('organization_id')
    .optional()
    .isUUID()
    .withMessage('Invalid organization ID format'),
  query('category')
    .optional()
    .isIn(['financial', 'operational', 'analytical', 'custom'])
    .withMessage('Category must be one of: financial, operational, analytical, custom'),
  query('report_type')
    .optional()
    .isIn(['financial', 'operational', 'analytical', 'custom'])
    .withMessage('Report type must be one of: financial, operational, analytical, custom'),
  query('is_global')
    .optional()
    .isBoolean()
    .withMessage('Is global must be a boolean'),
  query('is_active')
    .optional()
    .isBoolean()
    .withMessage('Is active must be a boolean'),
  query('limit')
    .optional()
    .isInt({ min: 1, max: 100 })
    .withMessage('Limit must be between 1 and 100'),
  query('offset')
    .optional()
    .isInt({ min: 0 })
    .withMessage('Offset must be a non-negative integer')
]

// Validation for generate report
const generateReportValidation = [
  body('organization_id')
    .isUUID()
    .withMessage('Invalid organization ID format'),
  body('template_id')
    .optional()
    .isUUID()
    .withMessage('Invalid template ID format'),
  body('title')
    .isString()
    .isLength({ min: 1, max: 255 })
    .withMessage('Title must be between 1 and 255 characters'),
  body('description')
    .optional()
    .isString()
    .isLength({ max: 1000 })
    .withMessage('Description must be at most 1000 characters'),
  body('report_type')
    .isIn(['financial', 'operational', 'analytical', 'custom'])
    .withMessage('Report type must be one of: financial, operational, analytical, custom'),
  body('parameters')
    .optional()
    .isObject()
    .withMessage('Parameters must be an object'),
  body('filters')
    .optional()
    .isObject()
    .withMessage('Filters must be an object'),
  body('format')
    .optional()
    .isIn(['json', 'pdf', 'excel', 'csv'])
    .withMessage('Format must be one of: json, pdf, excel, csv')
]

// Validation for get report
const getReportValidation = [
  param('id')
    .isUUID()
    .withMessage('Invalid report ID format'),
  query('include_data')
    .optional()
    .isBoolean()
    .withMessage('Include data must be a boolean')
]

// Validation for export report
const exportReportValidation = [
  param('id')
    .isUUID()
    .withMessage('Invalid report ID format'),
  body('format')
    .optional()
    .isIn(['pdf', 'excel', 'csv'])
    .withMessage('Format must be one of: pdf, excel, csv'),
  body('email_to')
    .optional()
    .isArray()
    .withMessage('Email to must be an array'),
  body('email_to.*')
    .optional()
    .isEmail()
    .withMessage('Email must be valid')
]

// Validation for schedule report
const scheduleReportValidation = [
  body('organization_id')
    .isUUID()
    .withMessage('Invalid organization ID format'),
  body('report_id')
    .optional()
    .isUUID()
    .withMessage('Invalid report ID format'),
  body('template_id')
    .optional()
    .isUUID()
    .withMessage('Invalid template ID format'),
  body('title')
    .isString()
    .isLength({ min: 1, max: 255 })
    .withMessage('Title must be between 1 and 255 characters'),
  body('description')
    .optional()
    .isString()
    .isLength({ max: 1000 })
    .withMessage('Description must be at most 1000 characters'),
  body('schedule_type')
    .isIn(['once', 'daily', 'weekly', 'monthly'])
    .withMessage('Schedule type must be one of: once, daily, weekly, monthly'),
  body('schedule_config')
    .optional()
    .isObject()
    .withMessage('Schedule config must be an object'),
  body('next_run')
    .isISO8601()
    .withMessage('Next run must be a valid ISO 8601 date'),
  body('parameters')
    .optional()
    .isObject()
    .withMessage('Parameters must be an object'),
  body('filters')
    .optional()
    .isObject()
    .withMessage('Filters must be an object'),
  body('format')
    .optional()
    .isIn(['json', 'pdf', 'excel', 'csv'])
    .withMessage('Format must be one of: json, pdf, excel, csv'),
  body('email_recipients')
    .optional()
    .isArray()
    .withMessage('Email recipients must be an array'),
  body('email_recipients.*')
    .optional()
    .isEmail()
    .withMessage('Email must be valid'),
  body('email_subject')
    .optional()
    .isString()
    .isLength({ max: 255 })
    .withMessage('Email subject must be at most 255 characters'),
  body('email_body')
    .optional()
    .isString()
    .isLength({ max: 2000 })
    .withMessage('Email body must be at most 2000 characters')
]

// Validation for get scheduled reports
const getScheduledReportsValidation = [
  query('organization_id')
    .optional()
    .isUUID()
    .withMessage('Invalid organization ID format'),
  query('status')
    .optional()
    .isIn(['active', 'paused', 'completed', 'failed'])
    .withMessage('Status must be one of: active, paused, completed, failed'),
  query('schedule_type')
    .optional()
    .isIn(['once', 'daily', 'weekly', 'monthly'])
    .withMessage('Schedule type must be one of: once, daily, weekly, monthly'),
  query('limit')
    .optional()
    .isInt({ min: 1, max: 100 })
    .withMessage('Limit must be between 1 and 100'),
  query('offset')
    .optional()
    .isInt({ min: 0 })
    .withMessage('Offset must be a non-negative integer')
]

// Validation for cancel scheduled report
const cancelScheduledReportValidation = [
  param('id')
    .isUUID()
    .withMessage('Invalid scheduled report ID format')
]

module.exports = {
  getReportTemplatesValidation,
  generateReportValidation,
  getReportValidation,
  exportReportValidation,
  scheduleReportValidation,
  getScheduledReportsValidation,
  cancelScheduledReportValidation
}
