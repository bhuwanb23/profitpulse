const { DataTypes } = require('sequelize');
const { sequelize } = require('../config/database');
const crypto = require('crypto');

const Service = sequelize.define('Service', {
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
  name: {
    type: DataTypes.STRING,
    allowNull: false,
    validate: {
      len: [2, 255]
    }
  },
  description: {
    type: DataTypes.TEXT,
    allowNull: true
  },
  category: {
    type: DataTypes.STRING,
    allowNull: true
  },
  type: {
    type: DataTypes.ENUM('basic', 'premium', 'enterprise', 'custom'),
    defaultValue: 'basic',
    allowNull: false
  },
  status: {
    type: DataTypes.ENUM('active', 'inactive', 'suspended', 'terminated'),
    defaultValue: 'active',
    allowNull: false
  },
  base_price: {
    type: DataTypes.DECIMAL(10, 2),
    allowNull: true
  },
  monthly_cost: {
    type: DataTypes.DECIMAL(10, 2),
    allowNull: true
  },
  billing_type: {
    type: DataTypes.ENUM('hourly', 'monthly', 'per-user', 'per-device'),
    allowNull: true
  },
  is_active: {
    type: DataTypes.BOOLEAN,
    defaultValue: true,
    allowNull: false
  }
}, {
  tableName: 'services',
  timestamps: true,
  paranoid: true,
  indexes: [
    {
      fields: ['organization_id']
    },
    {
      fields: ['name']
    },
    {
      fields: ['category']
    },
    {
      fields: ['is_active']
    }
  ]
});

module.exports = Service;
