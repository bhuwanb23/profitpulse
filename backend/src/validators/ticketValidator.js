const { body, param, query } = require('express-validator')

// Validation for creating ticket
const createTicketValidation = [
  body('title')
    .notEmpty()
    .withMessage('Ticket title is required')
    .isLength({ min: 5, max: 200 })
    .withMessage('Title must be between 5 and 200 characters'),
  body('description')
    .notEmpty()
    .withMessage('Ticket description is required')
    .isLength({ min: 10, max: 2000 })
    .withMessage('Description must be between 10 and 2000 characters'),
  body('priority')
    .optional()
    .isIn(['low', 'medium', 'high', 'urgent', 'critical'])
    .withMessage('Invalid priority. Must be one of: low, medium, high, urgent, critical'),
  body('category')
    .optional()
    .isLength({ min: 2, max: 50 })
    .withMessage('Category must be between 2 and 50 characters'),
  body('status')
    .optional()
    .isIn(['open', 'in_progress', 'pending', 'resolved', 'closed', 'cancelled'])
    .withMessage('Invalid status. Must be one of: open, in_progress, pending, resolved, closed, cancelled'),
  body('client_id')
    .isUUID()
    .withMessage('Invalid client ID format'),
  body('organization_id')
    .isUUID()
    .withMessage('Invalid organization ID format'),
  body('assigned_to')
    .optional()
    .isUUID()
    .withMessage('Invalid assigned user ID format'),
  body('due_date')
    .optional()
    .isISO8601()
    .withMessage('Due date must be a valid ISO 8601 date'),
  body('estimated_hours')
    .optional()
    .isFloat({ min: 0, max: 1000 })
    .withMessage('Estimated hours must be between 0 and 1000'),
  body('created_by')
    .optional()
    .isUUID()
    .withMessage('Invalid created by user ID format')
]

// Validation for updating ticket
const updateTicketValidation = [
  param('id').isUUID().withMessage('Invalid ticket ID format'),
  body('title')
    .optional()
    .isLength({ min: 5, max: 200 })
    .withMessage('Title must be between 5 and 200 characters'),
  body('description')
    .optional()
    .isLength({ min: 10, max: 2000 })
    .withMessage('Description must be between 10 and 2000 characters'),
  body('priority')
    .optional()
    .isIn(['low', 'medium', 'high', 'urgent', 'critical'])
    .withMessage('Invalid priority. Must be one of: low, medium, high, urgent, critical'),
  body('category')
    .optional()
    .isLength({ min: 2, max: 50 })
    .withMessage('Category must be between 2 and 50 characters'),
  body('status')
    .optional()
    .isIn(['open', 'in_progress', 'pending', 'resolved', 'closed', 'cancelled'])
    .withMessage('Invalid status. Must be one of: open, in_progress, pending, resolved, closed, cancelled'),
  body('client_id')
    .optional()
    .isUUID()
    .withMessage('Invalid client ID format'),
  body('assigned_to')
    .optional()
    .isUUID()
    .withMessage('Invalid assigned user ID format'),
  body('due_date')
    .optional()
    .isISO8601()
    .withMessage('Due date must be a valid ISO 8601 date'),
  body('estimated_hours')
    .optional()
    .isFloat({ min: 0, max: 1000 })
    .withMessage('Estimated hours must be between 0 and 1000'),
  body('resolution_notes')
    .optional()
    .isLength({ min: 5, max: 1000 })
    .withMessage('Resolution notes must be between 5 and 1000 characters')
]

// Validation for ticket ID parameter
const ticketIdValidation = [
  param('id').isUUID().withMessage('Invalid ticket ID format')
]

// Validation for query parameters
const getTicketsValidation = [
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
  query('status')
    .optional()
    .isIn(['open', 'in_progress', 'pending', 'resolved', 'closed', 'cancelled'])
    .withMessage('Invalid status filter'),
  query('priority')
    .optional()
    .isIn(['low', 'medium', 'high', 'urgent', 'critical'])
    .withMessage('Invalid priority filter'),
  query('category')
    .optional()
    .isLength({ min: 1, max: 50 })
    .withMessage('Category filter must be between 1 and 50 characters'),
  query('assigned_to')
    .optional()
    .isUUID()
    .withMessage('Invalid assigned user ID format'),
  query('client_id')
    .optional()
    .isUUID()
    .withMessage('Invalid client ID format'),
  query('organization_id')
    .optional()
    .isUUID()
    .withMessage('Invalid organization ID format'),
  query('created_from')
    .optional()
    .isISO8601()
    .withMessage('Created from date must be a valid ISO 8601 date'),
  query('created_to')
    .optional()
    .isISO8601()
    .withMessage('Created to date must be a valid ISO 8601 date'),
  query('sort_by')
    .optional()
    .isIn(['title', 'status', 'priority', 'category', 'created_at', 'updated_at', 'due_date'])
    .withMessage('Invalid sort field'),
  query('sort_order')
    .optional()
    .isIn(['ASC', 'DESC', 'asc', 'desc'])
    .withMessage('Sort order must be ASC or DESC')
]

// Validation for assigning ticket
const assignTicketValidation = [
  param('id').isUUID().withMessage('Invalid ticket ID format'),
  body('assigned_to')
    .isUUID()
    .withMessage('Invalid assigned user ID format')
]

// Validation for updating ticket status
const updateStatusValidation = [
  param('id').isUUID().withMessage('Invalid ticket ID format'),
  body('status')
    .isIn(['open', 'in_progress', 'pending', 'resolved', 'closed', 'cancelled'])
    .withMessage('Invalid status. Must be one of: open, in_progress, pending, resolved, closed, cancelled'),
  body('resolution_notes')
    .optional()
    .isLength({ min: 5, max: 1000 })
    .withMessage('Resolution notes must be between 5 and 1000 characters')
]

// Validation for logging time
const logTimeValidation = [
  param('id').isUUID().withMessage('Invalid ticket ID format'),
  body('hours_spent')
    .isFloat({ min: 0.1, max: 24 })
    .withMessage('Hours spent must be between 0.1 and 24'),
  body('description')
    .notEmpty()
    .withMessage('Time log description is required')
    .isLength({ min: 5, max: 500 })
    .withMessage('Description must be between 5 and 500 characters'),
  body('user_id')
    .optional()
    .isUUID()
    .withMessage('Invalid user ID format'),
  body('date_worked')
    .optional()
    .isISO8601()
    .withMessage('Date worked must be a valid ISO 8601 date')
]

module.exports = {
  createTicketValidation,
  updateTicketValidation,
  ticketIdValidation,
  getTicketsValidation,
  assignTicketValidation,
  updateStatusValidation,
  logTimeValidation
}
