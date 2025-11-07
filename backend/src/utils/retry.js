const winston = require('winston');

/**
 * Retry Utility with Exponential Backoff
 * Provides robust retry mechanisms for AI/ML service calls
 */
class RetryUtility {
  /**
   * Execute function with retry logic
   * @param {Function} fn - Function to execute
   * @param {Object} options - Retry options
   * @returns {Promise} - Function result or throws error
   */
  static async withRetry(fn, options = {}) {
    const {
      retries = 3,
      delay = 1000,
      backoff = 2,
      maxDelay = 30000,
      retryCondition = null,
      onRetry = null,
      context = 'unknown'
    } = options;

    let lastError;
    let currentDelay = delay;

    for (let attempt = 0; attempt <= retries; attempt++) {
      try {
        const result = await fn();
        
        // Log successful execution after retries
        if (attempt > 0) {
          winston.info(`Retry successful for ${context} after ${attempt} attempts`);
        }
        
        return result;
      } catch (error) {
        lastError = error;
        
        // Check if we should retry this error
        if (retryCondition && !retryCondition(error)) {
          winston.warn(`Retry condition not met for ${context}, not retrying:`, error.message);
          throw error;
        }
        
        // Don't retry on the last attempt
        if (attempt === retries) {
          winston.error(`All retry attempts failed for ${context}:`, error.message);
          break;
        }
        
        // Calculate delay with jitter to avoid thundering herd
        const jitter = Math.random() * 0.1 * currentDelay;
        const delayWithJitter = Math.min(currentDelay + jitter, maxDelay);
        
        winston.warn(`Retry attempt ${attempt + 1}/${retries} for ${context} in ${delayWithJitter}ms:`, error.message);
        
        // Call onRetry callback if provided
        if (onRetry) {
          try {
            await onRetry(error, attempt + 1);
          } catch (callbackError) {
            winston.error(`Retry callback failed for ${context}:`, callbackError.message);
          }
        }
        
        // Wait before next attempt
        await this.delay(delayWithJitter);
        
        // Increase delay for next attempt (exponential backoff)
        currentDelay = Math.min(currentDelay * backoff, maxDelay);
      }
    }
    
    throw lastError;
  }

  /**
   * Retry with specific conditions for AI/ML service calls
   * @param {Function} fn - Function to execute
   * @param {Object} options - Retry options
   * @returns {Promise} - Function result
   */
  static async withAIMLRetry(fn, options = {}) {
    const aimlRetryCondition = (error) => {
      // Retry on network errors, timeouts, and 5xx server errors
      if (error.code === 'ECONNREFUSED' || 
          error.code === 'ETIMEDOUT' || 
          error.code === 'ENOTFOUND') {
        return true;
      }
      
      // Retry on HTTP 5xx errors and 429 (rate limiting)
      if (error.response) {
        const status = error.response.status;
        return status >= 500 || status === 429;
      }
      
      // Don't retry on 4xx client errors (except 429)
      if (error.response && error.response.status >= 400 && error.response.status < 500) {
        return false;
      }
      
      return true;
    };

    const defaultOptions = {
      retries: 3,
      delay: 1000,
      backoff: 2,
      maxDelay: 10000,
      retryCondition: aimlRetryCondition,
      context: 'AI/ML Service Call',
      ...options
    };

    return this.withRetry(fn, defaultOptions);
  }

  /**
   * Retry with circuit breaker pattern
   * @param {Function} fn - Function to execute
   * @param {Object} circuitBreaker - Circuit breaker instance
   * @param {Object} options - Retry options
   * @returns {Promise} - Function result
   */
  static async withCircuitBreakerRetry(fn, circuitBreaker, options = {}) {
    return this.withRetry(async () => {
      return circuitBreaker.execute(fn);
    }, {
      ...options,
      retryCondition: (error) => {
        // Don't retry if circuit breaker is open
        if (error.message && error.message.includes('Circuit breaker is OPEN')) {
          return false;
        }
        return options.retryCondition ? options.retryCondition(error) : true;
      }
    });
  }

  /**
   * Batch retry for multiple operations
   * @param {Array} operations - Array of functions to execute
   * @param {Object} options - Retry options
   * @returns {Promise<Array>} - Array of results
   */
  static async batchWithRetry(operations, options = {}) {
    const {
      concurrency = 5,
      failFast = false,
      ...retryOptions
    } = options;

    const results = [];
    const errors = [];

    // Process operations in batches
    for (let i = 0; i < operations.length; i += concurrency) {
      const batch = operations.slice(i, i + concurrency);
      
      const batchPromises = batch.map(async (operation, index) => {
        try {
          const result = await this.withRetry(operation, {
            ...retryOptions,
            context: `Batch operation ${i + index + 1}`
          });
          return { success: true, result, index: i + index };
        } catch (error) {
          const errorResult = { success: false, error, index: i + index };
          
          if (failFast) {
            throw error;
          }
          
          return errorResult;
        }
      });

      const batchResults = await Promise.all(batchPromises);
      
      batchResults.forEach(result => {
        if (result.success) {
          results[result.index] = result.result;
        } else {
          errors[result.index] = result.error;
        }
      });
    }

    return { results, errors };
  }

  /**
   * Delay utility
   * @param {number} ms - Milliseconds to delay
   * @returns {Promise} - Resolves after delay
   */
  static delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  /**
   * Create retry decorator for class methods
   * @param {Object} retryOptions - Default retry options
   * @returns {Function} - Decorator function
   */
  static createRetryDecorator(retryOptions = {}) {
    return function(target, propertyName, descriptor) {
      const originalMethod = descriptor.value;
      
      descriptor.value = async function(...args) {
        return RetryUtility.withRetry(
          () => originalMethod.apply(this, args),
          {
            ...retryOptions,
            context: `${target.constructor.name}.${propertyName}`
          }
        );
      };
      
      return descriptor;
    };
  }

  /**
   * Get retry statistics
   * @param {Function} fn - Function to monitor
   * @param {Object} options - Options
   * @returns {Object} - Statistics
   */
  static async withRetryStats(fn, options = {}) {
    const stats = {
      attempts: 0,
      totalTime: 0,
      success: false,
      error: null
    };

    const startTime = Date.now();

    try {
      const result = await this.withRetry(fn, {
        ...options,
        onRetry: (error, attempt) => {
          stats.attempts = attempt;
          if (options.onRetry) {
            return options.onRetry(error, attempt);
          }
        }
      });

      stats.success = true;
      stats.totalTime = Date.now() - startTime;
      
      return { result, stats };
    } catch (error) {
      stats.error = error;
      stats.totalTime = Date.now() - startTime;
      
      throw error;
    }
  }
}

module.exports = RetryUtility;
