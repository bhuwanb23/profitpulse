const { validationResult } = require('express-validator')
const aiClient = require('../services/ai-ml')
const winston = require('winston')

// Historical Data Analysis Controllers

// POST /api/advanced/historical/analysis - Get historical analysis
const getHistoricalAnalysis = async (req, res) => {
  try {
    const errors = validationResult(req)
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        message: 'Validation failed',
        errors: errors.array()
      })
    }

    const {
      model_type,
      organization_id,
      start_date,
      end_date,
      analysis_type = 'trend',
      parameters = {}
    } = req.body

    // Call AI/ML service for historical analysis
    const aiResponse = await aiClient.getHistoricalAnalysis({
      model_type,
      organization_id,
      start_date,
      end_date,
      analysis_type,
      parameters
    })

    if (aiResponse.success) {
      winston.info('Historical analysis completed successfully', {
        modelType: model_type,
        organizationId: organization_id,
        analysisType: analysis_type
      })

      res.json({
        success: true,
        message: 'Historical analysis completed successfully',
        data: aiResponse.data
      })
    } else {
      throw new Error('AI/ML service failed to generate historical analysis')
    }

  } catch (error) {
    winston.error('Historical analysis error:', error)
    res.status(500).json({
      success: false,
      message: 'Failed to generate historical analysis',
      error: error.message
    })
  }
}

// POST /api/advanced/trends/analysis - Get trend analysis
const getTrendAnalysis = async (req, res) => {
  try {
    const errors = validationResult(req)
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        message: 'Validation failed',
        errors: errors.array()
      })
    }

    const {
      model_type,
      organization_id,
      time_period = '30d',
      metrics = [],
      granularity = 'daily'
    } = req.body

    // Call AI/ML service for trend analysis
    const aiResponse = await aiClient.getTrendAnalysis({
      model_type,
      organization_id,
      time_period,
      metrics,
      granularity
    })

    if (aiResponse.success) {
      winston.info('Trend analysis completed successfully', {
        modelType: model_type,
        organizationId: organization_id,
        timePeriod: time_period
      })

      res.json({
        success: true,
        message: 'Trend analysis completed successfully',
        data: aiResponse.data
      })
    } else {
      throw new Error('AI/ML service failed to generate trend analysis')
    }

  } catch (error) {
    winston.error('Trend analysis error:', error)
    res.status(500).json({
      success: false,
      message: 'Failed to generate trend analysis',
      error: error.message
    })
  }
}

// Performance Reporting Controllers

// POST /api/advanced/performance/report - Generate performance report
const getPerformanceReport = async (req, res) => {
  try {
    const errors = validationResult(req)
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        message: 'Validation failed',
        errors: errors.array()
      })
    }

    const {
      model_type,
      organization_id,
      report_type = 'summary',
      time_range = '30d',
      metrics = []
    } = req.body

    // Call AI/ML service for performance report
    const aiResponse = await aiClient.getPerformanceReport({
      model_type,
      organization_id,
      report_type,
      time_range,
      metrics
    })

    if (aiResponse.success) {
      winston.info('Performance report generated successfully', {
        modelType: model_type,
        organizationId: organization_id,
        reportType: report_type
      })

      res.json({
        success: true,
        message: 'Performance report generated successfully',
        data: aiResponse.data
      })
    } else {
      throw new Error('AI/ML service failed to generate performance report')
    }

  } catch (error) {
    winston.error('Performance report error:', error)
    res.status(500).json({
      success: false,
      message: 'Failed to generate performance report',
      error: error.message
    })
  }
}

// GET /api/advanced/performance/metrics - Get model metrics
const getModelMetrics = async (req, res) => {
  try {
    const { model_type, organization_id } = req.query

    // Call AI/ML service for model metrics
    const aiResponse = await aiClient.getModelMetrics({
      model_type,
      organization_id
    })

    if (aiResponse.success) {
      winston.info('Model metrics retrieved successfully', {
        modelType: model_type,
        organizationId: organization_id
      })

      res.json({
        success: true,
        message: 'Model metrics retrieved successfully',
        data: aiResponse.data
      })
    } else {
      throw new Error('AI/ML service failed to retrieve model metrics')
    }

  } catch (error) {
    winston.error('Model metrics error:', error)
    res.status(500).json({
      success: false,
      message: 'Failed to retrieve model metrics',
      error: error.message
    })
  }
}

// Model Retraining Controllers

// POST /api/advanced/retraining/trigger - Trigger model retraining
const triggerRetraining = async (req, res) => {
  try {
    const errors = validationResult(req)
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        message: 'Validation failed',
        errors: errors.array()
      })
    }

    const {
      model_type,
      organization_id,
      trigger_type = 'performance',
      threshold_metrics = {},
      parameters = {}
    } = req.body

    // Call AI/ML service to trigger retraining
    const aiResponse = await aiClient.triggerRetraining({
      model_type,
      organization_id,
      trigger_type,
      threshold_metrics,
      parameters
    })

    if (aiResponse.success) {
      winston.info('Model retraining triggered successfully', {
        modelType: model_type,
        organizationId: organization_id,
        triggerType: trigger_type,
        jobId: aiResponse.data.job_id
      })

      res.status(201).json({
        success: true,
        message: 'Model retraining triggered successfully',
        data: aiResponse.data
      })
    } else {
      throw new Error('AI/ML service failed to trigger retraining')
    }

  } catch (error) {
    winston.error('Retraining trigger error:', error)
    res.status(500).json({
      success: false,
      message: 'Failed to trigger model retraining',
      error: error.message
    })
  }
}

// GET /api/advanced/retraining/status/:jobId - Get retraining status
const getRetrainingStatus = async (req, res) => {
  try {
    const { jobId } = req.params

    // Call AI/ML service for retraining status
    const aiResponse = await aiClient.getRetrainingStatus(jobId)

    if (aiResponse.success) {
      res.json({
        success: true,
        message: 'Retraining status retrieved successfully',
        data: aiResponse.data
      })
    } else {
      throw new Error('AI/ML service failed to retrieve retraining status')
    }

  } catch (error) {
    winston.error('Retraining status error:', error)
    
    if (error.message.includes('not found')) {
      res.status(404).json({
        success: false,
        message: 'Retraining job not found'
      })
    } else {
      res.status(500).json({
        success: false,
        message: 'Failed to retrieve retraining status',
        error: error.message
      })
    }
  }
}

// GET /api/advanced/retraining/jobs - List retraining jobs
const listRetrainingJobs = async (req, res) => {
  try {
    const { model_type, organization_id, status } = req.query

    // Call AI/ML service for retraining jobs list
    const aiResponse = await aiClient.listRetrainingJobs({
      model_type,
      organization_id,
      status
    })

    if (aiResponse.success) {
      winston.info('Retraining jobs listed successfully', {
        modelType: model_type,
        organizationId: organization_id,
        totalJobs: aiResponse.data.total_count
      })

      res.json({
        success: true,
        message: 'Retraining jobs retrieved successfully',
        data: aiResponse.data
      })
    } else {
      throw new Error('AI/ML service failed to retrieve retraining jobs')
    }

  } catch (error) {
    winston.error('Retraining jobs list error:', error)
    res.status(500).json({
      success: false,
      message: 'Failed to retrieve retraining jobs',
      error: error.message
    })
  }
}

// Dashboard and Alerting Controllers

// GET /api/advanced/dashboard/metrics - Get dashboard metrics
const getDashboardMetrics = async (req, res) => {
  try {
    const { organization_id } = req.query

    // Get metrics for all models
    const [
      modelMetrics,
      performanceReport
    ] = await Promise.all([
      aiClient.getModelMetrics({ organization_id }),
      aiClient.getPerformanceReport({
        organization_id,
        report_type: 'summary',
        time_range: '7d'
      })
    ])

    const dashboardData = {
      model_metrics: modelMetrics.success ? modelMetrics.data.metrics : {},
      performance_summary: performanceReport.success ? performanceReport.data.report.executive_summary : {},
      alerts: generateAlerts(modelMetrics.data?.metrics || {}),
      last_updated: new Date().toISOString()
    }

    winston.info('Dashboard metrics retrieved successfully', {
      organizationId: organization_id
    })

    res.json({
      success: true,
      message: 'Dashboard metrics retrieved successfully',
      data: dashboardData
    })

  } catch (error) {
    winston.error('Dashboard metrics error:', error)
    res.status(500).json({
      success: false,
      message: 'Failed to retrieve dashboard metrics',
      error: error.message
    })
  }
}

// Helper function to generate alerts based on metrics
function generateAlerts(metrics) {
  const alerts = []
  
  Object.entries(metrics).forEach(([modelType, modelMetrics]) => {
    // Check accuracy threshold
    if (modelMetrics.accuracy < 0.85) {
      alerts.push({
        type: 'accuracy_low',
        severity: 'warning',
        model: modelType,
        message: `${modelType} model accuracy (${modelMetrics.accuracy}) is below threshold (0.85)`,
        recommendation: 'Consider retraining the model with more recent data'
      })
    }
    
    // Check prediction volume
    if (modelMetrics.predictions_today < 10) {
      alerts.push({
        type: 'low_volume',
        severity: 'info',
        model: modelType,
        message: `${modelType} model has low prediction volume today (${modelMetrics.predictions_today})`,
        recommendation: 'Monitor usage patterns and client engagement'
      })
    }
    
    // Check confidence levels
    if (modelMetrics.avg_confidence < 0.75) {
      alerts.push({
        type: 'low_confidence',
        severity: 'warning',
        model: modelType,
        message: `${modelType} model has low average confidence (${modelMetrics.avg_confidence})`,
        recommendation: 'Review input data quality and model parameters'
      })
    }
  })
  
  return alerts
}

module.exports = {
  getHistoricalAnalysis,
  getTrendAnalysis,
  getPerformanceReport,
  getModelMetrics,
  triggerRetraining,
  getRetrainingStatus,
  listRetrainingJobs,
  getDashboardMetrics
}
