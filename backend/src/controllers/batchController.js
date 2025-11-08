const { BatchJob, BatchJobResult, Organization, Client } = require('../models')
const { Op } = require('sequelize')
const { validationResult } = require('express-validator')
const aiClient = require('../services/ai-ml')
const winston = require('winston')

// POST /api/batch/jobs - Submit a new batch job
const submitBatchJob = async (req, res) => {
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
      job_type,
      organization_id,
      client_ids,
      parameters = {},
      priority = 'normal',
      scheduled_at
    } = req.body

    // Validate organization exists
    const organization = await Organization.findByPk(organization_id)
    if (!organization) {
      return res.status(404).json({
        success: false,
        message: 'Organization not found'
      })
    }

    // If client_ids provided, validate they exist and belong to organization
    if (client_ids && client_ids.length > 0) {
      const clients = await Client.findAll({
        where: {
          id: { [Op.in]: client_ids },
          organization_id: organization_id
        }
      })

      if (clients.length !== client_ids.length) {
        return res.status(400).json({
          success: false,
          message: 'Some client IDs are invalid or do not belong to the organization'
        })
      }
    }

    // Create batch job record
    const batchJob = await BatchJob.create({
      job_type,
      organization_id,
      client_ids,
      parameters,
      priority,
      scheduled_at: scheduled_at ? new Date(scheduled_at) : null,
      total_items: client_ids ? client_ids.length : 0,
      created_by: req.user?.id
    })

    // Submit job to AI/ML service
    try {
      const aimlJobRequest = {
        job_type,
        organization_id,
        client_ids,
        parameters,
        priority,
        scheduled_at
      }

      const aimlResponse = await aiClient.submitBatchJob(aimlJobRequest)
      
      if (aimlResponse.success) {
        // Update batch job with AI/ML job ID
        await batchJob.update({
          aiml_job_id: aimlResponse.job_id,
          status: 'pending'
        })

        winston.info('Batch job submitted successfully', {
          batchJobId: batchJob.id,
          aimlJobId: aimlResponse.job_id,
          jobType: job_type,
          organizationId: organization_id
        })

        res.status(201).json({
          success: true,
          message: 'Batch job submitted successfully',
          data: {
            job_id: batchJob.id,
            aiml_job_id: aimlResponse.job_id,
            status: batchJob.status,
            job_type: batchJob.job_type,
            estimated_items: batchJob.total_items,
            created_at: batchJob.createdAt
          }
        })
      } else {
        throw new Error('AI/ML service rejected the batch job')
      }

    } catch (aiError) {
      winston.error('Failed to submit job to AI/ML service', {
        error: aiError.message,
        batchJobId: batchJob.id
      })

      // Update job status to failed
      await batchJob.update({
        status: 'failed',
        error_message: `AI/ML service error: ${aiError.message}`
      })

      res.status(500).json({
        success: false,
        message: 'Failed to submit job to AI/ML service',
        error: aiError.message
      })
    }

  } catch (error) {
    winston.error('Submit batch job error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while submitting batch job'
    })
  }
}

// GET /api/batch/jobs - List batch jobs
const listBatchJobs = async (req, res) => {
  try {
    const {
      organization_id,
      status,
      job_type,
      page = 1,
      limit = 20,
      sort_by = 'createdAt',
      sort_order = 'DESC'
    } = req.query

    const whereClause = {}
    
    if (organization_id) {
      whereClause.organization_id = organization_id
    }
    
    if (status) {
      whereClause.status = status
    }
    
    if (job_type) {
      whereClause.job_type = job_type
    }

    const offset = (page - 1) * limit

    const { count, rows: batchJobs } = await BatchJob.findAndCountAll({
      where: whereClause,
      include: [
        {
          model: Organization,
          as: 'organization',
          attributes: ['id', 'name']
        }
      ],
      order: [[sort_by, sort_order.toUpperCase()]],
      limit: parseInt(limit),
      offset: parseInt(offset)
    })

    res.json({
      success: true,
      data: {
        jobs: batchJobs,
        pagination: {
          total: count,
          page: parseInt(page),
          limit: parseInt(limit),
          total_pages: Math.ceil(count / limit)
        }
      }
    })

  } catch (error) {
    winston.error('List batch jobs error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while listing batch jobs'
    })
  }
}

// GET /api/batch/jobs/:id - Get batch job details
const getBatchJob = async (req, res) => {
  try {
    const { id } = req.params

    const batchJob = await BatchJob.findByPk(id, {
      include: [
        {
          model: Organization,
          as: 'organization',
          attributes: ['id', 'name']
        },
        {
          model: BatchJobResult,
          as: 'results',
          limit: 10,
          order: [['createdAt', 'DESC']]
        }
      ]
    })

    if (!batchJob) {
      return res.status(404).json({
        success: false,
        message: 'Batch job not found'
      })
    }

    // Get latest status from AI/ML service if job is still running
    if (batchJob.status === 'running' || batchJob.status === 'pending') {
      try {
        const aimlStatus = await aiClient.getBatchJobStatus(batchJob.aiml_job_id)
        
        if (aimlStatus.success) {
          // Update local job status
          const updateData = {
            status: aimlStatus.status,
            progress: aimlStatus.progress?.percentage || 0,
            processed_items: aimlStatus.progress?.processed_items || 0,
            failed_items: aimlStatus.progress?.failed_items || 0
          }

          if (aimlStatus.timestamps?.started_at && !batchJob.started_at) {
            updateData.started_at = new Date(aimlStatus.timestamps.started_at)
          }

          if (aimlStatus.timestamps?.completed_at && !batchJob.completed_at) {
            updateData.completed_at = new Date(aimlStatus.timestamps.completed_at)
          }

          await batchJob.update(updateData)
          
          // Refresh the job data
          await batchJob.reload()
        }
      } catch (aiError) {
        winston.warn('Failed to get AI/ML job status', {
          batchJobId: id,
          aimlJobId: batchJob.aiml_job_id,
          error: aiError.message
        })
      }
    }

    res.json({
      success: true,
      data: batchJob
    })

  } catch (error) {
    winston.error('Get batch job error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while getting batch job'
    })
  }
}

// GET /api/batch/jobs/:id/status - Get batch job status
const getBatchJobStatus = async (req, res) => {
  try {
    const { id } = req.params

    const batchJob = await BatchJob.findByPk(id, {
      attributes: ['id', 'status', 'progress', 'total_items', 'processed_items', 'failed_items', 'started_at', 'completed_at', 'estimated_completion', 'aiml_job_id']
    })

    if (!batchJob) {
      return res.status(404).json({
        success: false,
        message: 'Batch job not found'
      })
    }

    // Get real-time status from AI/ML service
    let aimlStatus = null
    if (batchJob.aiml_job_id && (batchJob.status === 'running' || batchJob.status === 'pending')) {
      try {
        aimlStatus = await aiClient.getBatchJobStatus(batchJob.aiml_job_id)
      } catch (aiError) {
        winston.warn('Failed to get AI/ML status', { error: aiError.message })
      }
    }

    const statusData = {
      job_id: batchJob.id,
      status: aimlStatus?.status || batchJob.status,
      progress: {
        percentage: aimlStatus?.progress?.percentage || batchJob.progress,
        processed_items: aimlStatus?.progress?.processed_items || batchJob.processed_items,
        total_items: aimlStatus?.progress?.total_items || batchJob.total_items,
        failed_items: aimlStatus?.progress?.failed_items || batchJob.failed_items
      },
      timestamps: {
        created_at: batchJob.createdAt,
        started_at: aimlStatus?.timestamps?.started_at || batchJob.started_at,
        completed_at: aimlStatus?.timestamps?.completed_at || batchJob.completed_at,
        estimated_completion: aimlStatus?.timestamps?.estimated_completion || batchJob.estimated_completion
      }
    }

    res.json({
      success: true,
      data: statusData
    })

  } catch (error) {
    winston.error('Get batch job status error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while getting batch job status'
    })
  }
}

// GET /api/batch/jobs/:id/results - Get batch job results
const getBatchJobResults = async (req, res) => {
  try {
    const { id } = req.params
    const { page = 1, limit = 50 } = req.query

    const batchJob = await BatchJob.findByPk(id, {
      attributes: ['id', 'status', 'job_type', 'aiml_job_id']
    })

    if (!batchJob) {
      return res.status(404).json({
        success: false,
        message: 'Batch job not found'
      })
    }

    if (batchJob.status !== 'completed') {
      return res.status(400).json({
        success: false,
        message: 'Job not yet completed'
      })
    }

    // Get results from AI/ML service
    try {
      const aimlResults = await aiClient.getBatchJobResults(batchJob.aiml_job_id)
      
      if (aimlResults.success) {
        res.json({
          success: true,
          data: {
            job_id: batchJob.id,
            status: batchJob.status,
            results: aimlResults.results,
            summary: aimlResults.summary
          }
        })
      } else {
        throw new Error('Failed to retrieve results from AI/ML service')
      }

    } catch (aiError) {
      winston.error('Failed to get AI/ML results', {
        batchJobId: id,
        aimlJobId: batchJob.aiml_job_id,
        error: aiError.message
      })

      // Fall back to local results if available
      const localResults = await BatchJobResult.findAll({
        where: { batch_job_id: id },
        limit: parseInt(limit),
        offset: (page - 1) * limit,
        order: [['createdAt', 'DESC']]
      })

      res.json({
        success: true,
        data: {
          job_id: batchJob.id,
          status: batchJob.status,
          results: localResults,
          summary: {
            total_processed: localResults.length,
            source: 'local_fallback'
          }
        }
      })
    }

  } catch (error) {
    winston.error('Get batch job results error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while getting batch job results'
    })
  }
}

// DELETE /api/batch/jobs/:id - Cancel batch job
const cancelBatchJob = async (req, res) => {
  try {
    const { id } = req.params

    const batchJob = await BatchJob.findByPk(id)

    if (!batchJob) {
      return res.status(404).json({
        success: false,
        message: 'Batch job not found'
      })
    }

    if (batchJob.status === 'completed' || batchJob.status === 'failed') {
      return res.status(400).json({
        success: false,
        message: 'Cannot cancel completed or failed job'
      })
    }

    // Cancel job in AI/ML service
    try {
      if (batchJob.aiml_job_id) {
        await aiClient.cancelBatchJob(batchJob.aiml_job_id)
      }
    } catch (aiError) {
      winston.warn('Failed to cancel AI/ML job', {
        batchJobId: id,
        aimlJobId: batchJob.aiml_job_id,
        error: aiError.message
      })
    }

    // Update local job status
    await batchJob.update({
      status: 'cancelled',
      completed_at: new Date()
    })

    winston.info('Batch job cancelled', {
      batchJobId: id,
      aimlJobId: batchJob.aiml_job_id
    })

    res.json({
      success: true,
      message: 'Batch job cancelled successfully'
    })

  } catch (error) {
    winston.error('Cancel batch job error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while cancelling batch job'
    })
  }
}

module.exports = {
  submitBatchJob,
  listBatchJobs,
  getBatchJob,
  getBatchJobStatus,
  getBatchJobResults,
  cancelBatchJob
}
