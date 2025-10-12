const { Invoice, Client, User, Organization } = require('../models')
const { Op } = require('sequelize')
const { validationResult } = require('express-validator')

// GET /api/invoices - List invoices with filters
const getInvoices = async (req, res) => {
  try {
    const { 
      page = 1, 
      limit = 10, 
      search, 
      status,
      client_id,
      organization_id,
      date_from,
      date_to,
      amount_min,
      amount_max,
      sort_by = 'created_at',
      sort_order = 'DESC'
    } = req.query
    const offset = (page - 1) * limit

    // Build where clause
    const whereClause = {}
    if (search) {
      whereClause[Op.or] = [
        { invoice_number: { [Op.iLike]: `%${search}%` } },
        { notes: { [Op.iLike]: `%${search}%` } }
      ]
    }
    if (status) whereClause.status = status
    if (client_id) whereClause.client_id = client_id
    if (organization_id) whereClause.organization_id = organization_id
    
    // Date range filtering
    if (date_from || date_to) {
      whereClause.invoice_date = {}
      if (date_from) whereClause.invoice_date[Op.gte] = new Date(date_from)
      if (date_to) whereClause.invoice_date[Op.lte] = new Date(date_to)
    }
    
    // Amount range filtering
    if (amount_min || amount_max) {
      whereClause.total_amount = {}
      if (amount_min) whereClause.total_amount[Op.gte] = parseFloat(amount_min)
      if (amount_max) whereClause.total_amount[Op.lte] = parseFloat(amount_max)
    }

    // Build order clause
    const orderClause = [[sort_by, sort_order.toUpperCase()]]

    const { count, rows: invoices } = await Invoice.findAndCountAll({
      where: whereClause,
      include: [
        {
          model: Organization,
          as: 'organization',
          attributes: ['id', 'name', 'domain']
        },
        {
          model: Client,
          as: 'client',
          attributes: ['id', 'name', 'email', 'company', 'contact_person', 'phone']
        }
      ],
      limit: parseInt(limit),
      offset: parseInt(offset),
      order: orderClause
    })

    res.json({
      success: true,
      data: {
        invoices,
        pagination: {
          total: count,
          page: parseInt(page),
          limit: parseInt(limit),
          pages: Math.ceil(count / limit)
        }
      }
    })
  } catch (error) {
    console.error('Get invoices error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching invoices'
    })
  }
}

// POST /api/invoices - Create invoice
const createInvoice = async (req, res) => {
  try {
    const errors = validationResult(req)
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        message: 'Validation failed',
        errors: errors.array()
      })
    }

    const {
      client_id,
      organization_id,
      invoice_date,
      due_date,
      line_items = [],
      subtotal,
      tax_amount = 0,
      total_amount,
      notes,
      terms,
      created_by
    } = req.body

    // Check if client exists and belongs to organization
    const client = await Client.findOne({
      where: { 
        id: client_id,
        organization_id: organization_id
      }
    })
    if (!client) {
      return res.status(400).json({
        success: false,
        message: 'Client not found or does not belong to the organization'
      })
    }

    // Generate invoice number
    const invoiceNumber = `INV-${Date.now()}-${Math.random().toString(36).substr(2, 4).toUpperCase()}`

    // Calculate totals if not provided
    let calculatedSubtotal = subtotal
    let calculatedTotal = total_amount
    
    if (line_items && line_items.length > 0) {
      calculatedSubtotal = line_items.reduce((sum, item) => {
        return sum + (parseFloat(item.quantity || 0) * parseFloat(item.unit_price || 0))
      }, 0)
      calculatedTotal = calculatedSubtotal + parseFloat(tax_amount || 0)
    }

    const invoice = await Invoice.create({
      client_id,
      organization_id,
      invoice_number: invoiceNumber,
      invoice_date: invoice_date ? new Date(invoice_date) : new Date(),
      due_date: due_date ? new Date(due_date) : null,
      line_items,
      subtotal: calculatedSubtotal,
      tax_amount: parseFloat(tax_amount || 0),
      total_amount: calculatedTotal,
      notes,
      terms,
      created_by,
      status: 'draft'
    })

    // Fetch the created invoice with associations
    const createdInvoice = await Invoice.findByPk(invoice.id, {
      include: [
        {
          model: Organization,
          as: 'organization',
          attributes: ['id', 'name', 'domain']
        },
        {
          model: Client,
          as: 'client',
          attributes: ['id', 'name', 'email', 'company', 'contact_person', 'phone']
        }
      ]
    })

    res.status(201).json({
      success: true,
      message: 'Invoice created successfully',
      data: { invoice: createdInvoice }
    })
  } catch (error) {
    console.error('Create invoice error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while creating invoice'
    })
  }
}

// GET /api/invoices/:id - Get invoice details
const getInvoiceById = async (req, res) => {
  try {
    const { id } = req.params

    const invoice = await Invoice.findByPk(id, {
      include: [
        {
          model: Organization,
          as: 'organization',
          attributes: ['id', 'name', 'domain']
        },
        {
          model: Client,
          as: 'client',
          attributes: ['id', 'name', 'email', 'company', 'contact_person', 'phone']
        }
      ]
    })

    if (!invoice) {
      return res.status(404).json({
        success: false,
        message: 'Invoice not found'
      })
    }

    res.json({
      success: true,
      data: { invoice }
    })
  } catch (error) {
    console.error('Get invoice by ID error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching invoice'
    })
  }
}

// PUT /api/invoices/:id - Update invoice
const updateInvoice = async (req, res) => {
  try {
    const errors = validationResult(req)
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        message: 'Validation failed',
        errors: errors.array()
      })
    }

    const { id } = req.params
    const updateData = req.body

    const invoice = await Invoice.findByPk(id)
    if (!invoice) {
      return res.status(404).json({
        success: false,
        message: 'Invoice not found'
      })
    }

    // Validate client if being updated
    if (updateData.client_id && updateData.client_id !== invoice.client_id) {
      const client = await Client.findOne({
        where: { 
          id: updateData.client_id,
          organization_id: invoice.organization_id
        }
      })
      if (!client) {
        return res.status(400).json({
          success: false,
          message: 'Client not found or does not belong to the organization'
        })
      }
    }

    // Recalculate totals if line_items are updated
    if (updateData.line_items && updateData.line_items.length > 0) {
      const calculatedSubtotal = updateData.line_items.reduce((sum, item) => {
        return sum + (parseFloat(item.quantity || 0) * parseFloat(item.unit_price || 0))
      }, 0)
      const calculatedTotal = calculatedSubtotal + parseFloat(updateData.tax_amount || invoice.tax_amount || 0)
      
      updateData.subtotal = calculatedSubtotal
      updateData.total_amount = calculatedTotal
    }

    // Update invoice
    await invoice.update(updateData)

    // Fetch updated invoice with associations
    const updatedInvoice = await Invoice.findByPk(id, {
      include: [
        {
          model: Organization,
          as: 'organization',
          attributes: ['id', 'name', 'domain']
        },
        {
          model: Client,
          as: 'client',
          attributes: ['id', 'name', 'email', 'company', 'contact_person', 'phone']
        }
      ]
    })

    res.json({
      success: true,
      message: 'Invoice updated successfully',
      data: { invoice: updatedInvoice }
    })
  } catch (error) {
    console.error('Update invoice error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while updating invoice'
    })
  }
}

// DELETE /api/invoices/:id - Delete invoice
const deleteInvoice = async (req, res) => {
  try {
    const { id } = req.params

    const invoice = await Invoice.findByPk(id)
    if (!invoice) {
      return res.status(404).json({
        success: false,
        message: 'Invoice not found'
      })
    }

    // Prevent deletion of paid invoices
    if (invoice.status === 'paid') {
      return res.status(400).json({
        success: false,
        message: 'Cannot delete paid invoices'
      })
    }

    await invoice.destroy()

    res.json({
      success: true,
      message: 'Invoice deleted successfully'
    })
  } catch (error) {
    console.error('Delete invoice error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while deleting invoice'
    })
  }
}

// POST /api/invoices/:id/send - Send invoice
const sendInvoice = async (req, res) => {
  try {
    const errors = validationResult(req)
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        message: 'Validation failed',
        errors: errors.array()
      })
    }

    const { id } = req.params
    const { 
      email,
      subject,
      message,
      send_copy_to_self = false
    } = req.body

    const invoice = await Invoice.findByPk(id, {
      include: [
        {
          model: Client,
          as: 'client',
          attributes: ['id', 'name', 'email', 'company']
        }
      ]
    })

    if (!invoice) {
      return res.status(404).json({
        success: false,
        message: 'Invoice not found'
      })
    }

    // Use provided email or client's email
    const recipientEmail = email || invoice.client.email
    if (!recipientEmail) {
      return res.status(400).json({
        success: false,
        message: 'No email address available for sending invoice'
      })
    }

    // Update invoice status and send timestamp
    await invoice.update({
      status: 'sent',
      sent_at: new Date(),
      sent_to_email: recipientEmail
    })

    // In a real application, you would send the actual email here
    const emailData = {
      to: recipientEmail,
      subject: subject || `Invoice ${invoice.invoice_number} from ${invoice.organization?.name || 'Your Service Provider'}`,
      message: message || `Please find attached invoice ${invoice.invoice_number} for ${invoice.total_amount}.`,
      invoice_number: invoice.invoice_number,
      total_amount: invoice.total_amount,
      due_date: invoice.due_date,
      send_copy_to_self
    }

    res.json({
      success: true,
      message: 'Invoice sent successfully',
      data: {
        invoice: {
          id: invoice.id,
          invoice_number: invoice.invoice_number,
          status: 'sent',
          sent_at: invoice.sent_at,
          sent_to_email: recipientEmail
        },
        email: emailData
      }
    })
  } catch (error) {
    console.error('Send invoice error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while sending invoice'
    })
  }
}

// PUT /api/invoices/:id/payment - Record payment
const recordPayment = async (req, res) => {
  try {
    const errors = validationResult(req)
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        message: 'Validation failed',
        errors: errors.array()
      })
    }

    const { id } = req.params
    const { 
      payment_date,
      payment_method,
      payment_reference,
      amount,
      notes
    } = req.body

    const invoice = await Invoice.findByPk(id)
    if (!invoice) {
      return res.status(404).json({
        success: false,
        message: 'Invoice not found'
      })
    }

    // Check if invoice is already paid
    if (invoice.status === 'paid') {
      return res.status(400).json({
        success: false,
        message: 'Invoice is already marked as paid'
      })
    }

    // Validate payment amount
    const paymentAmount = parseFloat(amount || invoice.total_amount)
    if (paymentAmount <= 0) {
      return res.status(400).json({
        success: false,
        message: 'Payment amount must be greater than zero'
      })
    }

    // Update invoice with payment information
    const updateData = {
      status: 'paid',
      payment_date: payment_date ? new Date(payment_date) : new Date(),
      payment_method,
      payment_reference,
      notes: notes || invoice.notes
    }

    await invoice.update(updateData)

    // Fetch updated invoice with associations
    const updatedInvoice = await Invoice.findByPk(id, {
      include: [
        {
          model: Organization,
          as: 'organization',
          attributes: ['id', 'name', 'domain']
        },
        {
          model: Client,
          as: 'client',
          attributes: ['id', 'name', 'email', 'company', 'contact_person', 'phone']
        }
      ]
    })

    res.json({
      success: true,
      message: 'Payment recorded successfully',
      data: {
        invoice: updatedInvoice,
        payment: {
          amount: paymentAmount,
          payment_date: updateData.payment_date,
          payment_method,
          payment_reference
        }
      }
    })
  } catch (error) {
    console.error('Record payment error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while recording payment'
    })
  }
}

// POST /api/invoices/bulk - Bulk invoice operations
const bulkInvoiceOperations = async (req, res) => {
  try {
    const errors = validationResult(req)
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        message: 'Validation failed',
        errors: errors.array()
      })
    }

    const { 
      operation, // 'create', 'update', 'delete', 'send', 'payment'
      invoices,
      filters
    } = req.body

    let results = {
      success: [],
      failed: [],
      total_processed: 0,
      total_success: 0,
      total_failed: 0
    }

    switch (operation) {
      case 'create':
        // Bulk create invoices
        for (const invoiceData of invoices) {
          try {
            const invoiceNumber = `INV-${Date.now()}-${Math.random().toString(36).substr(2, 4).toUpperCase()}`
            const invoice = await Invoice.create({
              ...invoiceData,
              invoice_number: invoiceNumber
            })
            results.success.push({
              id: invoice.id,
              invoice_number: invoice.invoice_number,
              total_amount: invoice.total_amount
            })
            results.total_success++
          } catch (error) {
            results.failed.push({
              data: invoiceData,
              error: error.message
            })
            results.total_failed++
          }
          results.total_processed++
        }
        break

      case 'update':
        // Bulk update invoices
        for (const updateData of invoices) {
          try {
            const { id, ...updateFields } = updateData
            const invoice = await Invoice.findByPk(id)
            if (!invoice) {
              results.failed.push({
                id,
                error: 'Invoice not found'
              })
              results.total_failed++
            } else {
              await invoice.update(updateFields)
              results.success.push({
                id: invoice.id,
                invoice_number: invoice.invoice_number,
                status: invoice.status
              })
              results.total_success++
            }
          } catch (error) {
            results.failed.push({
              id: updateData.id,
              error: error.message
            })
            results.total_failed++
          }
          results.total_processed++
        }
        break

      case 'delete':
        // Bulk delete invoices
        for (const invoiceId of invoices) {
          try {
            const invoice = await Invoice.findByPk(invoiceId)
            if (!invoice) {
              results.failed.push({
                id: invoiceId,
                error: 'Invoice not found'
              })
              results.total_failed++
            } else if (invoice.status === 'paid') {
              results.failed.push({
                id: invoiceId,
                error: 'Cannot delete paid invoices'
              })
              results.total_failed++
            } else {
              await invoice.destroy()
              results.success.push({
                id: invoiceId,
                invoice_number: invoice.invoice_number
              })
              results.total_success++
            }
          } catch (error) {
            results.failed.push({
              id: invoiceId,
              error: error.message
            })
            results.total_failed++
          }
          results.total_processed++
        }
        break

      case 'send':
        // Bulk send invoices
        for (const sendData of invoices) {
          try {
            const { invoice_id, email } = sendData
            const invoice = await Invoice.findByPk(invoice_id)
            if (!invoice) {
              results.failed.push({
                invoice_id,
                error: 'Invoice not found'
              })
              results.total_failed++
            } else {
              await invoice.update({
                status: 'sent',
                sent_at: new Date(),
                sent_to_email: email
              })
              results.success.push({
                id: invoice.id,
                invoice_number: invoice.invoice_number,
                sent_to: email
              })
              results.total_success++
            }
          } catch (error) {
            results.failed.push({
              invoice_id: sendData.invoice_id,
              error: error.message
            })
            results.total_failed++
          }
          results.total_processed++
        }
        break

      case 'payment':
        // Bulk record payments
        for (const paymentData of invoices) {
          try {
            const { invoice_id, payment_date, payment_method, payment_reference } = paymentData
            const invoice = await Invoice.findByPk(invoice_id)
            if (!invoice) {
              results.failed.push({
                invoice_id,
                error: 'Invoice not found'
              })
              results.total_failed++
            } else if (invoice.status === 'paid') {
              results.failed.push({
                invoice_id,
                error: 'Invoice is already paid'
              })
              results.total_failed++
            } else {
              await invoice.update({
                status: 'paid',
                payment_date: payment_date ? new Date(payment_date) : new Date(),
                payment_method,
                payment_reference
              })
              results.success.push({
                id: invoice.id,
                invoice_number: invoice.invoice_number,
                payment_date: payment_date || new Date()
              })
              results.total_success++
            }
          } catch (error) {
            results.failed.push({
              invoice_id: paymentData.invoice_id,
              error: error.message
            })
            results.total_failed++
          }
          results.total_processed++
        }
        break

      default:
        return res.status(400).json({
          success: false,
          message: 'Invalid operation. Supported operations: create, update, delete, send, payment'
        })
    }

    res.json({
      success: true,
      message: `Bulk ${operation} operation completed`,
      data: results
    })
  } catch (error) {
    console.error('Bulk invoice operations error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while performing bulk operations'
    })
  }
}

module.exports = {
  getInvoices,
  createInvoice,
  getInvoiceById,
  updateInvoice,
  deleteInvoice,
  sendInvoice,
  recordPayment,
  bulkInvoiceOperations
}
