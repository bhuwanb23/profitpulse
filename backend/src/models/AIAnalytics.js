const { DataTypes } = require('sequelize');
const { sequelize } = require('../config/database');
const crypto = require('crypto');

const AIAnalytics = sequelize.define('AIAnalytics', {
  id: {
    type: DataTypes.TEXT,
    defaultValue: () => crypto.randomUUID(),
    primaryKey: true
  },
  organization_id: {
    type: DataTypes.TEXT,
    allowNull: false,
    references: {
      model: 'organizations',
      key: 'id'
    }
  },
  analysis_type: {
    type: DataTypes.ENUM('profitability', 'revenue_leak', 'budget_optimization', 'churn_prediction', 'demand_forecast'),
    allowNull: false
  },
  client_id: {
    type: DataTypes.TEXT,
    allowNull: true,
    references: {
      model: 'clients',
      key: 'id'
    }
  },
  data: {
    type: DataTypes.TEXT, // JSON string for SQLite compatibility
    allowNull: false
  },
  confidence_score: {
    type: DataTypes.DECIMAL(3, 2),
    allowNull: true,
    validate: {
      min: 0,
      max: 1
    }
  },
  status: {
    type: DataTypes.ENUM('pending', 'completed', 'failed'),
    defaultValue: 'pending',
    allowNull: false
  }
}, {
  tableName: 'ai_analytics',
  timestamps: true,
  paranoid: true,
  indexes: [
    {
      fields: ['organization_id']
    },
    {
      fields: ['analysis_type']
    },
    {
      fields: ['client_id']
    },
    {
      fields: ['status']
    }
  ]
});

module.exports = AIAnalytics;
