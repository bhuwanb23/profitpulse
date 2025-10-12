const express = require('express')
const router = express.Router()
const {
  getInvoices,
  createInvoice,
  getInvoiceById,
  updateInvoice,
  deleteInvoice,
  sendInvoice,
  recordPayment,
  bulkInvoiceOperations
} = require('../controllers/invoiceController')
const {
  getInvoicesValidation,
  createInvoiceValidation,
  getInvoiceByIdValidation,
  updateInvoiceValidation,
  deleteInvoiceValidation,
  sendInvoiceValidation,
  recordPaymentValidation,
  bulkOperationsValidation
} = require('../validators/invoiceValidator')

// GET /api/invoices - List invoices with filters
router.get('/', 
  getInvoicesValidation,
  getInvoices
)

// POST /api/invoices - Create invoice
router.post('/', 
  createInvoiceValidation,
  createInvoice
)

// GET /api/invoices/:id - Get invoice details
router.get('/:id', 
  getInvoiceByIdValidation,
  getInvoiceById
)

// PUT /api/invoices/:id - Update invoice
router.put('/:id', 
  updateInvoiceValidation,
  updateInvoice
)

// DELETE /api/invoices/:id - Delete invoice
router.delete('/:id', 
  deleteInvoiceValidation,
  deleteInvoice
)

// POST /api/invoices/:id/send - Send invoice
router.post('/:id/send', 
  sendInvoiceValidation,
  sendInvoice
)

// PUT /api/invoices/:id/payment - Record payment
router.put('/:id/payment', 
  recordPaymentValidation,
  recordPayment
)

// POST /api/invoices/bulk - Bulk invoice operations
router.post('/bulk', 
  bulkOperationsValidation,
  bulkInvoiceOperations
)

module.exports = router