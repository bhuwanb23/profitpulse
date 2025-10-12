const { body, param, query } = require('express-validator')

// Validation for bulk operations
const bulkOperationsValidation = [
  body('operation')
    .isIn(['create', 'update', 'delete', 'assign', 'status_change'])
    .withMessage('Invalid operation. Must be one of: create, update, delete, assign, status_change'),
  body('tickets')
    .isArray({ min: 1 })
    .withMessage('Tickets must be a non-empty array'),
  body('tickets.*.title')
    .if(body('operation').equals('create'))
    .notEmpty()
    .withMessage('Title is required for ticket creation'),
  body('tickets.*.description')
    .if(body('operation').equals('create'))
    .notEmpty()
    .withMessage('Description is required for ticket creation'),
  body('tickets.*.client_id')
    .if(body('operation').equals('create'))
    .isUUID()
    .withMessage('Valid client ID is required for ticket creation'),
  body('tickets.*.organization_id')
    .if(body('operation').equals('create'))
    .isUUID()
    .withMessage('Valid organization ID is required for ticket creation'),
  body('tickets.*.id')
    .if(body('operation').isIn(['update', 'delete']))
    .isUUID()
    .withMessage('Valid ticket ID is required for update/delete operations'),
  body('tickets.*.ticket_id')
    .if(body('operation').isIn(['assign', 'status_change']))
    .isUUID()
    .withMessage('Valid ticket ID is required for assign/status_change operations'),
  body('tickets.*.assigned_to')
    .if(body('operation').equals('assign'))
    .isUUID()
    .withMessage('Valid assigned user ID is required for assignment'),
  body('tickets.*.status')
    .if(body('operation').equals('status_change'))
    .isIn(['open', 'in_progress', 'pending', 'resolved', 'closed', 'cancelled'])
    .withMessage('Invalid status for status change operation')
]

// Validation for ticket templates
const getTemplatesValidation = [
  query('organization_id')
    .optional()
    .isUUID()
    .withMessage('Invalid organization ID format'),
  query('category')
    .optional()
    .isLength({ min: 2, max: 50 })
    .withMessage('Category must be between 2 and 50 characters'),
  query('search')
    .optional()
    .isLength({ min: 1, max: 100 })
    .withMessage('Search term must be between 1 and 100 characters')
]

// Validation for creating ticket template
const createTemplateValidation = [
  body('name')
    .notEmpty()
    .withMessage('Template name is required')
    .isLength({ min: 3, max: 100 })
    .withMessage('Template name must be between 3 and 100 characters'),
  body('category')
    .notEmpty()
    .withMessage('Category is required')
    .isLength({ min: 2, max: 50 })
    .withMessage('Category must be between 2 and 50 characters'),
  body('description')
    .optional()
    .isLength({ min: 5, max: 500 })
    .withMessage('Description must be between 5 and 500 characters'),
  body('priority')
    .optional()
    .isIn(['low', 'medium', 'high', 'urgent', 'critical'])
    .withMessage('Invalid priority. Must be one of: low, medium, high, urgent, critical'),
  body('estimated_hours')
    .optional()
    .isFloat({ min: 0.1, max: 1000 })
    .withMessage('Estimated hours must be between 0.1 and 1000'),
  body('template_fields')
    .isObject()
    .withMessage('Template fields must be an object'),
  body('organization_id')
    .optional()
    .isUUID()
    .withMessage('Invalid organization ID format')
]

// Validation for ticket escalation
const escalateTicketValidation = [
  param('id').isUUID().withMessage('Invalid ticket ID format'),
  body('escalation_reason')
    .notEmpty()
    .withMessage('Escalation reason is required')
    .isLength({ min: 10, max: 500 })
    .withMessage('Escalation reason must be between 10 and 500 characters'),
  body('escalated_to')
    .optional()
    .isUUID()
    .withMessage('Invalid escalated to user ID format'),
  body('priority_increase')
    .optional()
    .isBoolean()
    .withMessage('Priority increase must be a boolean'),
  body('notify_stakeholders')
    .optional()
    .isBoolean()
    .withMessage('Notify stakeholders must be a boolean')
]

// Validation for routing rules
const getRoutingRulesValidation = [
  query('organization_id')
    .optional()
    .isUUID()
    .withMessage('Invalid organization ID format')
]

// Validation for SLA monitoring
const getSLAMonitoringValidation = [
  query('organization_id')
    .optional()
    .isUUID()
    .withMessage('Invalid organization ID format'),
  query('period')
    .optional()
    .isIn(['1h', '6h', '24h', '7d'])
    .withMessage('Invalid period. Must be one of: 1h, 6h, 24h, 7d')
]

module.exports = {
  bulkOperationsValidation,
  getTemplatesValidation,
  createTemplateValidation,
  escalateTicketValidation,
  getRoutingRulesValidation,
  getSLAMonitoringValidation
}
