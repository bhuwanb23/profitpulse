const { DataTypes } = require('sequelize');
const { sequelize } = require('../config/database');
const crypto = require('crypto');

const NotificationPreference = sequelize.define('NotificationPreference', {
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
  user_id: {
    type: DataTypes.TEXT,
    allowNull: true, // Organization-wide preferences can be null
    references: {
      model: 'users',
      key: 'id'
    }
  },
  category: {
    type: DataTypes.ENUM('system', 'ticket', 'invoice', 'budget', 'report', 'ai', 'integration'),
    allowNull: false
  },
  type: {
    type: DataTypes.ENUM('info', 'warning', 'error', 'success', 'alert'),
    allowNull: false
  },
  enabled: {
    type: DataTypes.BOOLEAN,
    defaultValue: true,
    allowNull: false
  },
  email_enabled: {
    type: DataTypes.BOOLEAN,
    defaultValue: true,
    allowNull: false
  },
  push_enabled: {
    type: DataTypes.BOOLEAN,
    defaultValue: true,
    allowNull: false
  },
  sms_enabled: {
    type: DataTypes.BOOLEAN,
    defaultValue: false,
    allowNull: false
  },
  webhook_enabled: {
    type: DataTypes.BOOLEAN,
    defaultValue: false,
    allowNull: false
  },
  webhook_url: {
    type: DataTypes.STRING,
    allowNull: true
  },
  frequency: {
    type: DataTypes.ENUM('immediate', 'hourly', 'daily', 'weekly'),
    defaultValue: 'immediate',
    allowNull: false
  },
  quiet_hours_start: {
    type: DataTypes.TIME,
    allowNull: true
  },
  quiet_hours_end: {
    type: DataTypes.TIME,
    allowNull: true
  },
  timezone: {
    type: DataTypes.STRING,
    defaultValue: 'UTC',
    allowNull: false
  }
}, {
  tableName: 'notification_preferences',
  timestamps: true,
  paranoid: true,
  indexes: [
    {
      fields: ['organization_id']
    },
    {
      fields: ['user_id']
    },
    {
      fields: ['category']
    },
    {
      fields: ['type']
    },
    {
      fields: ['enabled']
    }
  ]
});

module.exports = NotificationPreference;
