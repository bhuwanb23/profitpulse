const { DataTypes } = require('sequelize');
const { sequelize } = require('../config/database');
const crypto = require('crypto');

const Report = sequelize.define('Report', {
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
  report_type: {
    type: DataTypes.ENUM('financial', 'operational', 'analytical', 'custom'),
    allowNull: false
  },
  status: {
    type: DataTypes.ENUM('pending', 'generating', 'completed', 'failed'),
    defaultValue: 'pending',
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
  data: {
    type: DataTypes.TEXT, // JSON string for SQLite compatibility
    allowNull: true
  },
  format: {
    type: DataTypes.ENUM('json', 'pdf', 'excel', 'csv'),
    defaultValue: 'json',
    allowNull: false
  },
  file_path: {
    type: DataTypes.STRING,
    allowNull: true
  },
  file_size: {
    type: DataTypes.INTEGER,
    allowNull: true
  },
  generated_at: {
    type: DataTypes.DATE,
    allowNull: true
  },
  expires_at: {
    type: DataTypes.DATE,
    allowNull: true
  },
  created_by: {
    type: DataTypes.TEXT,
    allowNull: true,
    references: {
      model: 'users',
      key: 'id'
    }
  },
  scheduled_at: {
    type: DataTypes.DATE,
    allowNull: true
  },
  schedule_frequency: {
    type: DataTypes.ENUM('once', 'daily', 'weekly', 'monthly'),
    allowNull: true
  },
  schedule_enabled: {
    type: DataTypes.BOOLEAN,
    defaultValue: false,
    allowNull: false
  },
  last_generated: {
    type: DataTypes.DATE,
    allowNull: true
  },
  next_generation: {
    type: DataTypes.DATE,
    allowNull: true
  }
}, {
  tableName: 'reports',
  timestamps: true,
  paranoid: true,
  indexes: [
    {
      fields: ['organization_id']
    },
    {
      fields: ['template_id']
    },
    {
      fields: ['report_type']
    },
    {
      fields: ['status']
    },
    {
      fields: ['created_by']
    },
    {
      fields: ['scheduled_at']
    },
    {
      fields: ['schedule_enabled']
    }
  ]
});

module.exports = Report;
