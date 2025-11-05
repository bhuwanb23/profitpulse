const request = require('supertest');
const express = require('express');
const { body, validationResult } = require('express-validator');

// Mock the AI client
jest.mock('../src/services/ai-ml', () => ({
  client: {
    healthCheck: jest.fn(),
    predictProfitability: jest.fn(),
    predictChurn: jest.fn(),
    detectRevenueLeaks: jest.fn(),
    getDynamicPricing: jest.fn(),
    optimizeBudget: jest.fn(),
    forecastDemand: jest.fn(),
    detectAnomalies: jest.fn(),
    getModelInfo: jest.fn(),
    getModelHealth: jest.fn(),
    batchPredict: jest.fn()
  }
}));

const { client } = require('../src/services/ai-ml');
const {
  healthCheck,
  predictProfitability,
  predictChurn,
  detectRevenueLeaks,
  getDynamicPricing,
  optimizeBudget,
  forecastDemand,
  detectAnomalies,
  getModelInfo,
  getModelHealth,
  batchPredict
} = require('../src/controllers/aiController');

// Create a test app
const app = express();
app.use(express.json());

// Mock express-validator
jest.mock('express-validator', () => ({
  validationResult: jest.fn(() => ({
    isEmpty: jest.fn(() => true),
    array: jest.fn(() => [])
  })),
  body: jest.fn(() => ({ notEmpty: jest.fn(() => ({ withMessage: jest.fn(() => ({})) })) })),
  param: jest.fn(() => ({ notEmpty: jest.fn(() => ({ withMessage: jest.fn(() => ({})) })) })),
  query: jest.fn(() => ({ optional: jest.fn(() => ({ isString: jest.fn(() => ({ withMessage: jest.fn(() => ({})) })) })) }))
}));

// Test routes
app.get('/health', healthCheck);
app.post('/profitability', predictProfitability);
app.post('/churn', predictChurn);
app.post('/revenue-leaks', detectRevenueLeaks);
app.post('/pricing', getDynamicPricing);
app.post('/budget', optimizeBudget);
app.post('/demand', forecastDemand);
app.post('/anomalies', detectAnomalies);
app.get('/models/:model_name/info', getModelInfo);
app.get('/models/:model_name/health', getModelHealth);
app.post('/batch', batchPredict);

describe('AI Controller', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('healthCheck', () => {
    it('should return health status', async () => {
      const mockHealth = {
        status: 'healthy',
        version: '1.0.0'
      };
      
      client.healthCheck.mockResolvedValue(mockHealth);

      const response = await request(app)
        .get('/health')
        .expect(200);

      expect(response.body).toEqual({
        success: true,
        data: mockHealth
      });
    });

    it('should handle health check errors', async () => {
      client.healthCheck.mockRejectedValue(new Error('Service unavailable'));

      const response = await request(app)
        .get('/health')
        .expect(500);

      expect(response.body).toEqual({
        success: false,
        message: 'AI/ML service health check failed',
        error: 'Service unavailable'
      });
    });
  });

  describe('predictProfitability', () => {
    it('should make profitability prediction', async () => {
      const mockRequest = {
        client_id: 'client123',
        financial_data: { revenue: 10000 }
      };
      
      const mockResponse = {
        prediction: 85,
        profitability_score: 85
      };
      
      client.predictProfitability.mockResolvedValue(mockResponse);

      const response = await request(app)
        .post('/profitability')
        .send(mockRequest)
        .expect(200);

      expect(response.body).toEqual({
        success: true,
        data: mockResponse
      });
    });
  });

  describe('predictChurn', () => {
    it('should make churn prediction', async () => {
      const mockRequest = {
        client_id: 'client123',
        features: { usage: 0.5 }
      };
      
      const mockResponse = {
        prediction: 0.3,
        churn_probability: 0.3
      };
      
      client.predictChurn.mockResolvedValue(mockResponse);

      const response = await request(app)
        .post('/churn')
        .send(mockRequest)
        .expect(200);

      expect(response.body).toEqual({
        success: true,
        data: mockResponse
      });
    });
  });

  describe('detectRevenueLeaks', () => {
    it('should detect revenue leaks', async () => {
      const mockRequest = {
        billing_data: [],
        service_data: []
      };
      
      const mockResponse = {
        leak_probability: 0.1,
        leak_amount: 100
      };
      
      client.detectRevenueLeaks.mockResolvedValue(mockResponse);

      const response = await request(app)
        .post('/revenue-leaks')
        .send(mockRequest)
        .expect(200);

      expect(response.body).toEqual({
        success: true,
        data: mockResponse
      });
    });
  });

  describe('getDynamicPricing', () => {
    it('should get dynamic pricing recommendation', async () => {
      const mockRequest = {
        client_profile: {},
        service_type: 'support'
      };
      
      const mockResponse = {
        recommended_price: 150,
        price_range: { min: 120, max: 180 }
      };
      
      client.getDynamicPricing.mockResolvedValue(mockResponse);

      const response = await request(app)
        .post('/pricing')
        .send(mockRequest)
        .expect(200);

      expect(response.body).toEqual({
        success: true,
        data: mockResponse
      });
    });
  });

  describe('optimizeBudget', () => {
    it('should optimize budget allocation', async () => {
      const mockRequest = {
        current_budget: 10000,
        departments: []
      };
      
      const mockResponse = {
        optimized_allocation: {},
        expected_roi_improvement: 0.15
      };
      
      client.optimizeBudget.mockResolvedValue(mockResponse);

      const response = await request(app)
        .post('/budget')
        .send(mockRequest)
        .expect(200);

      expect(response.body).toEqual({
        success: true,
        data: mockResponse
      });
    });
  });

  describe('forecastDemand', () => {
    it('should forecast demand', async () => {
      const mockRequest = {
        historical_data: [],
        forecast_horizon: 30
      };
      
      const mockResponse = {
        forecast: [],
        confidence_intervals: []
      };
      
      client.forecastDemand.mockResolvedValue(mockResponse);

      const response = await request(app)
        .post('/demand')
        .send(mockRequest)
        .expect(200);

      expect(response.body).toEqual({
        success: true,
        data: mockResponse
      });
    });
  });

  describe('detectAnomalies', () => {
    it('should detect anomalies', async () => {
      const mockRequest = {
        data: [],
        stream_type: 'metrics'
      };
      
      const mockResponse = {
        anomalies: [],
        severity_scores: []
      };
      
      client.detectAnomalies.mockResolvedValue(mockResponse);

      const response = await request(app)
        .post('/anomalies')
        .send(mockRequest)
        .expect(200);

      expect(response.body).toEqual({
        success: true,
        data: mockResponse
      });
    });
  });

  describe('getModelInfo', () => {
    it('should get model information', async () => {
      const modelName = 'profitability';
      const mockResponse = {
        name: modelName,
        version: '1.0.0'
      };
      
      client.getModelInfo.mockResolvedValue(mockResponse);

      const response = await request(app)
        .get(`/models/${modelName}/info`)
        .expect(200);

      expect(response.body).toEqual({
        success: true,
        data: mockResponse
      });
    });
  });

  describe('getModelHealth', () => {
    it('should get model health status', async () => {
      const modelName = 'profitability';
      const mockResponse = {
        status: 'healthy',
        healthy: true
      };
      
      client.getModelHealth.mockResolvedValue(mockResponse);

      const response = await request(app)
        .get(`/models/${modelName}/health`)
        .expect(200);

      expect(response.body).toEqual({
        success: true,
        data: mockResponse
      });
    });
  });

  describe('batchPredict', () => {
    it('should perform batch predictions', async () => {
      const mockRequest = {
        model_name: 'profitability',
        data: [{}, {}]
      };
      
      const mockResponse = {
        predictions: [],
        total_predictions: 2
      };
      
      client.batchPredict.mockResolvedValue(mockResponse);

      const response = await request(app)
        .post('/batch')
        .send(mockRequest)
        .expect(200);

      expect(response.body).toEqual({
        success: true,
        data: mockResponse
      });
    });
  });
});