const { DataTypes } = require('sequelize');

module.exports = (sequelize) => {
  const BatchJob = sequelize.define('BatchJob', {
    id: {
      type: DataTypes.UUID,
      defaultValue: DataTypes.UUIDV4,
      primaryKey: true
    },
    job_type: {
      type: DataTypes.ENUM('profitability', 'churn', 'revenue_leak', 'pricing', 'budget', 'demand', 'anomaly'),
      allowNull: false
    },
    organization_id: {
      type: DataTypes.UUID,
      allowNull: false,
      references: {
        model: 'Organizations',
        key: 'id'
      }
    },
    client_ids: {
      type: DataTypes.JSON,
      allowNull: true,
      comment: 'Array of client IDs to process, null for organization-wide'
    },
    parameters: {
      type: DataTypes.JSON,
      allowNull: true,
      defaultValue: {},
      comment: 'Job-specific parameters'
    },
    priority: {
      type: DataTypes.ENUM('low', 'normal', 'high', 'urgent'),
      defaultValue: 'normal'
    },
    status: {
      type: DataTypes.ENUM('pending', 'running', 'completed', 'failed', 'cancelled'),
      defaultValue: 'pending'
    },
    progress: {
      type: DataTypes.INTEGER,
      defaultValue: 0,
      comment: 'Progress percentage (0-100)'
    },
    total_items: {
      type: DataTypes.INTEGER,
      defaultValue: 0
    },
    processed_items: {
      type: DataTypes.INTEGER,
      defaultValue: 0
    },
    failed_items: {
      type: DataTypes.INTEGER,
      defaultValue: 0
    },
    started_at: {
      type: DataTypes.DATE,
      allowNull: true
    },
    completed_at: {
      type: DataTypes.DATE,
      allowNull: true
    },
    scheduled_at: {
      type: DataTypes.DATE,
      allowNull: true,
      comment: 'For scheduled jobs'
    },
    estimated_completion: {
      type: DataTypes.DATE,
      allowNull: true
    },
    aiml_job_id: {
      type: DataTypes.STRING,
      allowNull: true,
      comment: 'Job ID from AI/ML service'
    },
    error_message: {
      type: DataTypes.TEXT,
      allowNull: true
    },
    results_summary: {
      type: DataTypes.JSON,
      allowNull: true,
      comment: 'Summary of job results'
    },
    created_by: {
      type: DataTypes.UUID,
      allowNull: true,
      references: {
        model: 'Users',
        key: 'id'
      }
    }
  }, {
    tableName: 'batch_jobs',
    timestamps: true,
    indexes: [
      {
        fields: ['organization_id']
      },
      {
        fields: ['status']
      },
      {
        fields: ['job_type']
      },
      {
        fields: ['created_at']
      },
      {
        fields: ['scheduled_at']
      }
    ]
  });

  BatchJob.associate = (models) => {
    BatchJob.belongsTo(models.Organization, {
      foreignKey: 'organization_id',
      as: 'organization'
    });
    
    BatchJob.belongsTo(models.User, {
      foreignKey: 'created_by',
      as: 'creator'
    });
    
    BatchJob.hasMany(models.BatchJobResult, {
      foreignKey: 'batch_job_id',
      as: 'results'
    });
  };

  return BatchJob;
};
