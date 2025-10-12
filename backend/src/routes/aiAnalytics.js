const express = require('express')
const router = express.Router()
const {
  getAIAnalyticsOverview,
  getRevenueLeaks,
  getProfitabilityScores,
  getAIRecommendations,
  runAIAnalysis,
  getAnalysisStatus
} = require('../controllers/aiAnalyticsController')
const {
  getAIAnalyticsOverviewValidation,
  getRevenueLeaksValidation,
  getProfitabilityScoresValidation,
  getAIRecommendationsValidation,
  runAIAnalysisValidation,
  getAnalysisStatusValidation
} = require('../validators/aiAnalyticsValidator')

// GET /api/ai/analytics/overview - AI analytics overview
router.get('/overview', 
  getAIAnalyticsOverviewValidation,
  getAIAnalyticsOverview
)

// GET /api/ai/analytics/revenue-leaks - Revenue leak detection
router.get('/revenue-leaks', 
  getRevenueLeaksValidation,
  getRevenueLeaks
)

// GET /api/ai/analytics/profitability-scores - Profitability scoring
router.get('/profitability-scores', 
  getProfitabilityScoresValidation,
  getProfitabilityScores
)

// GET /api/ai/analytics/recommendations - AI recommendations
router.get('/recommendations', 
  getAIRecommendationsValidation,
  getAIRecommendations
)

// POST /api/ai/analytics/run-analysis - Trigger AI analysis
router.post('/run-analysis', 
  runAIAnalysisValidation,
  runAIAnalysis
)

// GET /api/ai/analytics/status/:id - Analysis status
router.get('/status/:id', 
  getAnalysisStatusValidation,
  getAnalysisStatus
)

module.exports = router
