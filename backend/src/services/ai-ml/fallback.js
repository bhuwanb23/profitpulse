const winston = require('winston');

/**
 * AI/ML Fallback Service
 * Provides cached responses and simulated data when AI/ML service is unavailable
 */
class AIMLFallbackService {
  constructor() {
    this.cache = new Map();
    this.maxCacheSize = 1000;
    this.defaultTTL = 5 * 60 * 1000; // 5 minutes
    
    // Initialize simulated responses
    this.simulatedResponses = this.initializeSimulatedResponses();
    
    winston.info('AI/ML Fallback Service initialized');
  }

  /**
   * Initialize simulated responses for different models
   */
  initializeSimulatedResponses() {
    return {
      profitability: {
        predict: (data) => ({
          success: true,
          data: {
            profitability_score: 0.75 + (Math.random() * 0.2 - 0.1), // 0.65-0.85
            confidence: 0.8,
            factors: {
              revenue_trend: Math.random() > 0.5 ? 'positive' : 'stable',
              cost_efficiency: 0.7 + (Math.random() * 0.2),
              client_satisfaction: 0.8 + (Math.random() * 0.15),
              service_utilization: 0.75 + (Math.random() * 0.2)
            },
            recommendations: [
              'Optimize service delivery processes',
              'Review pricing strategy for underperforming services',
              'Focus on high-value client segments'
            ],
            prediction_date: new Date().toISOString(),
            model_version: 'fallback-v1.0',
            is_fallback: true
          }
        })
      },

      churn: {
        predict: (data) => ({
          success: true,
          data: {
            churn_probability: Math.random() * 0.3, // 0-30% churn risk
            risk_level: Math.random() > 0.7 ? 'high' : Math.random() > 0.4 ? 'medium' : 'low',
            confidence: 0.75,
            risk_factors: [
              'Decreased ticket volume',
              'Payment delays',
              'Reduced engagement'
            ].filter(() => Math.random() > 0.5),
            retention_recommendations: [
              'Schedule regular check-ins',
              'Provide proactive support',
              'Offer service optimization review'
            ],
            time_to_churn: Math.floor(Math.random() * 90) + 30, // 30-120 days
            prediction_date: new Date().toISOString(),
            model_version: 'fallback-v1.0',
            is_fallback: true
          }
        })
      },

      revenue_leak: {
        detect: (data) => ({
          success: true,
          data: {
            leaks_detected: Math.floor(Math.random() * 5) + 1,
            total_leak_amount: Math.floor(Math.random() * 50000) + 5000,
            leak_categories: [
              {
                category: 'unbilled_hours',
                amount: Math.floor(Math.random() * 20000) + 2000,
                confidence: 0.8,
                description: 'Hours worked but not billed to clients'
              },
              {
                category: 'underpriced_services',
                amount: Math.floor(Math.random() * 15000) + 1500,
                confidence: 0.7,
                description: 'Services priced below market rate'
              }
            ].filter(() => Math.random() > 0.3),
            recommendations: [
              'Implement automated time tracking',
              'Review and update service pricing',
              'Establish regular billing audits'
            ],
            detection_date: new Date().toISOString(),
            model_version: 'fallback-v1.0',
            is_fallback: true
          }
        })
      },

      pricing: {
        recommend: (data) => ({
          success: true,
          data: {
            recommended_price: Math.floor(Math.random() * 200) + 100,
            price_range: {
              min: Math.floor(Math.random() * 50) + 80,
              max: Math.floor(Math.random() * 100) + 250
            },
            confidence: 0.75,
            market_position: Math.random() > 0.5 ? 'competitive' : 'premium',
            factors: {
              market_rate: Math.floor(Math.random() * 50) + 120,
              complexity_score: Math.random() * 0.5 + 0.5,
              client_value: Math.random() * 0.4 + 0.6,
              competition_level: Math.random() > 0.5 ? 'high' : 'medium'
            },
            recommendations: [
              'Consider value-based pricing model',
              'Monitor competitor pricing regularly',
              'Implement tiered pricing structure'
            ],
            recommendation_date: new Date().toISOString(),
            model_version: 'fallback-v1.0',
            is_fallback: true
          }
        })
      },

      budget: {
        optimize: (data) => ({
          success: true,
          data: {
            optimization_score: 0.7 + (Math.random() * 0.2),
            potential_savings: Math.floor(Math.random() * 25000) + 5000,
            optimizations: [
              {
                category: 'infrastructure',
                current_spend: Math.floor(Math.random() * 20000) + 10000,
                recommended_spend: Math.floor(Math.random() * 15000) + 8000,
                savings: Math.floor(Math.random() * 5000) + 1000,
                confidence: 0.8
              },
              {
                category: 'software_licenses',
                current_spend: Math.floor(Math.random() * 15000) + 5000,
                recommended_spend: Math.floor(Math.random() * 12000) + 4000,
                savings: Math.floor(Math.random() * 3000) + 500,
                confidence: 0.75
              }
            ].filter(() => Math.random() > 0.3),
            recommendations: [
              'Consolidate software licenses',
              'Optimize infrastructure utilization',
              'Implement cost monitoring tools'
            ],
            optimization_date: new Date().toISOString(),
            model_version: 'fallback-v1.0',
            is_fallback: true
          }
        })
      },

      demand: {
        forecast: (data) => ({
          success: true,
          data: {
            forecast_horizon: 30,
            predictions: Array.from({ length: 30 }, (_, i) => ({
              date: new Date(Date.now() + i * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
              demand: Math.floor(Math.random() * 50) + 75,
              confidence: 0.7 + (Math.random() * 0.2),
              trend: Math.random() > 0.6 ? 'increasing' : Math.random() > 0.3 ? 'stable' : 'decreasing'
            })),
            seasonality_detected: Math.random() > 0.5,
            trend_direction: Math.random() > 0.5 ? 'upward' : 'stable',
            confidence: 0.75,
            recommendations: [
              'Prepare for peak demand periods',
              'Optimize resource allocation',
              'Consider capacity planning adjustments'
            ],
            forecast_date: new Date().toISOString(),
            model_version: 'fallback-v1.0',
            is_fallback: true
          }
        })
      },

      anomaly: {
        detect: (data) => ({
          success: true,
          data: {
            anomalies_detected: Math.floor(Math.random() * 3),
            anomalies: [
              {
                timestamp: new Date(Date.now() - Math.random() * 24 * 60 * 60 * 1000).toISOString(),
                metric: 'response_time',
                value: Math.floor(Math.random() * 1000) + 500,
                expected_range: [100, 300],
                severity: Math.random() > 0.7 ? 'high' : 'medium',
                confidence: 0.8
              },
              {
                timestamp: new Date(Date.now() - Math.random() * 12 * 60 * 60 * 1000).toISOString(),
                metric: 'error_rate',
                value: Math.random() * 0.1,
                expected_range: [0, 0.02],
                severity: 'medium',
                confidence: 0.75
              }
            ].filter(() => Math.random() > 0.4),
            recommendations: [
              'Investigate performance bottlenecks',
              'Review system logs for errors',
              'Monitor resource utilization'
            ],
            detection_date: new Date().toISOString(),
            model_version: 'fallback-v1.0',
            is_fallback: true
          }
        })
      }
    };
  }

  /**
   * Get fallback response for a specific model and method
   * @param {string} model - Model name (profitability, churn, etc.)
   * @param {string} method - Method name (predict, detect, etc.)
   * @param {Object} data - Request data
   * @param {Object} options - Additional options
   * @returns {Promise<Object>} - Fallback response
   */
  async getFallbackResponse(model, method, data = {}, options = {}) {
    try {
      // Check cache first
      const cacheKey = this.generateCacheKey(model, method, data);
      const cachedResponse = this.getFromCache(cacheKey);
      
      if (cachedResponse) {
        winston.debug('Returning cached fallback response', { model, method, cacheKey });
        return cachedResponse;
      }
      
      // Generate simulated response
      const simulatedResponse = this.generateSimulatedResponse(model, method, data);
      
      // Cache the response
      this.setCache(cacheKey, simulatedResponse, options.ttl || this.defaultTTL);
      
      winston.info('Generated fallback response', { 
        model, 
        method, 
        cacheKey,
        dataSize: JSON.stringify(data).length 
      });
      
      return simulatedResponse;
      
    } catch (error) {
      winston.error('Error generating fallback response', { 
        model, 
        method, 
        error: error.message 
      });
      
      // Return basic error response
      return {
        success: false,
        error: 'Fallback service error',
        message: 'Unable to generate fallback response',
        is_fallback: true,
        timestamp: new Date().toISOString()
      };
    }
  }

  /**
   * Generate simulated response for a model/method combination
   * @param {string} model - Model name
   * @param {string} method - Method name
   * @param {Object} data - Request data
   * @returns {Object} - Simulated response
   */
  generateSimulatedResponse(model, method, data) {
    const modelHandlers = this.simulatedResponses[model];
    
    if (!modelHandlers) {
      throw new Error(`No fallback handler for model: ${model}`);
    }
    
    const methodHandler = modelHandlers[method];
    
    if (!methodHandler) {
      throw new Error(`No fallback handler for method: ${model}.${method}`);
    }
    
    // Add some realistic delay to simulate processing
    const delay = Math.floor(Math.random() * 100) + 50; // 50-150ms
    
    return new Promise(resolve => {
      setTimeout(() => {
        const response = methodHandler(data);
        resolve(response);
      }, delay);
    });
  }

  /**
   * Generate cache key for request
   * @param {string} model - Model name
   * @param {string} method - Method name
   * @param {Object} data - Request data
   * @returns {string} - Cache key
   */
  generateCacheKey(model, method, data) {
    // Create a hash of the request data for caching
    const dataStr = JSON.stringify(data);
    const hash = this.simpleHash(dataStr);
    return `${model}_${method}_${hash}`;
  }

  /**
   * Simple hash function for cache keys
   * @param {string} str - String to hash
   * @returns {string} - Hash
   */
  simpleHash(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash; // Convert to 32-bit integer
    }
    return Math.abs(hash).toString(36);
  }

  /**
   * Set cache entry
   * @param {string} key - Cache key
   * @param {Object} value - Value to cache
   * @param {number} ttl - Time to live in ms
   */
  setCache(key, value, ttl = this.defaultTTL) {
    // Implement LRU eviction if cache is full
    if (this.cache.size >= this.maxCacheSize) {
      const firstKey = this.cache.keys().next().value;
      this.cache.delete(firstKey);
    }
    
    const expiresAt = Date.now() + ttl;
    this.cache.set(key, {
      value,
      expiresAt,
      createdAt: Date.now()
    });
    
    winston.debug('Cached fallback response', { key, ttl, cacheSize: this.cache.size });
  }

  /**
   * Get cache entry
   * @param {string} key - Cache key
   * @returns {Object|null} - Cached value or null
   */
  getFromCache(key) {
    const entry = this.cache.get(key);
    
    if (!entry) {
      return null;
    }
    
    // Check if expired
    if (Date.now() > entry.expiresAt) {
      this.cache.delete(key);
      winston.debug('Cache entry expired', { key });
      return null;
    }
    
    winston.debug('Cache hit', { key, age: Date.now() - entry.createdAt });
    return entry.value;
  }

  /**
   * Clear cache
   * @param {string} pattern - Optional pattern to match keys
   */
  clearCache(pattern = null) {
    if (!pattern) {
      this.cache.clear();
      winston.info('Cleared all fallback cache');
      return;
    }
    
    const regex = new RegExp(pattern);
    let cleared = 0;
    
    for (const key of this.cache.keys()) {
      if (regex.test(key)) {
        this.cache.delete(key);
        cleared++;
      }
    }
    
    winston.info('Cleared fallback cache entries', { pattern, cleared });
  }

  /**
   * Get cache statistics
   * @returns {Object} - Cache stats
   */
  getCacheStats() {
    const now = Date.now();
    let expired = 0;
    let totalAge = 0;
    
    for (const [key, entry] of this.cache.entries()) {
      if (now > entry.expiresAt) {
        expired++;
      } else {
        totalAge += now - entry.createdAt;
      }
    }
    
    const active = this.cache.size - expired;
    const averageAge = active > 0 ? totalAge / active : 0;
    
    return {
      totalEntries: this.cache.size,
      activeEntries: active,
      expiredEntries: expired,
      maxSize: this.maxCacheSize,
      utilizationRate: (this.cache.size / this.maxCacheSize) * 100,
      averageAge: Math.round(averageAge),
      defaultTTL: this.defaultTTL
    };
  }

  /**
   * Check if fallback is available for model/method
   * @param {string} model - Model name
   * @param {string} method - Method name
   * @returns {boolean} - True if fallback available
   */
  isAvailable(model, method) {
    return !!(this.simulatedResponses[model] && this.simulatedResponses[model][method]);
  }

  /**
   * Get list of available fallback handlers
   * @returns {Object} - Available handlers
   */
  getAvailableHandlers() {
    const handlers = {};
    
    for (const [model, methods] of Object.entries(this.simulatedResponses)) {
      handlers[model] = Object.keys(methods);
    }
    
    return handlers;
  }

  /**
   * Clean up expired cache entries
   */
  cleanupCache() {
    const now = Date.now();
    let cleaned = 0;
    
    for (const [key, entry] of this.cache.entries()) {
      if (now > entry.expiresAt) {
        this.cache.delete(key);
        cleaned++;
      }
    }
    
    if (cleaned > 0) {
      winston.debug('Cleaned up expired cache entries', { cleaned, remaining: this.cache.size });
    }
  }

  /**
   * Start periodic cache cleanup
   * @param {number} interval - Cleanup interval in ms (default: 5 minutes)
   */
  startCacheCleanup(interval = 5 * 60 * 1000) {
    this.cleanupInterval = setInterval(() => {
      this.cleanupCache();
    }, interval);
    
    winston.info('Started fallback cache cleanup', { interval });
  }

  /**
   * Stop periodic cache cleanup
   */
  stopCacheCleanup() {
    if (this.cleanupInterval) {
      clearInterval(this.cleanupInterval);
      this.cleanupInterval = null;
      winston.info('Stopped fallback cache cleanup');
    }
  }

  /**
   * Destroy fallback service
   */
  destroy() {
    this.stopCacheCleanup();
    this.cache.clear();
    winston.info('AI/ML Fallback Service destroyed');
  }
}

module.exports = AIMLFallbackService;
