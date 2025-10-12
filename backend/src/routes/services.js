const express = require('express')
const router = express.Router()
const {
  getServices,
  createService,
  getServiceById,
  updateService,
  deleteService,
  assignServiceToClient,
  updateServicePricing
} = require('../controllers/serviceController')
const {
  createServiceValidation,
  updateServiceValidation,
  serviceIdValidation,
  getServicesValidation,
  assignServiceValidation,
  updatePricingValidation
} = require('../validators/serviceValidator')
const { requireRole } = require('../middleware/rbac')

// GET /api/services - List services
router.get('/', 
  getServicesValidation,
  getServices
)

// POST /api/services - Create service
router.post('/', 
  createServiceValidation,
  createService
)

// GET /api/services/:id - Get service details
router.get('/:id', 
  serviceIdValidation,
  getServiceById
)

// PUT /api/services/:id - Update service
router.put('/:id', 
  updateServiceValidation,
  updateService
)

// DELETE /api/services/:id - Delete service
router.delete('/:id', 
  serviceIdValidation,
  deleteService
)

// POST /api/services/:id/assign - Assign service to client
router.post('/:id/assign', 
  assignServiceValidation,
  assignServiceToClient
)

// PUT /api/services/:id/pricing - Update service pricing
router.put('/:id/pricing', 
  updatePricingValidation,
  updateServicePricing
)

module.exports = router