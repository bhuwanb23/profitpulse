const { DataTypes } = require('sequelize');
const { sequelize } = require('../config/database');
const crypto = require('crypto');

const ReportTemplate = sequelize.define('ReportTemplate', {
  id: {
    type: DataTypes.TEXT,
    defaultValue: () => crypto.randomUUID(),
    primaryKey: true
  },
  organization_id: {
    type: DataTypes.TEXT,
    allowNull: true, // Global templates can be null
    references: {
      model: 'organizations',
      key: 'id'
    }
  },
  name: {
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
  category: {
    type: DataTypes.ENUM('financial', 'operational', 'analytical', 'custom'),
    allowNull: false
  },
  report_type: {
    type: DataTypes.ENUM('financial', 'operational', 'analytical', 'custom'),
    allowNull: false
  },
  template_data: {
    type: DataTypes.TEXT, // JSON string for SQLite compatibility
    allowNull: false
  },
  parameters: {
    type: DataTypes.TEXT, // JSON string for SQLite compatibility
    allowNull: true
  },
  default_filters: {
    type: DataTypes.TEXT, // JSON string for SQLite compatibility
    allowNull: true
  },
  is_global: {
    type: DataTypes.BOOLEAN,
    defaultValue: false,
    allowNull: false
  },
  is_active: {
    type: DataTypes.BOOLEAN,
    defaultValue: true,
    allowNull: false
  },
  created_by: {
    type: DataTypes.TEXT,
    allowNull: true,
    references: {
      model: 'users',
      key: 'id'
    }
  },
  usage_count: {
    type: DataTypes.INTEGER,
    defaultValue: 0,
    allowNull: false
  },
  last_used: {
    type: DataTypes.DATE,
    allowNull: true
  }
}, {
  tableName: 'report_templates',
  timestamps: true,
  paranoid: true,
  indexes: [
    {
      fields: ['organization_id']
    },
    {
      fields: ['category']
    },
    {
      fields: ['report_type']
    },
    {
      fields: ['is_global']
    },
    {
      fields: ['is_active']
    },
    {
      fields: ['created_by']
    }
  ]
});

module.exports = ReportTemplate;
