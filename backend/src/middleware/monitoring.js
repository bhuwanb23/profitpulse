const winston = require('winston');
const { v4: uuidv4 } = require('uuid');

/**
 * Middleware to add correlation ID to requests
 */
const correlationId = (req, res, next) => {
  // Get correlation ID from header or generate new one
  req.correlationId = req.get('X-Correlation-ID') || 
                     req.get('X-Request-ID') || 
                     uuidv4();
  
  // Add correlation ID to response headers
  res.set('X-Correlation-ID', req.correlationId);
  
  // Add to request context for logging
  req.context = {
    correlationId: req.correlationId,
    startTime: Date.now(),
    userAgent: req.get('User-Agent'),
    ip: req.ip || req.connection.remoteAddress,
    userId: null, // Will be set by auth middleware
    organizationId: null
  };

  next();
};

/**
 * Middleware for comprehensive request/response logging
 */
const requestLogger = (req, res, next) => {
  const startTime = Date.now();

  // Log incoming request
  winston.info('Incoming request', {
    correlationId: req.correlationId,
    method: req.method,
    url: req.originalUrl,
    userAgent: req.get('User-Agent'),
    ip: req.ip,
    headers: sanitizeHeaders(req.headers),
    body: req.method !== 'GET' ? sanitizeBody(req.body) : undefined,
    query: Object.keys(req.query).length > 0 ? req.query : undefined
  });

  // Capture original res.end to log response
  const originalEnd = res.end;
  
  res.end = function(chunk, encoding) {
    const duration = Date.now() - startTime;

    // Log response
    winston.info('Outgoing response', {
      correlationId: req.correlationId,
      method: req.method,
      url: req.originalUrl,
      statusCode: res.statusCode,
      duration: `${duration}ms`,
      contentLength: res.get('Content-Length'),
      userId: req.user?.id,
      organizationId: req.body?.organization_id || req.query?.organization_id
    });

    // Call original end
    originalEnd.call(this, chunk, encoding);
  };

  next();
};

/**
 * Middleware for performance monitoring
 */
const performanceMonitor = (req, res, next) => {
  const startTime = process.hrtime();
  
  // Monitor memory usage
  const memoryBefore = process.memoryUsage();
  
  res.on('finish', () => {
    const [seconds, nanoseconds] = process.hrtime(startTime);
    const duration = seconds + nanoseconds / 1e9;
    
    const memoryAfter = process.memoryUsage();
    const memoryDelta = {
      rss: memoryAfter.rss - memoryBefore.rss,
      heapUsed: memoryAfter.heapUsed - memoryBefore.heapUsed,
      heapTotal: memoryAfter.heapTotal - memoryBefore.heapTotal,
      external: memoryAfter.external - memoryBefore.external
    };

    // Log performance metrics for slow requests
    if (duration > 1) { // Log requests taking more than 1 second
      winston.warn('Slow request detected', {
        correlationId: req.correlationId,
        method: req.method,
        url: req.originalUrl,
        duration: `${duration.toFixed(3)}s`,
        statusCode: res.statusCode,
        memoryDelta,
        userAgent: req.get('User-Agent')
      });
    }
  });

  next();
};

/**
 * Middleware for caching responses (simplified)
 */
const cacheMiddleware = (options = {}) => {
  const {
    ttl = 300, // 5 minutes default
    exclude = []
  } = options;

  return (req, res, next) => {
    // Skip caching for excluded paths
    if (exclude.some(path => req.originalUrl.includes(path))) {
      return next();
    }

    // Set cache headers to indicate no caching for now
    res.set('X-Cache', 'DISABLED');
    
    next();
  };
};

/**
 * Error handling middleware with detailed logging
 */
const errorMiddleware = (error, req, res, next) => {
  // Log the error
  winston.error('Request error', {
    correlationId: req.correlationId,
    error: error.message,
    stack: error.stack,
    url: req.originalUrl,
    method: req.method,
    ip: req.ip
  });

  // Determine error response
  let statusCode = 500;
  let message = 'Internal server error';

  if (error.status || error.statusCode) {
    statusCode = error.status || error.statusCode;
  }

  if (error.message && statusCode < 500) {
    message = error.message;
  }

  // Send error response
  res.status(statusCode).json({
    success: false,
    message,
    correlationId: req.correlationId,
    timestamp: new Date().toISOString(),
    ...(process.env.NODE_ENV === 'development' && { 
      stack: error.stack,
      details: error.details 
    })
  });
};

/**
 * Health check middleware
 */
const healthCheck = async (req, res, next) => {
  if (req.path === '/health' || req.path === '/health/detailed') {
    try {
      const isDetailed = req.path === '/health/detailed';
      
      // Basic health info
      const health = {
        status: 'healthy',
        timestamp: new Date().toISOString(),
        uptime: process.uptime(),
        version: process.env.npm_package_version || '1.0.0',
        correlationId: req.correlationId
      };

      if (isDetailed) {
        // Add detailed health information
        health.details = {
          memory: process.memoryUsage(),
          environment: {
            nodeVersion: process.version,
            platform: process.platform,
            arch: process.arch
          }
        };
      }

      return res.json(health);
    } catch (error) {
      winston.error('Health check error', {
        correlationId: req.correlationId,
        error: error.message
      });
      
      return res.status(503).json({
        status: 'unhealthy',
        message: 'Health check failed',
        correlationId: req.correlationId,
        timestamp: new Date().toISOString()
      });
    }
  }

  next();
};

/**
 * Metrics endpoint middleware
 */
const metricsEndpoint = async (req, res, next) => {
  if (req.path === '/metrics') {
    try {
      const metrics = {
        timestamp: new Date().toISOString(),
        uptime: process.uptime(),
        memory: process.memoryUsage(),
        performance: {
          totalRequests: 0,
          avgDuration: 0,
          errorCount: 0,
          errorRate: 0
        }
      };
      
      return res.json(metrics);
    } catch (error) {
      winston.error('Metrics endpoint error', {
        correlationId: req.correlationId,
        error: error.message
      });
      
      return res.status(500).json({
        success: false,
        message: 'Failed to retrieve metrics',
        correlationId: req.correlationId
      });
    }
  }

  next();
};

/**
 * Sanitize headers for logging (remove sensitive information)
 */
function sanitizeHeaders(headers) {
  const sanitized = { ...headers };
  const sensitiveHeaders = [
    'authorization', 'cookie', 'x-api-key', 'x-auth-token',
    'x-access-token', 'x-refresh-token'
  ];
  
  sensitiveHeaders.forEach(header => {
    if (sanitized[header]) {
      sanitized[header] = '[REDACTED]';
    }
  });

  return sanitized;
}

/**
 * Sanitize request body for logging (remove sensitive information)
 */
function sanitizeBody(body) {
  if (!body || typeof body !== 'object') {
    return body;
  }

  const sanitized = { ...body };
  const sensitiveFields = [
    'password', 'token', 'secret', 'key', 'auth', 'credential',
    'ssn', 'social_security', 'credit_card', 'cvv'
  ];
  
  sensitiveFields.forEach(field => {
    if (sanitized[field]) {
      sanitized[field] = '[REDACTED]';
    }
  });

  return sanitized;
}

module.exports = {
  correlationId,
  requestLogger,
  performanceMonitor,
  cacheMiddleware,
  errorMiddleware,
  healthCheck,
  metricsEndpoint,
  sanitizeHeaders,
  sanitizeBody
};
