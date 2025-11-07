const winston = require('winston');
const { EventEmitter } = require('events');

/**
 * Circuit Breaker States
 */
const STATES = {
  CLOSED: 'CLOSED',     // Normal operation
  OPEN: 'OPEN',         // Failing, requests blocked
  HALF_OPEN: 'HALF_OPEN' // Testing if service recovered
};

/**
 * Circuit Breaker Implementation
 * Prevents cascading failures by monitoring service health
 */
class CircuitBreaker extends EventEmitter {
  constructor(options = {}) {
    super();
    
    this.options = {
      threshold: options.threshold || 5,           // Failure threshold
      timeout: options.timeout || 60000,          // Time to wait before retry (ms)
      resetTimeout: options.resetTimeout || 30000, // Time to stay in HALF_OPEN
      monitoringPeriod: options.monitoringPeriod || 10000, // Monitoring window (ms)
      expectedErrors: options.expectedErrors || [], // Errors that don't count as failures
      ...options
    };
    
    this.state = STATES.CLOSED;
    this.failureCount = 0;
    this.successCount = 0;
    this.lastFailureTime = null;
    this.nextAttemptTime = null;
    this.halfOpenStartTime = null;
    
    // Statistics
    this.stats = {
      totalRequests: 0,
      totalFailures: 0,
      totalSuccesses: 0,
      totalRejections: 0,
      averageResponseTime: 0,
      lastRequestTime: null
    };
    
    // Monitoring window for failure rate calculation
    this.requestHistory = [];
    
    winston.info('Circuit Breaker initialized', {
      threshold: this.options.threshold,
      timeout: this.options.timeout,
      resetTimeout: this.options.resetTimeout
    });
  }

  /**
   * Execute function with circuit breaker protection
   * @param {Function} fn - Function to execute
   * @returns {Promise} - Function result or throws CircuitBreakerError
   */
  async execute(fn) {
    this.stats.totalRequests++;
    this.stats.lastRequestTime = Date.now();
    
    // Check if circuit breaker should block the request
    if (this.shouldRejectRequest()) {
      this.stats.totalRejections++;
      const error = new CircuitBreakerError(
        `Circuit breaker is ${this.state}. Service is currently unavailable.`,
        this.state
      );
      this.emit('reject', error);
      throw error;
    }
    
    const startTime = Date.now();
    
    try {
      const result = await fn();
      
      // Record success
      const responseTime = Date.now() - startTime;
      this.onSuccess(responseTime);
      
      return result;
    } catch (error) {
      // Record failure
      const responseTime = Date.now() - startTime;
      this.onFailure(error, responseTime);
      
      throw error;
    }
  }

  /**
   * Check if request should be rejected
   * @returns {boolean} - True if request should be rejected
   */
  shouldRejectRequest() {
    const now = Date.now();
    
    switch (this.state) {
      case STATES.CLOSED:
        return false;
        
      case STATES.OPEN:
        // Check if timeout period has passed
        if (this.nextAttemptTime && now >= this.nextAttemptTime) {
          this.moveToHalfOpen();
          return false;
        }
        return true;
        
      case STATES.HALF_OPEN:
        // Check if half-open period has expired
        if (this.halfOpenStartTime && 
            (now - this.halfOpenStartTime) > this.options.resetTimeout) {
          winston.warn('Half-open period expired, moving back to OPEN');
          this.moveToOpen();
          return true;
        }
        return false;
        
      default:
        return false;
    }
  }

  /**
   * Handle successful execution
   * @param {number} responseTime - Response time in milliseconds
   */
  onSuccess(responseTime) {
    this.successCount++;
    this.stats.totalSuccesses++;
    this.updateAverageResponseTime(responseTime);
    this.addToHistory(true, responseTime);
    
    winston.debug('Circuit Breaker: Success recorded', {
      state: this.state,
      successCount: this.successCount,
      responseTime
    });
    
    // Reset failure count on success
    if (this.state === STATES.HALF_OPEN) {
      // If we're in half-open and got a success, consider closing
      if (this.successCount >= Math.ceil(this.options.threshold / 2)) {
        this.moveToClosed();
      }
    } else if (this.state === STATES.CLOSED) {
      // Reset failure count in closed state
      this.failureCount = 0;
    }
    
    this.emit('success', { responseTime, state: this.state });
  }

  /**
   * Handle failed execution
   * @param {Error} error - The error that occurred
   * @param {number} responseTime - Response time in milliseconds
   */
  onFailure(error, responseTime) {
    // Check if this is an expected error that shouldn't count
    if (this.isExpectedError(error)) {
      winston.debug('Circuit Breaker: Expected error, not counting as failure', {
        error: error.message
      });
      return;
    }
    
    this.failureCount++;
    this.stats.totalFailures++;
    this.lastFailureTime = Date.now();
    this.updateAverageResponseTime(responseTime);
    this.addToHistory(false, responseTime);
    
    winston.warn('Circuit Breaker: Failure recorded', {
      state: this.state,
      failureCount: this.failureCount,
      threshold: this.options.threshold,
      error: error.message
    });
    
    // Check if we should open the circuit
    if (this.state === STATES.CLOSED && this.failureCount >= this.options.threshold) {
      this.moveToOpen();
    } else if (this.state === STATES.HALF_OPEN) {
      // Any failure in half-open state moves back to open
      this.moveToOpen();
    }
    
    this.emit('failure', { error, responseTime, state: this.state });
  }

  /**
   * Move to CLOSED state
   */
  moveToClosed() {
    const previousState = this.state;
    this.state = STATES.CLOSED;
    this.failureCount = 0;
    this.successCount = 0;
    this.nextAttemptTime = null;
    this.halfOpenStartTime = null;
    
    winston.info('Circuit Breaker: Moved to CLOSED state', {
      previousState,
      totalRequests: this.stats.totalRequests
    });
    
    this.emit('stateChange', {
      from: previousState,
      to: this.state,
      reason: 'Service recovered'
    });
  }

  /**
   * Move to OPEN state
   */
  moveToOpen() {
    const previousState = this.state;
    this.state = STATES.OPEN;
    this.nextAttemptTime = Date.now() + this.options.timeout;
    this.halfOpenStartTime = null;
    
    winston.error('Circuit Breaker: Moved to OPEN state', {
      previousState,
      failureCount: this.failureCount,
      threshold: this.options.threshold,
      nextAttemptTime: new Date(this.nextAttemptTime).toISOString()
    });
    
    this.emit('stateChange', {
      from: previousState,
      to: this.state,
      reason: 'Failure threshold exceeded'
    });
  }

  /**
   * Move to HALF_OPEN state
   */
  moveToHalfOpen() {
    const previousState = this.state;
    this.state = STATES.HALF_OPEN;
    this.successCount = 0;
    this.halfOpenStartTime = Date.now();
    
    winston.info('Circuit Breaker: Moved to HALF_OPEN state', {
      previousState,
      halfOpenStartTime: new Date(this.halfOpenStartTime).toISOString()
    });
    
    this.emit('stateChange', {
      from: previousState,
      to: this.state,
      reason: 'Testing service recovery'
    });
  }

  /**
   * Check if error is expected and shouldn't count as failure
   * @param {Error} error - The error to check
   * @returns {boolean} - True if error is expected
   */
  isExpectedError(error) {
    return this.options.expectedErrors.some(expectedError => {
      if (typeof expectedError === 'string') {
        return error.message.includes(expectedError);
      }
      if (expectedError instanceof RegExp) {
        return expectedError.test(error.message);
      }
      if (typeof expectedError === 'function') {
        return expectedError(error);
      }
      return false;
    });
  }

  /**
   * Add request to history for monitoring
   * @param {boolean} success - Whether request was successful
   * @param {number} responseTime - Response time in milliseconds
   */
  addToHistory(success, responseTime) {
    const now = Date.now();
    this.requestHistory.push({
      timestamp: now,
      success,
      responseTime
    });
    
    // Clean old entries outside monitoring period
    const cutoff = now - this.options.monitoringPeriod;
    this.requestHistory = this.requestHistory.filter(entry => entry.timestamp >= cutoff);
  }

  /**
   * Update average response time
   * @param {number} responseTime - New response time
   */
  updateAverageResponseTime(responseTime) {
    const totalRequests = this.stats.totalRequests;
    this.stats.averageResponseTime = 
      ((this.stats.averageResponseTime * (totalRequests - 1)) + responseTime) / totalRequests;
  }

  /**
   * Get current circuit breaker status
   * @returns {Object} - Current status
   */
  getStatus() {
    const now = Date.now();
    const recentHistory = this.requestHistory.filter(
      entry => (now - entry.timestamp) <= this.options.monitoringPeriod
    );
    
    const recentFailures = recentHistory.filter(entry => !entry.success).length;
    const recentSuccesses = recentHistory.filter(entry => entry.success).length;
    const failureRate = recentHistory.length > 0 ? 
      (recentFailures / recentHistory.length) * 100 : 0;
    
    return {
      state: this.state,
      failureCount: this.failureCount,
      successCount: this.successCount,
      threshold: this.options.threshold,
      nextAttemptTime: this.nextAttemptTime,
      halfOpenStartTime: this.halfOpenStartTime,
      stats: {
        ...this.stats,
        failureRate: Math.round(failureRate * 100) / 100,
        recentRequests: recentHistory.length,
        recentFailures,
        recentSuccesses
      },
      isOpen: this.state === STATES.OPEN,
      isHalfOpen: this.state === STATES.HALF_OPEN,
      isClosed: this.state === STATES.CLOSED
    };
  }

  /**
   * Reset circuit breaker to initial state
   */
  reset() {
    winston.info('Circuit Breaker: Manual reset');
    
    this.state = STATES.CLOSED;
    this.failureCount = 0;
    this.successCount = 0;
    this.lastFailureTime = null;
    this.nextAttemptTime = null;
    this.halfOpenStartTime = null;
    this.requestHistory = [];
    
    // Reset stats
    this.stats = {
      totalRequests: 0,
      totalFailures: 0,
      totalSuccesses: 0,
      totalRejections: 0,
      averageResponseTime: 0,
      lastRequestTime: null
    };
    
    this.emit('reset');
  }
}

/**
 * Circuit Breaker Error
 */
class CircuitBreakerError extends Error {
  constructor(message, state) {
    super(message);
    this.name = 'CircuitBreakerError';
    this.state = state;
    this.isCircuitBreakerError = true;
  }
}

module.exports = {
  CircuitBreaker,
  CircuitBreakerError,
  STATES
};
