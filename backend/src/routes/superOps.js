const express = require('express')
const router = express.Router()
const {
  connectSuperOps,
  getSuperOpsStatus,
  syncSuperOpsData,
  getSuperOpsTickets,
  getSuperOpsClients,
  updateSuperOpsSettings
} = require('../controllers/superOpsController')
const {
  connectSuperOpsValidation,
  getSuperOpsStatusValidation,
  syncSuperOpsDataValidation,
  getSuperOpsTicketsValidation,
  getSuperOpsClientsValidation,
  updateSuperOpsSettingsValidation
} = require('../validators/superOpsValidator')

// POST /api/integrations/superops/connect - Connect SuperOps
router.post('/connect', 
  connectSuperOpsValidation,
  connectSuperOps
)

// GET /api/integrations/superops/status - Connection status
router.get('/status', 
  getSuperOpsStatusValidation,
  getSuperOpsStatus
)

// POST /api/integrations/superops/sync - Sync data
router.post('/sync', 
  syncSuperOpsDataValidation,
  syncSuperOpsData
)

// GET /api/integrations/superops/tickets - Import tickets
router.get('/tickets', 
  getSuperOpsTicketsValidation,
  getSuperOpsTickets
)

// GET /api/integrations/superops/clients - Import clients
router.get('/clients', 
  getSuperOpsClientsValidation,
  getSuperOpsClients
)

// PUT /api/integrations/superops/settings - Update settings
router.put('/settings', 
  updateSuperOpsSettingsValidation,
  updateSuperOpsSettings
)

module.exports = router
