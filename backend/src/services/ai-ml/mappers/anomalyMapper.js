const winston = require('winston');

/**
 * Anomaly Detection Data Mapper
 * Maps data between backend format and AI/ML service format for anomaly detection
 */
class AnomalyMapper {
  static mapBackendToAIML(data, options = {}) {
    try {
      const aimlRequest = {
        organization_id: data.organizationId,
        time_series_data: {
          metrics: data.metrics || [],
          timestamps: data.timestamps || [],
          data_points: data.dataPoints || [],
          sampling_frequency: data.samplingFrequency || 'hourly'
        },
        system_data: {
          performance_metrics: data.performanceMetrics || {},
          resource_utilization: data.resourceUtilization || {},
          error_rates: data.errorRates || [],
          response_times: data.responseTimes || []
        },
        business_data: {
          transaction_volumes: data.transactionVolumes || [],
          revenue_metrics: data.revenueMetrics || [],
          user_activity: data.userActivity || [],
          service_usage: data.serviceUsage || []
        },
        detection_options: {
          sensitivity_level: options.sensitivityLevel || 'medium',
          detection_method: options.detectionMethod || 'ensemble',
          window_size: options.windowSize || 100,
          threshold_percentile: options.thresholdPercentile || 95,
          include_forecasting: options.includeForecasting !== false
        }
      };

      return aimlRequest;
    } catch (error) {
      winston.error('Error mapping anomaly data:', error);
      throw new Error(`Anomaly data mapping failed: ${error.message}`);
    }
  }

  static mapAIMLToBackend(aimlResponse, options = {}) {
    try {
      const data = aimlResponse.data;
      
      return {
        success: true,
        detection: {
          anomaliesDetected: data.anomalies_detected || 0,
          overallScore: data.overall_score || 0,
          confidence: data.confidence || 0.7,
          detectionMethod: data.detection_method || 'ensemble'
        },
        anomalies: (data.anomalies || []).map(anomaly => ({
          timestamp: anomaly.timestamp,
          metric: anomaly.metric,
          value: anomaly.value,
          expectedRange: anomaly.expected_range,
          severity: anomaly.severity,
          confidence: anomaly.confidence,
          description: anomaly.description,
          possibleCauses: anomaly.possible_causes || []
        })),
        patterns: {
          trendAnomalies: data.patterns?.trend_anomalies || [],
          seasonalAnomalies: data.patterns?.seasonal_anomalies || [],
          pointAnomalies: data.patterns?.point_anomalies || [],
          contextualAnomalies: data.patterns?.contextual_anomalies || []
        },
        insights: {
          rootCauses: data.insights?.root_causes || [],
          correlations: data.insights?.correlations || [],
          impactAssessment: data.insights?.impact_assessment || {}
        },
        recommendations: data.recommendations || [],
        forecasting: {
          futureAnomalies: data.forecasting?.future_anomalies || [],
          riskPeriods: data.forecasting?.risk_periods || [],
          preventiveMeasures: data.forecasting?.preventive_measures || []
        },
        metadata: {
          modelVersion: data.model_version || 'v1.0',
          detectionDate: data.detection_date || new Date().toISOString(),
          isFallback: data.is_fallback || false
        }
      };
    } catch (error) {
      winston.error('Error mapping anomaly response:', error);
      throw new Error(`Anomaly response mapping failed: ${error.message}`);
    }
  }

  static validateBackendData(data) {
    const errors = [];
    const warnings = [];
    
    if (!data.organizationId) errors.push('Organization ID is required');
    if (!data.metrics || !Array.isArray(data.metrics)) warnings.push('Metrics data is missing');
    if (!data.dataPoints || data.dataPoints.length < 50) warnings.push('Insufficient data points for anomaly detection');
    
    return {
      isValid: errors.length === 0,
      errors,
      warnings,
      dataQuality: warnings.length === 0 ? 'excellent' : warnings.length <= 2 ? 'good' : 'poor'
    };
  }

  static validateAIMLResponse(aimlResponse) {
    const errors = [];
    
    if (!aimlResponse?.data) errors.push('AI/ML anomaly response data is missing');
    if (aimlResponse.data && typeof aimlResponse.data.anomalies_detected !== 'number') {
      errors.push('Anomalies detected count is missing or invalid');
    }
    
    return { isValid: errors.length === 0, errors };
  }

  static createCacheKey(data, options = {}) {
    const orgId = data.organizationId;
    const method = options.detectionMethod || 'ensemble';
    const timestamp = Math.floor(Date.now() / (1000 * 60 * 60 * 6)); // 6-hour caching
    return `anomaly_${orgId}_${method}_${timestamp}`;
  }
}

module.exports = AnomalyMapper;
