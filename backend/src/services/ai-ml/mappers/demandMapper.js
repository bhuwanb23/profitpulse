const winston = require('winston');

/**
 * Demand Forecasting Data Mapper
 * Maps data between backend format and AI/ML service format for demand forecasting
 */
class DemandMapper {
  static mapBackendToAIML(data, options = {}) {
    try {
      const aimlRequest = {
        organization_id: data.organizationId,
        historical_data: {
          demand_history: data.demandHistory || [],
          service_requests: data.serviceRequests || [],
          capacity_utilization: data.capacityUtilization || [],
          seasonal_patterns: data.seasonalPatterns || {}
        },
        external_factors: {
          market_trends: data.marketTrends || {},
          economic_indicators: data.economicIndicators || {},
          industry_events: data.industryEvents || [],
          competitor_activity: data.competitorActivity || {}
        },
        service_data: {
          service_types: data.serviceTypes || [],
          capacity_constraints: data.capacityConstraints || {},
          resource_availability: data.resourceAvailability || {},
          delivery_models: data.deliveryModels || []
        },
        forecasting_options: {
          forecast_horizon: options.forecastHorizon || 90,
          granularity: options.granularity || 'daily',
          confidence_intervals: options.confidenceIntervals !== false,
          seasonality: options.seasonality !== false,
          include_scenarios: options.includeScenarios !== false
        }
      };

      return aimlRequest;
    } catch (error) {
      winston.error('Error mapping demand data:', error);
      throw new Error(`Demand data mapping failed: ${error.message}`);
    }
  }

  static mapAIMLToBackend(aimlResponse, options = {}) {
    try {
      const data = aimlResponse.data;
      
      return {
        success: true,
        forecast: {
          forecastHorizon: data.forecast_horizon || 90,
          predictions: data.predictions || [],
          confidence: data.confidence || 0.7,
          trendDirection: data.trend_direction || 'stable',
          seasonalityDetected: data.seasonality_detected || false
        },
        scenarios: {
          optimistic: data.scenarios?.optimistic || {},
          expected: data.scenarios?.expected || {},
          pessimistic: data.scenarios?.pessimistic || {}
        },
        insights: {
          keyDrivers: data.insights?.key_drivers || [],
          riskFactors: data.insights?.risk_factors || [],
          opportunities: data.insights?.opportunities || []
        },
        recommendations: data.recommendations || [],
        capacityPlanning: {
          recommendedCapacity: data.capacity_planning?.recommended_capacity || {},
          resourceNeeds: data.capacity_planning?.resource_needs || [],
          scalingRecommendations: data.capacity_planning?.scaling_recommendations || []
        },
        metadata: {
          modelVersion: data.model_version || 'v1.0',
          forecastDate: data.forecast_date || new Date().toISOString(),
          isFallback: data.is_fallback || false
        }
      };
    } catch (error) {
      winston.error('Error mapping demand response:', error);
      throw new Error(`Demand response mapping failed: ${error.message}`);
    }
  }

  static validateBackendData(data) {
    const errors = [];
    const warnings = [];
    
    if (!data.organizationId) errors.push('Organization ID is required');
    if (!data.demandHistory || !Array.isArray(data.demandHistory)) warnings.push('Historical demand data is missing');
    if (data.demandHistory && data.demandHistory.length < 30) warnings.push('Insufficient historical data for accurate forecasting');
    
    return {
      isValid: errors.length === 0,
      errors,
      warnings,
      dataQuality: warnings.length === 0 ? 'excellent' : warnings.length <= 2 ? 'good' : 'poor'
    };
  }

  static validateAIMLResponse(aimlResponse) {
    const errors = [];
    
    if (!aimlResponse?.data) errors.push('AI/ML demand response data is missing');
    if (aimlResponse.data && !Array.isArray(aimlResponse.data.predictions)) {
      errors.push('Demand predictions are missing or invalid');
    }
    
    return { isValid: errors.length === 0, errors };
  }

  static createCacheKey(data, options = {}) {
    const orgId = data.organizationId;
    const horizon = options.forecastHorizon || 90;
    const timestamp = Math.floor(Date.now() / (1000 * 60 * 60 * 12)); // 12-hour caching
    return `demand_${orgId}_${horizon}_${timestamp}`;
  }
}

module.exports = DemandMapper;
