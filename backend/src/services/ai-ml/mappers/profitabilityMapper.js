const winston = require('winston');

/**
 * Profitability Prediction Data Mapper
 * Maps data between backend format and AI/ML service format
 */
class ProfitabilityMapper {
  /**
   * Map backend client data to AI/ML service request format
   * @param {Object} clientData - Client data from backend
   * @param {Object} options - Additional options
   * @returns {Object} - AI/ML service request format
   */
  static mapBackendToAIML(clientData, options = {}) {
    try {
      // Extract financial metrics
      const financialMetrics = {
        monthly_revenue: clientData.monthlyRevenue || 0,
        total_costs: clientData.totalCosts || 0,
        profit_margin: clientData.profitMargin || 0,
        revenue_growth: clientData.revenueGrowth || 0,
        cost_trend: clientData.costTrend || 0,
        billing_efficiency: clientData.billingEfficiency || 0.8
      };

      // Extract operational metrics
      const operationalMetrics = {
        ticket_volume: clientData.ticketCount || 0,
        avg_resolution_time: clientData.avgResolutionTime || 0,
        sla_compliance: clientData.slaCompliance || 0.95,
        client_satisfaction: clientData.clientSatisfaction || 4.0,
        service_utilization: clientData.serviceUtilization || 0.7,
        support_hours: clientData.supportHours || 0
      };

      // Extract client characteristics
      const clientCharacteristics = {
        client_size: clientData.clientSize || 'medium',
        industry: clientData.industry || 'technology',
        contract_length: clientData.contractLength || 12,
        payment_terms: clientData.paymentTerms || 30,
        service_tier: clientData.serviceTier || 'standard',
        geographic_location: clientData.location || 'domestic'
      };

      // Extract historical data
      const historicalData = {
        months_active: clientData.monthsActive || 12,
        revenue_history: clientData.revenueHistory || [],
        cost_history: clientData.costHistory || [],
        incident_history: clientData.incidentHistory || [],
        satisfaction_history: clientData.satisfactionHistory || []
      };

      // Build AI/ML request
      const aimlRequest = {
        client_id: clientData.id || clientData.clientId,
        financial_metrics: financialMetrics,
        operational_metrics: operationalMetrics,
        client_characteristics: clientCharacteristics,
        historical_data: historicalData,
        prediction_options: {
          forecast_horizon: options.forecastHorizon || 6,
          include_confidence: options.includeConfidence !== false,
          include_factors: options.includeFactors !== false,
          include_recommendations: options.includeRecommendations !== false
        }
      };

      winston.debug('Mapped backend data to AI/ML format for profitability prediction', {
        clientId: clientData.id,
        requestSize: JSON.stringify(aimlRequest).length
      });

      return aimlRequest;

    } catch (error) {
      winston.error('Error mapping backend data to AI/ML format:', error);
      throw new Error(`Data mapping failed: ${error.message}`);
    }
  }

  /**
   * Map AI/ML service response to backend format
   * @param {Object} aimlResponse - Response from AI/ML service
   * @param {Object} options - Additional options
   * @returns {Object} - Backend response format
   */
  static mapAIMLToBackend(aimlResponse, options = {}) {
    try {
      if (!aimlResponse || !aimlResponse.data) {
        throw new Error('Invalid AI/ML response format');
      }

      const data = aimlResponse.data;

      // Map profitability metrics
      const profitabilityMetrics = {
        profitabilityScore: data.profitability_score || 0,
        confidence: data.confidence || 0,
        riskLevel: this.calculateRiskLevel(data.profitability_score),
        trend: data.trend || 'stable',
        forecastAccuracy: data.forecast_accuracy || 0.85
      };

      // Map contributing factors
      const factors = {
        revenueImpact: data.factors?.revenue_trend || 0,
        costEfficiency: data.factors?.cost_efficiency || 0,
        clientSatisfaction: data.factors?.client_satisfaction || 0,
        serviceUtilization: data.factors?.service_utilization || 0,
        operationalEfficiency: data.factors?.operational_efficiency || 0,
        marketPosition: data.factors?.market_position || 0
      };

      // Map recommendations
      const recommendations = (data.recommendations || []).map(rec => ({
        category: rec.category || 'general',
        priority: rec.priority || 'medium',
        description: rec.description || rec,
        impact: rec.impact || 'medium',
        effort: rec.effort || 'medium',
        timeframe: rec.timeframe || 'short-term'
      }));

      // Map forecast data
      const forecast = {
        nextMonth: data.forecast?.next_month || profitabilityMetrics.profitabilityScore,
        nextQuarter: data.forecast?.next_quarter || profitabilityMetrics.profitabilityScore,
        nextYear: data.forecast?.next_year || profitabilityMetrics.profitabilityScore,
        confidence: data.forecast?.confidence || profitabilityMetrics.confidence
      };

      // Map insights
      const insights = {
        keyStrengths: data.insights?.strengths || [],
        keyWeaknesses: data.insights?.weaknesses || [],
        opportunities: data.insights?.opportunities || [],
        threats: data.insights?.threats || []
      };

      // Build backend response
      const backendResponse = {
        success: true,
        profitability: profitabilityMetrics,
        factors: factors,
        recommendations: recommendations,
        forecast: forecast,
        insights: insights,
        metadata: {
          modelVersion: data.model_version || 'v1.0',
          predictionDate: data.prediction_date || new Date().toISOString(),
          processingTime: data.processing_time || 0,
          dataQuality: data.data_quality || 'good',
          isFallback: data.is_fallback || false
        }
      };

      winston.debug('Mapped AI/ML response to backend format for profitability prediction', {
        profitabilityScore: profitabilityMetrics.profitabilityScore,
        confidence: profitabilityMetrics.confidence,
        recommendationsCount: recommendations.length
      });

      return backendResponse;

    } catch (error) {
      winston.error('Error mapping AI/ML response to backend format:', error);
      throw new Error(`Response mapping failed: ${error.message}`);
    }
  }

  /**
   * Calculate risk level based on profitability score
   * @param {number} score - Profitability score (0-1)
   * @returns {string} - Risk level
   */
  static calculateRiskLevel(score) {
    if (score >= 0.8) return 'low';
    if (score >= 0.6) return 'medium';
    if (score >= 0.4) return 'high';
    return 'critical';
  }

  /**
   * Validate backend data before mapping
   * @param {Object} clientData - Client data to validate
   * @returns {Object} - Validation result
   */
  static validateBackendData(clientData) {
    const errors = [];
    const warnings = [];

    // Required fields
    if (!clientData.id && !clientData.clientId) {
      errors.push('Client ID is required');
    }

    // Data quality checks
    if (!clientData.monthlyRevenue || clientData.monthlyRevenue <= 0) {
      warnings.push('Monthly revenue is missing or invalid');
    }

    if (!clientData.totalCosts || clientData.totalCosts < 0) {
      warnings.push('Total costs data is missing or invalid');
    }

    if (!clientData.ticketCount || clientData.ticketCount < 0) {
      warnings.push('Ticket count data is missing or invalid');
    }

    return {
      isValid: errors.length === 0,
      errors,
      warnings,
      dataQuality: warnings.length === 0 ? 'excellent' : 
                   warnings.length <= 2 ? 'good' : 'poor'
    };
  }

  /**
   * Validate AI/ML response before mapping
   * @param {Object} aimlResponse - AI/ML response to validate
   * @returns {Object} - Validation result
   */
  static validateAIMLResponse(aimlResponse) {
    const errors = [];

    if (!aimlResponse) {
      errors.push('AI/ML response is null or undefined');
      return { isValid: false, errors };
    }

    if (!aimlResponse.data) {
      errors.push('AI/ML response data is missing');
    }

    if (aimlResponse.data && typeof aimlResponse.data.profitability_score !== 'number') {
      errors.push('Profitability score is missing or invalid');
    }

    if (aimlResponse.data && aimlResponse.data.profitability_score < 0 || aimlResponse.data.profitability_score > 1) {
      errors.push('Profitability score is out of valid range (0-1)');
    }

    return {
      isValid: errors.length === 0,
      errors
    };
  }

  /**
   * Create cache key for profitability prediction
   * @param {Object} clientData - Client data
   * @param {Object} options - Options
   * @returns {string} - Cache key
   */
  static createCacheKey(clientData, options = {}) {
    const clientId = clientData.id || clientData.clientId;
    const horizon = options.forecastHorizon || 6;
    const timestamp = Math.floor(Date.now() / (1000 * 60 * 60)); // Hour-based caching
    
    return `profitability_${clientId}_${horizon}_${timestamp}`;
  }
}

module.exports = ProfitabilityMapper;
