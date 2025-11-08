const cron = require('node-cron');
const { BatchJob, Organization } = require('../models');
const { Op } = require('sequelize');
const winston = require('winston');
const aiClient = require('./ai-ml');

class SchedulerService {
  constructor() {
    this.jobs = new Map();
    this.isInitialized = false;
  }

  /**
   * Initialize the scheduler service
   */
  async initialize() {
    if (this.isInitialized) return;

    winston.info('Initializing Scheduler Service...');

    // Start the main scheduler that checks for scheduled jobs every minute
    this.startMainScheduler();

    // Load existing scheduled jobs from database
    await this.loadScheduledJobs();

    this.isInitialized = true;
    winston.info('Scheduler Service initialized successfully');
  }

  /**
   * Start the main scheduler
   */
  startMainScheduler() {
    // Check for scheduled jobs every minute
    const mainScheduler = cron.schedule('* * * * *', async () => {
      await this.processScheduledJobs();
    }, {
      scheduled: false
    });

    mainScheduler.start();
    winston.info('Main scheduler started - checking for scheduled jobs every minute');
  }

  /**
   * Load scheduled jobs from database
   */
  async loadScheduledJobs() {
    try {
      const scheduledJobs = await BatchJob.findAll({
        where: {
          status: 'pending',
          scheduled_at: {
            [Op.not]: null
          }
        },
        include: [{
          model: Organization,
          as: 'organization',
          attributes: ['id', 'name']
        }]
      });

      winston.info(`Loaded ${scheduledJobs.length} scheduled jobs from database`);

      for (const job of scheduledJobs) {
        this.scheduleJob(job);
      }
    } catch (error) {
      winston.error('Error loading scheduled jobs:', error);
    }
  }

  /**
   * Schedule a batch job
   * @param {Object} batchJob - Batch job instance
   */
  scheduleJob(batchJob) {
    const scheduledAt = new Date(batchJob.scheduled_at);
    const now = new Date();

    if (scheduledAt <= now) {
      // Job should run immediately
      winston.info(`Scheduling immediate execution for job ${batchJob.id}`);
      setImmediate(() => this.executeScheduledJob(batchJob));
      return;
    }

    // Calculate delay until execution
    const delay = scheduledAt.getTime() - now.getTime();

    // Schedule the job
    const timeoutId = setTimeout(() => {
      this.executeScheduledJob(batchJob);
      this.jobs.delete(batchJob.id);
    }, delay);

    this.jobs.set(batchJob.id, {
      timeoutId,
      batchJob,
      scheduledAt
    });

    winston.info(`Scheduled job ${batchJob.id} to run at ${scheduledAt.toISOString()}`);
  }

  /**
   * Process scheduled jobs that are due
   */
  async processScheduledJobs() {
    try {
      const now = new Date();
      
      // Find jobs that are due to run
      const dueJobs = await BatchJob.findAll({
        where: {
          status: 'pending',
          scheduled_at: {
            [Op.lte]: now,
            [Op.not]: null
          }
        },
        include: [{
          model: Organization,
          as: 'organization',
          attributes: ['id', 'name']
        }]
      });

      for (const job of dueJobs) {
        await this.executeScheduledJob(job);
      }

    } catch (error) {
      winston.error('Error processing scheduled jobs:', error);
    }
  }

  /**
   * Execute a scheduled job
   * @param {Object} batchJob - Batch job to execute
   */
  async executeScheduledJob(batchJob) {
    try {
      winston.info(`Executing scheduled job ${batchJob.id} (${batchJob.job_type})`);

      // Prepare job data for AI/ML service
      const jobData = {
        job_type: batchJob.job_type,
        organization_id: batchJob.organization_id,
        client_ids: batchJob.client_ids,
        parameters: batchJob.parameters,
        priority: batchJob.priority
      };

      // Submit to AI/ML service
      const aimlResponse = await aiClient.submitBatchJob(jobData);

      if (aimlResponse.success) {
        // Update job status and AI/ML job ID
        await batchJob.update({
          status: 'running',
          started_at: new Date(),
          aiml_job_id: aimlResponse.job_id
        });

        winston.info(`Scheduled job ${batchJob.id} submitted to AI/ML service with ID ${aimlResponse.job_id}`);
      } else {
        throw new Error('AI/ML service rejected the scheduled job');
      }

    } catch (error) {
      winston.error(`Error executing scheduled job ${batchJob.id}:`, error);

      // Update job status to failed
      await batchJob.update({
        status: 'failed',
        error_message: `Scheduled execution failed: ${error.message}`,
        completed_at: new Date()
      });
    }
  }

  /**
   * Cancel a scheduled job
   * @param {string} jobId - Job ID to cancel
   */
  cancelScheduledJob(jobId) {
    const scheduledJob = this.jobs.get(jobId);
    
    if (scheduledJob) {
      clearTimeout(scheduledJob.timeoutId);
      this.jobs.delete(jobId);
      winston.info(`Cancelled scheduled job ${jobId}`);
      return true;
    }

    return false;
  }

  /**
   * Get scheduled jobs status
   * @returns {Object} Scheduler status
   */
  getStatus() {
    return {
      initialized: this.isInitialized,
      scheduled_jobs_count: this.jobs.size,
      scheduled_jobs: Array.from(this.jobs.entries()).map(([jobId, job]) => ({
        job_id: jobId,
        job_type: job.batchJob.job_type,
        scheduled_at: job.scheduledAt.toISOString(),
        organization_id: job.batchJob.organization_id
      }))
    };
  }

  /**
   * Create recurring job schedules
   * @param {Object} config - Recurring job configuration
   */
  createRecurringJob(config) {
    const {
      name,
      cronExpression,
      jobType,
      organizationId,
      parameters = {},
      priority = 'normal'
    } = config;

    const recurringJob = cron.schedule(cronExpression, async () => {
      try {
        winston.info(`Executing recurring job: ${name}`);

        // Create a new batch job
        const batchJob = await BatchJob.create({
          job_type: jobType,
          organization_id: organizationId,
          parameters,
          priority,
          status: 'pending'
        });

        // Execute immediately
        await this.executeScheduledJob(batchJob);

      } catch (error) {
        winston.error(`Error in recurring job ${name}:`, error);
      }
    }, {
      scheduled: false
    });

    recurringJob.start();
    winston.info(`Created recurring job: ${name} with schedule: ${cronExpression}`);

    return recurringJob;
  }

  /**
   * Destroy the scheduler service
   */
  destroy() {
    // Cancel all scheduled jobs
    for (const [jobId, scheduledJob] of this.jobs) {
      clearTimeout(scheduledJob.timeoutId);
    }
    this.jobs.clear();

    winston.info('Scheduler Service destroyed');
  }
}

// Export singleton instance
module.exports = new SchedulerService();
