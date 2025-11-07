const winston = require('winston');
const { EventEmitter } = require('events');
const axios = require('axios');

/**
 * AI/ML Health Monitor
 * Continuously monitors the health of the AI/ML service
 */
class AIMLHealthMonitor extends EventEmitter {
  constructor(client, config = {}) {
    super();
    
    this.client = client;
    this.config = {
      checkInterval: config.checkInterval || 30000,  // 30 seconds
      timeout: config.timeout || 5000,              // 5 seconds
      retries: config.retries || 2,                 // 2 retries
      unhealthyThreshold: config.unhealthyThreshold || 3, // 3 consecutive failures
      recoveryThreshold: config.recoveryThreshold || 2,   // 2 consecutive successes
      ...config
    };
    
    // Health state
    this.isHealthy = false;
    this.isMonitoring = false;
    this.consecutiveFailures = 0;
    this.consecutiveSuccesses = 0;
    this.lastHealthCheck = null;
    this.lastHealthCheckDuration = null;
    this.healthCheckInterval = null;
    
    // Health history for trends
    this.healthHistory = [];
    this.maxHistorySize = 100;
    
    // Statistics
    this.stats = {
      totalChecks: 0,
      successfulChecks: 0,
      failedChecks: 0,
      averageResponseTime: 0,
      uptime: 0,
      downtimeStart: null,
      lastDowntime: null,
      uptimeStart: null
    };
    
    winston.info('AI/ML Health Monitor initialized', {
      checkInterval: this.config.checkInterval,
      timeout: this.config.timeout,
      unhealthyThreshold: this.config.unhealthyThreshold
    });
  }

  /**
   * Start health monitoring
   */
  startMonitoring() {
    if (this.isMonitoring) {
      winston.warn('Health monitoring is already running');
      return;
    }
    
    winston.info('Starting AI/ML health monitoring');
    this.isMonitoring = true;
    
    // Perform initial health check
    this.performHealthCheck();
    
    // Set up periodic health checks
    this.healthCheckInterval = setInterval(() => {
      this.performHealthCheck();
    }, this.config.checkInterval);
    
    this.emit('monitoringStarted');
  }

  /**
   * Stop health monitoring
   */
  stopMonitoring() {
    if (!this.isMonitoring) {
      winston.warn('Health monitoring is not running');
      return;
    }
    
    winston.info('Stopping AI/ML health monitoring');
    this.isMonitoring = false;
    
    if (this.healthCheckInterval) {
      clearInterval(this.healthCheckInterval);
      this.healthCheckInterval = null;
    }
    
    this.emit('monitoringStopped');
  }

  /**
   * Perform a single health check
   */
  async performHealthCheck() {
    const startTime = Date.now();
    this.stats.totalChecks++;
    
    try {
      winston.debug('Performing AI/ML health check');
      
      // Create a health check specific axios instance with shorter timeout
      const healthClient = axios.create({
        baseURL: this.client.baseUrl,
        timeout: this.config.timeout,
        headers: {
          'Authorization': `Bearer ${this.client.apiKey}`,
          'Content-Type': 'application/json'
        }
      });
      
      // Perform health check with retries
      let lastError;
      let success = false;
      
      for (let attempt = 0; attempt <= this.config.retries; attempt++) {
        try {
          const response = await healthClient.get('/api/health');
          
          // Check if response indicates healthy service
          if (response.status === 200 && response.data) {
            success = true;
            break;
          }
        } catch (error) {
          lastError = error;
          
          // Don't retry on the last attempt
          if (attempt < this.config.retries) {
            winston.debug(`Health check attempt ${attempt + 1} failed, retrying...`);
            await this.delay(1000); // Wait 1 second before retry
          }
        }
      }
      
      const duration = Date.now() - startTime;
      
      if (success) {
        this.onHealthCheckSuccess(duration);
      } else {
        this.onHealthCheckFailure(lastError || new Error('Health check failed'), duration);
      }
      
    } catch (error) {
      const duration = Date.now() - startTime;
      this.onHealthCheckFailure(error, duration);
    }
  }

  /**
   * Handle successful health check
   * @param {number} duration - Health check duration in ms
   */
  onHealthCheckSuccess(duration) {
    this.lastHealthCheck = new Date();
    this.lastHealthCheckDuration = duration;
    this.consecutiveFailures = 0;
    this.consecutiveSuccesses++;
    this.stats.successfulChecks++;
    
    // Update average response time
    this.updateAverageResponseTime(duration);
    
    // Add to history
    this.addToHistory(true, duration);
    
    winston.debug('AI/ML health check successful', {
      duration,
      consecutiveSuccesses: this.consecutiveSuccesses,
      isHealthy: this.isHealthy
    });
    
    // Check if service has recovered
    if (!this.isHealthy && this.consecutiveSuccesses >= this.config.recoveryThreshold) {
      this.markAsHealthy();
    }
    
    this.emit('healthCheckSuccess', { duration, consecutiveSuccesses: this.consecutiveSuccesses });
  }

  /**
   * Handle failed health check
   * @param {Error} error - The error that occurred
   * @param {number} duration - Health check duration in ms
   */
  onHealthCheckFailure(error, duration) {
    this.lastHealthCheck = new Date();
    this.lastHealthCheckDuration = duration;
    this.consecutiveSuccesses = 0;
    this.consecutiveFailures++;
    this.stats.failedChecks++;
    
    // Add to history
    this.addToHistory(false, duration, error.message);
    
    winston.warn('AI/ML health check failed', {
      error: error.message,
      duration,
      consecutiveFailures: this.consecutiveFailures,
      isHealthy: this.isHealthy
    });
    
    // Check if service should be marked as unhealthy
    if (this.isHealthy && this.consecutiveFailures >= this.config.unhealthyThreshold) {
      this.markAsUnhealthy();
    }
    
    this.emit('healthCheckFailure', { 
      error, 
      duration, 
      consecutiveFailures: this.consecutiveFailures 
    });
  }

  /**
   * Mark service as healthy
   */
  markAsHealthy() {
    if (this.isHealthy) return;
    
    winston.info('AI/ML service marked as HEALTHY');
    
    this.isHealthy = true;
    this.stats.uptimeStart = Date.now();
    
    // Calculate downtime if we were previously unhealthy
    if (this.stats.downtimeStart) {
      this.stats.lastDowntime = Date.now() - this.stats.downtimeStart;
      this.stats.downtimeStart = null;
    }
    
    this.emit('serviceHealthy', {
      consecutiveSuccesses: this.consecutiveSuccesses,
      lastDowntime: this.stats.lastDowntime
    });
  }

  /**
   * Mark service as unhealthy
   */
  markAsUnhealthy() {
    if (!this.isHealthy) return;
    
    winston.error('AI/ML service marked as UNHEALTHY');
    
    this.isHealthy = false;
    this.stats.downtimeStart = Date.now();
    
    // Calculate uptime if we were previously healthy
    if (this.stats.uptimeStart) {
      this.stats.uptime += Date.now() - this.stats.uptimeStart;
      this.stats.uptimeStart = null;
    }
    
    this.emit('serviceUnhealthy', {
      consecutiveFailures: this.consecutiveFailures,
      lastUptime: this.stats.uptime
    });
  }

  /**
   * Add health check result to history
   * @param {boolean} success - Whether check was successful
   * @param {number} duration - Duration in ms
   * @param {string} error - Error message if failed
   */
  addToHistory(success, duration, error = null) {
    this.healthHistory.push({
      timestamp: Date.now(),
      success,
      duration,
      error
    });
    
    // Keep history size manageable
    if (this.healthHistory.length > this.maxHistorySize) {
      this.healthHistory.shift();
    }
  }

  /**
   * Update average response time
   * @param {number} duration - New duration
   */
  updateAverageResponseTime(duration) {
    const totalChecks = this.stats.totalChecks;
    this.stats.averageResponseTime = 
      ((this.stats.averageResponseTime * (totalChecks - 1)) + duration) / totalChecks;
  }

  /**
   * Get current health status
   * @returns {Object} - Health status
   */
  getHealthStatus() {
    const now = Date.now();
    const recentHistory = this.healthHistory.slice(-10); // Last 10 checks
    const successRate = this.stats.totalChecks > 0 ? 
      (this.stats.successfulChecks / this.stats.totalChecks) * 100 : 0;
    
    // Calculate current uptime/downtime
    let currentUptime = this.stats.uptime;
    let currentDowntime = 0;
    
    if (this.isHealthy && this.stats.uptimeStart) {
      currentUptime += now - this.stats.uptimeStart;
    } else if (!this.isHealthy && this.stats.downtimeStart) {
      currentDowntime = now - this.stats.downtimeStart;
    }
    
    return {
      isHealthy: this.isHealthy,
      isMonitoring: this.isMonitoring,
      lastHealthCheck: this.lastHealthCheck,
      lastHealthCheckDuration: this.lastHealthCheckDuration,
      consecutiveFailures: this.consecutiveFailures,
      consecutiveSuccesses: this.consecutiveSuccesses,
      stats: {
        ...this.stats,
        successRate: Math.round(successRate * 100) / 100,
        currentUptime,
        currentDowntime,
        averageResponseTime: Math.round(this.stats.averageResponseTime * 100) / 100
      },
      recentHistory,
      config: this.config
    };
  }

  /**
   * Get health trends
   * @param {number} minutes - Number of minutes to analyze
   * @returns {Object} - Health trends
   */
  getHealthTrends(minutes = 60) {
    const cutoff = Date.now() - (minutes * 60 * 1000);
    const recentHistory = this.healthHistory.filter(entry => entry.timestamp >= cutoff);
    
    if (recentHistory.length === 0) {
      return {
        totalChecks: 0,
        successfulChecks: 0,
        failedChecks: 0,
        successRate: 0,
        averageResponseTime: 0,
        trend: 'unknown'
      };
    }
    
    const successful = recentHistory.filter(entry => entry.success);
    const failed = recentHistory.filter(entry => !entry.success);
    const successRate = (successful.length / recentHistory.length) * 100;
    const avgResponseTime = successful.length > 0 ? 
      successful.reduce((sum, entry) => sum + entry.duration, 0) / successful.length : 0;
    
    // Determine trend (improving, degrading, stable)
    const halfPoint = Math.floor(recentHistory.length / 2);
    const firstHalf = recentHistory.slice(0, halfPoint);
    const secondHalf = recentHistory.slice(halfPoint);
    
    const firstHalfSuccess = firstHalf.filter(entry => entry.success).length / firstHalf.length;
    const secondHalfSuccess = secondHalf.filter(entry => entry.success).length / secondHalf.length;
    
    let trend = 'stable';
    if (secondHalfSuccess > firstHalfSuccess + 0.1) {
      trend = 'improving';
    } else if (secondHalfSuccess < firstHalfSuccess - 0.1) {
      trend = 'degrading';
    }
    
    return {
      totalChecks: recentHistory.length,
      successfulChecks: successful.length,
      failedChecks: failed.length,
      successRate: Math.round(successRate * 100) / 100,
      averageResponseTime: Math.round(avgResponseTime * 100) / 100,
      trend
    };
  }

  /**
   * Force a health check
   * @returns {Promise<Object>} - Health check result
   */
  async forceHealthCheck() {
    winston.info('Forcing AI/ML health check');
    await this.performHealthCheck();
    return this.getHealthStatus();
  }

  /**
   * Reset health monitor state
   */
  reset() {
    winston.info('Resetting AI/ML health monitor');
    
    this.isHealthy = false;
    this.consecutiveFailures = 0;
    this.consecutiveSuccesses = 0;
    this.lastHealthCheck = null;
    this.lastHealthCheckDuration = null;
    this.healthHistory = [];
    
    // Reset stats
    this.stats = {
      totalChecks: 0,
      successfulChecks: 0,
      failedChecks: 0,
      averageResponseTime: 0,
      uptime: 0,
      downtimeStart: null,
      lastDowntime: null,
      uptimeStart: null
    };
    
    this.emit('reset');
  }

  /**
   * Delay utility
   * @param {number} ms - Milliseconds to delay
   * @returns {Promise} - Resolves after delay
   */
  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  /**
   * Cleanup resources
   */
  destroy() {
    this.stopMonitoring();
    this.removeAllListeners();
    winston.info('AI/ML health monitor destroyed');
  }
}

module.exports = AIMLHealthMonitor;
