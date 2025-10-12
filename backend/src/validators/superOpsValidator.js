const { body, query } = require('express-validator')

// Validation for connect SuperOps
const connectSuperOpsValidation = [
  body('organization_id')
    .isUUID()
    .withMessage('Invalid organization ID format'),
  body('api_key')
    .isString()
    .isLength({ min: 10, max: 100 })
    .withMessage('API key must be between 10 and 100 characters'),
  body('api_secret')
    .isString()
    .isLength({ min: 10, max: 100 })
    .withMessage('API secret must be between 10 and 100 characters'),
  body('base_url')
    .isURL()
    .withMessage('Base URL must be a valid URL'),
  body('webhook_url')
    .optional()
    .isURL()
    .withMessage('Webhook URL must be a valid URL'),
  body('sync_settings')
    .optional()
    .isObject()
    .withMessage('Sync settings must be an object'),
  body('sync_settings.auto_sync')
    .optional()
    .isBoolean()
    .withMessage('Auto sync must be a boolean'),
  body('sync_settings.sync_interval')
    .optional()
    .isInt({ min: 300, max: 86400 })
    .withMessage('Sync interval must be between 300 and 86400 seconds'),
  body('sync_settings.sync_tickets')
    .optional()
    .isBoolean()
    .withMessage('Sync tickets must be a boolean'),
  body('sync_settings.sync_clients')
    .optional()
    .isBoolean()
    .withMessage('Sync clients must be a boolean'),
  body('sync_settings.sync_services')
    .optional()
    .isBoolean()
    .withMessage('Sync services must be a boolean'),
  body('sync_settings.sync_users')
    .optional()
    .isBoolean()
    .withMessage('Sync users must be a boolean')
]

// Validation for get SuperOps status
const getSuperOpsStatusValidation = [
  query('organization_id')
    .optional()
    .isUUID()
    .withMessage('Invalid organization ID format'),
  query('connection_id')
    .optional()
    .isUUID()
    .withMessage('Invalid connection ID format')
]

// Validation for sync SuperOps data
const syncSuperOpsDataValidation = [
  body('organization_id')
    .optional()
    .isUUID()
    .withMessage('Invalid organization ID format'),
  body('connection_id')
    .optional()
    .isUUID()
    .withMessage('Invalid connection ID format'),
  body('sync_type')
    .optional()
    .isIn(['all', 'tickets', 'clients', 'services', 'users'])
    .withMessage('Sync type must be one of: all, tickets, clients, services, users'),
  body('force_sync')
    .optional()
    .isBoolean()
    .withMessage('Force sync must be a boolean')
]

// Validation for get SuperOps tickets
const getSuperOpsTicketsValidation = [
  query('organization_id')
    .optional()
    .isUUID()
    .withMessage('Invalid organization ID format'),
  query('connection_id')
    .optional()
    .isUUID()
    .withMessage('Invalid connection ID format'),
  query('status')
    .optional()
    .isIn(['open', 'in_progress', 'resolved', 'closed'])
    .withMessage('Status must be one of: open, in_progress, resolved, closed'),
  query('priority')
    .optional()
    .isIn(['low', 'medium', 'high', 'critical'])
    .withMessage('Priority must be one of: low, medium, high, critical'),
  query('assigned_to')
    .optional()
    .isString()
    .isLength({ min: 1, max: 100 })
    .withMessage('Assigned to must be between 1 and 100 characters'),
  query('created_after')
    .optional()
    .isISO8601()
    .withMessage('Created after must be a valid ISO 8601 date'),
  query('created_before')
    .optional()
    .isISO8601()
    .withMessage('Created before must be a valid ISO 8601 date'),
  query('limit')
    .optional()
    .isInt({ min: 1, max: 100 })
    .withMessage('Limit must be between 1 and 100'),
  query('offset')
    .optional()
    .isInt({ min: 0 })
    .withMessage('Offset must be a non-negative integer')
]

// Validation for get SuperOps clients
const getSuperOpsClientsValidation = [
  query('organization_id')
    .optional()
    .isUUID()
    .withMessage('Invalid organization ID format'),
  query('connection_id')
    .optional()
    .isUUID()
    .withMessage('Invalid connection ID format'),
  query('status')
    .optional()
    .isIn(['active', 'inactive', 'suspended'])
    .withMessage('Status must be one of: active, inactive, suspended'),
  query('created_after')
    .optional()
    .isISO8601()
    .withMessage('Created after must be a valid ISO 8601 date'),
  query('created_before')
    .optional()
    .isISO8601()
    .withMessage('Created before must be a valid ISO 8601 date'),
  query('limit')
    .optional()
    .isInt({ min: 1, max: 100 })
    .withMessage('Limit must be between 1 and 100'),
  query('offset')
    .optional()
    .isInt({ min: 0 })
    .withMessage('Offset must be a non-negative integer')
]

// Validation for update SuperOps settings
const updateSuperOpsSettingsValidation = [
  body('organization_id')
    .optional()
    .isUUID()
    .withMessage('Invalid organization ID format'),
  body('connection_id')
    .optional()
    .isUUID()
    .withMessage('Invalid connection ID format'),
  body('sync_settings')
    .optional()
    .isObject()
    .withMessage('Sync settings must be an object'),
  body('sync_settings.auto_sync')
    .optional()
    .isBoolean()
    .withMessage('Auto sync must be a boolean'),
  body('sync_settings.sync_interval')
    .optional()
    .isInt({ min: 300, max: 86400 })
    .withMessage('Sync interval must be between 300 and 86400 seconds'),
  body('sync_settings.sync_tickets')
    .optional()
    .isBoolean()
    .withMessage('Sync tickets must be a boolean'),
  body('sync_settings.sync_clients')
    .optional()
    .isBoolean()
    .withMessage('Sync clients must be a boolean'),
  body('sync_settings.sync_services')
    .optional()
    .isBoolean()
    .withMessage('Sync services must be a boolean'),
  body('sync_settings.sync_users')
    .optional()
    .isBoolean()
    .withMessage('Sync users must be a boolean'),
  body('webhook_settings')
    .optional()
    .isObject()
    .withMessage('Webhook settings must be an object'),
  body('webhook_settings.webhook_url')
    .optional()
    .isURL()
    .withMessage('Webhook URL must be a valid URL'),
  body('webhook_settings.webhook_secret')
    .optional()
    .isString()
    .isLength({ min: 10, max: 100 })
    .withMessage('Webhook secret must be between 10 and 100 characters'),
  body('field_mappings')
    .optional()
    .isObject()
    .withMessage('Field mappings must be an object'),
  body('sync_filters')
    .optional()
    .isObject()
    .withMessage('Sync filters must be an object')
]

module.exports = {
  connectSuperOpsValidation,
  getSuperOpsStatusValidation,
  syncSuperOpsDataValidation,
  getSuperOpsTicketsValidation,
  getSuperOpsClientsValidation,
  updateSuperOpsSettingsValidation
}
