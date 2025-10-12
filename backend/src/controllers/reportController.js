const { Report, ReportTemplate, ScheduledReport, Organization, User } = require('../models')
const { Op } = require('sequelize')
const { validationResult } = require('express-validator')
const crypto = require('crypto')
const fs = require('fs')
const path = require('path')

// GET /api/reports/templates - Report templates
const getReportTemplates = async (req, res) => {
  try {
    const { 
      organization_id,
      category,
      report_type,
      is_global,
      is_active,
      limit = 50,
      offset = 0
    } = req.query

    const whereClause = {}
    
    if (organization_id) {
      whereClause.organization_id = organization_id
    }
    if (category) {
      whereClause.category = category
    }
    if (report_type) {
      whereClause.report_type = report_type
    }
    if (is_global !== undefined) {
      whereClause.is_global = is_global === 'true'
    }
    if (is_active !== undefined) {
      whereClause.is_active = is_active === 'true'
    }

    // Mock data for demonstration
    const templates = [
      {
        id: 'template-1',
        name: 'Financial Summary Report',
        description: 'Comprehensive financial overview with revenue, expenses, and profit analysis',
        category: 'financial',
        report_type: 'financial',
        is_global: true,
        is_active: true,
        usage_count: 25,
        last_used: new Date().toISOString(),
        createdAt: new Date().toISOString(),
        organization: { id: organization_id, name: 'TechWave MSP' },
        createdByUser: { id: 'user-1', firstName: 'Admin', lastName: 'User', email: 'admin@techwave.com' }
      },
      {
        id: 'template-2',
        name: 'Operational Performance Report',
        description: 'Ticket resolution metrics, SLA compliance, and technician performance',
        category: 'operational',
        report_type: 'operational',
        is_global: true,
        is_active: true,
        usage_count: 18,
        last_used: new Date().toISOString(),
        createdAt: new Date().toISOString(),
        organization: { id: organization_id, name: 'TechWave MSP' },
        createdByUser: { id: 'user-1', firstName: 'Admin', lastName: 'User', email: 'admin@techwave.com' }
      },
      {
        id: 'template-3',
        name: 'Client Analytics Report',
        description: 'Client segmentation, churn analysis, and growth metrics',
        category: 'analytical',
        report_type: 'analytical',
        is_global: true,
        is_active: true,
        usage_count: 12,
        last_used: new Date().toISOString(),
        createdAt: new Date().toISOString(),
        organization: { id: organization_id, name: 'TechWave MSP' },
        createdByUser: { id: 'user-1', firstName: 'Admin', lastName: 'User', email: 'admin@techwave.com' }
      }
    ]

    const count = templates.length

    res.json({
      success: true,
      data: {
        templates,
        pagination: {
          total: count,
          limit: parseInt(limit),
          offset: parseInt(offset),
          pages: Math.ceil(count / parseInt(limit))
        }
      }
    })
  } catch (error) {
    console.error('Get report templates error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching report templates'
    })
  }
}

// POST /api/reports/generate - Generate custom report
const generateReport = async (req, res) => {
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
      organization_id,
      template_id,
      title,
      description,
      report_type,
      parameters,
      filters,
      format = 'json'
    } = req.body

    // Mock organization and template validation
    const organization = { id: organization_id, name: 'TechWave MSP' }
    const template = template_id ? { id: template_id, name: 'Financial Summary Report', category: 'financial' } : null

    // Mock report creation
    const report = {
      id: crypto.randomUUID(),
      organization_id,
      template_id,
      title,
      description,
      report_type,
      parameters: parameters ? JSON.stringify(parameters) : null,
      filters: filters ? JSON.stringify(filters) : null,
      format,
      status: 'pending',
      created_by: req.user?.id || 'user-1'
    }

    // Generate report data (simulated)
    const reportData = await generateReportData(report, parameters, filters)

    // Update report with generated data
    report.data = JSON.stringify(reportData)
    report.status = 'completed'
    report.generated_at = new Date()

    res.json({
      success: true,
      message: 'Report generated successfully',
      data: {
        report_id: report.id,
        title: report.title,
        report_type: report.report_type,
        format: report.format,
        status: report.status,
        generated_at: report.generated_at,
        data: reportData,
        template_used: template ? {
          id: template.id,
          name: template.name,
          category: template.category
        } : null
      }
    })
  } catch (error) {
    console.error('Generate report error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while generating report'
    })
  }
}

// GET /api/reports/:id - Get report
const getReport = async (req, res) => {
  try {
    const { id } = req.params
    const { include_data = true } = req.query

    // Mock report data
    const report = {
      id: id,
      title: 'Monthly Financial Report',
      description: 'Monthly financial summary for December 2024',
      report_type: 'financial',
      status: 'completed',
      format: 'json',
      parameters: JSON.stringify({ period: 'monthly', year: 2024, month: 12 }),
      filters: JSON.stringify({ include_details: true, currency: 'USD' }),
      file_path: null,
      file_size: null,
      generated_at: new Date().toISOString(),
      expires_at: null,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      data: JSON.stringify({
        summary: {
          total_revenue: 125000,
          total_expenses: 85000,
          net_profit: 40000,
          profit_margin: 32
        }
      }),
      organization: { id: 'f4e806f0-8201-43d3-a80b-ca3bd051497b', name: 'TechWave MSP' },
      template: { id: '550e8400-e29b-41d4-a716-446655440000', name: 'Financial Summary Report', category: 'financial', description: 'Comprehensive financial overview' },
      createdByUser: { id: 'user-1', firstName: 'Admin', lastName: 'User', email: 'admin@techwave.com' }
    }

    const reportData = {
      id: report.id,
      title: report.title,
      description: report.description,
      report_type: report.report_type,
      status: report.status,
      format: report.format,
      parameters: report.parameters ? JSON.parse(report.parameters) : null,
      filters: report.filters ? JSON.parse(report.filters) : null,
      file_path: report.file_path,
      file_size: report.file_size,
      generated_at: report.generated_at,
      expires_at: report.expires_at,
      created_at: report.createdAt,
      updated_at: report.updatedAt,
      organization: report.organization,
      template: report.template,
      created_by: report.createdByUser
    }

    if (include_data === 'true' && report.data) {
      reportData.data = JSON.parse(report.data)
    }

    res.json({
      success: true,
      data: reportData
    })
  } catch (error) {
    console.error('Get report error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching report'
    })
  }
}

// POST /api/reports/:id/export - Export report (PDF/Excel)
const exportReport = async (req, res) => {
  try {
    const errors = validationResult(req)
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        message: 'Validation failed',
        errors: errors.array()
      })
    }

    const { id } = req.params
    const { format = 'pdf', email_to } = req.body

    // Mock report validation
    const report = {
      id: id,
      title: 'Monthly Financial Report',
      status: 'completed'
    }

    // Generate export file (simulated)
    const exportResult = await generateExportFile(report, format)

    // Mock file information update
    report.file_path = exportResult.file_path
    report.file_size = exportResult.file_size

    // Send email if requested (simulated)
    if (email_to) {
      await sendReportEmail(report, exportResult, email_to)
    }

    res.json({
      success: true,
      message: 'Report exported successfully',
      data: {
        report_id: report.id,
        format: format,
        file_path: exportResult.file_path,
        file_size: exportResult.file_size,
        download_url: `/api/reports/${report.id}/download`,
        email_sent: !!email_to,
        email_recipients: email_to
      }
    })
  } catch (error) {
    console.error('Export report error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while exporting report'
    })
  }
}

// POST /api/reports/schedule - Schedule report
const scheduleReport = async (req, res) => {
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
      organization_id,
      report_id,
      template_id,
      title,
      description,
      schedule_type,
      schedule_config,
      next_run,
      parameters,
      filters,
      format = 'json',
      email_recipients,
      email_subject,
      email_body
    } = req.body

    // Mock organization validation
    const organization = { id: organization_id, name: 'TechWave MSP' }

    // Validate schedule configuration
    const scheduleValidation = validateScheduleConfig(schedule_type, schedule_config, next_run)
    if (!scheduleValidation.valid) {
      return res.status(400).json({
        success: false,
        message: 'Invalid schedule configuration',
        errors: scheduleValidation.errors
      })
    }

    // Mock scheduled report creation
    const scheduledReport = {
      id: crypto.randomUUID(),
      organization_id,
      report_id,
      template_id,
      title,
      description,
      schedule_type,
      schedule_config: schedule_config ? JSON.stringify(schedule_config) : null,
      next_run: new Date(next_run),
      status: 'active',
      parameters: parameters ? JSON.stringify(parameters) : null,
      filters: filters ? JSON.stringify(filters) : null,
      format,
      email_recipients: email_recipients ? JSON.stringify(email_recipients) : null,
      email_subject,
      email_body,
      created_by: req.user?.id || 'user-1'
    }

    res.json({
      success: true,
      message: 'Report scheduled successfully',
      data: {
        scheduled_report_id: scheduledReport.id,
        title: scheduledReport.title,
        schedule_type: scheduledReport.schedule_type,
        next_run: scheduledReport.next_run,
        status: scheduledReport.status,
        email_recipients: email_recipients,
        schedule_config: schedule_config
      }
    })
  } catch (error) {
    console.error('Schedule report error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while scheduling report'
    })
  }
}

// GET /api/reports/scheduled - List scheduled reports
const getScheduledReports = async (req, res) => {
  try {
    const { 
      organization_id,
      status,
      schedule_type,
      limit = 50,
      offset = 0
    } = req.query

    const whereClause = {}
    
    if (organization_id) {
      whereClause.organization_id = organization_id
    }
    if (status) {
      whereClause.status = status
    }
    if (schedule_type) {
      whereClause.schedule_type = schedule_type
    }

    const { count, rows: scheduledReports } = await ScheduledReport.findAndCountAll({
      where: whereClause,
      include: [
        {
          model: Organization,
          as: 'organization',
          attributes: ['id', 'name']
        },
        {
          model: Report,
          as: 'report',
          attributes: ['id', 'title', 'status']
        },
        {
          model: ReportTemplate,
          as: 'template',
          attributes: ['id', 'name', 'category']
        },
        {
          model: User,
          as: 'createdByUser',
          attributes: ['id', 'firstName', 'lastName', 'email']
        }
      ],
      limit: parseInt(limit),
      offset: parseInt(offset),
      order: [['next_run', 'ASC']]
    })

    res.json({
      success: true,
      data: {
        scheduled_reports: scheduledReports,
        pagination: {
          total: count,
          limit: parseInt(limit),
          offset: parseInt(offset),
          pages: Math.ceil(count / parseInt(limit))
        }
      }
    })
  } catch (error) {
    console.error('Get scheduled reports error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching scheduled reports'
    })
  }
}

// DELETE /api/reports/scheduled/:id - Cancel scheduled report
const cancelScheduledReport = async (req, res) => {
  try {
    const { id } = req.params

    // Mock scheduled report cancellation
    const scheduledReport = {
      id: id,
      title: 'Weekly Financial Report',
      status: 'cancelled'
    }

    res.json({
      success: true,
      message: 'Scheduled report cancelled successfully',
      data: {
        scheduled_report_id: id,
        title: scheduledReport.title,
        status: 'cancelled'
      }
    })
  } catch (error) {
    console.error('Cancel scheduled report error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while cancelling scheduled report'
    })
  }
}

// Helper function to generate report data
const generateReportData = async (report, parameters, filters) => {
  try {
    // Simulate report data generation based on report type
    const reportType = report.report_type
    const now = new Date()
    
    switch (reportType) {
      case 'financial':
        return {
          summary: {
            total_revenue: 125000,
            total_expenses: 85000,
            net_profit: 40000,
            profit_margin: 32
          },
          revenue_breakdown: [
            { category: 'Services', amount: 75000, percentage: 60 },
            { category: 'Products', amount: 35000, percentage: 28 },
            { category: 'Support', amount: 15000, percentage: 12 }
          ],
          expenses_breakdown: [
            { category: 'Personnel', amount: 45000, percentage: 53 },
            { category: 'Infrastructure', amount: 20000, percentage: 24 },
            { category: 'Marketing', amount: 15000, percentage: 18 },
            { category: 'Other', amount: 5000, percentage: 5 }
          ],
          period: {
            start_date: new Date(now.getFullYear(), now.getMonth(), 1).toISOString(),
            end_date: now.toISOString()
          }
        }
      
      case 'operational':
        return {
          summary: {
            total_tickets: 150,
            resolved_tickets: 120,
            pending_tickets: 30,
            resolution_rate: 80
          },
          ticket_breakdown: [
            { status: 'Open', count: 15, percentage: 10 },
            { status: 'In Progress', count: 15, percentage: 10 },
            { status: 'Resolved', count: 120, percentage: 80 }
          ],
          performance_metrics: [
            { metric: 'Average Resolution Time', value: '2.5 hours', target: '4 hours' },
            { metric: 'Customer Satisfaction', value: '4.2/5', target: '4.0/5' },
            { metric: 'First Call Resolution', value: '65%', target: '60%' }
          ],
          period: {
            start_date: new Date(now.getFullYear(), now.getMonth(), 1).toISOString(),
            end_date: now.toISOString()
          }
        }
      
      case 'analytical':
        return {
          summary: {
            total_clients: 25,
            active_clients: 22,
            churn_rate: 12,
            growth_rate: 15
          },
          client_analytics: [
            { segment: 'Enterprise', count: 5, revenue: 75000, percentage: 60 },
            { segment: 'SMB', count: 15, revenue: 40000, percentage: 32 },
            { segment: 'Startup', count: 5, revenue: 10000, percentage: 8 }
          ],
          trends: [
            { metric: 'Monthly Recurring Revenue', trend: 'up', change: '+8%' },
            { metric: 'Customer Acquisition Cost', trend: 'down', change: '-12%' },
            { metric: 'Customer Lifetime Value', trend: 'up', change: '+15%' }
          ],
          period: {
            start_date: new Date(now.getFullYear(), now.getMonth(), 1).toISOString(),
            end_date: now.toISOString()
          }
        }
      
      default:
        return {
          summary: {
            message: 'Custom report generated successfully',
            generated_at: now.toISOString()
          },
          data: {
            parameters: parameters || {},
            filters: filters || {}
          }
        }
    }
  } catch (error) {
    console.error('Generate report data error:', error)
    return {
      error: 'Failed to generate report data',
      message: error.message
    }
  }
}

// Helper function to generate export file
const generateExportFile = async (report, format) => {
  try {
    // Simulate file generation
    const fileName = `${report.title.replace(/[^a-zA-Z0-9]/g, '_')}_${Date.now()}.${format}`
    const filePath = path.join(process.cwd(), 'exports', fileName)
    const fileSize = Math.floor(Math.random() * 1000000) + 50000 // 50KB - 1MB

    // Ensure exports directory exists
    const exportsDir = path.join(process.cwd(), 'exports')
    if (!fs.existsSync(exportsDir)) {
      fs.mkdirSync(exportsDir, { recursive: true })
    }

    // Create a dummy file for demonstration
    fs.writeFileSync(filePath, JSON.stringify({
      report_id: report.id,
      title: report.title,
      generated_at: new Date().toISOString(),
      format: format,
      data: report.data ? JSON.parse(report.data) : null
    }))

    return {
      file_path: filePath,
      file_size: fileSize,
      file_name: fileName
    }
  } catch (error) {
    console.error('Generate export file error:', error)
    throw error
  }
}

// Helper function to send report email
const sendReportEmail = async (report, exportResult, emailTo) => {
  try {
    // Simulate email sending
    console.log(`Sending report email to: ${emailTo}`)
    console.log(`Report: ${report.title}`)
    console.log(`File: ${exportResult.file_name}`)
    
    return {
      success: true,
      message: 'Email sent successfully',
      recipients: emailTo
    }
  } catch (error) {
    console.error('Send report email error:', error)
    throw error
  }
}

// Helper function to validate schedule configuration
const validateScheduleConfig = (scheduleType, scheduleConfig, nextRun) => {
  const errors = []
  
  if (!scheduleType) {
    errors.push('Schedule type is required')
  }
  
  if (!nextRun) {
    errors.push('Next run date is required')
  }
  
  if (scheduleType === 'weekly' && (!scheduleConfig || !scheduleConfig.day_of_week)) {
    errors.push('Day of week is required for weekly schedule')
  }
  
  if (scheduleType === 'monthly' && (!scheduleConfig || !scheduleConfig.day_of_month)) {
    errors.push('Day of month is required for monthly schedule')
  }
  
  return {
    valid: errors.length === 0,
    errors
  }
}

module.exports = {
  getReportTemplates,
  generateReport,
  getReport,
  exportReport,
  scheduleReport,
  getScheduledReports,
  cancelScheduledReport
}
