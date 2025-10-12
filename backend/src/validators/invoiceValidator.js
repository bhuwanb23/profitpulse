const { body, param, query } = require('express-validator')

// Validation for getting invoices
const getInvoicesValidation = [
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
    .isIn(['draft', 'sent', 'paid', 'overdue'])
    .withMessage('Invalid status. Must be one of: draft, sent, paid, overdue'),
  query('client_id')
    .optional()
    .isUUID()
    .withMessage('Invalid client ID format'),
  query('organization_id')
    .optional()
    .isUUID()
    .withMessage('Invalid organization ID format'),
  query('date_from')
    .optional()
    .isISO8601()
    .withMessage('Invalid date format for date_from'),
  query('date_to')
    .optional()
    .isISO8601()
    .withMessage('Invalid date format for date_to'),
  query('amount_min')
    .optional()
    .isFloat({ min: 0 })
    .withMessage('Amount minimum must be a positive number'),
  query('amount_max')
    .optional()
    .isFloat({ min: 0 })
    .withMessage('Amount maximum must be a positive number'),
  query('sort_by')
    .optional()
    .isIn(['created_at', 'updated_at', 'invoice_date', 'due_date', 'total_amount', 'status'])
    .withMessage('Invalid sort field'),
  query('sort_order')
    .optional()
    .isIn(['ASC', 'DESC'])
    .withMessage('Sort order must be ASC or DESC')
]

// Validation for creating invoice
const createInvoiceValidation = [
  body('client_id')
    .isUUID()
    .withMessage('Valid client ID is required'),
  body('organization_id')
    .isUUID()
    .withMessage('Valid organization ID is required'),
  body('invoice_date')
    .optional()
    .isISO8601()
    .withMessage('Invalid invoice date format'),
  body('due_date')
    .optional()
    .isISO8601()
    .withMessage('Invalid due date format'),
  body('line_items')
    .optional()
    .isArray()
    .withMessage('Line items must be an array'),
  body('line_items.*.description')
    .if(body('line_items').isArray())
    .notEmpty()
    .withMessage('Line item description is required'),
  body('line_items.*.quantity')
    .if(body('line_items').isArray())
    .isFloat({ min: 0.01 })
    .withMessage('Line item quantity must be greater than 0'),
  body('line_items.*.unit_price')
    .if(body('line_items').isArray())
    .isFloat({ min: 0 })
    .withMessage('Line item unit price must be non-negative'),
  body('subtotal')
    .optional()
    .isFloat({ min: 0 })
    .withMessage('Subtotal must be non-negative'),
  body('tax_amount')
    .optional()
    .isFloat({ min: 0 })
    .withMessage('Tax amount must be non-negative'),
  body('total_amount')
    .optional()
    .isFloat({ min: 0 })
    .withMessage('Total amount must be non-negative'),
  body('notes')
    .optional()
    .isLength({ max: 1000 })
    .withMessage('Notes must not exceed 1000 characters'),
  body('terms')
    .optional()
    .isLength({ max: 1000 })
    .withMessage('Terms must not exceed 1000 characters'),
  body('created_by')
    .optional()
    .isUUID()
    .withMessage('Invalid created by user ID format')
]

// Validation for getting invoice by ID
const getInvoiceByIdValidation = [
  param('id').isUUID().withMessage('Invalid invoice ID format')
]

// Validation for updating invoice
const updateInvoiceValidation = [
  param('id').isUUID().withMessage('Invalid invoice ID format'),
  body('client_id')
    .optional()
    .isUUID()
    .withMessage('Invalid client ID format'),
  body('invoice_date')
    .optional()
    .isISO8601()
    .withMessage('Invalid invoice date format'),
  body('due_date')
    .optional()
    .isISO8601()
    .withMessage('Invalid due date format'),
  body('line_items')
    .optional()
    .isArray()
    .withMessage('Line items must be an array'),
  body('line_items.*.description')
    .if(body('line_items').isArray())
    .notEmpty()
    .withMessage('Line item description is required'),
  body('line_items.*.quantity')
    .if(body('line_items').isArray())
    .isFloat({ min: 0.01 })
    .withMessage('Line item quantity must be greater than 0'),
  body('line_items.*.unit_price')
    .if(body('line_items').isArray())
    .isFloat({ min: 0 })
    .withMessage('Line item unit price must be non-negative'),
  body('subtotal')
    .optional()
    .isFloat({ min: 0 })
    .withMessage('Subtotal must be non-negative'),
  body('tax_amount')
    .optional()
    .isFloat({ min: 0 })
    .withMessage('Tax amount must be non-negative'),
  body('total_amount')
    .optional()
    .isFloat({ min: 0 })
    .withMessage('Total amount must be non-negative'),
  body('status')
    .optional()
    .isIn(['draft', 'sent', 'paid', 'overdue'])
    .withMessage('Invalid status. Must be one of: draft, sent, paid, overdue'),
  body('notes')
    .optional()
    .isLength({ max: 1000 })
    .withMessage('Notes must not exceed 1000 characters'),
  body('terms')
    .optional()
    .isLength({ max: 1000 })
    .withMessage('Terms must not exceed 1000 characters')
]

// Validation for deleting invoice
const deleteInvoiceValidation = [
  param('id').isUUID().withMessage('Invalid invoice ID format')
]

// Validation for sending invoice
const sendInvoiceValidation = [
  param('id').isUUID().withMessage('Invalid invoice ID format'),
  body('email')
    .optional()
    .isEmail()
    .withMessage('Invalid email format'),
  body('subject')
    .optional()
    .isLength({ min: 1, max: 200 })
    .withMessage('Subject must be between 1 and 200 characters'),
  body('message')
    .optional()
    .isLength({ max: 1000 })
    .withMessage('Message must not exceed 1000 characters'),
  body('send_copy_to_self')
    .optional()
    .isBoolean()
    .withMessage('Send copy to self must be a boolean')
]

// Validation for recording payment
const recordPaymentValidation = [
  param('id').isUUID().withMessage('Invalid invoice ID format'),
  body('payment_date')
    .optional()
    .isISO8601()
    .withMessage('Invalid payment date format'),
  body('payment_method')
    .optional()
    .isIn(['cash', 'check', 'credit_card', 'bank_transfer', 'paypal', 'other'])
    .withMessage('Invalid payment method'),
  body('payment_reference')
    .optional()
    .isLength({ max: 100 })
    .withMessage('Payment reference must not exceed 100 characters'),
  body('amount')
    .optional()
    .isFloat({ min: 0.01 })
    .withMessage('Payment amount must be greater than 0'),
  body('notes')
    .optional()
    .isLength({ max: 500 })
    .withMessage('Payment notes must not exceed 500 characters')
]

// Validation for bulk operations
const bulkOperationsValidation = [
  body('operation')
    .isIn(['create', 'update', 'delete', 'send', 'payment'])
    .withMessage('Invalid operation. Must be one of: create, update, delete, send, payment'),
  body('invoices')
    .isArray({ min: 1 })
    .withMessage('Invoices must be a non-empty array'),
  body('invoices.*.client_id')
    .if(body('operation').equals('create'))
    .isUUID()
    .withMessage('Valid client ID is required for invoice creation'),
  body('invoices.*.organization_id')
    .if(body('operation').equals('create'))
    .isUUID()
    .withMessage('Valid organization ID is required for invoice creation'),
  body('invoices.*.id')
    .if(body('operation').isIn(['update', 'delete']))
    .isUUID()
    .withMessage('Valid invoice ID is required for update/delete operations'),
  body('invoices.*.invoice_id')
    .if(body('operation').isIn(['send', 'payment']))
    .isUUID()
    .withMessage('Valid invoice ID is required for send/payment operations'),
  body('invoices.*.email')
    .if(body('operation').equals('send'))
    .optional()
    .isEmail()
    .withMessage('Invalid email format for send operation')
]

module.exports = {
  getInvoicesValidation,
  createInvoiceValidation,
  getInvoiceByIdValidation,
  updateInvoiceValidation,
  deleteInvoiceValidation,
  sendInvoiceValidation,
  recordPaymentValidation,
  bulkOperationsValidation
}
