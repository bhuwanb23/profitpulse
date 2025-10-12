const { DataTypes } = require('sequelize');
const { sequelize } = require('../config/database');
const crypto = require('crypto');

const Organization = sequelize.define('Organization', {
  id: {
    type: DataTypes.TEXT,
    defaultValue: () => crypto.randomUUID(),
    primaryKey: true
  },
  name: {
    type: DataTypes.STRING,
    allowNull: false,
    validate: {
      len: [2, 255]
    }
  },
  domain: {
    type: DataTypes.STRING,
    allowNull: true,
    validate: {
      isUrl: true
    }
  },
  subscription_plan: {
    type: DataTypes.ENUM('basic', 'pro', 'enterprise'),
    defaultValue: 'basic',
    allowNull: false
  },
  is_active: {
    type: DataTypes.BOOLEAN,
    defaultValue: true,
    allowNull: false
  }
}, {
  tableName: 'organizations',
  timestamps: true,
  paranoid: true,
  indexes: [
    {
      fields: ['name']
    },
    {
      fields: ['subscription_plan']
    },
    {
      fields: ['is_active']
    }
  ]
});

module.exports = Organization;
