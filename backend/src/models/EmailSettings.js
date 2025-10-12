const { DataTypes } = require('sequelize');
const { sequelize } = require('../config/database');
const crypto = require('crypto');

const EmailSettings = sequelize.define('EmailSettings', {
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
  smtp_host: {
    type: DataTypes.STRING,
    allowNull: true
  },
  smtp_port: {
    type: DataTypes.INTEGER,
    allowNull: true
  },
  smtp_secure: {
    type: DataTypes.BOOLEAN,
    defaultValue: true,
    allowNull: false
  },
  smtp_username: {
    type: DataTypes.STRING,
    allowNull: true
  },
  smtp_password: {
    type: DataTypes.STRING,
    allowNull: true
  },
  from_email: {
    type: DataTypes.STRING,
    allowNull: false,
    validate: {
      isEmail: true
    }
  },
  from_name: {
    type: DataTypes.STRING,
    allowNull: false
  },
  reply_to_email: {
    type: DataTypes.STRING,
    allowNull: true,
    validate: {
      isEmail: true
    }
  },
  reply_to_name: {
    type: DataTypes.STRING,
    allowNull: true
  },
  is_active: {
    type: DataTypes.BOOLEAN,
    defaultValue: true,
    allowNull: false
  },
  test_email: {
    type: DataTypes.STRING,
    allowNull: true,
    validate: {
      isEmail: true
    }
  },
  last_test_at: {
    type: DataTypes.DATE,
    allowNull: true
  },
  last_test_status: {
    type: DataTypes.ENUM('success', 'failed'),
    allowNull: true
  },
  last_test_error: {
    type: DataTypes.TEXT,
    allowNull: true
  },
  daily_limit: {
    type: DataTypes.INTEGER,
    defaultValue: 1000,
    allowNull: false
  },
  hourly_limit: {
    type: DataTypes.INTEGER,
    defaultValue: 100,
    allowNull: false
  },
  template_settings: {
    type: DataTypes.TEXT, // JSON string for SQLite compatibility
    allowNull: true
  }
}, {
  tableName: 'email_settings',
  timestamps: true,
  paranoid: true,
  indexes: [
    {
      fields: ['organization_id']
    },
    {
      fields: ['is_active']
    },
    {
      fields: ['last_test_at']
    }
  ]
});

module.exports = EmailSettings;
