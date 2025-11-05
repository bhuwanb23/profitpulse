const axios = require('axios');
const winston = require('winston');

class AIClient {
  constructor() {
    // Get configuration from environment variables
    this.baseUrl = process.env.AI_ML_SERVICE_URL || 'http://localhost:8000';
    this.apiKey = process.env.AI_ML_API_KEY || 'admin_key';
    this.timeout = process.env.AI_ML_TIMEOUT ? parseInt(process.env.AI_ML_TIMEOUT) : 30000;
    
    // Create axios instance with default configuration
    this.client = axios.create({
      baseURL: this.baseUrl,
      timeout: this.timeout,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.apiKey}`
      }
    });

    // Add request interceptor for logging (only if interceptors exist)
    if (this.client && this.client.interceptors) {
      this.client.interceptors.request.use(
        (config) => {
          winston.info(`AI/ML API Request: ${config.method?.toUpperCase()} ${config.url}`, {
            method: config.method?.toUpperCase(),
            url: config.url,
            headers: config.headers,
            data: config.data
          });
          return config;
        },
        (error) => {
          winston.error('AI/ML API Request Error:', error);
          return Promise.reject(error);
        }
      );

      // Add response interceptor for logging and error handling
      this.client.interceptors.response.use(
        (response) => {
          winston.info(`AI/ML API Response: ${response.status} ${response.config?.url}`, {
            status: response.status,
            url: response.config?.url,
            data: response.data
          });
          return response;
        },
        (error) => {
          winston.error('AI/ML API Response Error:', {
            message: error.message,
            status: error.response?.status,
            url: error.response?.config?.url,
            data: error.response?.data
          });
          return Promise.reject(error);
        }
      );
    }
  }

  /**
   * Health check for the AI/ML service
   * @returns {Promise<Object>} Health status
   */
  async healthCheck() {
    try {
      const response = await this.client.get('/api/health');
      return response.data;
    } catch (error) {
      throw new Error(`Health check failed: ${error.message}`);
    }
  }

  /**
   * Predict client profitability
   * @param {Object} data - Client data for prediction
   * @param {Object} options - Prediction options
   * @returns {Promise<Object>} Prediction result
   */
  async predictProfitability(data, options = {}) {
    try {
      const response = await this.client.post('/api/profitability', data, {
        params: {
          model_version: options.modelVersion,
          return_confidence: options.returnConfidence || false,
          return_explanation: options.returnExplanation || false
        }
      });
      return response.data;
    } catch (error) {
      throw new Error(`Profitability prediction failed: ${error.message}`);
    }
  }

  /**
   * Predict client churn
   * @param {Object} data - Client data for prediction
   * @param {Object} options - Prediction options
   * @returns {Promise<Object>} Prediction result
   */
  async predictChurn(data, options = {}) {
    try {
      const response = await this.client.post('/api/churn/predict', data, {
        params: {
          model_version: options.modelVersion
        }
      });
      return response.data;
    } catch (error) {
      throw new Error(`Churn prediction failed: ${error.message}`);
    }
  }

  /**
   * Detect revenue leaks
   * @param {Object} data - Billing and service data
   * @param {Object} options - Detection options
   * @returns {Promise<Object>} Detection result
   */
  async detectRevenueLeaks(data, options = {}) {
    try {
      const response = await this.client.post('/api/revenue-leak/detect', data, {
        params: {
          model_version: options.modelVersion
        }
      });
      return response.data;
    } catch (error) {
      throw new Error(`Revenue leak detection failed: ${error.message}`);
    }
  }

  /**
   * Get dynamic pricing recommendation
   * @param {Object} data - Client and market data
   * @param {Object} options - Pricing options
   * @returns {Promise<Object>} Pricing recommendation
   */
  async getDynamicPricing(data, options = {}) {
    try {
      const response = await this.client.post('/api/pricing/recommend', data, {
        params: {
          model_version: options.modelVersion
        }
      });
      return response.data;
    } catch (error) {
      throw new Error(`Dynamic pricing recommendation failed: ${error.message}`);
    }
  }

  /**
   * Optimize budget allocation
   * @param {Object} data - Budget and department data
   * @param {Object} options - Optimization options
   * @returns {Promise<Object>} Optimization result
   */
  async optimizeBudget(data, options = {}) {
    try {
      const response = await this.client.post('/api/budget/optimize', data, {
        params: {
          model_version: options.modelVersion
        }
      });
      return response.data;
    } catch (error) {
      throw new Error(`Budget optimization failed: ${error.message}`);
    }
  }

  /**
   * Forecast demand
   * @param {Object} data - Historical demand data
   * @param {Object} options - Forecasting options
   * @returns {Promise<Object>} Forecast result
   */
  async forecastDemand(data, options = {}) {
    try {
      const response = await this.client.post('/api/demand/forecast', data, {
        params: {
          model_version: options.modelVersion,
          forecast_horizon: options.forecastHorizon || 30,
          seasonality: options.seasonality !== false
        }
      });
      return response.data;
    } catch (error) {
      throw new Error(`Demand forecasting failed: ${error.message}`);
    }
  }

  /**
   * Detect anomalies
   * @param {Object} data - Time series data
   * @param {Object} options - Detection options
   * @returns {Promise<Object>} Anomaly detection result
   */
  async detectAnomalies(data, options = {}) {
    try {
      const response = await this.client.post('/api/anomaly/detect', data, {
        params: {
          model_version: options.modelVersion,
          detection_method: options.detectionMethod || 'ensemble',
          window_size: options.windowSize || 100
        }
      });
      return response.data;
    } catch (error) {
      throw new Error(`Anomaly detection failed: ${error.message}`);
    }
  }

  /**
   * Get model information
   * @param {string} modelName - Name of the model
   * @returns {Promise<Object>} Model information
   */
  async getModelInfo(modelName) {
    try {
      const response = await this.client.get(`/api/models/${modelName}/info`);
      return response.data;
    } catch (error) {
      throw new Error(`Getting model info failed: ${error.message}`);
    }
  }

  /**
   * Get model health status
   * @param {string} modelName - Name of the model
   * @returns {Promise<Object>} Model health status
   */
  async getModelHealth(modelName) {
    try {
      const response = await this.client.get(`/api/models/${modelName}/health`);
      return response.data;
    } catch (error) {
      throw new Error(`Getting model health failed: ${error.message}`);
    }
  }

  /**
   * Perform batch predictions
   * @param {string} modelName - Name of the model to use
   * @param {Array} data - Array of data for predictions
   * @param {Object} options - Batch options
   * @returns {Promise<Object>} Batch prediction result
   */
  async batchPredict(modelName, data, options = {}) {
    try {
      const response = await this.client.post(`/api/${modelName}/batch`, { data }, {
        params: {
          model_version: options.modelVersion
        }
      });
      return response.data;
    } catch (error) {
      throw new Error(`Batch prediction failed: ${error.message}`);
    }
  }
}

// Export singleton instance
module.exports = new AIClient();