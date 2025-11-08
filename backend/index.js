const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const dotenv = require('dotenv');
const winston = require('winston');

// Load environment variables
dotenv.config();

// Import middleware
const errorHandler = require('./src/middleware/errorHandler');
const { rateLimiter } = require('./src/middleware/rateLimiter');

// Import routes
const authRoutes = require('./src/routes/auth');
const userRoutes = require('./src/routes/users');
const organizationRoutes = require('./src/routes/organizations');
const clientRoutes = require('./src/routes/clients');
const serviceRoutes = require('./src/routes/services');
const ticketRoutes = require('./src/routes/tickets');
const ticketAnalyticsRoutes = require('./src/routes/ticketAnalytics');
const ticketOperationsRoutes = require('./src/routes/ticketOperations');
const invoiceRoutes = require('./src/routes/invoices');
const budgetRoutes = require('./src/routes/budgets');
const analyticsRoutes = require('./src/routes/analytics');
const billingAnalyticsRoutes = require('./src/routes/billingAnalytics');
const aiRoutes = require('./src/routes/ai');
const aiAnalyticsRoutes = require('./src/routes/aiAnalytics');
const predictiveAnalyticsRoutes = require('./src/routes/predictiveAnalytics');
const aiInsightsRoutes = require('./src/routes/aiInsights');
const superOpsRoutes = require('./src/routes/superOps');
const integrationRoutes = require('./src/routes/integrations');
const reportRoutes = require('./src/routes/reports');
const notificationRoutes = require('./src/routes/notifications');
const aiHealthRoutes = require('./src/routes/aiHealth');
const batchRoutes = require('./src/routes/batch');
const advancedFeaturesRoutes = require('./src/routes/advancedFeatures');

// Import database connection
const { connectDatabase } = require('./src/config/database');
const scheduler = require('./src/services/scheduler');

// Import monitoring middleware
const {
  correlationId,
  requestLogger,
  performanceMonitor,
  cacheMiddleware,
  errorMiddleware,
  healthCheck,
  metricsEndpoint
} = require('./src/middleware/monitoring');

// Create Express app
const app = express();
const PORT = process.env.PORT || 3000;

// Configure Winston logger
const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  defaultMeta: { service: 'superhack-backend' },
  transports: [
    new winston.transports.File({ filename: 'logs/error.log', level: 'error' }),
    new winston.transports.File({ filename: 'logs/combined.log' }),
  ],
});

// Add console transport for development
if (process.env.NODE_ENV !== 'production') {
  logger.add(new winston.transports.Console({
    format: winston.format.combine(
      winston.format.colorize(),
      winston.format.simple()
    )
  }));
}

// Monitoring middleware (early in the stack)
app.use(correlationId);
app.use(healthCheck);
app.use(metricsEndpoint);
app.use(requestLogger);
app.use(performanceMonitor);

// Security middleware
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", "data:", "https:"],
    },
  },
  crossOriginEmbedderPolicy: false
}));

// CORS configuration
app.use(cors({
  origin: process.env.CORS_ORIGIN || 'http://localhost:5173',
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization', 'X-Requested-With']
}));

// Rate limiting
app.use(rateLimiter);

// Body parsing middleware
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Logging middleware
app.use(morgan('combined', {
  stream: {
    write: (message) => logger.info(message.trim())
  }
}));

// Import health controller
const { getSystemHealth, getDatabaseHealth } = require('./src/controllers/healthController');

// Health check endpoints
app.get('/health', getSystemHealth);
app.get('/health/database', getDatabaseHealth);

// API routes with caching for read-heavy endpoints
app.use('/api/auth', authRoutes);
app.use('/api/users', userRoutes);
app.use('/api/organizations', organizationRoutes);
app.use('/api/clients', cacheMiddleware({ ttl: 300, exclude: ['/create', '/update', '/delete'] }), clientRoutes);
app.use('/api/services', cacheMiddleware({ ttl: 600 }), serviceRoutes);
app.use('/api/tickets/analytics', cacheMiddleware({ ttl: 180 }), ticketAnalyticsRoutes);
app.use('/api/tickets', ticketOperationsRoutes);
app.use('/api/tickets', ticketRoutes);
app.use('/api/invoices', invoiceRoutes);
app.use('/api/budgets', budgetRoutes);
app.use('/api/analytics', cacheMiddleware({ ttl: 300 }), analyticsRoutes);
app.use('/api/analytics', cacheMiddleware({ ttl: 300 }), billingAnalyticsRoutes);
app.use('/api/ai', cacheMiddleware({ ttl: 120, exclude: ['/predict', '/analyze'] }), aiRoutes);
app.use('/api/ai/analytics', cacheMiddleware({ ttl: 180 }), aiAnalyticsRoutes);
app.use('/api/ai/predictions', cacheMiddleware({ ttl: 60 }), predictiveAnalyticsRoutes);
app.use('/api/ai/insights', cacheMiddleware({ ttl: 300 }), aiInsightsRoutes);
app.use('/api/integrations/superops', superOpsRoutes);
app.use('/api/integrations', integrationRoutes);
app.use('/api/reports', cacheMiddleware({ ttl: 600 }), reportRoutes);
app.use('/api/notifications', notificationRoutes);
app.use('/api/ai', aiHealthRoutes);
app.use('/api/batch', batchRoutes);
app.use('/api/advanced', cacheMiddleware({ ttl: 180 }), advancedFeaturesRoutes);

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    success: false,
    message: 'API endpoint not found',
    path: req.originalUrl,
    method: req.method
  });
});

// Enhanced error handling middleware
app.use(errorMiddleware);

// Graceful shutdown
process.on('SIGTERM', () => {
  logger.info('SIGTERM received, shutting down gracefully');
  process.exit(0);
});

process.on('SIGINT', () => {
  logger.info('SIGINT received, shutting down gracefully');
  process.exit(0);
});

// Unhandled promise rejection handler
process.on('unhandledRejection', (err) => {
  logger.error('Unhandled Promise Rejection:', err);
  process.exit(1);
});

// Uncaught exception handler
process.on('uncaughtException', (err) => {
  logger.error('Uncaught Exception:', err);
  process.exit(1);
});

// Start server
const startServer = async () => {
  try {
    // Connect to database
    await connectDatabase();
    logger.info('Database connected successfully');

    // Initialize scheduler service
    await scheduler.initialize();
    logger.info('Scheduler service initialized');

    // Start server
    app.listen(PORT, () => {
      logger.info(`🚀 SuperHack Backend Server running on port ${PORT}`);
      logger.info(`📊 Environment: ${process.env.NODE_ENV || 'development'}`);
      logger.info(`🔗 Health check: http://localhost:${PORT}/health`);
      logger.info(`📚 API Documentation: http://localhost:${PORT}/api-docs`);
    });
  } catch (error) {
    logger.error('Failed to start server:', error);
    process.exit(1);
  }
};

// Start the server
startServer();

module.exports = app;
