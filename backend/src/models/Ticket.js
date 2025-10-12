const { DataTypes } = require('sequelize');
const { sequelize } = require('../config/database');
const crypto = require('crypto');

const Ticket = sequelize.define('Ticket', {
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
  ticket_number: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: true
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
    allowNull: true
  },
  priority: {
    type: DataTypes.ENUM('low', 'medium', 'high', 'critical'),
    defaultValue: 'medium',
    allowNull: false
  },
  status: {
    type: DataTypes.ENUM('open', 'in_progress', 'resolved', 'closed'),
    defaultValue: 'open',
    allowNull: false
  },
  category: {
    type: DataTypes.STRING,
    allowNull: true
  },
  assigned_to: {
    type: DataTypes.TEXT,
    allowNull: true,
    references: {
      model: 'users',
      key: 'id'
    }
  },
  time_spent: {
    type: DataTypes.DECIMAL(8, 2),
    defaultValue: 0,
    allowNull: false
  },
  billable_hours: {
    type: DataTypes.DECIMAL(8, 2),
    defaultValue: 0,
    allowNull: false
  },
  hourly_rate: {
    type: DataTypes.DECIMAL(8, 2),
    allowNull: true
  },
  resolved_at: {
    type: DataTypes.DATE,
    allowNull: true
  }
}, {
  tableName: 'tickets',
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
      fields: ['ticket_number']
    },
    {
      fields: ['status']
    },
    {
      fields: ['priority']
    },
    {
      fields: ['assigned_to']
    }
  ]
});

module.exports = Ticket;
