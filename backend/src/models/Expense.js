const { DataTypes } = require('sequelize');
const { sequelize } = require('../config/database');
const crypto = require('crypto');

const Expense = sequelize.define('Expense', {
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
  budget_id: {
    type: DataTypes.TEXT,
    allowNull: true,
    references: {
      model: 'budgets',
      key: 'id'
    }
  },
  budget_category_id: {
    type: DataTypes.TEXT,
    allowNull: true,
    references: {
      model: 'budget_categories',
      key: 'id'
    }
  },
  description: {
    type: DataTypes.STRING,
    allowNull: false,
    validate: {
      len: [5, 255]
    }
  },
  amount: {
    type: DataTypes.DECIMAL(10, 2),
    allowNull: false
  },
  expense_date: {
    type: DataTypes.DATEONLY,
    allowNull: false
  },
  category: {
    type: DataTypes.STRING,
    allowNull: true
  },
  vendor: {
    type: DataTypes.STRING,
    allowNull: true
  },
  is_billable: {
    type: DataTypes.BOOLEAN,
    defaultValue: false,
    allowNull: false
  },
  client_id: {
    type: DataTypes.TEXT,
    allowNull: true,
    references: {
      model: 'clients',
      key: 'id'
    }
  }
}, {
  tableName: 'expenses',
  timestamps: true,
  paranoid: true,
  indexes: [
    {
      fields: ['organization_id']
    },
    {
      fields: ['budget_id']
    },
    {
      fields: ['expense_date']
    },
    {
      fields: ['category']
    },
    {
      fields: ['is_billable']
    }
  ]
});

module.exports = Expense;
