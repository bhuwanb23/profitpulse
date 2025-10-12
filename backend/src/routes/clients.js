const express = require('express')
const router = express.Router()
const {
  getClients,
  createClient,
  getClientById,
  updateClient,
  deleteClient,
  getClientServices,
  getClientAnalytics,
  getClientProfitability
} = require('../controllers/clientController')
const {
  createClientValidation,
  updateClientValidation,
  clientIdValidation,
  getClientsValidation,
  getClientServicesValidation,
  getClientAnalyticsValidation,
  getClientProfitabilityValidation
} = require('../validators/clientValidator')
const { requireRole } = require('../middleware/rbac')

// GET /api/clients - List clients with filters
router.get('/', 
  getClientsValidation,
  getClients
)

// POST /api/clients - Create new client
router.post('/', 
  createClientValidation,
  createClient
)

// GET /api/clients/:id - Get client details
router.get('/:id', 
  clientIdValidation,
  getClientById
)

// PUT /api/clients/:id - Update client
router.put('/:id', 
  updateClientValidation,
  updateClient
)

// DELETE /api/clients/:id - Delete client
router.delete('/:id', 
  clientIdValidation,
  deleteClient
)

// GET /api/clients/:id/services - Get client services
router.get('/:id/services', 
  getClientServicesValidation,
  getClientServices
)

// GET /api/clients/:id/analytics - Get client analytics
router.get('/:id/analytics', 
  getClientAnalyticsValidation,
  getClientAnalytics
)

// GET /api/clients/:id/profitability - Get client profitability
router.get('/:id/profitability', 
  getClientProfitabilityValidation,
  getClientProfitability
)

module.exports = router