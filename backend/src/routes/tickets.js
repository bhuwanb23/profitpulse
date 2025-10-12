const express = require('express')
const router = express.Router()
const {
  getTickets,
  createTicket,
  getTicketById,
  updateTicket,
  deleteTicket,
  assignTicket,
  updateTicketStatus,
  logTimeSpent
} = require('../controllers/ticketController')
const {
  createTicketValidation,
  updateTicketValidation,
  ticketIdValidation,
  getTicketsValidation,
  assignTicketValidation,
  updateStatusValidation,
  logTimeValidation
} = require('../validators/ticketValidator')
const { requireRole } = require('../middleware/rbac')

// GET /api/tickets - List tickets with filters
router.get('/', 
  getTicketsValidation,
  getTickets
)

// POST /api/tickets - Create new ticket
router.post('/', 
  createTicketValidation,
  createTicket
)

// GET /api/tickets/:id - Get ticket details
router.get('/:id', 
  ticketIdValidation,
  getTicketById
)

// PUT /api/tickets/:id - Update ticket
router.put('/:id', 
  updateTicketValidation,
  updateTicket
)

// DELETE /api/tickets/:id - Delete ticket
router.delete('/:id', 
  ticketIdValidation,
  deleteTicket
)

// POST /api/tickets/:id/assign - Assign ticket to technician
router.post('/:id/assign', 
  assignTicketValidation,
  assignTicket
)

// PUT /api/tickets/:id/status - Update ticket status
router.put('/:id/status', 
  updateStatusValidation,
  updateTicketStatus
)

// POST /api/tickets/:id/time - Log time spent
router.post('/:id/time', 
  logTimeValidation,
  logTimeSpent
)

module.exports = router