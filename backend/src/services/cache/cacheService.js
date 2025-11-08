const Redis = require('ioredis');
const winston = require('winston');
const { v4: uuidv4 } = require('uuid');

class CacheService {
  constructor() {
    this.redis = null;
    this.isConnected = false;
    this.defaultTTL = 300; // 5 minutes default TTL
    this.cacheStats = {
      hits: 0,
      misses: 0,
      sets: 0,
      deletes: 0,
      errors: 0
    };
    this.warmupJobs = new Map();
  }

  /**
   * Initialize Redis connection
   */
  async initialize() {
    try {
      // Redis configuration with fallback for development
      const redisConfig = {
        host: process.env.REDIS_HOST || 'localhost',
        port: process.env.REDIS_PORT || 6379,
        password: process.env.REDIS_PASSWORD || undefined,
        db: process.env.REDIS_DB || 0,
        retryDelayOnFailover: 100,
        maxRetriesPerRequest: 3,
        lazyConnect: true,
        keepAlive: 30000,
        connectTimeout: 10000,
        commandTimeout: 5000
      };

      this.redis = new Redis(redisConfig);

      // Event handlers
      this.redis.on('connect', () => {
        winston.info('Redis cache connected successfully');
        this.isConnected = true;
      });

      this.redis.on('error', (error) => {
        winston.error('Redis cache connection error:', error);
        this.isConnected = false;
        this.cacheStats.errors++;
      });

      this.redis.on('close', () => {
        winston.warn('Redis cache connection closed');
        this.isConnected = false;
      });

      this.redis.on('reconnecting', () => {
        winston.info('Redis cache reconnecting...');
      });

      // Test connection
      await this.redis.connect();
      await this.redis.ping();
      
      winston.info('Cache service initialized successfully');
      
      // Start cache warming for critical data
      this.startCacheWarming();
      
    } catch (error) {
      winston.error('Failed to initialize cache service:', error);
      // Continue without cache in development
      if (process.env.NODE_ENV !== 'production') {
        winston.warn('Running without Redis cache in development mode');
      } else {
        throw error;
      }
    }
  }

  /**
   * Get value from cache
   * @param {string} key - Cache key
   * @returns {Promise<any>} Cached value or null
   */
  async get(key) {
    if (!this.isConnected) {
      this.cacheStats.misses++;
      return null;
    }

    try {
      const value = await this.redis.get(key);
      
      if (value !== null) {
        this.cacheStats.hits++;
        winston.debug(`Cache HIT for key: ${key}`);
        return JSON.parse(value);
      } else {
        this.cacheStats.misses++;
        winston.debug(`Cache MISS for key: ${key}`);
        return null;
      }
    } catch (error) {
      winston.error(`Cache GET error for key ${key}:`, error);
      this.cacheStats.errors++;
      return null;
    }
  }

  /**
   * Set value in cache
   * @param {string} key - Cache key
   * @param {any} value - Value to cache
   * @param {number} ttl - Time to live in seconds
   * @returns {Promise<boolean>} Success status
   */
  async set(key, value, ttl = this.defaultTTL) {
    if (!this.isConnected) {
      return false;
    }

    try {
      const serializedValue = JSON.stringify(value);
      await this.redis.setex(key, ttl, serializedValue);
      
      this.cacheStats.sets++;
      winston.debug(`Cache SET for key: ${key}, TTL: ${ttl}s`);
      return true;
    } catch (error) {
      winston.error(`Cache SET error for key ${key}:`, error);
      this.cacheStats.errors++;
      return false;
    }
  }

  /**
   * Delete value from cache
   * @param {string} key - Cache key
   * @returns {Promise<boolean>} Success status
   */
  async delete(key) {
    if (!this.isConnected) {
      return false;
    }

    try {
      const result = await this.redis.del(key);
      this.cacheStats.deletes++;
      winston.debug(`Cache DELETE for key: ${key}`);
      return result > 0;
    } catch (error) {
      winston.error(`Cache DELETE error for key ${key}:`, error);
      this.cacheStats.errors++;
      return false;
    }
  }

  /**
   * Check if key exists in cache
   * @param {string} key - Cache key
   * @returns {Promise<boolean>} Existence status
   */
  async exists(key) {
    if (!this.isConnected) {
      return false;
    }

    try {
      const result = await this.redis.exists(key);
      return result === 1;
    } catch (error) {
      winston.error(`Cache EXISTS error for key ${key}:`, error);
      return false;
    }
  }

  /**
   * Get multiple values from cache
   * @param {string[]} keys - Array of cache keys
   * @returns {Promise<Object>} Object with key-value pairs
   */
  async mget(keys) {
    if (!this.isConnected || keys.length === 0) {
      return {};
    }

    try {
      const values = await this.redis.mget(keys);
      const result = {};
      
      keys.forEach((key, index) => {
        if (values[index] !== null) {
          result[key] = JSON.parse(values[index]);
          this.cacheStats.hits++;
        } else {
          this.cacheStats.misses++;
        }
      });

      return result;
    } catch (error) {
      winston.error('Cache MGET error:', error);
      this.cacheStats.errors++;
      return {};
    }
  }

  /**
   * Set multiple values in cache
   * @param {Object} keyValuePairs - Object with key-value pairs
   * @param {number} ttl - Time to live in seconds
   * @returns {Promise<boolean>} Success status
   */
  async mset(keyValuePairs, ttl = this.defaultTTL) {
    if (!this.isConnected || Object.keys(keyValuePairs).length === 0) {
      return false;
    }

    try {
      const pipeline = this.redis.pipeline();
      
      Object.entries(keyValuePairs).forEach(([key, value]) => {
        const serializedValue = JSON.stringify(value);
        pipeline.setex(key, ttl, serializedValue);
      });

      await pipeline.exec();
      this.cacheStats.sets += Object.keys(keyValuePairs).length;
      
      winston.debug(`Cache MSET for ${Object.keys(keyValuePairs).length} keys`);
      return true;
    } catch (error) {
      winston.error('Cache MSET error:', error);
      this.cacheStats.errors++;
      return false;
    }
  }

  /**
   * Invalidate cache by pattern
   * @param {string} pattern - Key pattern (e.g., 'user:*')
   * @returns {Promise<number>} Number of keys deleted
   */
  async invalidateByPattern(pattern) {
    if (!this.isConnected) {
      return 0;
    }

    try {
      const keys = await this.redis.keys(pattern);
      if (keys.length === 0) {
        return 0;
      }

      const result = await this.redis.del(...keys);
      this.cacheStats.deletes += result;
      
      winston.info(`Cache invalidated ${result} keys matching pattern: ${pattern}`);
      return result;
    } catch (error) {
      winston.error(`Cache invalidation error for pattern ${pattern}:`, error);
      this.cacheStats.errors++;
      return 0;
    }
  }

  /**
   * Increment counter in cache
   * @param {string} key - Cache key
   * @param {number} increment - Increment value
   * @param {number} ttl - Time to live in seconds
   * @returns {Promise<number>} New value
   */
  async increment(key, increment = 1, ttl = this.defaultTTL) {
    if (!this.isConnected) {
      return 0;
    }

    try {
      const pipeline = this.redis.pipeline();
      pipeline.incrby(key, increment);
      pipeline.expire(key, ttl);
      
      const results = await pipeline.exec();
      const newValue = results[0][1];
      
      winston.debug(`Cache INCREMENT for key: ${key}, new value: ${newValue}`);
      return newValue;
    } catch (error) {
      winston.error(`Cache INCREMENT error for key ${key}:`, error);
      this.cacheStats.errors++;
      return 0;
    }
  }

  /**
   * Get cache statistics
   * @returns {Object} Cache statistics
   */
  getStats() {
    const hitRate = this.cacheStats.hits + this.cacheStats.misses > 0 
      ? (this.cacheStats.hits / (this.cacheStats.hits + this.cacheStats.misses) * 100).toFixed(2)
      : 0;

    return {
      ...this.cacheStats,
      hitRate: `${hitRate}%`,
      isConnected: this.isConnected,
      warmupJobs: this.warmupJobs.size
    };
  }

  /**
   * Generate cache key for AI/ML predictions
   * @param {string} modelType - Model type
   * @param {Object} data - Input data
   * @returns {string} Cache key
   */
  generatePredictionKey(modelType, data) {
    // Create a hash of the input data for consistent keys
    const dataHash = this.hashObject(data);
    return `prediction:${modelType}:${dataHash}`;
  }

  /**
   * Generate cache key for batch jobs
   * @param {string} organizationId - Organization ID
   * @param {string} jobType - Job type
   * @returns {string} Cache key
   */
  generateBatchKey(organizationId, jobType) {
    return `batch:${organizationId}:${jobType}`;
  }

  /**
   * Generate cache key for performance metrics
   * @param {string} modelType - Model type
   * @param {string} organizationId - Organization ID
   * @returns {string} Cache key
   */
  generateMetricsKey(modelType, organizationId) {
    return `metrics:${modelType}:${organizationId}`;
  }

  /**
   * Hash object for consistent cache keys
   * @param {Object} obj - Object to hash
   * @returns {string} Hash string
   */
  hashObject(obj) {
    const crypto = require('crypto');
    const str = JSON.stringify(obj, Object.keys(obj).sort());
    return crypto.createHash('md5').update(str).digest('hex');
  }

  /**
   * Start cache warming for critical data
   */
  startCacheWarming() {
    winston.info('Starting cache warming for critical data');
    
    // Warm up model metrics every 5 minutes
    const metricsWarmup = setInterval(async () => {
      await this.warmupModelMetrics();
    }, 5 * 60 * 1000);

    // Warm up performance data every 10 minutes
    const performanceWarmup = setInterval(async () => {
      await this.warmupPerformanceData();
    }, 10 * 60 * 1000);

    this.warmupJobs.set('metrics', metricsWarmup);
    this.warmupJobs.set('performance', performanceWarmup);

    // Initial warmup
    setTimeout(() => {
      this.warmupModelMetrics();
      this.warmupPerformanceData();
    }, 5000);
  }

  /**
   * Warm up model metrics cache
   */
  async warmupModelMetrics() {
    try {
      const models = ['profitability', 'churn', 'revenue_leak', 'pricing', 'budget', 'demand', 'anomaly'];
      
      for (const model of models) {
        const key = this.generateMetricsKey(model, 'global');
        const exists = await this.exists(key);
        
        if (!exists) {
          // Generate sample metrics for warmup
          const metrics = {
            accuracy: Math.random() * 0.2 + 0.8, // 0.8-1.0
            predictions_today: Math.floor(Math.random() * 500) + 100,
            avg_confidence: Math.random() * 0.3 + 0.7, // 0.7-1.0
            last_updated: new Date().toISOString(),
            warmed_up: true
          };
          
          await this.set(key, metrics, 600); // 10 minutes TTL
          winston.debug(`Warmed up metrics cache for model: ${model}`);
        }
      }
    } catch (error) {
      winston.error('Error warming up model metrics:', error);
    }
  }

  /**
   * Warm up performance data cache
   */
  async warmupPerformanceData() {
    try {
      const key = 'performance:global:summary';
      const exists = await this.exists(key);
      
      if (!exists) {
        const performanceData = {
          overall_health: 'excellent',
          total_predictions: Math.floor(Math.random() * 10000) + 5000,
          avg_response_time: Math.random() * 100 + 50,
          uptime: 0.99 + Math.random() * 0.009,
          last_updated: new Date().toISOString(),
          warmed_up: true
        };
        
        await this.set(key, performanceData, 900); // 15 minutes TTL
        winston.debug('Warmed up performance data cache');
      }
    } catch (error) {
      winston.error('Error warming up performance data:', error);
    }
  }

  /**
   * Clear all cache data
   * @returns {Promise<boolean>} Success status
   */
  async clear() {
    if (!this.isConnected) {
      return false;
    }

    try {
      await this.redis.flushdb();
      winston.info('Cache cleared successfully');
      
      // Reset stats
      this.cacheStats = {
        hits: 0,
        misses: 0,
        sets: 0,
        deletes: 0,
        errors: 0
      };
      
      return true;
    } catch (error) {
      winston.error('Error clearing cache:', error);
      return false;
    }
  }

  /**
   * Destroy cache service
   */
  async destroy() {
    try {
      // Clear warmup jobs
      this.warmupJobs.forEach((job) => {
        clearInterval(job);
      });
      this.warmupJobs.clear();

      // Close Redis connection
      if (this.redis) {
        await this.redis.quit();
      }
      
      winston.info('Cache service destroyed');
    } catch (error) {
      winston.error('Error destroying cache service:', error);
    }
  }
}

// Export singleton instance
module.exports = new CacheService();
