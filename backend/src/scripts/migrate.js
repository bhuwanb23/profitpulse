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

async function runMigrations() {
  try {
    console.log('🔄 Starting database migrations...');
    
    // Sync all models with database
    await sequelize.sync({ force: false, alter: true });
    console.log('✅ Database tables synchronized');
    
    console.log('🎉 Database migrations completed successfully!');
    process.exit(0);
  } catch (error) {
    console.error('❌ Migration failed:', error);
    process.exit(1);
  }
}

runMigrations();
