const express = require('express')
const router = express.Router()
const {
  getRevenueTrends,
  getPaymentStatus,
  getOutstandingPayments,
  getBillingEfficiency,
  getPaymentMethods,
  getRevenueForecasting
} = require('../controllers/billingAnalyticsController')
const {
  getRevenueTrendsValidation,
  getPaymentStatusValidation,
  getOutstandingPaymentsValidation,
  getBillingEfficiencyValidation,
  getPaymentMethodsValidation,
  getRevenueForecastingValidation
} = require('../validators/billingAnalyticsValidator')

// GET /api/analytics/revenue-trends - Revenue trends
router.get('/revenue-trends', 
  getRevenueTrendsValidation,
  getRevenueTrends
)

// GET /api/analytics/payment-status - Payment status charts
router.get('/payment-status', 
  getPaymentStatusValidation,
  getPaymentStatus
)

// GET /api/analytics/outstanding-payments - Outstanding payments
router.get('/outstanding-payments', 
  getOutstandingPaymentsValidation,
  getOutstandingPayments
)

// GET /api/analytics/billing-efficiency - Billing efficiency
router.get('/billing-efficiency', 
  getBillingEfficiencyValidation,
  getBillingEfficiency
)

// GET /api/analytics/payment-methods - Payment method analytics
router.get('/payment-methods', 
  getPaymentMethodsValidation,
  getPaymentMethods
)

// GET /api/analytics/revenue-forecasting - Revenue forecasting
router.get('/revenue-forecasting', 
  getRevenueForecastingValidation,
  getRevenueForecasting
)

module.exports = router
