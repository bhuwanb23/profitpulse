const winston = require('winston');

/**
 * Churn Prediction Data Mapper
 * Maps data between backend format and AI/ML service format for churn prediction
 */
class ChurnMapper {
  /**
   * Map backend client data to AI/ML service request format
   * @param {Object} clientData - Client data from backend
   * @param {Object} options - Additional options
   * @returns {Object} - AI/ML service request format
   */
  static mapBackendToAIML(clientData, options = {}) {
    try {
      // Extract client behavior metrics
      const behaviorMetrics = {
        engagement_score: clientData.engagementScore || 0.7,
        communication_frequency: clientData.communicationFrequency || 0.5,
        support_ticket_volume: clientData.ticketCount || 0,
        response_time_satisfaction: clientData.responseTimeSatisfaction || 0.8,
        feature_adoption_rate: clientData.featureAdoptionRate || 0.6,
        login_frequency: clientData.loginFrequency || 0.5
      };

      // Extract financial metrics
      const financialMetrics = {
        payment_history: clientData.paymentHistory || 'good',
        payment_delays: clientData.paymentDelays || 0,
        contract_value: clientData.contractValue || 0,
        price_sensitivity: clientData.priceSensitivity || 0.5,
        billing_disputes: clientData.billingDisputes || 0,
        revenue_trend: clientData.revenueTrend || 'stable'
      };

      // Extract service metrics
      const serviceMetrics = {
        service_utilization: clientData.serviceUtilization || 0.7,
        downtime_incidents: clientData.downtimeIncidents || 0,
        sla_compliance: clientData.slaCompliance || 0.95,
        resolution_satisfaction: clientData.resolutionSatisfaction || 0.8,
        escalation_rate: clientData.escalationRate || 0.1,
        service_adoption: clientData.serviceAdoption || 0.7
      };

      // Extract relationship metrics
      const relationshipMetrics = {
        relationship_duration: clientData.relationshipDuration || 12,
        key_contact_stability: clientData.keyContactStability || 0.8,
        stakeholder_satisfaction: clientData.stakeholderSatisfaction || 0.8,
        renewal_history: clientData.renewalHistory || [],
        expansion_opportunities: clientData.expansionOpportunities || 0.5,
        competitive_pressure: clientData.competitivePressure || 0.3
      };

      // Build AI/ML request
      const aimlRequest = {
        client_id: clientData.id || clientData.clientId,
        behavior_metrics: behaviorMetrics,
        financial_metrics: financialMetrics,
        service_metrics: serviceMetrics,
        relationship_metrics: relationshipMetrics,
        prediction_options: {
          prediction_horizon: options.predictionHorizon || 90,
          include_confidence: options.includeConfidence !== false,
          include_risk_factors: options.includeRiskFactors !== false,
          include_retention_strategies: options.includeRetentionStrategies !== false
        }
      };

      winston.debug('Mapped backend data to AI/ML format for churn prediction', {
        clientId: clientData.id,
        requestSize: JSON.stringify(aimlRequest).length
      });

      return aimlRequest;

    } catch (error) {
      winston.error('Error mapping backend data to AI/ML format for churn:', error);
      throw new Error(`Churn data mapping failed: ${error.message}`);
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
        throw new Error('Invalid AI/ML churn response format');
      }

      const data = aimlResponse.data;

      // Map churn prediction metrics
      const churnPrediction = {
        churnProbability: data.churn_probability || 0,
        riskLevel: this.calculateChurnRiskLevel(data.churn_probability),
        confidence: data.confidence || 0,
        timeToChurn: data.time_to_churn || null,
        predictionHorizon: data.prediction_horizon || 90
      };

      // Map risk factors
      const riskFactors = (data.risk_factors || []).map(factor => ({
        factor: factor.factor || factor,
        impact: factor.impact || 'medium',
        severity: factor.severity || 'medium',
        trend: factor.trend || 'stable',
        actionable: factor.actionable !== false
      }));

      // Map retention strategies
      const retentionStrategies = (data.retention_recommendations || []).map(strategy => ({
        strategy: strategy.strategy || strategy.description || strategy,
        priority: strategy.priority || 'medium',
        effort: strategy.effort || 'medium',
        impact: strategy.impact || 'medium',
        timeframe: strategy.timeframe || 'short-term',
        cost: strategy.cost || 'low'
      }));

      // Map early warning indicators
      const earlyWarningIndicators = {
        behavioralChanges: data.behavioral_changes || [],
        engagementDrops: data.engagement_drops || [],
        supportPatterns: data.support_patterns || [],
        usageAnomalies: data.usage_anomalies || []
      };

      // Map intervention recommendations
      const interventions = {
        immediate: data.interventions?.immediate || [],
        shortTerm: data.interventions?.short_term || [],
        longTerm: data.interventions?.long_term || []
      };

      // Build backend response
      const backendResponse = {
        success: true,
        churnPrediction: churnPrediction,
        riskFactors: riskFactors,
        retentionStrategies: retentionStrategies,
        earlyWarningIndicators: earlyWarningIndicators,
        interventions: interventions,
        insights: {
          primaryRiskDrivers: data.insights?.primary_drivers || [],
          protectiveFactors: data.insights?.protective_factors || [],
          similarClientPatterns: data.insights?.similar_patterns || [],
          industryBenchmarks: data.insights?.benchmarks || {}
        },
        metadata: {
          modelVersion: data.model_version || 'v1.0',
          predictionDate: data.prediction_date || new Date().toISOString(),
          processingTime: data.processing_time || 0,
          dataQuality: data.data_quality || 'good',
          isFallback: data.is_fallback || false
        }
      };

      winston.debug('Mapped AI/ML response to backend format for churn prediction', {
        churnProbability: churnPrediction.churnProbability,
        riskLevel: churnPrediction.riskLevel,
        confidence: churnPrediction.confidence,
        strategiesCount: retentionStrategies.length
      });

      return backendResponse;

    } catch (error) {
      winston.error('Error mapping AI/ML churn response to backend format:', error);
      throw new Error(`Churn response mapping failed: ${error.message}`);
    }
  }

  /**
   * Calculate churn risk level based on probability
   * @param {number} probability - Churn probability (0-1)
   * @returns {string} - Risk level
   */
  static calculateChurnRiskLevel(probability) {
    if (probability >= 0.7) return 'critical';
    if (probability >= 0.5) return 'high';
    if (probability >= 0.3) return 'medium';
    return 'low';
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
    if (clientData.ticketCount < 0) {
      warnings.push('Ticket count cannot be negative');
    }

    if (clientData.slaCompliance && (clientData.slaCompliance < 0 || clientData.slaCompliance > 1)) {
      warnings.push('SLA compliance should be between 0 and 1');
    }

    if (clientData.relationshipDuration && clientData.relationshipDuration < 0) {
      warnings.push('Relationship duration cannot be negative');
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
      errors.push('AI/ML churn response is null or undefined');
      return { isValid: false, errors };
    }

    if (!aimlResponse.data) {
      errors.push('AI/ML churn response data is missing');
    }

    if (aimlResponse.data && typeof aimlResponse.data.churn_probability !== 'number') {
      errors.push('Churn probability is missing or invalid');
    }

    if (aimlResponse.data && (aimlResponse.data.churn_probability < 0 || aimlResponse.data.churn_probability > 1)) {
      errors.push('Churn probability is out of valid range (0-1)');
    }

    return {
      isValid: errors.length === 0,
      errors
    };
  }

  /**
   * Create cache key for churn prediction
   * @param {Object} clientData - Client data
   * @param {Object} options - Options
   * @returns {string} - Cache key
   */
  static createCacheKey(clientData, options = {}) {
    const clientId = clientData.id || clientData.clientId;
    const horizon = options.predictionHorizon || 90;
    const timestamp = Math.floor(Date.now() / (1000 * 60 * 60 * 24)); // Day-based caching
    
    return `churn_${clientId}_${horizon}_${timestamp}`;
  }
}

module.exports = ChurnMapper;
