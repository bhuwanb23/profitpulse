const { client } = require('../services/ai-ml');
const { validationResult } = require('express-validator');

/**
 * Health check for AI/ML service
 */
const healthCheck = async (req, res) => {
  try {
    const health = await client.healthCheck();
    res.json({
      success: true,
      data: health
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'AI/ML service health check failed',
      error: error.message
    });
  }
};

/**
 * Predict client profitability
 */
const predictProfitability = async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        message: 'Validation failed',
        errors: errors.array()
      });
    }

    const { client_id, financial_data, operational_data, historical_period_months } = req.body;
    const { model_version, return_confidence, return_explanation } = req.query;

    const data = {
      client_id,
      financial_data,
      operational_data,
      historical_period_months
    };

    const options = {
      modelVersion: model_version,
      returnConfidence: return_confidence === 'true',
      returnExplanation: return_explanation === 'true'
    };

    const result = await client.predictProfitability(data, options);
    
    res.json({
      success: true,
      data: result
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Profitability prediction failed',
      error: error.message
    });
  }
};

/**
 * Predict client churn
 */
const predictChurn = async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        message: 'Validation failed',
        errors: errors.array()
      });
    }

    const { client_id, features, timeframe_days } = req.body;
    const { model_version } = req.query;

    const data = {
      client_id,
      features,
      timeframe_days
    };

    const options = {
      modelVersion: model_version
    };

    const result = await client.predictChurn(data, options);
    
    res.json({
      success: true,
      data: result
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Churn prediction failed',
      error: error.message
    });
  }
};

/**
 * Detect revenue leaks
 */
const detectRevenueLeaks = async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        message: 'Validation failed',
        errors: errors.array()
      });
    }

    const { billing_data, service_data, time_period_days } = req.body;
    const { model_version } = req.query;

    const data = {
      billing_data,
      service_data,
      time_period_days
    };

    const options = {
      modelVersion: model_version
    };

    const result = await client.detectRevenueLeaks(data, options);
    
    res.json({
      success: true,
      data: result
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Revenue leak detection failed',
      error: error.message
    });
  }
};

/**
 * Get dynamic pricing recommendation
 */
const getDynamicPricing = async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        message: 'Validation failed',
        errors: errors.array()
      });
    }

    const { client_profile, service_type, market_conditions, competitor_data } = req.body;
    const { model_version } = req.query;

    const data = {
      client_profile,
      service_type,
      market_conditions,
      competitor_data
    };

    const options = {
      modelVersion: model_version
    };

    const result = await client.getDynamicPricing(data, options);
    
    res.json({
      success: true,
      data: result
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Dynamic pricing recommendation failed',
      error: error.message
    });
  }
};

/**
 * Optimize budget allocation
 */
const optimizeBudget = async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        message: 'Validation failed',
        errors: errors.array()
      });
    }

    const { current_budget, departments, constraints, optimization_method } = req.body;
    const { model_version } = req.query;

    const data = {
      current_budget,
      departments,
      constraints,
      optimization_method
    };

    const options = {
      modelVersion: model_version
    };

    const result = await client.optimizeBudget(data, options);
    
    res.json({
      success: true,
      data: result
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Budget optimization failed',
      error: error.message
    });
  }
};

/**
 * Forecast demand
 */
const forecastDemand = async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        message: 'Validation failed',
        errors: errors.array()
      });
    }

    const { historical_data, forecast_horizon, seasonality, method } = req.body;
    const { model_version } = req.query;

    const data = {
      historical_data,
      forecast_horizon,
      seasonality,
      method
    };

    const options = {
      modelVersion: model_version,
      forecastHorizon: forecast_horizon,
      seasonality: seasonality
    };

    const result = await client.forecastDemand(data, options);
    
    res.json({
      success: true,
      data: result
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Demand forecasting failed',
      error: error.message
    });
  }
};

/**
 * Detect anomalies
 */
const detectAnomalies = async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        message: 'Validation failed',
        errors: errors.array()
      });
    }

    const { data, stream_type, detection_method, window_size } = req.body;
    const { model_version } = req.query;

    const requestData = {
      data,
      stream_type,
      detection_method,
      window_size
    };

    const options = {
      modelVersion: model_version,
      detectionMethod: detection_method,
      windowSize: window_size
    };

    const result = await client.detectAnomalies(requestData, options);
    
    res.json({
      success: true,
      data: result
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Anomaly detection failed',
      error: error.message
    });
  }
};

/**
 * Get model information
 */
const getModelInfo = async (req, res) => {
  try {
    const { model_name } = req.params;
    const result = await client.getModelInfo(model_name);
    
    res.json({
      success: true,
      data: result
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Getting model info failed',
      error: error.message
    });
  }
};

/**
 * Get model health status
 */
const getModelHealth = async (req, res) => {
  try {
    const { model_name } = req.params;
    const result = await client.getModelHealth(model_name);
    
    res.json({
      success: true,
      data: result
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Getting model health failed',
      error: error.message
    });
  }
};

/**
 * Perform batch predictions
 */
const batchPredict = async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        message: 'Validation failed',
        errors: errors.array()
      });
    }

    const { model_name, data } = req.body;
    const { model_version } = req.query;

    const options = {
      modelVersion: model_version
    };

    const result = await client.batchPredict(model_name, data, options);
    
    res.json({
      success: true,
      data: result
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Batch prediction failed',
      error: error.message
    });
  }
};

module.exports = {
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
};