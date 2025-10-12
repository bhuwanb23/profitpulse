const express = require('express')
const router = express.Router()
const {
  getRevenueForecasting,
  getChurnPrediction,
  getDemandForecasting,
  getBudgetOptimization,
  getMarketTrendAnalysis,
  getGrowthOpportunities
} = require('../controllers/predictiveAnalyticsController')
const {
  getRevenueForecastingValidation,
  getChurnPredictionValidation,
  getDemandForecastingValidation,
  getBudgetOptimizationValidation,
  getMarketTrendAnalysisValidation,
  getGrowthOpportunitiesValidation
} = require('../validators/predictiveAnalyticsValidator')

// GET /api/ai/predictions/revenue - Revenue forecasting
router.get('/revenue', 
  getRevenueForecastingValidation,
  getRevenueForecasting
)

// GET /api/ai/predictions/churn - Client churn prediction
router.get('/churn', 
  getChurnPredictionValidation,
  getChurnPrediction
)

// GET /api/ai/predictions/demand - Service demand forecasting
router.get('/demand', 
  getDemandForecastingValidation,
  getDemandForecasting
)

// GET /api/ai/predictions/budget - Budget optimization
router.get('/budget', 
  getBudgetOptimizationValidation,
  getBudgetOptimization
)

// GET /api/ai/predictions/market - Market trend analysis
router.get('/market', 
  getMarketTrendAnalysisValidation,
  getMarketTrendAnalysis
)

// GET /api/ai/predictions/growth - Growth opportunities
router.get('/growth', 
  getGrowthOpportunitiesValidation,
  getGrowthOpportunities
)

module.exports = router
