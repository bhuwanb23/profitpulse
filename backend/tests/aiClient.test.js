// Mock axios before importing the client
jest.mock('axios');
jest.mock('winston', () => ({
  createLogger: jest.fn(() => ({
    info: jest.fn(),
    error: jest.fn()
  })),
  format: {
    combine: jest.fn(),
    timestamp: jest.fn(),
    errors: jest.fn(),
    json: jest.fn()
  },
  transports: {
    File: jest.fn(),
    Console: jest.fn()
  }
}));

const axios = require('axios');

describe('AI/ML Client', () => {
  let client;
  
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('constructor', () => {
    it('should create axios client with correct configuration', () => {
      // Reset module cache to re-import the client
      jest.resetModules();
      jest.mock('axios');
      
      // Import after resetting modules
      const freshAxios = require('axios');
      const { client: freshClient } = require('../src/services/ai-ml');
      
      expect(freshAxios.create).toHaveBeenCalledWith({
        baseURL: 'http://localhost:8000',
        timeout: 30000,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer admin_key'
        }
      });
    });
  });

  describe('healthCheck', () => {
    it('should call GET /api/health', async () => {
      // Create a mock client for this test
      const mockClient = {
        get: jest.fn().mockResolvedValue({ data: { status: 'healthy' } }),
        post: jest.fn(),
        interceptors: {
          request: { use: jest.fn() },
          response: { use: jest.fn() }
        }
      };
      
      // Create a fresh client instance for testing
      const AIClient = require('../src/services/ai-ml/client.js').constructor;
      const testClient = new AIClient();
      testClient.client = mockClient;
      
      const result = await testClient.healthCheck();
      
      expect(mockClient.get).toHaveBeenCalledWith('/api/health');
      expect(result).toEqual({ status: 'healthy' });
    });
  });
});