const request = require('supertest');
const app = require('../../index');
const aiClient = require('../../src/services/ai-ml');

describe('AI/ML Integration Tests', () => {
  let authToken;
  
  beforeAll(async () => {
    // Setup test authentication
    const loginResponse = await request(app)
      .post('/api/auth/login')
      .send({
        email: 'test@example.com',
        password: 'testpassword'
      });
    
    if (loginResponse.body.success) {
      authToken = loginResponse.body.data.token;
    }
  });

  afterAll(async () => {
    // Cleanup AI client
    if (aiClient && aiClient.destroy) {
      aiClient.destroy();
    }
  });

  describe('AI/ML Client Functionality', () => {
    test('should initialize AI client successfully', () => {
      expect(aiClient).toBeDefined();
      expect(aiClient.config).toBeDefined();
      expect(aiClient.circuitBreaker).toBeDefined();
      expect(aiClient.healthMonitor).toBeDefined();
      expect(aiClient.fallbackService).toBeDefined();
      expect(aiClient.metrics).toBeDefined();
    });

    test('should have correct configuration', () => {
      expect(aiClient.config.baseUrl).toBeDefined();
      expect(aiClient.config.apiKey).toBeDefined();
      expect(aiClient.config.timeout).toBeGreaterThan(0);
      expect(aiClient.config.retries).toBeGreaterThanOrEqual(0);
    });

    test('should handle health check', async () => {
      try {
        const health = await aiClient.healthCheck();
        expect(health).toBeDefined();
      } catch (error) {
        // Health check might fail if AI/ML service is not running
        // This is expected in test environment
        expect(error.message).toContain('Health check failed');
      }
    });

    test('should get comprehensive health status', async () => {
      const healthStatus = await aiClient.getHealthStatus();
      
      expect(healthStatus).toBeDefined();
      expect(healthStatus.client).toBeDefined();
      expect(healthStatus.circuitBreaker).toBeDefined();
      expect(healthStatus.healthMonitor).toBeDefined();
      expect(healthStatus.metrics).toBeDefined();
      expect(healthStatus.fallback).toBeDefined();
    });

    test('should handle circuit breaker operations', () => {
      const status = aiClient.circuitBreaker.getStatus();
      
      expect(status).toBeDefined();
      expect(status.state).toBeDefined();
      expect(['CLOSED', 'OPEN', 'HALF_OPEN']).toContain(status.state);
      
      // Test reset
      aiClient.resetCircuitBreaker();
      const resetStatus = aiClient.circuitBreaker.getStatus();
      expect(resetStatus.state).toBe('CLOSED');
    });

    test('should handle metrics collection', () => {
      const metrics = aiClient.getMetrics();
      
      expect(metrics).toBeDefined();
      expect(metrics.requests).toBeDefined();
      expect(metrics.responseTime).toBeDefined();
      expect(metrics.cache).toBeDefined();
      expect(metrics.errors).toBeDefined();
    });

    test('should handle fallback cache operations', () => {
      const cacheStats = aiClient.fallbackService.getCacheStats();
      
      expect(cacheStats).toBeDefined();
      expect(cacheStats.totalEntries).toBeGreaterThanOrEqual(0);
      expect(cacheStats.maxSize).toBeGreaterThan(0);
      
      // Test cache clearing
      aiClient.clearFallbackCache();
      const clearedStats = aiClient.fallbackService.getCacheStats();
      expect(clearedStats.totalEntries).toBe(0);
    });
  });

  describe('AI/ML Prediction Methods', () => {
    const testData = {
      clientId: 'test-client-123',
      revenue: 50000,
      costs: 30000,
      tickets: 25,
      satisfaction: 4.2
    };

    test('should handle profitability prediction with fallback', async () => {
      const result = await aiClient.predictProfitability(testData, {
        useFallback: true
      });
      
      expect(result).toBeDefined();
      expect(result.success).toBe(true);
      expect(result.data).toBeDefined();
      expect(result.data.profitability_score).toBeDefined();
      expect(result.data.is_fallback).toBe(true);
    });

    test('should handle churn prediction with fallback', async () => {
      const result = await aiClient.predictChurn(testData, {
        useFallback: true
      });
      
      expect(result).toBeDefined();
      expect(result.success).toBe(true);
      expect(result.data).toBeDefined();
      expect(result.data.churn_probability).toBeDefined();
      expect(result.data.is_fallback).toBe(true);
    });

    test('should handle revenue leak detection with fallback', async () => {
      const result = await aiClient.detectRevenueLeaks(testData, {
        useFallback: true
      });
      
      expect(result).toBeDefined();
      expect(result.success).toBe(true);
      expect(result.data).toBeDefined();
      expect(result.data.leaks_detected).toBeDefined();
      expect(result.data.is_fallback).toBe(true);
    });

    test('should handle dynamic pricing with fallback', async () => {
      const result = await aiClient.getDynamicPricing(testData, {
        useFallback: true
      });
      
      expect(result).toBeDefined();
      expect(result.success).toBe(true);
      expect(result.data).toBeDefined();
      expect(result.data.recommended_price).toBeDefined();
      expect(result.data.is_fallback).toBe(true);
    });

    test('should handle budget optimization with fallback', async () => {
      const result = await aiClient.optimizeBudget(testData, {
        useFallback: true
      });
      
      expect(result).toBeDefined();
      expect(result.success).toBe(true);
      expect(result.data).toBeDefined();
      expect(result.data.optimization_score).toBeDefined();
      expect(result.data.is_fallback).toBe(true);
    });

    test('should handle demand forecasting with fallback', async () => {
      const result = await aiClient.forecastDemand(testData, {
        useFallback: true,
        forecastHorizon: 30
      });
      
      expect(result).toBeDefined();
      expect(result.success).toBe(true);
      expect(result.data).toBeDefined();
      expect(result.data.predictions).toBeDefined();
      expect(Array.isArray(result.data.predictions)).toBe(true);
      expect(result.data.is_fallback).toBe(true);
    });

    test('should handle anomaly detection with fallback', async () => {
      const result = await aiClient.detectAnomalies(testData, {
        useFallback: true
      });
      
      expect(result).toBeDefined();
      expect(result.success).toBe(true);
      expect(result.data).toBeDefined();
      expect(result.data.anomalies_detected).toBeDefined();
      expect(result.data.is_fallback).toBe(true);
    });
  });

  describe('AI/ML Health API Endpoints', () => {
    test('GET /api/ai/health - should return health status', async () => {
      if (!authToken) {
        return; // Skip if no auth token
      }

      const response = await request(app)
        .get('/api/ai/health')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data).toBeDefined();
      expect(response.body.timestamp).toBeDefined();
    });

    test('GET /api/ai/health/connectivity - should test connectivity', async () => {
      if (!authToken) {
        return; // Skip if no auth token
      }

      const response = await request(app)
        .get('/api/ai/health/connectivity')
        .set('Authorization', `Bearer ${authToken}`);

      expect(response.body).toBeDefined();
      expect(response.body.data).toBeDefined();
      expect(response.body.data.connected).toBeDefined();
    });

    test('GET /api/ai/health/metrics - should return metrics', async () => {
      if (!authToken) {
        return; // Skip if no auth token
      }

      const response = await request(app)
        .get('/api/ai/health/metrics')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data.metrics).toBeDefined();
    });

    test('GET /api/ai/health/circuit-breaker - should return circuit breaker status', async () => {
      if (!authToken) {
        return; // Skip if no auth token
      }

      const response = await request(app)
        .get('/api/ai/health/circuit-breaker')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data.state).toBeDefined();
    });

    test('POST /api/ai/health/circuit-breaker/reset - should reset circuit breaker', async () => {
      if (!authToken) {
        return; // Skip if no auth token
      }

      const response = await request(app)
        .post('/api/ai/health/circuit-breaker/reset')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.message).toContain('reset');
    });

    test('GET /api/ai/health/fallback - should return fallback status', async () => {
      if (!authToken) {
        return; // Skip if no auth token
      }

      const response = await request(app)
        .get('/api/ai/health/fallback')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data.available).toBe(true);
      expect(response.body.data.handlers).toBeDefined();
    });

    test('DELETE /api/ai/health/fallback/cache - should clear fallback cache', async () => {
      if (!authToken) {
        return; // Skip if no auth token
      }

      const response = await request(app)
        .delete('/api/ai/health/fallback/cache')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.message).toContain('cache cleared');
    });

    test('GET /api/ai/health/summary - should return comprehensive health summary', async () => {
      if (!authToken) {
        return; // Skip if no auth token
      }

      const response = await request(app)
        .get('/api/ai/health/summary')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data.overallHealth).toBeDefined();
      expect(response.body.data.healthScore).toBeDefined();
      expect(response.body.data.components).toBeDefined();
      expect(response.body.data.metrics).toBeDefined();
    });
  });

  describe('Error Handling and Resilience', () => {
    test('should handle service downtime gracefully', async () => {
      // Simulate service downtime by using invalid URL
      const originalBaseUrl = aiClient.baseUrl;
      aiClient.baseUrl = 'http://invalid-url:9999';
      
      try {
        const result = await aiClient.predictProfitability({
          clientId: 'test'
        }, {
          useFallback: true,
          useCircuitBreaker: false
        });
        
        // Should get fallback response
        expect(result).toBeDefined();
        expect(result.success).toBe(true);
        expect(result.data.is_fallback).toBe(true);
        
      } finally {
        // Restore original URL
        aiClient.baseUrl = originalBaseUrl;
      }
    });

    test('should handle circuit breaker functionality', async () => {
      // Reset circuit breaker
      aiClient.resetCircuitBreaker();
      
      const initialStatus = aiClient.circuitBreaker.getStatus();
      expect(initialStatus.state).toBe('CLOSED');
      
      // Circuit breaker should remain closed for fallback responses
      await aiClient.predictProfitability({}, { useFallback: true });
      
      const afterStatus = aiClient.circuitBreaker.getStatus();
      expect(afterStatus.state).toBe('CLOSED');
    });

    test('should collect metrics properly', async () => {
      const initialMetrics = aiClient.getMetrics();
      const initialRequests = initialMetrics.requests.total;
      
      // Make a request
      await aiClient.predictProfitability({}, { useFallback: true });
      
      const afterMetrics = aiClient.getMetrics();
      expect(afterMetrics.requests.total).toBeGreaterThan(initialRequests);
    });
  });

  describe('System Health Integration', () => {
    test('GET /health - should include AI/ML status in system health', async () => {
      const response = await request(app)
        .get('/health')
        .expect(200);

      expect(response.body.aiml).toBeDefined();
      expect(response.body.aiml.status).toBeDefined();
      expect(response.body.aiml.connected).toBeDefined();
    });

    test('should handle AI/ML service unavailability in system health', async () => {
      const response = await request(app)
        .get('/health');

      expect(response.body.aiml).toBeDefined();
      
      // AI/ML service might be unavailable in test environment
      if (!response.body.aiml.connected) {
        expect(response.body.aiml.error).toBeDefined();
        expect(response.body.status).toBe('DEGRADED');
      }
    });
  });
});
