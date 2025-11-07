const winston = require('winston');

/**
 * AI/ML Logger Utility
 * Specialized logging for AI/ML service interactions
 */
class AIMLLogger {
  constructor() {
    // Create specialized logger for AI/ML operations
    this.logger = winston.createLogger({
      level: process.env.LOG_LEVEL || 'info',
      format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.errors({ stack: true }),
        winston.format.json(),
        winston.format.label({ label: 'AI/ML' })
      ),
      defaultMeta: { 
        service: 'superhack-aiml',
        component: 'ai-ml-client'
      },
      transports: [
        new winston.transports.File({ 
          filename: 'logs/aiml-error.log', 
          level: 'error',
          maxsize: 5242880, // 5MB
          maxFiles: 5
        }),
        new winston.transports.File({ 
          filename: 'logs/aiml-combined.log',
          maxsize: 5242880, // 5MB
          maxFiles: 5
        })
      ]
    });

    // Add console transport for development
    if (process.env.NODE_ENV !== 'production') {
      this.logger.add(new winston.transports.Console({
        format: winston.format.combine(
          winston.format.colorize(),
          winston.format.timestamp({ format: 'HH:mm:ss' }),
          winston.format.printf(({ timestamp, level, message, ...meta }) => {
            const metaStr = Object.keys(meta).length ? JSON.stringify(meta, null, 2) : '';
            return `${timestamp} [AI/ML] ${level}: ${message} ${metaStr}`;
          })
        )
      }));
    }
  }

  /**
   * Log AI/ML request
   * @param {string} method - HTTP method
   * @param {string} url - Request URL
   * @param {Object} data - Request data
   * @param {Object} options - Additional options
   */
  logRequest(method, url, data = null, options = {}) {
    const {
      requestId = null,
      clientId = null,
      modelName = null,
      timeout = null
    } = options;

    const logData = {
      type: 'request',
      method: method.toUpperCase(),
      url,
      requestId,
      clientId,
      modelName,
      timeout,
      dataSize: data ? JSON.stringify(data).length : 0,
      timestamp: new Date().toISOString()
    };

    // Don't log sensitive data in production
    if (process.env.NODE_ENV !== 'production' && data) {
      logData.data = this.sanitizeData(data);
    }

    this.logger.info('AI/ML Request', logData);
  }

  /**
   * Log AI/ML response
   * @param {string} method - HTTP method
   * @param {string} url - Request URL
   * @param {number} status - Response status
   * @param {Object} data - Response data
   * @param {number} duration - Request duration in ms
   * @param {Object} options - Additional options
   */
  logResponse(method, url, status, data = null, duration, options = {}) {
    const {
      requestId = null,
      clientId = null,
      modelName = null,
      cacheHit = false
    } = options;

    const logData = {
      type: 'response',
      method: method.toUpperCase(),
      url,
      status,
      requestId,
      clientId,
      modelName,
      duration,
      cacheHit,
      responseSize: data ? JSON.stringify(data).length : 0,
      timestamp: new Date().toISOString()
    };

    // Don't log response data in production for privacy
    if (process.env.NODE_ENV !== 'production' && data) {
      logData.data = this.sanitizeData(data);
    }

    const level = status >= 400 ? 'error' : status >= 300 ? 'warn' : 'info';
    this.logger[level]('AI/ML Response', logData);
  }

  /**
   * Log AI/ML error
   * @param {string} method - HTTP method
   * @param {string} url - Request URL
   * @param {Error} error - Error object
   * @param {number} duration - Request duration in ms
   * @param {number} retryCount - Number of retries attempted
   * @param {Object} options - Additional options
   */
  logError(method, url, error, duration = null, retryCount = 0, options = {}) {
    const {
      requestId = null,
      clientId = null,
      modelName = null,
      circuitBreakerState = null
    } = options;

    const logData = {
      type: 'error',
      method: method.toUpperCase(),
      url,
      requestId,
      clientId,
      modelName,
      error: {
        name: error.name,
        message: error.message,
        code: error.code,
        status: error.response?.status,
        stack: error.stack
      },
      duration,
      retryCount,
      circuitBreakerState,
      timestamp: new Date().toISOString()
    };

    // Add response data if available
    if (error.response?.data) {
      logData.error.responseData = this.sanitizeData(error.response.data);
    }

    this.logger.error('AI/ML Error', logData);
  }

  /**
   * Log retry attempt
   * @param {string} method - HTTP method
   * @param {string} url - Request URL
   * @param {number} attempt - Current attempt number
   * @param {number} maxRetries - Maximum retry attempts
   * @param {number} delay - Delay before retry in ms
   * @param {Error} error - Error that caused retry
   * @param {Object} options - Additional options
   */
  logRetry(method, url, attempt, maxRetries, delay, error, options = {}) {
    const {
      requestId = null,
      clientId = null,
      modelName = null
    } = options;

    this.logger.warn('AI/ML Retry Attempt', {
      type: 'retry',
      method: method.toUpperCase(),
      url,
      requestId,
      clientId,
      modelName,
      attempt,
      maxRetries,
      delay,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }

  /**
   * Log circuit breaker state change
   * @param {string} from - Previous state
   * @param {string} to - New state
   * @param {string} reason - Reason for state change
   * @param {Object} stats - Circuit breaker statistics
   */
  logCircuitBreakerStateChange(from, to, reason, stats = {}) {
    this.logger.warn('Circuit Breaker State Change', {
      type: 'circuit_breaker',
      from,
      to,
      reason,
      stats,
      timestamp: new Date().toISOString()
    });
  }

  /**
   * Log health check result
   * @param {boolean} success - Whether health check succeeded
   * @param {number} duration - Health check duration in ms
   * @param {Error} error - Error if health check failed
   * @param {Object} stats - Health statistics
   */
  logHealthCheck(success, duration, error = null, stats = {}) {
    const logData = {
      type: 'health_check',
      success,
      duration,
      stats,
      timestamp: new Date().toISOString()
    };

    if (error) {
      logData.error = {
        name: error.name,
        message: error.message,
        code: error.code
      };
    }

    const level = success ? 'debug' : 'warn';
    this.logger[level]('AI/ML Health Check', logData);
  }

  /**
   * Log fallback usage
   * @param {string} method - Original method
   * @param {string} url - Original URL
   * @param {string} fallbackType - Type of fallback used
   * @param {Error} originalError - Original error that triggered fallback
   * @param {Object} options - Additional options
   */
  logFallback(method, url, fallbackType, originalError, options = {}) {
    const {
      requestId = null,
      clientId = null,
      modelName = null
    } = options;

    this.logger.warn('AI/ML Fallback Used', {
      type: 'fallback',
      method: method.toUpperCase(),
      url,
      requestId,
      clientId,
      modelName,
      fallbackType,
      originalError: {
        name: originalError.name,
        message: originalError.message,
        code: originalError.code
      },
      timestamp: new Date().toISOString()
    });
  }

  /**
   * Log cache operation
   * @param {string} operation - Cache operation (hit, miss, set, delete)
   * @param {string} key - Cache key
   * @param {number} ttl - Time to live (for set operations)
   * @param {Object} options - Additional options
   */
  logCache(operation, key, ttl = null, options = {}) {
    const {
      requestId = null,
      size = null
    } = options;

    this.logger.debug('AI/ML Cache Operation', {
      type: 'cache',
      operation,
      key,
      ttl,
      requestId,
      size,
      timestamp: new Date().toISOString()
    });
  }

  /**
   * Log performance metrics
   * @param {string} operation - Operation name
   * @param {Object} metrics - Performance metrics
   */
  logMetrics(operation, metrics) {
    this.logger.info('AI/ML Performance Metrics', {
      type: 'metrics',
      operation,
      metrics,
      timestamp: new Date().toISOString()
    });
  }

  /**
   * Sanitize sensitive data for logging
   * @param {Object} data - Data to sanitize
   * @returns {Object} - Sanitized data
   */
  sanitizeData(data) {
    if (!data || typeof data !== 'object') {
      return data;
    }

    const sensitiveFields = [
      'password', 'token', 'apiKey', 'secret', 'key',
      'authorization', 'auth', 'credential', 'ssn',
      'creditCard', 'bankAccount'
    ];

    const sanitized = { ...data };

    const sanitizeObject = (obj) => {
      for (const key in obj) {
        if (obj.hasOwnProperty(key)) {
          const lowerKey = key.toLowerCase();
          
          if (sensitiveFields.some(field => lowerKey.includes(field))) {
            obj[key] = '[REDACTED]';
          } else if (typeof obj[key] === 'object' && obj[key] !== null) {
            sanitizeObject(obj[key]);
          }
        }
      }
    };

    sanitizeObject(sanitized);
    return sanitized;
  }

  /**
   * Create request context for correlation
   * @param {string} clientId - Client ID
   * @param {string} modelName - Model name
   * @returns {Object} - Request context
   */
  createRequestContext(clientId = null, modelName = null) {
    return {
      requestId: this.generateRequestId(),
      clientId,
      modelName,
      startTime: Date.now()
    };
  }

  /**
   * Generate unique request ID
   * @returns {string} - Unique request ID
   */
  generateRequestId() {
    return `aiml_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * Get logger instance
   * @returns {Object} - Winston logger instance
   */
  getLogger() {
    return this.logger;
  }
}

// Export singleton instance
module.exports = new AIMLLogger();
