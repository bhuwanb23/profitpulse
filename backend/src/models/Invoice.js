const { DataTypes } = require('sequelize');
const { sequelize } = require('../config/database');
const crypto = require('crypto');

const Invoice = sequelize.define('Invoice', {
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
    allowNull: false,
    references: {
      model: 'clients',
      key: 'id'
    }
  },
  invoice_number: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: true
  },
  invoice_date: {
    type: DataTypes.DATEONLY,
    allowNull: false
  },
  due_date: {
    type: DataTypes.DATEONLY,
    allowNull: true
  },
  subtotal: {
    type: DataTypes.DECIMAL(12, 2),
    allowNull: false
  },
  tax_amount: {
    type: DataTypes.DECIMAL(12, 2),
    defaultValue: 0,
    allowNull: false
  },
  total_amount: {
    type: DataTypes.DECIMAL(12, 2),
    allowNull: false
  },
  status: {
    type: DataTypes.ENUM('draft', 'sent', 'paid', 'overdue'),
    defaultValue: 'draft',
    allowNull: false
  },
  payment_date: {
    type: DataTypes.DATEONLY,
    allowNull: true
  }
}, {
  tableName: 'invoices',
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
      fields: ['invoice_number']
    },
    {
      fields: ['status']
    },
    {
      fields: ['invoice_date']
    }
  ]
});

module.exports = Invoice;
