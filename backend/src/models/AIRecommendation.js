const { DataTypes } = require('sequelize');
const { sequelize } = require('../config/database');
const crypto = require('crypto');

const AIRecommendation = sequelize.define('AIRecommendation', {
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
  client_id: {
    type: DataTypes.TEXT,
    allowNull: true,
    references: {
      model: 'clients',
      key: 'id'
    }
  },
  recommendation_type: {
    type: DataTypes.ENUM('pricing_adjustment', 'service_optimization', 'budget_reallocation', 'contract_renewal', 'upsell_opportunity'),
    allowNull: false
  },
  title: {
    type: DataTypes.STRING,
    allowNull: false,
    validate: {
      len: [5, 255]
    }
  },
  description: {
    type: DataTypes.TEXT,
    allowNull: false
  },
  impact_score: {
    type: DataTypes.DECIMAL(3, 2),
    allowNull: true,
    validate: {
      min: 0,
      max: 1
    }
  },
  implementation_effort: {
    type: DataTypes.ENUM('low', 'medium', 'high'),
    allowNull: true
  },
  estimated_savings: {
    type: DataTypes.DECIMAL(12, 2),
    allowNull: true
  },
  estimated_revenue_increase: {
    type: DataTypes.DECIMAL(12, 2),
    allowNull: true
  },
  status: {
    type: DataTypes.ENUM('pending', 'accepted', 'rejected', 'implemented'),
    defaultValue: 'pending',
    allowNull: false
  }
}, {
  tableName: 'ai_recommendations',
  timestamps: true,
  paranoid: true,
  indexes: [
    {
      fields: ['organization_id']
    },
    {
      fields: ['client_id']
    },
    {
      fields: ['recommendation_type']
    },
    {
      fields: ['status']
    }
  ]
});

module.exports = AIRecommendation;
