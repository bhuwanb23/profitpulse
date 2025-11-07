const dotenv = require('dotenv');

// Load environment variables
dotenv.config();

/**
 * AI/ML Service Configuration
 * Centralized configuration for AI/ML service integration
 */
const aimlConfig = {
  // Basic Configuration
  baseUrl: process.env.AI_ML_SERVICE_URL || 'http://localhost:8000',
  apiKey: process.env.AI_ML_API_KEY || 'admin_key',
  timeout: parseInt(process.env.AI_ML_TIMEOUT) || 30000,
  
  // Retry Configuration
  retries: parseInt(process.env.AI_ML_RETRIES) || 3,
  retryDelay: parseInt(process.env.AI_ML_RETRY_DELAY) || 1000,
  retryBackoff: parseFloat(process.env.AI_ML_RETRY_BACKOFF) || 2,
  
  // Circuit Breaker Configuration
  circuitBreaker: {
    threshold: parseInt(process.env.AI_ML_CB_THRESHOLD) || 5,
    timeout: parseInt(process.env.AI_ML_CB_TIMEOUT) || 60000,
    resetTimeout: parseInt(process.env.AI_ML_CB_RESET_TIMEOUT) || 30000
  },
  
  // Health Monitoring Configuration
  health: {
    checkInterval: parseInt(process.env.AI_ML_HEALTH_INTERVAL) || 30000,
    timeout: parseInt(process.env.AI_ML_HEALTH_TIMEOUT) || 5000,
    retries: parseInt(process.env.AI_ML_HEALTH_RETRIES) || 2
  },
  
  // Caching Configuration
  cache: {
    ttl: parseInt(process.env.AI_ML_CACHE_TTL) || 300000, // 5 minutes
    maxSize: parseInt(process.env.AI_ML_CACHE_MAX_SIZE) || 1000,
    enabled: process.env.AI_ML_CACHE_ENABLED !== 'false'
  },
  
  // Feature Flags
  features: {
    enableFallback: process.env.AI_ML_ENABLE_FALLBACK !== 'false',
    enableMetrics: process.env.AI_ML_ENABLE_METRICS !== 'false',
    enableLogging: process.env.AI_ML_ENABLE_LOGGING !== 'false',
    enableCircuitBreaker: process.env.AI_ML_ENABLE_CB !== 'false'
  },
  
  // Model Configuration
  models: {
    confidenceThreshold: parseFloat(process.env.AI_CONFIDENCE_THRESHOLD) || 0.7,
    maxPredictionAge: parseInt(process.env.AI_ML_MAX_PREDICTION_AGE) || 3600000, // 1 hour
    batchSize: parseInt(process.env.AI_ML_BATCH_SIZE) || 100
  },
  
  // Logging Configuration
  logging: {
    level: process.env.LOG_LEVEL || 'info',
    enableRequestLogging: process.env.AI_ML_LOG_REQUESTS !== 'false',
    enableResponseLogging: process.env.AI_ML_LOG_RESPONSES !== 'false',
    enableMetricsLogging: process.env.AI_ML_LOG_METRICS !== 'false'
  }
};

/**
 * Validate configuration
 */
const validateConfig = () => {
  const errors = [];
  
  if (!aimlConfig.baseUrl) {
    errors.push('AI_ML_SERVICE_URL is required');
  }
  
  if (!aimlConfig.apiKey) {
    errors.push('AI_ML_API_KEY is required');
  }
  
  if (aimlConfig.timeout < 1000) {
    errors.push('AI_ML_TIMEOUT must be at least 1000ms');
  }
  
  if (aimlConfig.retries < 0 || aimlConfig.retries > 10) {
    errors.push('AI_ML_RETRIES must be between 0 and 10');
  }
  
  if (aimlConfig.circuitBreaker.threshold < 1) {
    errors.push('AI_ML_CB_THRESHOLD must be at least 1');
  }
  
  if (errors.length > 0) {
    throw new Error(`AI/ML Configuration validation failed:\n${errors.join('\n')}`);
  }
  
  return true;
};

/**
 * Get configuration with validation
 */
const getConfig = () => {
  validateConfig();
  return aimlConfig;
};

/**
 * Get specific configuration section
 */
const getSection = (section) => {
  validateConfig();
  return aimlConfig[section] || {};
};

/**
 * Check if a feature is enabled
 */
const isFeatureEnabled = (feature) => {
  return aimlConfig.features[feature] === true;
};

/**
 * Get environment-specific configuration
 */
const getEnvironmentConfig = () => {
  const env = process.env.NODE_ENV || 'development';
  
  const envConfigs = {
    development: {
      logging: { level: 'debug' },
      features: { enableLogging: true }
    },
    production: {
      logging: { level: 'info' },
      features: { enableLogging: false }
    },
    test: {
      timeout: 5000,
      retries: 1,
      features: { enableFallback: true }
    }
  };
  
  return envConfigs[env] || {};
};

module.exports = {
  aimlConfig,
  getConfig,
  getSection,
  isFeatureEnabled,
  getEnvironmentConfig,
  validateConfig
};
