const axios = require('axios');
const winston = require('winston');
const { getConfig } = require('../../config/aiml');
const RetryUtility = require('../../utils/retry');
const { CircuitBreaker } = require('./circuitBreaker');
const AIMLHealthMonitor = require('./healthMonitor');
const AIMLFallbackService = require('./fallback');
const AIMLMetrics = require('./metrics');
const aimlLogger = require('../../utils/aimlLogger');

class AIClient {
  constructor() {
    // Get configuration from centralized config
    this.config = getConfig();
    this.baseUrl = this.config.baseUrl;
    this.apiKey = this.config.apiKey;
    this.timeout = this.config.timeout;
    
    // Initialize services
    this.metrics = new AIMLMetrics();
    this.fallbackService = new AIMLFallbackService();
    
    // Initialize circuit breaker
    this.circuitBreaker = new CircuitBreaker({
      threshold: this.config.circuitBreaker.threshold,
      timeout: this.config.circuitBreaker.timeout,
      resetTimeout: this.config.circuitBreaker.resetTimeout,
      expectedErrors: ['ValidationError', 'AuthenticationError']
    });
    
    // Initialize health monitor
    this.healthMonitor = new AIMLHealthMonitor(this, this.config.health);
    
    // Create axios instance with default configuration
    this.client = axios.create({
      baseURL: this.baseUrl,
      timeout: this.timeout,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.apiKey}`
      }
    });
    
    // Setup event listeners
    this.setupEventListeners();
    
    // Start services (don't await to avoid blocking)
    this.initialize().catch(error => {
      winston.error('AI/ML Client initialization failed:', error);
    });

    // Setup axios interceptors
    this.setupInterceptors();
  }
  
  /**
   * Initialize AI client services
   */
  async initialize() {
    try {
      // Start fallback cache cleanup
      this.fallbackService.startCacheCleanup();
      
      // Start health monitoring if enabled
      if (this.config.features.enableMetrics) {
        this.healthMonitor.startMonitoring();
      }
      
      winston.info('AI/ML Client initialized successfully', {
        baseUrl: this.baseUrl,
        timeout: this.timeout,
        circuitBreakerEnabled: this.config.features.enableCircuitBreaker,
        metricsEnabled: this.config.features.enableMetrics
      });
      
    } catch (error) {
      winston.error('Failed to initialize AI/ML Client:', error);
      throw error;
    }
  }
  
  /**
   * Setup event listeners for services
   */
  setupEventListeners() {
    // Circuit breaker events
    this.circuitBreaker.on('stateChange', (event) => {
      aimlLogger.logCircuitBreakerStateChange(event.from, event.to, event.reason);
      this.metrics.recordCircuitBreakerTrip(event.reason);
    });
    
    // Health monitor events
    this.healthMonitor.on('serviceHealthy', () => {
      winston.info('AI/ML service is healthy');
    });
    
    this.healthMonitor.on('serviceUnhealthy', () => {
      winston.warn('AI/ML service is unhealthy');
    });
  }
  
  /**
   * Setup axios interceptors
   */
  setupInterceptors() {
    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        const context = aimlLogger.createRequestContext();
        config.metadata = { ...context, startTime: Date.now() };
        
        if (this.config.logging.enableRequestLogging) {
          aimlLogger.logRequest(
            config.method,
            config.url,
            config.data,
            {
              requestId: context.requestId,
              timeout: config.timeout
            }
          );
        }
        
        this.metrics.recordRequest(config.method, config.url);
        return config;
      },
      (error) => {
        winston.error('AI/ML API Request Setup Error:', error);
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response) => {
        const duration = Date.now() - response.config.metadata.startTime;
        
        if (this.config.logging.enableResponseLogging) {
          aimlLogger.logResponse(
            response.config.method,
            response.config.url,
            response.status,
            response.data,
            duration,
            {
              requestId: response.config.metadata.requestId
            }
          );
        }
        
        this.metrics.recordSuccess(
          response.config.method,
          response.config.url,
          duration
        );
        
        return response;
      },
      (error) => {
        const duration = error.config ? Date.now() - error.config.metadata.startTime : 0;
        
        aimlLogger.logError(
          error.config?.method || 'unknown',
          error.config?.url || 'unknown',
          error,
          duration,
          0,
          {
            requestId: error.config?.metadata?.requestId
          }
        );
        
        this.metrics.recordFailure(
          error.config?.method || 'unknown',
          error.config?.url || 'unknown',
          error,
          duration
        );
        
        return Promise.reject(error);
      }
    );
  }

  /**
   * Execute request with all enhancements (retry, circuit breaker, fallback)
   * @param {Function} requestFn - Function that makes the HTTP request
   * @param {string} model - Model name for fallback
   * @param {string} method - Method name for fallback
   * @param {Object} data - Request data for fallback
   * @param {Object} options - Additional options
   * @returns {Promise<Object>} Response data
   */
  async executeRequest(requestFn, model, method, data = {}, options = {}) {
    const {
      useCircuitBreaker = this.config.features.enableCircuitBreaker,
      useFallback = this.config.features.enableFallback,
      retryOptions = {}
    } = options;
    
    try {
      let result;
      
      if (useCircuitBreaker) {
        // Use circuit breaker with retry
        result = await RetryUtility.withCircuitBreakerRetry(
          requestFn,
          this.circuitBreaker,
          {
            retries: this.config.retries,
            delay: this.config.retryDelay,
            backoff: this.config.retryBackoff,
            context: `${model}.${method}`,
            onRetry: (error, attempt) => {
              aimlLogger.logRetry(
                'POST',
                `/${model}/${method}`,
                attempt,
                this.config.retries,
                this.config.retryDelay * Math.pow(this.config.retryBackoff, attempt - 1),
                error
              );
              this.metrics.recordRetry(error.message, attempt, model);
            },
            ...retryOptions
          }
        );
      } else {
        // Use regular retry
        result = await RetryUtility.withAIMLRetry(requestFn, {
          retries: this.config.retries,
          delay: this.config.retryDelay,
          backoff: this.config.retryBackoff,
          context: `${model}.${method}`,
          ...retryOptions
        });
      }
      
      return result.data;
      
    } catch (error) {
      winston.warn(`AI/ML request failed for ${model}.${method}:`, error.message);
      
      // Try fallback if enabled
      if (useFallback && this.fallbackService.isAvailable(model, method)) {
        aimlLogger.logFallback('POST', `/${model}/${method}`, 'simulated', error);
        this.metrics.recordFallback('simulated', model, error.message);
        
        return await this.fallbackService.getFallbackResponse(model, method, data, options);
      }
      
      throw error;
    }
  }
  
  /**
   * Health check for the AI/ML service
   * @returns {Promise<Object>} Health status
   */
  async healthCheck() {
    try {
      const response = await this.client.get('/api/health');
      return response.data;
    } catch (error) {
      throw new Error(`Health check failed: ${error.message}`);
    }
  }
  
  /**
   * Get comprehensive health status including all services
   * @returns {Promise<Object>} Complete health status
   */
  async getHealthStatus() {
    return {
      client: {
        initialized: true,
        baseUrl: this.baseUrl,
        timeout: this.timeout
      },
      circuitBreaker: this.circuitBreaker.getStatus(),
      healthMonitor: this.healthMonitor.getHealthStatus(),
      metrics: this.metrics.getMetricsSummary(),
      fallback: {
        available: true,
        handlers: this.fallbackService.getAvailableHandlers(),
        cacheStats: this.fallbackService.getCacheStats()
      }
    };
  }

  /**
   * Predict client profitability
   * @param {Object} data - Client data for prediction
   * @param {Object} options - Prediction options
   * @returns {Promise<Object>} Prediction result
   */
  async predictProfitability(data, options = {}) {
    return this.executeRequest(
      () => this.client.post('/api/profitability', data, {
        params: {
          model_version: options.modelVersion,
          return_confidence: options.returnConfidence || false,
          return_explanation: options.returnExplanation || false
        }
      }),
      'profitability',
      'predict',
      data,
      options
    );
  }

  /**
   * Predict client churn
   * @param {Object} data - Client data for prediction
   * @param {Object} options - Prediction options
   * @returns {Promise<Object>} Prediction result
   */
  async predictChurn(data, options = {}) {
    return this.executeRequest(
      () => this.client.post('/api/churn/predict', data, {
        params: {
          model_version: options.modelVersion
        }
      }),
      'churn',
      'predict',
      data,
      options
    );
  }

  /**
   * Detect revenue leaks
   * @param {Object} data - Billing and service data
   * @param {Object} options - Detection options
   * @returns {Promise<Object>} Detection result
   */
  async detectRevenueLeaks(data, options = {}) {
    return this.executeRequest(
      () => this.client.post('/api/revenue-leak/detect', data, {
        params: {
          model_version: options.modelVersion
        }
      }),
      'revenue_leak',
      'detect',
      data,
      options
    );
  }

  /**
   * Get dynamic pricing recommendation
   * @param {Object} data - Client and market data
   * @param {Object} options - Pricing options
   * @returns {Promise<Object>} Pricing recommendation
   */
  async getDynamicPricing(data, options = {}) {
    return this.executeRequest(
      () => this.client.post('/api/pricing/recommend', data, {
        params: {
          model_version: options.modelVersion
        }
      }),
      'pricing',
      'recommend',
      data,
      options
    );
  }

  /**
   * Optimize budget allocation
   * @param {Object} data - Budget and department data
   * @param {Object} options - Optimization options
   * @returns {Promise<Object>} Optimization result
   */
  async optimizeBudget(data, options = {}) {
    return this.executeRequest(
      () => this.client.post('/api/budget/optimize', data, {
        params: {
          model_version: options.modelVersion
        }
      }),
      'budget',
      'optimize',
      data,
      options
    );
  }

  /**
   * Forecast demand
   * @param {Object} data - Historical demand data
   * @param {Object} options - Forecasting options
   * @returns {Promise<Object>} Forecast result
   */
  async forecastDemand(data, options = {}) {
    return this.executeRequest(
      () => this.client.post('/api/demand/forecast', data, {
        params: {
          model_version: options.modelVersion,
          forecast_horizon: options.forecastHorizon || 30,
          seasonality: options.seasonality !== false
        }
      }),
      'demand',
      'forecast',
      data,
      options
    );
  }

  /**
   * Detect anomalies
   * @param {Object} data - Time series data
   * @param {Object} options - Detection options
   * @returns {Promise<Object>} Anomaly detection result
   */
  async detectAnomalies(data, options = {}) {
    return this.executeRequest(
      () => this.client.post('/api/anomaly/detect', data, {
        params: {
          model_version: options.modelVersion,
          detection_method: options.detectionMethod || 'ensemble',
          window_size: options.windowSize || 100
        }
      }),
      'anomaly',
      'detect',
      data,
      options
    );
  }

  /**
   * Get model information
   * @param {string} modelName - Name of the model
   * @returns {Promise<Object>} Model information
   */
  async getModelInfo(modelName) {
    try {
      const response = await this.client.get(`/api/models/${modelName}/info`);
      return response.data;
    } catch (error) {
      throw new Error(`Getting model info failed: ${error.message}`);
    }
  }

  /**
   * Get model health status
   * @param {string} modelName - Name of the model
   * @returns {Promise<Object>} Model health status
   */
  async getModelHealth(modelName) {
    try {
      const response = await this.client.get(`/api/models/${modelName}/health`);
      return response.data;
    } catch (error) {
      throw new Error(`Getting model health failed: ${error.message}`);
    }
  }

  /**
   * Perform batch predictions
   * @param {string} modelName - Name of the model to use
   * @param {Array} data - Array of data for predictions
   * @param {Object} options - Batch options
   * @returns {Promise<Object>} Batch prediction result
   */
  async batchPredict(modelName, data, options = {}) {
    try {
      const response = await this.client.post(`/api/${modelName}/batch`, { data }, {
        params: {
          model_version: options.modelVersion
        }
      });
      return response.data;
    } catch (error) {
      throw new Error(`Batch prediction failed: ${error.message}`);
    }
  }

  /**
   * Reset circuit breaker
   */
  resetCircuitBreaker() {
    this.circuitBreaker.reset();
    winston.info('Circuit breaker reset manually');
  }
  
  /**
   * Get metrics summary
   * @returns {Object} Metrics summary
   */
  getMetrics() {
    return this.metrics.getMetricsSummary();
  }
  
  /**
   * Clear fallback cache
   * @param {string} pattern - Optional pattern to match keys
   */
  clearFallbackCache(pattern = null) {
    this.fallbackService.clearCache(pattern);
  }
  
  /**
   * Destroy client and cleanup resources
   */
  destroy() {
    this.healthMonitor.destroy();
    this.fallbackService.destroy();
    this.circuitBreaker.removeAllListeners();
    winston.info('AI/ML Client destroyed');
  }
}

// Export singleton instance
module.exports = new AIClient();