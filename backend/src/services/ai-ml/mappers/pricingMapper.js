const winston = require('winston');

/**
 * Dynamic Pricing Data Mapper
 * Maps data between backend format and AI/ML service format for pricing recommendations
 */
class PricingMapper {
  static mapBackendToAIML(data, options = {}) {
    try {
      const aimlRequest = {
        client_id: data.clientId,
        service_data: {
          service_type: data.serviceType || 'managed_services',
          current_price: data.currentPrice || 0,
          service_complexity: data.serviceComplexity || 'medium',
          resource_requirements: data.resourceRequirements || {},
          delivery_model: data.deliveryModel || 'on-site'
        },
        market_data: {
          competitor_pricing: data.competitorPricing || [],
          market_rates: data.marketRates || {},
          demand_level: data.demandLevel || 'medium',
          market_segment: data.marketSegment || 'mid-market'
        },
        client_context: {
          client_size: data.clientSize || 'medium',
          industry: data.industry || 'technology',
          relationship_duration: data.relationshipDuration || 12,
          payment_history: data.paymentHistory || 'good',
          price_sensitivity: data.priceSensitivity || 0.5
        },
        pricing_options: {
          pricing_model: options.pricingModel || 'value_based',
          include_alternatives: options.includeAlternatives !== false,
          optimization_goal: options.optimizationGoal || 'profit_margin'
        }
      };

      return aimlRequest;
    } catch (error) {
      winston.error('Error mapping pricing data:', error);
      throw new Error(`Pricing data mapping failed: ${error.message}`);
    }
  }

  static mapAIMLToBackend(aimlResponse, options = {}) {
    try {
      const data = aimlResponse.data;
      
      return {
        success: true,
        pricingRecommendation: {
          recommendedPrice: data.recommended_price || 0,
          priceRange: data.price_range || { min: 0, max: 0 },
          confidence: data.confidence || 0.7,
          pricingModel: data.pricing_model || 'value_based',
          marketPosition: data.market_position || 'competitive'
        },
        alternatives: (data.alternatives || []).map(alt => ({
          price: alt.price,
          model: alt.model,
          rationale: alt.rationale,
          expectedOutcome: alt.expected_outcome
        })),
        factors: {
          marketRate: data.factors?.market_rate || 0,
          complexityScore: data.factors?.complexity_score || 0.5,
          clientValue: data.factors?.client_value || 0.5,
          competitionLevel: data.factors?.competition_level || 'medium'
        },
        recommendations: data.recommendations || [],
        metadata: {
          modelVersion: data.model_version || 'v1.0',
          recommendationDate: data.recommendation_date || new Date().toISOString(),
          isFallback: data.is_fallback || false
        }
      };
    } catch (error) {
      winston.error('Error mapping pricing response:', error);
      throw new Error(`Pricing response mapping failed: ${error.message}`);
    }
  }

  static validateBackendData(data) {
    const errors = [];
    const warnings = [];
    
    if (!data.clientId) errors.push('Client ID is required');
    if (!data.serviceType) warnings.push('Service type not specified');
    if (!data.currentPrice || data.currentPrice <= 0) warnings.push('Current price is missing or invalid');
    
    return {
      isValid: errors.length === 0,
      errors,
      warnings,
      dataQuality: warnings.length === 0 ? 'excellent' : warnings.length <= 2 ? 'good' : 'poor'
    };
  }

  static validateAIMLResponse(aimlResponse) {
    const errors = [];
    
    if (!aimlResponse?.data) errors.push('AI/ML pricing response data is missing');
    if (aimlResponse.data && typeof aimlResponse.data.recommended_price !== 'number') {
      errors.push('Recommended price is missing or invalid');
    }
    
    return { isValid: errors.length === 0, errors };
  }

  static createCacheKey(data, options = {}) {
    const clientId = data.clientId;
    const serviceType = data.serviceType || 'default';
    const timestamp = Math.floor(Date.now() / (1000 * 60 * 60 * 24)); // Daily caching
    return `pricing_${clientId}_${serviceType}_${timestamp}`;
  }
}

module.exports = PricingMapper;
