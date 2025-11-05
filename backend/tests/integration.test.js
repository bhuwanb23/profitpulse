const { client } = require('../src/services/ai-ml');

describe('AI/ML Integration', () => {
  // This is a simple integration test to verify the client is properly exported
  test('AI/ML client should be defined', () => {
    expect(client).toBeDefined();
    expect(typeof client).toBe('object');
  });

  test('AI/ML client should have required methods', () => {
    expect(client).toHaveProperty('healthCheck');
    expect(client).toHaveProperty('predictProfitability');
    expect(client).toHaveProperty('predictChurn');
    expect(client).toHaveProperty('detectRevenueLeaks');
    expect(client).toHaveProperty('getDynamicPricing');
    expect(client).toHaveProperty('optimizeBudget');
    expect(client).toHaveProperty('forecastDemand');
    expect(client).toHaveProperty('detectAnomalies');
    expect(client).toHaveProperty('getModelInfo');
    expect(client).toHaveProperty('getModelHealth');
    expect(client).toHaveProperty('batchPredict');
  });
});