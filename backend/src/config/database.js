const { Sequelize } = require('sequelize');
const winston = require('winston');

// Configure logger for database
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.Console({
      format: winston.format.combine(
        winston.format.colorize(),
        winston.format.simple()
      )
    })
  ]
});

// Database configuration
const config = {
  development: {
    dialect: 'sqlite',
    storage: process.env.DB_FILE || './database/superhack.db',
    logging: (msg) => logger.debug(msg),
    define: {
      timestamps: true,
      underscored: true,
      paranoid: true // Soft deletes
    }
  },
  production: {
    dialect: 'postgres',
    host: process.env.DB_HOST || 'localhost',
    port: process.env.DB_PORT || 5432,
    database: process.env.DB_NAME || 'superhack_db',
    username: process.env.DB_USER || 'superhack_user',
    password: process.env.DB_PASSWORD || 'superhack_password',
    logging: false,
    define: {
      timestamps: true,
      underscored: true,
      paranoid: true
    },
    pool: {
      max: 5,
      min: 0,
      acquire: 30000,
      idle: 10000
    }
  }
};

// Create Sequelize instance
const sequelize = new Sequelize(
  process.env.NODE_ENV === 'production' 
    ? config.production 
    : config.development
);

/**
 * Connect to database
 */
const connectDatabase = async () => {
  try {
    await sequelize.authenticate();
    logger.info('✅ Database connection established successfully');
    
    // Sync database in development
    if (process.env.NODE_ENV !== 'production') {
      await sequelize.sync({ alter: true });
      logger.info('✅ Database synchronized');
    }
    
    return sequelize;
  } catch (error) {
    logger.error('❌ Unable to connect to database:', error);
    throw error;
  }
};

/**
 * Close database connection
 */
const closeDatabase = async () => {
  try {
    await sequelize.close();
    logger.info('✅ Database connection closed');
  } catch (error) {
    logger.error('❌ Error closing database connection:', error);
    throw error;
  }
};

/**
 * Health check for database
 */
const checkDatabaseHealth = async () => {
  try {
    await sequelize.authenticate();
    return { status: 'healthy', timestamp: new Date().toISOString() };
  } catch (error) {
    return { status: 'unhealthy', error: error.message, timestamp: new Date().toISOString() };
  }
};

module.exports = {
  sequelize,
  connectDatabase,
  closeDatabase,
  checkDatabaseHealth
};
