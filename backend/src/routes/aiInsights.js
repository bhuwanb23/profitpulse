const express = require('express')
const router = express.Router()
const {
  getProfitabilityGenome,
  getServiceOptimization,
  getPricingRecommendations,
  getMarketAnalysis,
  getCompetitiveIntelligence,
  acceptRecommendation
} = require('../controllers/aiInsightsController')
const {
  getProfitabilityGenomeValidation,
  getServiceOptimizationValidation,
  getPricingRecommendationsValidation,
  getMarketAnalysisValidation,
  getCompetitiveIntelligenceValidation,
  acceptRecommendationValidation
} = require('../validators/aiInsightsValidator')

// GET /api/ai/insights/profitability-genome - Profitability genome
router.get('/profitability-genome', 
  getProfitabilityGenomeValidation,
  getProfitabilityGenome
)

// GET /api/ai/insights/service-optimization - Service optimization
router.get('/service-optimization', 
  getServiceOptimizationValidation,
  getServiceOptimization
)

// GET /api/ai/insights/pricing - Pricing recommendations
router.get('/pricing', 
  getPricingRecommendationsValidation,
  getPricingRecommendations
)

// GET /api/ai/insights/market - Market analysis
router.get('/market', 
  getMarketAnalysisValidation,
  getMarketAnalysis
)

// GET /api/ai/insights/competitive - Competitive intelligence
router.get('/competitive', 
  getCompetitiveIntelligenceValidation,
  getCompetitiveIntelligence
)

// POST /api/ai/insights/accept-recommendation - Accept recommendation
router.post('/accept-recommendation', 
  acceptRecommendationValidation,
  acceptRecommendation
)

module.exports = router
