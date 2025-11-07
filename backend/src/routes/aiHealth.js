const express = require('express');
const router = express.Router();
const aiClient = require('../services/ai-ml');
const { authenticateToken } = require('../middleware/auth');
const winston = require('winston');

/**
 * AI/ML Health Routes
 * Provides health monitoring and diagnostics for AI/ML service integration
 */

/**
 * @route GET /api/ai/health
 * @desc Get AI/ML service health status
 * @access Private
 */
router.get('/health', authenticateToken, async (req, res) => {
  try {
    const healthStatus = await aiClient.getHealthStatus();
    
    res.json({
      success: true,
      data: healthStatus,
      timestamp: new Date().toISOString()
    });
    
  } catch (error) {
    winston.error('AI/ML health check failed:', error);
    
    res.status(500).json({
      success: false,
      message: 'AI/ML health check failed',
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

/**
 * @route GET /api/ai/health/connectivity
 * @desc Test connectivity to AI/ML service
 * @access Private
 */
router.get('/health/connectivity', authenticateToken, async (req, res) => {
  try {
    const startTime = Date.now();
    const healthCheck = await aiClient.healthCheck();
    const responseTime = Date.now() - startTime;
    
    res.json({
      success: true,
      data: {
        connected: true,
        responseTime,
        serviceStatus: healthCheck,
        timestamp: new Date().toISOString()
      }
    });
    
  } catch (error) {
    winston.error('AI/ML connectivity test failed:', error);
    
    res.status(503).json({
      success: false,
      data: {
        connected: false,
        error: error.message,
        timestamp: new Date().toISOString()
      }
    });
  }
});

/**
 * @route GET /api/ai/health/metrics
 * @desc Get AI/ML service metrics
 * @access Private
 */
router.get('/health/metrics', authenticateToken, async (req, res) => {
  try {
    const { window = '5min', format = 'json' } = req.query;
    
    const metrics = aiClient.getMetrics();
    
    if (format === 'prometheus') {
      res.set('Content-Type', 'text/plain');
      res.send(aiClient.metrics.exportMetrics('prometheus'));
    } else {
      res.json({
        success: true,
        data: {
          metrics,
          window,
          timestamp: new Date().toISOString()
        }
      });
    }
    
  } catch (error) {
    winston.error('Failed to get AI/ML metrics:', error);
    
    res.status(500).json({
      success: false,
      message: 'Failed to get AI/ML metrics',
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

/**
 * @route GET /api/ai/health/circuit-breaker
 * @desc Get circuit breaker status
 * @access Private
 */
router.get('/health/circuit-breaker', authenticateToken, async (req, res) => {
  try {
    const status = aiClient.circuitBreaker.getStatus();
    
    res.json({
      success: true,
      data: status,
      timestamp: new Date().toISOString()
    });
    
  } catch (error) {
    winston.error('Failed to get circuit breaker status:', error);
    
    res.status(500).json({
      success: false,
      message: 'Failed to get circuit breaker status',
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

/**
 * @route POST /api/ai/health/circuit-breaker/reset
 * @desc Reset circuit breaker
 * @access Private
 */
router.post('/health/circuit-breaker/reset', authenticateToken, async (req, res) => {
  try {
    aiClient.resetCircuitBreaker();
    
    res.json({
      success: true,
      message: 'Circuit breaker reset successfully',
      timestamp: new Date().toISOString()
    });
    
  } catch (error) {
    winston.error('Failed to reset circuit breaker:', error);
    
    res.status(500).json({
      success: false,
      message: 'Failed to reset circuit breaker',
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

/**
 * @route GET /api/ai/health/fallback
 * @desc Get fallback service status
 * @access Private
 */
router.get('/health/fallback', authenticateToken, async (req, res) => {
  try {
    const fallbackStatus = {
      available: true,
      handlers: aiClient.fallbackService.getAvailableHandlers(),
      cacheStats: aiClient.fallbackService.getCacheStats()
    };
    
    res.json({
      success: true,
      data: fallbackStatus,
      timestamp: new Date().toISOString()
    });
    
  } catch (error) {
    winston.error('Failed to get fallback status:', error);
    
    res.status(500).json({
      success: false,
      message: 'Failed to get fallback status',
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

/**
 * @route DELETE /api/ai/health/fallback/cache
 * @desc Clear fallback cache
 * @access Private
 */
router.delete('/health/fallback/cache', authenticateToken, async (req, res) => {
  try {
    const { pattern } = req.query;
    
    aiClient.clearFallbackCache(pattern);
    
    res.json({
      success: true,
      message: pattern ? `Cache cleared for pattern: ${pattern}` : 'All cache cleared',
      timestamp: new Date().toISOString()
    });
    
  } catch (error) {
    winston.error('Failed to clear fallback cache:', error);
    
    res.status(500).json({
      success: false,
      message: 'Failed to clear fallback cache',
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

/**
 * @route GET /api/ai/health/monitor
 * @desc Get health monitor status
 * @access Private
 */
router.get('/health/monitor', authenticateToken, async (req, res) => {
  try {
    const { minutes = 60 } = req.query;
    
    const monitorStatus = aiClient.healthMonitor.getHealthStatus();
    const trends = aiClient.healthMonitor.getHealthTrends(parseInt(minutes));
    
    res.json({
      success: true,
      data: {
        status: monitorStatus,
        trends,
        timestamp: new Date().toISOString()
      }
    });
    
  } catch (error) {
    winston.error('Failed to get health monitor status:', error);
    
    res.status(500).json({
      success: false,
      message: 'Failed to get health monitor status',
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

/**
 * @route POST /api/ai/health/monitor/check
 * @desc Force a health check
 * @access Private
 */
router.post('/health/monitor/check', authenticateToken, async (req, res) => {
  try {
    const result = await aiClient.healthMonitor.forceHealthCheck();
    
    res.json({
      success: true,
      data: result,
      message: 'Health check completed',
      timestamp: new Date().toISOString()
    });
    
  } catch (error) {
    winston.error('Failed to perform health check:', error);
    
    res.status(500).json({
      success: false,
      message: 'Failed to perform health check',
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

/**
 * @route GET /api/ai/health/models/:modelName
 * @desc Get specific model health
 * @access Private
 */
router.get('/health/models/:modelName', authenticateToken, async (req, res) => {
  try {
    const { modelName } = req.params;
    
    const modelHealth = await aiClient.getModelHealth(modelName);
    const modelInfo = await aiClient.getModelInfo(modelName);
    
    res.json({
      success: true,
      data: {
        model: modelName,
        health: modelHealth,
        info: modelInfo,
        timestamp: new Date().toISOString()
      }
    });
    
  } catch (error) {
    winston.error(`Failed to get model health for ${req.params.modelName}:`, error);
    
    res.status(500).json({
      success: false,
      message: `Failed to get model health for ${req.params.modelName}`,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

/**
 * @route GET /api/ai/health/summary
 * @desc Get comprehensive health summary
 * @access Private
 */
router.get('/health/summary', authenticateToken, async (req, res) => {
  try {
    const healthStatus = await aiClient.getHealthStatus();
    const metrics = aiClient.getMetrics();
    
    // Calculate overall health score
    const circuitBreakerHealthy = healthStatus.circuitBreaker.isClosed;
    const serviceHealthy = healthStatus.healthMonitor.isHealthy;
    const metricsHealthy = metrics.requests.successRate > 90;
    
    const healthScore = [circuitBreakerHealthy, serviceHealthy, metricsHealthy]
      .filter(Boolean).length / 3 * 100;
    
    const summary = {
      overallHealth: healthScore >= 80 ? 'healthy' : healthScore >= 60 ? 'degraded' : 'unhealthy',
      healthScore: Math.round(healthScore),
      components: {
        aiService: {
          status: serviceHealthy ? 'healthy' : 'unhealthy',
          lastCheck: healthStatus.healthMonitor.lastHealthCheck,
          uptime: healthStatus.healthMonitor.stats.currentUptime
        },
        circuitBreaker: {
          status: circuitBreakerHealthy ? 'closed' : healthStatus.circuitBreaker.state.toLowerCase(),
          failureCount: healthStatus.circuitBreaker.failureCount,
          successRate: metrics.requests.successRate
        },
        fallback: {
          status: 'available',
          cacheHitRate: healthStatus.fallback.cacheStats.utilizationRate,
          handlersAvailable: Object.keys(healthStatus.fallback.handlers).length
        }
      },
      metrics: {
        totalRequests: metrics.requests.total,
        successRate: metrics.requests.successRate,
        averageResponseTime: metrics.responseTime.average,
        uptime: healthStatus.healthMonitor.stats.currentUptime
      },
      timestamp: new Date().toISOString()
    };
    
    res.json({
      success: true,
      data: summary
    });
    
  } catch (error) {
    winston.error('Failed to get health summary:', error);
    
    res.status(500).json({
      success: false,
      message: 'Failed to get health summary',
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

module.exports = router;
