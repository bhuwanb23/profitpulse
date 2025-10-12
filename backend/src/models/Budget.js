const { DataTypes } = require('sequelize');
const { sequelize } = require('../config/database');
const crypto = require('crypto');

const Budget = sequelize.define('Budget', {
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
  budget_type: {
    type: DataTypes.ENUM('monthly', 'quarterly', 'annual', 'project'),
    allowNull: true
  },
  total_amount: {
    type: DataTypes.DECIMAL(12, 2),
    allowNull: false
  },
  spent_amount: {
    type: DataTypes.DECIMAL(12, 2),
    defaultValue: 0,
    allowNull: false
  },
  start_date: {
    type: DataTypes.DATEONLY,
    allowNull: false
  },
  end_date: {
    type: DataTypes.DATEONLY,
    allowNull: false
  },
  is_active: {
    type: DataTypes.BOOLEAN,
    defaultValue: true,
    allowNull: false
  }
}, {
  tableName: 'budgets',
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
      fields: ['budget_type']
    },
    {
      fields: ['is_active']
    }
  ]
});

module.exports = Budget;
