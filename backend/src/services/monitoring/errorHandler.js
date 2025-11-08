const winston = require('winston');
const { v4: uuidv4 } = require('uuid');

class ErrorHandler {
  constructor() {
    this.errorStats = {
      total: 0,
      byType: {},
      byService: {},
      byEndpoint: {},
      last24Hours: []
    };
    
    this.retryConfig = {
      maxRetries: 3,
      baseDelay: 1000, // 1 second
      maxDelay: 30000, // 30 seconds
      backoffFactor: 2
    };

    this.fallbackData = new Map();
    this.initializeFallbackData();
  }

  /**
   * Initialize fallback data for when AI/ML service is down
   */
  initializeFallbackData() {
    // Fallback profitability data
    this.fallbackData.set('profitability', {
      profitability_score: 0.75,
      confidence: 0.60,
      risk_level: 'medium',
      factors: [
        { factor: 'historical_performance', impact: 0.3, description: 'Based on historical data' },
        { factor: 'service_utilization', impact: 0.25, description: 'Service usage patterns' }
      ],
      recommendations: ['Monitor service usage', 'Review pricing strategy'],
      is_fallback: true,
      fallback_reason: 'AI/ML service unavailable'
    });

    // Fallback churn data
    this.fallbackData.set('churn', {
      churn_probability: 0.35,
      risk_level: 'medium',
      confidence: 0.55,
      risk_factors: [
        { factor: 'payment_history', impact: 0.4, description: 'Payment patterns analysis' },
        { factor: 'support_tickets', impact: 0.3, description: 'Support interaction frequency' }
      ],
      recommendations: ['Increase customer engagement', 'Review service quality'],
      is_fallback: true,
      fallback_reason: 'AI/ML service unavailable'
    });

    // Fallback revenue leak data
    this.fallbackData.set('revenue_leak', {
      total_leak_amount: 5000,
      leak_categories: [
        { category: 'underutilized_services', amount: 2000, percentage: 40 },
        { category: 'pricing_gaps', amount: 1500, percentage: 30 },
        { category: 'billing_errors', amount: 1500, percentage: 30 }
      ],
      confidence: 0.50,
      recommendations: ['Review service utilization', 'Audit pricing structure'],
      is_fallback: true,
      fallback_reason: 'AI/ML service unavailable'
    });

    // Add more fallback data for other models
    this.fallbackData.set('pricing', {
      recommended_price: 150,
      price_range: { min: 120, max: 180 },
      confidence: 0.55,
      factors: ['market_analysis', 'cost_structure'],
      is_fallback: true,
      fallback_reason: 'AI/ML service unavailable'
    });

    this.fallbackData.set('budget', {
      optimized_allocation: {
        infrastructure: 40,
        personnel: 35,
        marketing: 15,
        operations: 10
      },
      projected_savings: 8500,
      confidence: 0.50,
      is_fallback: true,
      fallback_reason: 'AI/ML service unavailable'
    });

    this.fallbackData.set('demand', {
      forecasted_demand: 125,
      trend: 'stable',
      confidence: 0.55,
      seasonal_factors: ['end_of_quarter', 'business_growth'],
      is_fallback: true,
      fallback_reason: 'AI/ML service unavailable'
    });

    this.fallbackData.set('anomaly', {
      anomalies_detected: 2,
      severity_distribution: { low: 1, medium: 1, high: 0 },
      confidence: 0.50,
      recommendations: ['Monitor system performance', 'Review recent changes'],
      is_fallback: true,
      fallback_reason: 'AI/ML service unavailable'
    });
  }

  /**
   * Handle errors with retry logic and exponential backoff
   * @param {Function} operation - Operation to retry
   * @param {Object} context - Error context
   * @param {Object} options - Retry options
   * @returns {Promise<any>} Operation result
   */
  async handleWithRetry(operation, context = {}, options = {}) {
    const config = { ...this.retryConfig, ...options };
    const correlationId = context.correlationId || uuidv4();
    
    let lastError;
    
    for (let attempt = 0; attempt <= config.maxRetries; attempt++) {
      try {
        const result = await operation();
        
        if (attempt > 0) {
          winston.info('Operation succeeded after retry', {
            correlationId,
            attempt,
            context: context.operation || 'unknown'
          });
        }
        
        return result;
      } catch (error) {
        lastError = error;
        
        this.logError(error, {
          ...context,
          correlationId,
          attempt,
          maxRetries: config.maxRetries
        });

        if (attempt === config.maxRetries) {
          winston.error('Operation failed after all retries', {
            correlationId,
            totalAttempts: attempt + 1,
            finalError: error.message,
            context: context.operation || 'unknown'
          });
          break;
        }

        // Calculate delay with exponential backoff and jitter
        const delay = Math.min(
          config.baseDelay * Math.pow(config.backoffFactor, attempt),
          config.maxDelay
        );
        
        // Add jitter to prevent thundering herd
        const jitteredDelay = delay + (Math.random() * 1000);
        
        winston.warn('Retrying operation after delay', {
          correlationId,
          attempt: attempt + 1,
          delay: jitteredDelay,
          error: error.message
        });
        
        await this.sleep(jitteredDelay);
      }
    }

    // If all retries failed, try fallback
    if (context.modelType && this.fallbackData.has(context.modelType)) {
      winston.warn('Using fallback data after retry failure', {
        correlationId,
        modelType: context.modelType,
        error: lastError.message
      });
      
      return {
        success: true,
        data: this.fallbackData.get(context.modelType),
        is_fallback: true
      };
    }

    throw lastError;
  }

  /**
   * Log error with detailed context
   * @param {Error} error - Error object
   * @param {Object} context - Error context
   */
  logError(error, context = {}) {
    const errorId = uuidv4();
    const timestamp = new Date().toISOString();
    
    // Update error statistics
    this.errorStats.total++;
    
    const errorType = error.constructor.name;
    this.errorStats.byType[errorType] = (this.errorStats.byType[errorType] || 0) + 1;
    
    if (context.service) {
      this.errorStats.byService[context.service] = (this.errorStats.byService[context.service] || 0) + 1;
    }
    
    if (context.endpoint) {
      this.errorStats.byEndpoint[context.endpoint] = (this.errorStats.byEndpoint[context.endpoint] || 0) + 1;
    }

    // Add to 24-hour tracking
    this.errorStats.last24Hours.push({
      errorId,
      timestamp,
      type: errorType,
      message: error.message,
      service: context.service,
      endpoint: context.endpoint
    });

    // Keep only last 24 hours of errors
    const oneDayAgo = new Date(Date.now() - 24 * 60 * 60 * 1000);
    this.errorStats.last24Hours = this.errorStats.last24Hours.filter(
      err => new Date(err.timestamp) > oneDayAgo
    );

    // Log detailed error information
    winston.error('Detailed error log', {
      errorId,
      correlationId: context.correlationId,
      timestamp,
      error: {
        name: error.name,
        message: error.message,
        stack: error.stack,
        code: error.code,
        status: error.response?.status,
        statusText: error.response?.statusText
      },
      context: {
        service: context.service,
        endpoint: context.endpoint,
        operation: context.operation,
        attempt: context.attempt,
        maxRetries: context.maxRetries,
        userId: context.userId,
        organizationId: context.organizationId,
        modelType: context.modelType
      },
      request: {
        method: context.method,
        url: context.url,
        headers: context.headers ? this.sanitizeHeaders(context.headers) : undefined,
        body: context.body ? this.sanitizeBody(context.body) : undefined
      },
      response: {
        status: error.response?.status,
        statusText: error.response?.statusText,
        data: error.response?.data
      }
    });
  }

  /**
   * Get fallback data for a model type
   * @param {string} modelType - Model type
   * @param {Object} context - Request context
   * @returns {Object} Fallback data
   */
  getFallbackData(modelType, context = {}) {
    const fallbackData = this.fallbackData.get(modelType);
    
    if (!fallbackData) {
      winston.warn('No fallback data available for model type', { modelType });
      return {
        error: 'Service temporarily unavailable',
        is_fallback: true,
        fallback_reason: 'No fallback data configured'
      };
    }

    winston.info('Serving fallback data', {
      modelType,
      correlationId: context.correlationId,
      reason: 'AI/ML service unavailable'
    });

    return {
      ...fallbackData,
      served_at: new Date().toISOString(),
      correlation_id: context.correlationId
    };
  }

  /**
   * Check if error is retryable
   * @param {Error} error - Error object
   * @returns {boolean} Whether error is retryable
   */
  isRetryableError(error) {
    // Network errors are retryable
    if (error.code === 'ECONNREFUSED' || 
        error.code === 'ENOTFOUND' || 
        error.code === 'ETIMEDOUT' ||
        error.code === 'ECONNRESET') {
      return true;
    }

    // HTTP status codes that are retryable
    const retryableStatusCodes = [408, 429, 500, 502, 503, 504];
    if (error.response && retryableStatusCodes.includes(error.response.status)) {
      return true;
    }

    return false;
  }

  /**
   * Get error statistics
   * @returns {Object} Error statistics
   */
  getErrorStats() {
    const last24HoursCount = this.errorStats.last24Hours.length;
    const errorRate = last24HoursCount > 0 ? 
      (last24HoursCount / (24 * 60)).toFixed(2) : 0; // errors per minute

    return {
      ...this.errorStats,
      errorRate: `${errorRate}/min`,
      healthStatus: this.getHealthStatus()
    };
  }

  /**
   * Get system health status based on error rates
   * @returns {string} Health status
   */
  getHealthStatus() {
    const last24HoursCount = this.errorStats.last24Hours.length;
    const errorRate = last24HoursCount / (24 * 60); // errors per minute

    if (errorRate < 0.1) return 'healthy';
    if (errorRate < 0.5) return 'warning';
    return 'critical';
  }

  /**
   * Sanitize headers for logging (remove sensitive data)
   * @param {Object} headers - Request headers
   * @returns {Object} Sanitized headers
   */
  sanitizeHeaders(headers) {
    const sanitized = { ...headers };
    const sensitiveHeaders = ['authorization', 'cookie', 'x-api-key'];
    
    sensitiveHeaders.forEach(header => {
      if (sanitized[header]) {
        sanitized[header] = '[REDACTED]';
      }
    });

    return sanitized;
  }

  /**
   * Sanitize request body for logging (remove sensitive data)
   * @param {Object} body - Request body
   * @returns {Object} Sanitized body
   */
  sanitizeBody(body) {
    if (typeof body !== 'object') return body;
    
    const sanitized = { ...body };
    const sensitiveFields = ['password', 'token', 'secret', 'key'];
    
    sensitiveFields.forEach(field => {
      if (sanitized[field]) {
        sanitized[field] = '[REDACTED]';
      }
    });

    return sanitized;
  }

  /**
   * Sleep for specified milliseconds
   * @param {number} ms - Milliseconds to sleep
   * @returns {Promise} Promise that resolves after delay
   */
  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  /**
   * Create error context for tracking
   * @param {Object} req - Express request object
   * @param {string} service - Service name
   * @param {string} operation - Operation name
   * @returns {Object} Error context
   */
  createContext(req, service, operation) {
    return {
      correlationId: req.correlationId || uuidv4(),
      service,
      operation,
      endpoint: req.originalUrl,
      method: req.method,
      userId: req.user?.id,
      organizationId: req.body?.organization_id || req.query?.organization_id,
      userAgent: req.get('User-Agent'),
      ip: req.ip
    };
  }

  /**
   * Reset error statistics
   */
  resetStats() {
    this.errorStats = {
      total: 0,
      byType: {},
      byService: {},
      byEndpoint: {},
      last24Hours: []
    };
    
    winston.info('Error statistics reset');
  }
}

// Export singleton instance
module.exports = new ErrorHandler();
