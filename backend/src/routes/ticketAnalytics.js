const express = require('express')
const router = express.Router()
const {
  getTicketVolumeTrends,
  getResolutionTimeAnalytics,
  getCategoryBreakdown,
  getTechnicianPerformance,
  getSLACompliance,
  getCustomerSatisfaction
} = require('../controllers/ticketAnalyticsController')
const {
  volumeTrendsValidation,
  resolutionTimeValidation,
  categoryBreakdownValidation,
  technicianPerformanceValidation,
  slaComplianceValidation,
  customerSatisfactionValidation
} = require('../validators/ticketAnalyticsValidator')

// GET /api/tickets/analytics/volume - Ticket volume trends
router.get('/volume', 
  volumeTrendsValidation,
  getTicketVolumeTrends
)

// GET /api/tickets/analytics/resolution-time - Resolution time analytics
router.get('/resolution-time', 
  resolutionTimeValidation,
  getResolutionTimeAnalytics
)

// GET /api/tickets/analytics/categories - Category breakdown
router.get('/categories', 
  categoryBreakdownValidation,
  getCategoryBreakdown
)

// GET /api/tickets/analytics/technician-performance - Technician metrics
router.get('/technician-performance', 
  technicianPerformanceValidation,
  getTechnicianPerformance
)

// GET /api/tickets/analytics/sla-compliance - SLA compliance
router.get('/sla-compliance', 
  slaComplianceValidation,
  getSLACompliance
)

// GET /api/tickets/analytics/satisfaction - Customer satisfaction
router.get('/satisfaction', 
  customerSatisfactionValidation,
  getCustomerSatisfaction
)

module.exports = router
