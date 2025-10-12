const express = require('express')
const router = express.Router()
const {
  getReportTemplates,
  generateReport,
  getReport,
  exportReport,
  scheduleReport,
  getScheduledReports,
  cancelScheduledReport
} = require('../controllers/reportController')
const {
  getReportTemplatesValidation,
  generateReportValidation,
  getReportValidation,
  exportReportValidation,
  scheduleReportValidation,
  getScheduledReportsValidation,
  cancelScheduledReportValidation
} = require('../validators/reportValidator')

// GET /api/reports/templates - Report templates
router.get('/templates', 
  getReportTemplatesValidation,
  getReportTemplates
)

// POST /api/reports/generate - Generate custom report
router.post('/generate', 
  generateReportValidation,
  generateReport
)

// GET /api/reports/:id - Get report
router.get('/:id', 
  getReportValidation,
  getReport
)

// POST /api/reports/:id/export - Export report (PDF/Excel)
router.post('/:id/export', 
  exportReportValidation,
  exportReport
)

// POST /api/reports/schedule - Schedule report
router.post('/schedule', 
  scheduleReportValidation,
  scheduleReport
)

// GET /api/reports/scheduled - List scheduled reports
router.get('/scheduled', 
  getScheduledReportsValidation,
  getScheduledReports
)

// DELETE /api/reports/scheduled/:id - Cancel scheduled report
router.delete('/scheduled/:id', 
  cancelScheduledReportValidation,
  cancelScheduledReport
)

module.exports = router