const client = require('prom-client');
const winston = require('winston');

class MetricsCollector {
  constructor() {
    // Create a Registry to register the metrics
    this.register = new client.Registry();
    
    // Add default metrics
    client.collectDefaultMetrics({ register: this.register });

    // Initialize custom metrics
    this.initializeMetrics();
    
    // Performance tracking
    this.performanceData = {
      requests: new Map(),
      responses: new Map(),
      errors: new Map()
    };
  }

  /**
   * Initialize custom metrics
   */
  initializeMetrics() {
    // HTTP request metrics
    this.httpRequestDuration = new client.Histogram({
      name: 'http_request_duration_seconds',
      help: 'Duration of HTTP requests in seconds',
      labelNames: ['method', 'route', 'status_code'],
      buckets: [0.1, 0.5, 1, 2, 5, 10]
    });

    this.httpRequestTotal = new client.Counter({
      name: 'http_requests_total',
      help: 'Total number of HTTP requests',
      labelNames: ['method', 'route', 'status_code']
    });

    // AI/ML service metrics
    this.aimlRequestDuration = new client.Histogram({
      name: 'aiml_request_duration_seconds',
      help: 'Duration of AI/ML service requests in seconds',
      labelNames: ['model_type', 'operation', 'status'],
      buckets: [0.1, 0.5, 1, 2, 5, 10, 30]
    });

    this.aimlRequestTotal = new client.Counter({
      name: 'aiml_requests_total',
      help: 'Total number of AI/ML service requests',
      labelNames: ['model_type', 'operation', 'status']
    });

    this.aimlPredictionAccuracy = new client.Gauge({
      name: 'aiml_prediction_accuracy',
      help: 'AI/ML model prediction accuracy',
      labelNames: ['model_type']
    });

    // Cache metrics
    this.cacheHitRate = new client.Gauge({
      name: 'cache_hit_rate',
      help: 'Cache hit rate percentage',
      labelNames: ['cache_type']
    });

    this.cacheOperations = new client.Counter({
      name: 'cache_operations_total',
      help: 'Total cache operations',
      labelNames: ['operation', 'result']
    });

    // Database metrics
    this.dbConnectionPool = new client.Gauge({
      name: 'db_connection_pool_size',
      help: 'Database connection pool size',
      labelNames: ['status']
    });

    this.dbQueryDuration = new client.Histogram({
      name: 'db_query_duration_seconds',
      help: 'Database query duration in seconds',
      labelNames: ['operation', 'table'],
      buckets: [0.01, 0.05, 0.1, 0.5, 1, 2, 5]
    });

    // Business metrics
    this.activeUsers = new client.Gauge({
      name: 'active_users_total',
      help: 'Number of active users'
    });

    this.predictionsServed = new client.Counter({
      name: 'predictions_served_total',
      help: 'Total predictions served',
      labelNames: ['model_type', 'organization_id']
    });

    this.batchJobsTotal = new client.Counter({
      name: 'batch_jobs_total',
      help: 'Total batch jobs processed',
      labelNames: ['job_type', 'status']
    });

    // Error metrics
    this.errorRate = new client.Gauge({
      name: 'error_rate',
      help: 'Error rate percentage',
      labelNames: ['service', 'error_type']
    });

    this.circuitBreakerState = new client.Gauge({
      name: 'circuit_breaker_state',
      help: 'Circuit breaker state (0=closed, 1=open, 2=half-open)',
      labelNames: ['service']
    });

    // Register all metrics
    this.register.registerMetric(this.httpRequestDuration);
    this.register.registerMetric(this.httpRequestTotal);
    this.register.registerMetric(this.aimlRequestDuration);
    this.register.registerMetric(this.aimlRequestTotal);
    this.register.registerMetric(this.aimlPredictionAccuracy);
    this.register.registerMetric(this.cacheHitRate);
    this.register.registerMetric(this.cacheOperations);
    this.register.registerMetric(this.dbConnectionPool);
    this.register.registerMetric(this.dbQueryDuration);
    this.register.registerMetric(this.activeUsers);
    this.register.registerMetric(this.predictionsServed);
    this.register.registerMetric(this.batchJobsTotal);
    this.register.registerMetric(this.errorRate);
    this.register.registerMetric(this.circuitBreakerState);

    winston.info('Metrics collector initialized with custom metrics');
  }

  /**
   * Record HTTP request metrics
   * @param {string} method - HTTP method
   * @param {string} route - Route path
   * @param {number} statusCode - HTTP status code
   * @param {number} duration - Request duration in seconds
   */
  recordHttpRequest(method, route, statusCode, duration) {
    const labels = { method, route, status_code: statusCode };
    
    this.httpRequestDuration.observe(labels, duration);
    this.httpRequestTotal.inc(labels);
  }

  /**
   * Record AI/ML service request metrics
   * @param {string} modelType - Model type
   * @param {string} operation - Operation type
   * @param {string} status - Request status (success/error)
   * @param {number} duration - Request duration in seconds
   */
  recordAimlRequest(modelType, operation, status, duration) {
    const labels = { model_type: modelType, operation, status };
    
    this.aimlRequestDuration.observe(labels, duration);
    this.aimlRequestTotal.inc(labels);
  }

  /**
   * Update AI/ML model accuracy
   * @param {string} modelType - Model type
   * @param {number} accuracy - Accuracy value (0-1)
   */
  updateModelAccuracy(modelType, accuracy) {
    this.aimlPredictionAccuracy.set({ model_type: modelType }, accuracy);
  }

  /**
   * Record cache operation
   * @param {string} operation - Cache operation (get/set/delete)
   * @param {string} result - Operation result (hit/miss/success/error)
   */
  recordCacheOperation(operation, result) {
    this.cacheOperations.inc({ operation, result });
  }

  /**
   * Update cache hit rate
   * @param {string} cacheType - Cache type
   * @param {number} hitRate - Hit rate percentage
   */
  updateCacheHitRate(cacheType, hitRate) {
    this.cacheHitRate.set({ cache_type: cacheType }, hitRate);
  }

  /**
   * Record database query metrics
   * @param {string} operation - Database operation (select/insert/update/delete)
   * @param {string} table - Table name
   * @param {number} duration - Query duration in seconds
   */
  recordDbQuery(operation, table, duration) {
    this.dbQueryDuration.observe({ operation, table }, duration);
  }

  /**
   * Update database connection pool metrics
   * @param {number} active - Active connections
   * @param {number} idle - Idle connections
   * @param {number} total - Total connections
   */
  updateDbConnectionPool(active, idle, total) {
    this.dbConnectionPool.set({ status: 'active' }, active);
    this.dbConnectionPool.set({ status: 'idle' }, idle);
    this.dbConnectionPool.set({ status: 'total' }, total);
  }

  /**
   * Update active users count
   * @param {number} count - Number of active users
   */
  updateActiveUsers(count) {
    this.activeUsers.set(count);
  }

  /**
   * Record prediction served
   * @param {string} modelType - Model type
   * @param {string} organizationId - Organization ID
   */
  recordPredictionServed(modelType, organizationId) {
    this.predictionsServed.inc({ model_type: modelType, organization_id: organizationId });
  }

  /**
   * Record batch job completion
   * @param {string} jobType - Job type
   * @param {string} status - Job status (completed/failed)
   */
  recordBatchJob(jobType, status) {
    this.batchJobsTotal.inc({ job_type: jobType, status });
  }

  /**
   * Update error rate
   * @param {string} service - Service name
   * @param {string} errorType - Error type
   * @param {number} rate - Error rate percentage
   */
  updateErrorRate(service, errorType, rate) {
    this.errorRate.set({ service, error_type: errorType }, rate);
  }

  /**
   * Update circuit breaker state
   * @param {string} service - Service name
   * @param {string} state - Circuit breaker state (closed/open/half-open)
   */
  updateCircuitBreakerState(service, state) {
    const stateValue = { closed: 0, open: 1, 'half-open': 2 }[state] || 0;
    this.circuitBreakerState.set({ service }, stateValue);
  }

  /**
   * Start request tracking
   * @param {string} requestId - Request ID
   * @param {Object} metadata - Request metadata
   */
  startRequest(requestId, metadata) {
    this.performanceData.requests.set(requestId, {
      startTime: Date.now(),
      metadata
    });
  }

  /**
   * End request tracking
   * @param {string} requestId - Request ID
   * @param {Object} responseData - Response data
   */
  endRequest(requestId, responseData) {
    const requestData = this.performanceData.requests.get(requestId);
    
    if (requestData) {
      const duration = (Date.now() - requestData.startTime) / 1000;
      
      this.performanceData.responses.set(requestId, {
        duration,
        ...responseData,
        metadata: requestData.metadata
      });

      // Record HTTP metrics
      if (requestData.metadata) {
        this.recordHttpRequest(
          requestData.metadata.method,
          requestData.metadata.route,
          responseData.statusCode,
          duration
        );
      }

      // Clean up
      this.performanceData.requests.delete(requestId);
    }
  }

  /**
   * Record error
   * @param {string} requestId - Request ID
   * @param {Error} error - Error object
   * @param {Object} context - Error context
   */
  recordError(requestId, error, context) {
    this.performanceData.errors.set(requestId, {
      error: error.message,
      stack: error.stack,
      context,
      timestamp: Date.now()
    });

    // Update error rate metrics
    if (context.service) {
      // This would typically be calculated over a time window
      // For now, we'll increment the counter
      this.updateErrorRate(context.service, error.constructor.name, 1);
    }
  }

  /**
   * Get performance summary
   * @returns {Object} Performance summary
   */
  getPerformanceSummary() {
    const now = Date.now();
    const last5Minutes = now - (5 * 60 * 1000);
    
    // Get recent responses
    const recentResponses = Array.from(this.performanceData.responses.values())
      .filter(response => response.timestamp > last5Minutes);

    // Calculate statistics
    const totalRequests = recentResponses.length;
    const avgDuration = totalRequests > 0 
      ? recentResponses.reduce((sum, r) => sum + r.duration, 0) / totalRequests 
      : 0;
    
    const errorCount = Array.from(this.performanceData.errors.values())
      .filter(error => error.timestamp > last5Minutes).length;
    
    const errorRate = totalRequests > 0 ? (errorCount / totalRequests) * 100 : 0;

    return {
      totalRequests,
      avgDuration: Math.round(avgDuration * 1000), // Convert to ms
      errorCount,
      errorRate: Math.round(errorRate * 100) / 100,
      activeRequests: this.performanceData.requests.size,
      timestamp: new Date().toISOString()
    };
  }

  /**
   * Get metrics in Prometheus format
   * @returns {Promise<string>} Prometheus metrics
   */
  async getMetrics() {
    return this.register.metrics();
  }

  /**
   * Get metrics as JSON
   * @returns {Promise<Object>} Metrics as JSON
   */
  async getMetricsJSON() {
    const metrics = await this.register.getMetricsAsJSON();
    return {
      metrics,
      performance: this.getPerformanceSummary(),
      timestamp: new Date().toISOString()
    };
  }

  /**
   * Clear old performance data
   */
  cleanup() {
    const now = Date.now();
    const oneHourAgo = now - (60 * 60 * 1000);

    // Clean up old responses
    for (const [id, response] of this.performanceData.responses.entries()) {
      if (response.timestamp < oneHourAgo) {
        this.performanceData.responses.delete(id);
      }
    }

    // Clean up old errors
    for (const [id, error] of this.performanceData.errors.entries()) {
      if (error.timestamp < oneHourAgo) {
        this.performanceData.errors.delete(id);
      }
    }

    winston.debug('Cleaned up old performance data');
  }

  /**
   * Start periodic cleanup
   */
  startCleanup() {
    // Clean up every 10 minutes
    setInterval(() => {
      this.cleanup();
    }, 10 * 60 * 1000);

    winston.info('Started periodic cleanup for metrics collector');
  }

  /**
   * Reset all metrics
   */
  reset() {
    this.register.clear();
    this.performanceData.requests.clear();
    this.performanceData.responses.clear();
    this.performanceData.errors.clear();
    
    // Reinitialize metrics
    this.initializeMetrics();
    
    winston.info('Metrics collector reset');
  }
}

// Export singleton instance
module.exports = new MetricsCollector();
