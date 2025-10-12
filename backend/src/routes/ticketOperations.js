const express = require('express')
const router = express.Router()
const {
  bulkTicketOperations,
  getTicketTemplates,
  createTicketTemplate,
  escalateTicket,
  getTicketRoutingRules,
  getSLAMonitoring
} = require('../controllers/ticketOperationsController')
const {
  bulkOperationsValidation,
  getTemplatesValidation,
  createTemplateValidation,
  escalateTicketValidation,
  getRoutingRulesValidation,
  getSLAMonitoringValidation
} = require('../validators/ticketOperationsValidator')

// POST /api/tickets/bulk - Bulk ticket operations
router.post('/bulk', 
  bulkOperationsValidation,
  bulkTicketOperations
)

// GET /api/tickets/templates - Ticket templates
router.get('/templates', 
  getTemplatesValidation,
  getTicketTemplates
)

// POST /api/tickets/templates - Create template
router.post('/templates', 
  createTemplateValidation,
  createTicketTemplate
)

// POST /api/tickets/:id/escalate - Escalate ticket
router.post('/:id/escalate', 
  escalateTicketValidation,
  escalateTicket
)

// GET /api/tickets/routing - Ticket routing rules
router.get('/routing', 
  getRoutingRulesValidation,
  getTicketRoutingRules
)

// GET /api/tickets/sla-monitor - SLA monitoring
router.get('/sla-monitor', 
  getSLAMonitoringValidation,
  getSLAMonitoring
)

module.exports = router
