const express = require('express');
const { body, param, query } = require('express-validator');
const router = express.Router();
const {
  submitBatchJob,
  listBatchJobs,
  getBatchJob,
  getBatchJobStatus,
  getBatchJobResults,
  cancelBatchJob
} = require('../controllers/batchController');
const scheduler = require('../services/scheduler');
const { authenticateToken } = require('../middleware/auth');

// Validation middleware
const validateBatchJobSubmission = [
  body('job_type')
    .isIn(['profitability', 'churn', 'revenue_leak', 'pricing', 'budget', 'demand', 'anomaly'])
    .withMessage('Invalid job type'),
  body('organization_id')
    .isUUID()
    .withMessage('Invalid organization ID'),
  body('client_ids')
    .optional()
    .isArray()
    .withMessage('Client IDs must be an array'),
  body('client_ids.*')
    .optional()
    .isUUID()
    .withMessage('Invalid client ID format'),
  body('parameters')
    .optional()
    .isObject()
    .withMessage('Parameters must be an object'),
  body('priority')
    .optional()
    .isIn(['low', 'normal', 'high', 'urgent'])
    .withMessage('Invalid priority level'),
  body('scheduled_at')
    .optional()
    .isISO8601()
    .withMessage('Invalid scheduled date format')
];

const validateJobId = [
  param('id')
    .isUUID()
    .withMessage('Invalid job ID format')
];

const validateListQuery = [
  query('organization_id')
    .optional()
    .isUUID()
    .withMessage('Invalid organization ID'),
  query('status')
    .optional()
    .isIn(['pending', 'running', 'completed', 'failed', 'cancelled'])
    .withMessage('Invalid status'),
  query('job_type')
    .optional()
    .isIn(['profitability', 'churn', 'revenue_leak', 'pricing', 'budget', 'demand', 'anomaly'])
    .withMessage('Invalid job type'),
  query('page')
    .optional()
    .isInt({ min: 1 })
    .withMessage('Page must be a positive integer'),
  query('limit')
    .optional()
    .isInt({ min: 1, max: 100 })
    .withMessage('Limit must be between 1 and 100'),
  query('sort_by')
    .optional()
    .isIn(['createdAt', 'updatedAt', 'status', 'job_type', 'priority'])
    .withMessage('Invalid sort field'),
  query('sort_order')
    .optional()
    .isIn(['ASC', 'DESC', 'asc', 'desc'])
    .withMessage('Invalid sort order')
];

// Routes

/**
 * @route POST /api/batch/jobs
 * @desc Submit a new batch job
 * @access Private
 */
router.post('/jobs', 
  authenticateToken, 
  validateBatchJobSubmission, 
  submitBatchJob
);

/**
 * @route GET /api/batch/jobs
 * @desc List batch jobs with filtering and pagination
 * @access Private
 */
router.get('/jobs', 
  authenticateToken, 
  validateListQuery, 
  listBatchJobs
);

/**
 * @route GET /api/batch/jobs/:id
 * @desc Get detailed information about a specific batch job
 * @access Private
 */
router.get('/jobs/:id', 
  authenticateToken, 
  validateJobId, 
  getBatchJob
);

/**
 * @route GET /api/batch/jobs/:id/status
 * @desc Get real-time status of a batch job
 * @access Private
 */
router.get('/jobs/:id/status', 
  authenticateToken, 
  validateJobId, 
  getBatchJobStatus
);

/**
 * @route GET /api/batch/jobs/:id/results
 * @desc Get results of a completed batch job
 * @access Private
 */
router.get('/jobs/:id/results', 
  authenticateToken, 
  validateJobId, 
  getBatchJobResults
);

/**
 * @route DELETE /api/batch/jobs/:id
 * @desc Cancel a running batch job
 * @access Private
 */
router.delete('/jobs/:id', 
  authenticateToken, 
  validateJobId, 
  cancelBatchJob
);

// Batch job management endpoints

/**
 * @route POST /api/batch/profitability
 * @desc Submit batch profitability analysis job
 * @access Private
 */
router.post('/profitability', authenticateToken, [
  body('organization_id').isUUID().withMessage('Invalid organization ID'),
  body('client_ids').optional().isArray().withMessage('Client IDs must be an array'),
  body('parameters').optional().isObject().withMessage('Parameters must be an object')
], async (req, res) => {
  req.body.job_type = 'profitability';
  return submitBatchJob(req, res);
});

/**
 * @route POST /api/batch/churn
 * @desc Submit batch churn prediction job
 * @access Private
 */
router.post('/churn', authenticateToken, [
  body('organization_id').isUUID().withMessage('Invalid organization ID'),
  body('client_ids').optional().isArray().withMessage('Client IDs must be an array'),
  body('parameters').optional().isObject().withMessage('Parameters must be an object')
], async (req, res) => {
  req.body.job_type = 'churn';
  return submitBatchJob(req, res);
});

/**
 * @route POST /api/batch/revenue-leak
 * @desc Submit batch revenue leak detection job
 * @access Private
 */
router.post('/revenue-leak', authenticateToken, [
  body('organization_id').isUUID().withMessage('Invalid organization ID'),
  body('parameters').optional().isObject().withMessage('Parameters must be an object')
], async (req, res) => {
  req.body.job_type = 'revenue_leak';
  return submitBatchJob(req, res);
});

/**
 * @route POST /api/batch/pricing
 * @desc Submit batch pricing analysis job
 * @access Private
 */
router.post('/pricing', authenticateToken, [
  body('organization_id').isUUID().withMessage('Invalid organization ID'),
  body('client_ids').optional().isArray().withMessage('Client IDs must be an array'),
  body('parameters').optional().isObject().withMessage('Parameters must be an object')
], async (req, res) => {
  req.body.job_type = 'pricing';
  return submitBatchJob(req, res);
});

/**
 * @route POST /api/batch/budget
 * @desc Submit batch budget optimization job
 * @access Private
 */
router.post('/budget', authenticateToken, [
  body('organization_id').isUUID().withMessage('Invalid organization ID'),
  body('parameters').optional().isObject().withMessage('Parameters must be an object')
], async (req, res) => {
  req.body.job_type = 'budget';
  return submitBatchJob(req, res);
});

/**
 * @route POST /api/batch/demand
 * @desc Submit batch demand forecasting job
 * @access Private
 */
router.post('/demand', authenticateToken, [
  body('organization_id').isUUID().withMessage('Invalid organization ID'),
  body('parameters').optional().isObject().withMessage('Parameters must be an object')
], async (req, res) => {
  req.body.job_type = 'demand';
  return submitBatchJob(req, res);
});

/**
 * @route POST /api/batch/anomaly
 * @desc Submit batch anomaly detection job
 * @access Private
 */
router.post('/anomaly', authenticateToken, [
  body('organization_id').isUUID().withMessage('Invalid organization ID'),
  body('parameters').optional().isObject().withMessage('Parameters must be an object')
], async (req, res) => {
  req.body.job_type = 'anomaly';
  return submitBatchJob(req, res);
});

// Scheduler management endpoints

/**
 * @route GET /api/batch/scheduler/status
 * @desc Get scheduler service status
 * @access Private
 */
router.get('/scheduler/status', authenticateToken, (req, res) => {
  try {
    const status = scheduler.getStatus();
    res.json({
      success: true,
      data: status
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Failed to get scheduler status',
      error: error.message
    });
  }
});

/**
 * @route POST /api/batch/scheduler/recurring
 * @desc Create a recurring job schedule
 * @access Private
 */
router.post('/scheduler/recurring', authenticateToken, [
  body('name').notEmpty().withMessage('Job name is required'),
  body('cron_expression').notEmpty().withMessage('Cron expression is required'),
  body('job_type').isIn(['profitability', 'churn', 'revenue_leak', 'pricing', 'budget', 'demand', 'anomaly']).withMessage('Invalid job type'),
  body('organization_id').isUUID().withMessage('Invalid organization ID')
], (req, res) => {
  try {
    const { name, cron_expression, job_type, organization_id, parameters = {}, priority = 'normal' } = req.body;
    
    const recurringJob = scheduler.createRecurringJob({
      name,
      cronExpression: cron_expression,
      jobType: job_type,
      organizationId: organization_id,
      parameters,
      priority
    });

    res.status(201).json({
      success: true,
      message: 'Recurring job created successfully',
      data: {
        name,
        cron_expression,
        job_type,
        organization_id,
        status: 'scheduled'
      }
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Failed to create recurring job',
      error: error.message
    });
  }
});

module.exports = router;
