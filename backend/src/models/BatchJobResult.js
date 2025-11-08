const { DataTypes } = require('sequelize');

module.exports = (sequelize) => {
  const BatchJobResult = sequelize.define('BatchJobResult', {
    id: {
      type: DataTypes.UUID,
      defaultValue: DataTypes.UUIDV4,
      primaryKey: true
    },
    batch_job_id: {
      type: DataTypes.UUID,
      allowNull: false,
      references: {
        model: 'BatchJobs',
        key: 'id'
      }
    },
    item_id: {
      type: DataTypes.STRING,
      allowNull: false,
      comment: 'Client ID or item identifier'
    },
    item_type: {
      type: DataTypes.STRING,
      allowNull: false,
      defaultValue: 'client',
      comment: 'Type of item processed (client, organization, etc.)'
    },
    status: {
      type: DataTypes.ENUM('pending', 'processing', 'completed', 'failed'),
      defaultValue: 'pending'
    },
    prediction_result: {
      type: DataTypes.JSON,
      allowNull: true,
      comment: 'The actual prediction result from AI/ML service'
    },
    confidence_score: {
      type: DataTypes.DECIMAL(5, 4),
      allowNull: true,
      comment: 'Confidence score of the prediction (0-1)'
    },
    processing_time_ms: {
      type: DataTypes.INTEGER,
      allowNull: true,
      comment: 'Time taken to process this item in milliseconds'
    },
    error_message: {
      type: DataTypes.TEXT,
      allowNull: true
    },
    processed_at: {
      type: DataTypes.DATE,
      allowNull: true
    },
    metadata: {
      type: DataTypes.JSON,
      allowNull: true,
      comment: 'Additional metadata about the processing'
    }
  }, {
    tableName: 'batch_job_results',
    timestamps: true,
    indexes: [
      {
        fields: ['batch_job_id']
      },
      {
        fields: ['item_id']
      },
      {
        fields: ['status']
      },
      {
        fields: ['processed_at']
      },
      {
        unique: true,
        fields: ['batch_job_id', 'item_id']
      }
    ]
  });

  BatchJobResult.associate = (models) => {
    BatchJobResult.belongsTo(models.BatchJob, {
      foreignKey: 'batch_job_id',
      as: 'batchJob'
    });
  };

  return BatchJobResult;
};
