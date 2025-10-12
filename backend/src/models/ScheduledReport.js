const { DataTypes } = require('sequelize');
const { sequelize } = require('../config/database');
const crypto = require('crypto');

const ScheduledReport = sequelize.define('ScheduledReport', {
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
  report_id: {
    type: DataTypes.TEXT,
    allowNull: true,
    references: {
      model: 'reports',
      key: 'id'
    }
  },
  template_id: {
    type: DataTypes.TEXT,
    allowNull: true,
    references: {
      model: 'report_templates',
      key: 'id'
    }
  },
  title: {
    type: DataTypes.STRING,
    allowNull: false,
    validate: {
      len: [1, 255]
    }
  },
  description: {
    type: DataTypes.TEXT,
    allowNull: true
  },
  schedule_type: {
    type: DataTypes.ENUM('once', 'daily', 'weekly', 'monthly'),
    allowNull: false
  },
  schedule_config: {
    type: DataTypes.TEXT, // JSON string for SQLite compatibility
    allowNull: true
  },
  next_run: {
    type: DataTypes.DATE,
    allowNull: false
  },
  last_run: {
    type: DataTypes.DATE,
    allowNull: true
  },
  status: {
    type: DataTypes.ENUM('active', 'paused', 'completed', 'failed'),
    defaultValue: 'active',
    allowNull: false
  },
  parameters: {
    type: DataTypes.TEXT, // JSON string for SQLite compatibility
    allowNull: true
  },
  filters: {
    type: DataTypes.TEXT, // JSON string for SQLite compatibility
    allowNull: true
  },
  format: {
    type: DataTypes.ENUM('json', 'pdf', 'excel', 'csv'),
    defaultValue: 'json',
    allowNull: false
  },
  email_recipients: {
    type: DataTypes.TEXT, // JSON string for SQLite compatibility
    allowNull: true
  },
  email_subject: {
    type: DataTypes.STRING,
    allowNull: true
  },
  email_body: {
    type: DataTypes.TEXT,
    allowNull: true
  },
  run_count: {
    type: DataTypes.INTEGER,
    defaultValue: 0,
    allowNull: false
  },
  success_count: {
    type: DataTypes.INTEGER,
    defaultValue: 0,
    allowNull: false
  },
  failure_count: {
    type: DataTypes.INTEGER,
    defaultValue: 0,
    allowNull: false
  },
  last_error: {
    type: DataTypes.TEXT,
    allowNull: true
  },
  created_by: {
    type: DataTypes.TEXT,
    allowNull: true,
    references: {
      model: 'users',
      key: 'id'
    }
  }
}, {
  tableName: 'scheduled_reports',
  timestamps: true,
  paranoid: true,
  indexes: [
    {
      fields: ['organization_id']
    },
    {
      fields: ['report_id']
    },
    {
      fields: ['template_id']
    },
    {
      fields: ['schedule_type']
    },
    {
      fields: ['next_run']
    },
    {
      fields: ['status']
    },
    {
      fields: ['created_by']
    }
  ]
});

module.exports = ScheduledReport;
