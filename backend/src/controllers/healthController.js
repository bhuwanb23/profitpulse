const { sequelize } = require('../config/database');
const { 
  User, 
  Organization, 
  Client, 
  Service, 
  Ticket, 
  Invoice, 
  Budget, 
  Expense, 
  AIAnalytics, 
  AIRecommendation 
} = require('../models');
const aiClient = require('../services/ai-ml');

/**
 * Get database health status
 */
const getDatabaseHealth = async (req, res) => {
  try {
    // Test database connection
    await sequelize.authenticate();
    
    // Get table counts
    const counts = {
      users: await User.count(),
      organizations: await Organization.count(),
      clients: await Client.count(),
      services: await Service.count(),
      tickets: await Ticket.count(),
      invoices: await Invoice.count(),
      budgets: await Budget.count(),
      expenses: await Expense.count(),
      aiAnalytics: await AIAnalytics.count(),
      aiRecommendations: await AIRecommendation.count()
    };
    
    // Get database info
    const dbInfo = await sequelize.query('SELECT sqlite_version() as version', {
      type: sequelize.QueryTypes.SELECT
    });
    
    res.json({
      success: true,
      data: {
        status: 'healthy',
        database: {
          connected: true,
          version: dbInfo[0]?.version || 'unknown',
          dialect: sequelize.getDialect()
        },
        tables: counts,
        timestamp: new Date().toISOString()
      }
    });
    
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Database health check failed',
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
};

/**
 * Get system health status
 */
const getSystemHealth = async (req, res) => {
  try {
    const health = {
      status: 'OK',
      timestamp: new Date().toISOString(),
      uptime: process.uptime(),
      environment: process.env.NODE_ENV || 'development',
      version: process.env.npm_package_version || '1.0.0',
      memory: {
        used: Math.round(process.memoryUsage().heapUsed / 1024 / 1024),
        total: Math.round(process.memoryUsage().heapTotal / 1024 / 1024),
        external: Math.round(process.memoryUsage().external / 1024 / 1024)
      },
      database: {
        connected: false,
        status: 'unknown'
      },
      aiml: {
        connected: false,
        status: 'unknown',
        lastCheck: null,
        responseTime: null
      }
    };
    
    // Test database connection
    try {
      await sequelize.authenticate();
      health.database.connected = true;
      health.database.status = 'healthy';
    } catch (dbError) {
      health.database.connected = false;
      health.database.status = 'unhealthy';
      health.database.error = dbError.message;
    }
    
    // Test AI/ML service connection
    try {
      const aiStartTime = Date.now();
      await aiClient.healthCheck();
      
      health.aiml.connected = true;
      health.aiml.status = 'healthy';
      health.aiml.lastCheck = new Date().toISOString();
      health.aiml.responseTime = Date.now() - aiStartTime;
      
      // Get additional AI/ML metrics
      const aiHealthStatus = await aiClient.getHealthStatus();
      health.aiml.circuitBreaker = aiHealthStatus.circuitBreaker.state;
      health.aiml.monitoring = aiHealthStatus.healthMonitor.isMonitoring;
      health.aiml.successRate = aiHealthStatus.metrics.requests.successRate;
      
    } catch (aiError) {
      health.aiml.connected = false;
      health.aiml.status = 'unhealthy';
      health.aiml.error = aiError.message;
      health.aiml.lastCheck = new Date().toISOString();
    }
    
    // Determine overall status
    if (!health.database.connected || !health.aiml.connected) {
      health.status = 'DEGRADED';
    }
    
    res.json(health);
    
  } catch (error) {
    res.status(500).json({
      status: 'ERROR',
      message: 'System health check failed',
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
};

module.exports = {
  getDatabaseHealth,
  getSystemHealth
};
