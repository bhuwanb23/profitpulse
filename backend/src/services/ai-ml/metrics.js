const winston = require('winston');

/**
 * AI/ML Metrics Collection Service
 * Collects and analyzes performance metrics for AI/ML service interactions
 */
class AIMLMetrics {
  constructor() {
    this.metrics = {
      // Request metrics
      totalRequests: 0,
      successfulRequests: 0,
      failedRequests: 0,
      
      // Response time metrics
      totalResponseTime: 0,
      averageResponseTime: 0,
      minResponseTime: Infinity,
      maxResponseTime: 0,
      
      // Error metrics
      errorsByType: new Map(),
      errorsByModel: new Map(),
      
      // Model usage metrics
      modelUsage: new Map(),
      
      // Cache metrics
      cacheHits: 0,
      cacheMisses: 0,
      
      // Circuit breaker metrics
      circuitBreakerTrips: 0,
      
      // Retry metrics
      totalRetries: 0,
      retriesByReason: new Map(),
      
      // Fallback metrics
      fallbackUsage: new Map()
    };
    
    // Time-based metrics (sliding windows)
    this.timeWindows = {
      '1min': { duration: 60 * 1000, data: [] },
      '5min': { duration: 5 * 60 * 1000, data: [] },
      '15min': { duration: 15 * 60 * 1000, data: [] },
      '1hour': { duration: 60 * 60 * 1000, data: [] }
    };
    
    // Performance percentiles
    this.responseTimes = [];
    this.maxResponseTimeHistory = 1000; // Keep last 1000 response times
    
    // Start time for uptime calculation
    this.startTime = Date.now();
    
    winston.info('AI/ML Metrics service initialized');
  }

  /**
   * Record a request
   * @param {string} method - HTTP method
   * @param {string} url - Request URL
   * @param {string} modelName - Model name
   * @param {Object} options - Additional options
   */
  recordRequest(method, url, modelName = null, options = {}) {
    this.metrics.totalRequests++;
    
    if (modelName) {
      const usage = this.metrics.modelUsage.get(modelName) || 0;
      this.metrics.modelUsage.set(modelName, usage + 1);
    }
    
    // Add to time windows
    const timestamp = Date.now();
    this.addToTimeWindows('request', { timestamp, method, url, modelName, ...options });
    
    winston.debug('Request recorded', { method, url, modelName, total: this.metrics.totalRequests });
  }

  /**
   * Record a successful response
   * @param {string} method - HTTP method
   * @param {string} url - Request URL
   * @param {number} responseTime - Response time in ms
   * @param {string} modelName - Model name
   * @param {Object} options - Additional options
   */
  recordSuccess(method, url, responseTime, modelName = null, options = {}) {
    this.metrics.successfulRequests++;
    this.updateResponseTimeMetrics(responseTime);
    
    // Add to time windows
    const timestamp = Date.now();
    this.addToTimeWindows('success', { 
      timestamp, 
      method, 
      url, 
      responseTime, 
      modelName, 
      ...options 
    });
    
    winston.debug('Success recorded', { 
      method, 
      url, 
      responseTime, 
      modelName, 
      successRate: this.getSuccessRate() 
    });
  }

  /**
   * Record a failed request
   * @param {string} method - HTTP method
   * @param {string} url - Request URL
   * @param {Error} error - Error object
   * @param {number} responseTime - Response time in ms
   * @param {string} modelName - Model name
   * @param {Object} options - Additional options
   */
  recordFailure(method, url, error, responseTime = null, modelName = null, options = {}) {
    this.metrics.failedRequests++;
    
    if (responseTime !== null) {
      this.updateResponseTimeMetrics(responseTime);
    }
    
    // Record error by type
    const errorType = error.name || 'UnknownError';
    const errorCount = this.metrics.errorsByType.get(errorType) || 0;
    this.metrics.errorsByType.set(errorType, errorCount + 1);
    
    // Record error by model
    if (modelName) {
      const modelErrors = this.metrics.errorsByModel.get(modelName) || 0;
      this.metrics.errorsByModel.set(modelName, modelErrors + 1);
    }
    
    // Add to time windows
    const timestamp = Date.now();
    this.addToTimeWindows('failure', { 
      timestamp, 
      method, 
      url, 
      error: errorType, 
      responseTime, 
      modelName, 
      ...options 
    });
    
    winston.debug('Failure recorded', { 
      method, 
      url, 
      error: errorType, 
      modelName, 
      failureRate: this.getFailureRate() 
    });
  }

  /**
   * Record cache hit
   * @param {string} key - Cache key
   * @param {string} modelName - Model name
   */
  recordCacheHit(key, modelName = null) {
    this.metrics.cacheHits++;
    
    const timestamp = Date.now();
    this.addToTimeWindows('cache_hit', { timestamp, key, modelName });
    
    winston.debug('Cache hit recorded', { 
      key, 
      modelName, 
      hitRate: this.getCacheHitRate() 
    });
  }

  /**
   * Record cache miss
   * @param {string} key - Cache key
   * @param {string} modelName - Model name
   */
  recordCacheMiss(key, modelName = null) {
    this.metrics.cacheMisses++;
    
    const timestamp = Date.now();
    this.addToTimeWindows('cache_miss', { timestamp, key, modelName });
    
    winston.debug('Cache miss recorded', { 
      key, 
      modelName, 
      hitRate: this.getCacheHitRate() 
    });
  }

  /**
   * Record circuit breaker trip
   * @param {string} reason - Reason for trip
   */
  recordCircuitBreakerTrip(reason = 'threshold_exceeded') {
    this.metrics.circuitBreakerTrips++;
    
    const timestamp = Date.now();
    this.addToTimeWindows('circuit_breaker_trip', { timestamp, reason });
    
    winston.debug('Circuit breaker trip recorded', { 
      reason, 
      totalTrips: this.metrics.circuitBreakerTrips 
    });
  }

  /**
   * Record retry attempt
   * @param {string} reason - Reason for retry
   * @param {number} attempt - Attempt number
   * @param {string} modelName - Model name
   */
  recordRetry(reason, attempt, modelName = null) {
    this.metrics.totalRetries++;
    
    const retryCount = this.metrics.retriesByReason.get(reason) || 0;
    this.metrics.retriesByReason.set(reason, retryCount + 1);
    
    const timestamp = Date.now();
    this.addToTimeWindows('retry', { timestamp, reason, attempt, modelName });
    
    winston.debug('Retry recorded', { 
      reason, 
      attempt, 
      modelName, 
      totalRetries: this.metrics.totalRetries 
    });
  }

  /**
   * Record fallback usage
   * @param {string} fallbackType - Type of fallback used
   * @param {string} modelName - Model name
   * @param {string} reason - Reason for fallback
   */
  recordFallback(fallbackType, modelName = null, reason = 'service_unavailable') {
    const fallbackCount = this.metrics.fallbackUsage.get(fallbackType) || 0;
    this.metrics.fallbackUsage.set(fallbackType, fallbackCount + 1);
    
    const timestamp = Date.now();
    this.addToTimeWindows('fallback', { timestamp, fallbackType, modelName, reason });
    
    winston.debug('Fallback usage recorded', { 
      fallbackType, 
      modelName, 
      reason, 
      totalFallbacks: Array.from(this.metrics.fallbackUsage.values()).reduce((a, b) => a + b, 0) 
    });
  }

  /**
   * Update response time metrics
   * @param {number} responseTime - Response time in ms
   */
  updateResponseTimeMetrics(responseTime) {
    this.metrics.totalResponseTime += responseTime;
    this.metrics.averageResponseTime = this.metrics.totalResponseTime / this.metrics.totalRequests;
    this.metrics.minResponseTime = Math.min(this.metrics.minResponseTime, responseTime);
    this.metrics.maxResponseTime = Math.max(this.metrics.maxResponseTime, responseTime);
    
    // Keep response time history for percentile calculations
    this.responseTimes.push(responseTime);
    if (this.responseTimes.length > this.maxResponseTimeHistory) {
      this.responseTimes.shift();
    }
  }

  /**
   * Add data to time windows
   * @param {string} type - Event type
   * @param {Object} data - Event data
   */
  addToTimeWindows(type, data) {
    const now = Date.now();
    
    Object.keys(this.timeWindows).forEach(window => {
      this.timeWindows[window].data.push({ type, ...data });
      
      // Clean old data outside the window
      const cutoff = now - this.timeWindows[window].duration;
      this.timeWindows[window].data = this.timeWindows[window].data.filter(
        item => item.timestamp >= cutoff
      );
    });
  }

  /**
   * Get success rate
   * @returns {number} - Success rate as percentage
   */
  getSuccessRate() {
    if (this.metrics.totalRequests === 0) return 0;
    return (this.metrics.successfulRequests / this.metrics.totalRequests) * 100;
  }

  /**
   * Get failure rate
   * @returns {number} - Failure rate as percentage
   */
  getFailureRate() {
    if (this.metrics.totalRequests === 0) return 0;
    return (this.metrics.failedRequests / this.metrics.totalRequests) * 100;
  }

  /**
   * Get cache hit rate
   * @returns {number} - Cache hit rate as percentage
   */
  getCacheHitRate() {
    const totalCacheRequests = this.metrics.cacheHits + this.metrics.cacheMisses;
    if (totalCacheRequests === 0) return 0;
    return (this.metrics.cacheHits / totalCacheRequests) * 100;
  }

  /**
   * Get response time percentiles
   * @returns {Object} - Response time percentiles
   */
  getResponseTimePercentiles() {
    if (this.responseTimes.length === 0) {
      return { p50: 0, p90: 0, p95: 0, p99: 0 };
    }
    
    const sorted = [...this.responseTimes].sort((a, b) => a - b);
    const length = sorted.length;
    
    return {
      p50: sorted[Math.floor(length * 0.5)],
      p90: sorted[Math.floor(length * 0.9)],
      p95: sorted[Math.floor(length * 0.95)],
      p99: sorted[Math.floor(length * 0.99)]
    };
  }

  /**
   * Get metrics for a specific time window
   * @param {string} window - Time window ('1min', '5min', '15min', '1hour')
   * @returns {Object} - Window metrics
   */
  getWindowMetrics(window = '5min') {
    const windowData = this.timeWindows[window];
    if (!windowData) {
      throw new Error(`Invalid time window: ${window}`);
    }
    
    const data = windowData.data;
    const requests = data.filter(item => item.type === 'request');
    const successes = data.filter(item => item.type === 'success');
    const failures = data.filter(item => item.type === 'failure');
    const cacheHits = data.filter(item => item.type === 'cache_hit');
    const cacheMisses = data.filter(item => item.type === 'cache_miss');
    const retries = data.filter(item => item.type === 'retry');
    const fallbacks = data.filter(item => item.type === 'fallback');
    
    const totalRequests = requests.length;
    const successRate = totalRequests > 0 ? (successes.length / totalRequests) * 100 : 0;
    const failureRate = totalRequests > 0 ? (failures.length / totalRequests) * 100 : 0;
    
    const responseTimes = successes.map(s => s.responseTime).filter(rt => rt !== undefined);
    const avgResponseTime = responseTimes.length > 0 ? 
      responseTimes.reduce((a, b) => a + b, 0) / responseTimes.length : 0;
    
    const totalCacheRequests = cacheHits.length + cacheMisses.length;
    const cacheHitRate = totalCacheRequests > 0 ? (cacheHits.length / totalCacheRequests) * 100 : 0;
    
    return {
      window,
      duration: windowData.duration,
      totalRequests,
      successfulRequests: successes.length,
      failedRequests: failures.length,
      successRate: Math.round(successRate * 100) / 100,
      failureRate: Math.round(failureRate * 100) / 100,
      averageResponseTime: Math.round(avgResponseTime * 100) / 100,
      cacheHits: cacheHits.length,
      cacheMisses: cacheMisses.length,
      cacheHitRate: Math.round(cacheHitRate * 100) / 100,
      retries: retries.length,
      fallbacks: fallbacks.length
    };
  }

  /**
   * Get comprehensive metrics summary
   * @returns {Object} - Complete metrics summary
   */
  getMetricsSummary() {
    const uptime = Date.now() - this.startTime;
    const percentiles = this.getResponseTimePercentiles();
    
    return {
      uptime,
      startTime: this.startTime,
      requests: {
        total: this.metrics.totalRequests,
        successful: this.metrics.successfulRequests,
        failed: this.metrics.failedRequests,
        successRate: this.getSuccessRate(),
        failureRate: this.getFailureRate()
      },
      responseTime: {
        average: Math.round(this.metrics.averageResponseTime * 100) / 100,
        min: this.metrics.minResponseTime === Infinity ? 0 : this.metrics.minResponseTime,
        max: this.metrics.maxResponseTime,
        percentiles
      },
      cache: {
        hits: this.metrics.cacheHits,
        misses: this.metrics.cacheMisses,
        hitRate: this.getCacheHitRate()
      },
      errors: {
        byType: Object.fromEntries(this.metrics.errorsByType),
        byModel: Object.fromEntries(this.metrics.errorsByModel)
      },
      models: {
        usage: Object.fromEntries(this.metrics.modelUsage)
      },
      circuitBreaker: {
        trips: this.metrics.circuitBreakerTrips
      },
      retries: {
        total: this.metrics.totalRetries,
        byReason: Object.fromEntries(this.metrics.retriesByReason)
      },
      fallbacks: {
        usage: Object.fromEntries(this.metrics.fallbackUsage)
      },
      windows: {
        '1min': this.getWindowMetrics('1min'),
        '5min': this.getWindowMetrics('5min'),
        '15min': this.getWindowMetrics('15min'),
        '1hour': this.getWindowMetrics('1hour')
      }
    };
  }

  /**
   * Reset all metrics
   */
  reset() {
    winston.info('Resetting AI/ML metrics');
    
    this.metrics = {
      totalRequests: 0,
      successfulRequests: 0,
      failedRequests: 0,
      totalResponseTime: 0,
      averageResponseTime: 0,
      minResponseTime: Infinity,
      maxResponseTime: 0,
      errorsByType: new Map(),
      errorsByModel: new Map(),
      modelUsage: new Map(),
      cacheHits: 0,
      cacheMisses: 0,
      circuitBreakerTrips: 0,
      totalRetries: 0,
      retriesByReason: new Map(),
      fallbackUsage: new Map()
    };
    
    // Reset time windows
    Object.keys(this.timeWindows).forEach(window => {
      this.timeWindows[window].data = [];
    });
    
    this.responseTimes = [];
    this.startTime = Date.now();
  }

  /**
   * Export metrics for external monitoring systems
   * @param {string} format - Export format ('prometheus', 'json')
   * @returns {string} - Formatted metrics
   */
  exportMetrics(format = 'json') {
    const summary = this.getMetricsSummary();
    
    switch (format) {
      case 'prometheus':
        return this.toPrometheusFormat(summary);
      case 'json':
      default:
        return JSON.stringify(summary, null, 2);
    }
  }

  /**
   * Convert metrics to Prometheus format
   * @param {Object} summary - Metrics summary
   * @returns {string} - Prometheus formatted metrics
   */
  toPrometheusFormat(summary) {
    const lines = [];
    
    // Request metrics
    lines.push(`aiml_requests_total ${summary.requests.total}`);
    lines.push(`aiml_requests_successful_total ${summary.requests.successful}`);
    lines.push(`aiml_requests_failed_total ${summary.requests.failed}`);
    lines.push(`aiml_success_rate ${summary.requests.successRate}`);
    
    // Response time metrics
    lines.push(`aiml_response_time_average ${summary.responseTime.average}`);
    lines.push(`aiml_response_time_min ${summary.responseTime.min}`);
    lines.push(`aiml_response_time_max ${summary.responseTime.max}`);
    lines.push(`aiml_response_time_p50 ${summary.responseTime.percentiles.p50}`);
    lines.push(`aiml_response_time_p90 ${summary.responseTime.percentiles.p90}`);
    lines.push(`aiml_response_time_p95 ${summary.responseTime.percentiles.p95}`);
    lines.push(`aiml_response_time_p99 ${summary.responseTime.percentiles.p99}`);
    
    // Cache metrics
    lines.push(`aiml_cache_hits_total ${summary.cache.hits}`);
    lines.push(`aiml_cache_misses_total ${summary.cache.misses}`);
    lines.push(`aiml_cache_hit_rate ${summary.cache.hitRate}`);
    
    // Circuit breaker metrics
    lines.push(`aiml_circuit_breaker_trips_total ${summary.circuitBreaker.trips}`);
    
    // Retry metrics
    lines.push(`aiml_retries_total ${summary.retries.total}`);
    
    return lines.join('\n');
  }
}

module.exports = AIMLMetrics;
