const { sequelize } = require('../src/config/database');
const { User } = require('../src/models');

async function initializeDatabase() {
  try {
    console.log('🔄 Connecting to database...');
    await sequelize.authenticate();
    console.log('✅ Database connection established');

    console.log('🔄 Creating tables...');
    await sequelize.sync({ force: true });
    console.log('✅ Database tables created');

    console.log('🔄 Creating test user...');
    const testUser = await User.create({
      email: 'admin@superhack.com',
      password_hash: '$2a$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J.8QzKz2a', // 'admin123'
      first_name: 'Admin',
      last_name: 'User',
      role: 'admin',
      is_active: true
    });
    console.log('✅ Test user created:', testUser.email);

    console.log('🎉 Database initialization complete!');
    process.exit(0);
  } catch (error) {
    console.error('❌ Database initialization failed:', error);
    process.exit(1);
  }
}

initializeDatabase();
