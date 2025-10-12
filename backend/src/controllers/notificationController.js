const { Notification, NotificationPreference, EmailSettings, Organization, User } = require('../models')
const { Op } = require('sequelize')
const { validationResult } = require('express-validator')
const crypto = require('crypto')

// GET /api/notifications - List notifications
const getNotifications = async (req, res) => {
  try {
    const { 
      organization_id,
      user_id,
      type,
      category,
      is_read,
      priority,
      limit = 50,
      offset = 0
    } = req.query

    const whereClause = {}
    
    if (organization_id) {
      whereClause.organization_id = organization_id
    }
    if (user_id) {
      whereClause.user_id = user_id
    }
    if (type) {
      whereClause.type = type
    }
    if (category) {
      whereClause.category = category
    }
    if (is_read !== undefined) {
      whereClause.is_read = is_read === 'true'
    }
    if (priority) {
      whereClause.priority = priority
    }

    // Mock data for demonstration
    const notifications = [
      {
        id: 'notif-1',
        organization_id: organization_id || 'f4e806f0-8201-43d3-a80b-ca3bd051497b',
        user_id: user_id || 'user-1',
        type: 'warning',
        category: 'ticket',
        title: 'High Priority Ticket Assigned',
        message: 'You have been assigned a high priority ticket #1234 that requires immediate attention.',
        data: JSON.stringify({ ticket_id: '1234', priority: 'high' }),
        is_read: false,
        read_at: null,
        priority: 'high',
        expires_at: null,
        action_url: '/tickets/1234',
        action_text: 'View Ticket',
        source: 'ticket_system',
        source_id: '1234',
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
        organization: { id: organization_id || 'f4e806f0-8201-43d3-a80b-ca3bd051497b', name: 'TechWave MSP' },
        user: { id: user_id || 'user-1', firstName: 'Admin', lastName: 'User', email: 'admin@techwave.com' }
      },
      {
        id: 'notif-2',
        organization_id: organization_id || 'f4e806f0-8201-43d3-a80b-ca3bd051497b',
        user_id: user_id || 'user-1',
        type: 'info',
        category: 'invoice',
        title: 'Invoice Generated',
        message: 'Invoice #INV-2024-001 has been generated and is ready for review.',
        data: JSON.stringify({ invoice_id: 'INV-2024-001', amount: 2500.00 }),
        is_read: true,
        read_at: new Date(Date.now() - 3600000).toISOString(),
        priority: 'medium',
        expires_at: null,
        action_url: '/invoices/INV-2024-001',
        action_text: 'View Invoice',
        source: 'invoice_system',
        source_id: 'INV-2024-001',
        createdAt: new Date(Date.now() - 7200000).toISOString(),
        updatedAt: new Date(Date.now() - 3600000).toISOString(),
        organization: { id: organization_id || 'f4e806f0-8201-43d3-a80b-ca3bd051497b', name: 'TechWave MSP' },
        user: { id: user_id || 'user-1', firstName: 'Admin', lastName: 'User', email: 'admin@techwave.com' }
      },
      {
        id: 'notif-3',
        organization_id: organization_id || 'f4e806f0-8201-43d3-a80b-ca3bd051497b',
        user_id: user_id || 'user-1',
        type: 'alert',
        category: 'budget',
        title: 'Budget Alert',
        message: 'Monthly budget for IT Infrastructure has reached 85% of the allocated amount.',
        data: JSON.stringify({ budget_id: 'budget-1', category: 'IT Infrastructure', usage: 85 }),
        is_read: false,
        read_at: null,
        priority: 'urgent',
        expires_at: new Date(Date.now() + 86400000).toISOString(),
        action_url: '/budgets/budget-1',
        action_text: 'View Budget',
        source: 'budget_system',
        source_id: 'budget-1',
        createdAt: new Date(Date.now() - 1800000).toISOString(),
        updatedAt: new Date(Date.now() - 1800000).toISOString(),
        organization: { id: organization_id || 'f4e806f0-8201-43d3-a80b-ca3bd051497b', name: 'TechWave MSP' },
        user: { id: user_id || 'user-1', firstName: 'Admin', lastName: 'User', email: 'admin@techwave.com' }
      }
    ]

    const count = notifications.length

    res.json({
      success: true,
      data: {
        notifications,
        pagination: {
          total: count,
          limit: parseInt(limit),
          offset: parseInt(offset),
          pages: Math.ceil(count / parseInt(limit))
        },
        summary: {
          total: count,
          unread: notifications.filter(n => !n.is_read).length,
          by_type: {
            info: notifications.filter(n => n.type === 'info').length,
            warning: notifications.filter(n => n.type === 'warning').length,
            error: notifications.filter(n => n.type === 'error').length,
            success: notifications.filter(n => n.type === 'success').length,
            alert: notifications.filter(n => n.type === 'alert').length
          },
          by_priority: {
            low: notifications.filter(n => n.priority === 'low').length,
            medium: notifications.filter(n => n.priority === 'medium').length,
            high: notifications.filter(n => n.priority === 'high').length,
            urgent: notifications.filter(n => n.priority === 'urgent').length
          }
        }
      }
    })
  } catch (error) {
    console.error('Get notifications error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching notifications'
    })
  }
}

// PUT /api/notifications/:id/read - Mark as read
const markNotificationAsRead = async (req, res) => {
  try {
    const { id } = req.params

    // Mock notification update
    const notification = {
      id: id,
      title: 'High Priority Ticket Assigned',
      message: 'You have been assigned a high priority ticket #1234 that requires immediate attention.',
      is_read: true,
      read_at: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    }

    res.json({
      success: true,
      message: 'Notification marked as read',
      data: {
        notification_id: notification.id,
        title: notification.title,
        is_read: notification.is_read,
        read_at: notification.read_at,
        updated_at: notification.updatedAt
      }
    })
  } catch (error) {
    console.error('Mark notification as read error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while marking notification as read'
    })
  }
}

// POST /api/notifications/preferences - Update preferences
const updateNotificationPreferences = async (req, res) => {
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
      user_id,
      preferences
    } = req.body

    // Mock preferences update
    const updatedPreferences = preferences.map(pref => ({
      id: crypto.randomUUID(),
      organization_id,
      user_id,
      category: pref.category,
      type: pref.type,
      enabled: pref.enabled,
      email_enabled: pref.email_enabled,
      push_enabled: pref.push_enabled,
      sms_enabled: pref.sms_enabled,
      webhook_enabled: pref.webhook_enabled,
      webhook_url: pref.webhook_url,
      frequency: pref.frequency,
      quiet_hours_start: pref.quiet_hours_start,
      quiet_hours_end: pref.quiet_hours_end,
      timezone: pref.timezone,
      updatedAt: new Date().toISOString()
    }))

    res.json({
      success: true,
      message: 'Notification preferences updated successfully',
      data: {
        organization_id,
        user_id,
        preferences: updatedPreferences,
        updated_at: new Date().toISOString()
      }
    })
  } catch (error) {
    console.error('Update notification preferences error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while updating notification preferences'
    })
  }
}

// GET /api/notifications/email-settings - Email settings
const getEmailSettings = async (req, res) => {
  try {
    const { organization_id } = req.query

    // Mock email settings
    const emailSettings = {
      id: 'email-settings-1',
      organization_id: organization_id || 'f4e806f0-8201-43d3-a80b-ca3bd051497b',
      smtp_host: 'smtp.gmail.com',
      smtp_port: 587,
      smtp_secure: true,
      smtp_username: 'notifications@techwave.com',
      smtp_password: 'encrypted_password',
      from_email: 'notifications@techwave.com',
      from_name: 'TechWave MSP Notifications',
      reply_to_email: 'support@techwave.com',
      reply_to_name: 'TechWave Support',
      is_active: true,
      test_email: 'admin@techwave.com',
      last_test_at: new Date(Date.now() - 86400000).toISOString(),
      last_test_status: 'success',
      last_test_error: null,
      daily_limit: 1000,
      hourly_limit: 100,
      template_settings: JSON.stringify({
        header_color: '#2563eb',
        footer_text: 'TechWave MSP - Your Trusted IT Partner',
        logo_url: 'https://techwave.com/logo.png'
      }),
      createdAt: new Date(Date.now() - 2592000000).toISOString(),
      updatedAt: new Date(Date.now() - 86400000).toISOString(),
      organization: { id: organization_id || 'f4e806f0-8201-43d3-a80b-ca3bd051497b', name: 'TechWave MSP' }
    }

    res.json({
      success: true,
      data: emailSettings
    })
  } catch (error) {
    console.error('Get email settings error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching email settings'
    })
  }
}

// PUT /api/notifications/email-settings - Update email settings
const updateEmailSettings = async (req, res) => {
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
      smtp_host,
      smtp_port,
      smtp_secure,
      smtp_username,
      smtp_password,
      from_email,
      from_name,
      reply_to_email,
      reply_to_name,
      is_active,
      daily_limit,
      hourly_limit,
      template_settings
    } = req.body

    // Mock email settings update
    const updatedSettings = {
      id: 'email-settings-1',
      organization_id,
      smtp_host,
      smtp_port,
      smtp_secure,
      smtp_username,
      smtp_password: smtp_password ? 'encrypted_password' : undefined,
      from_email,
      from_name,
      reply_to_email,
      reply_to_name,
      is_active,
      daily_limit,
      hourly_limit,
      template_settings: template_settings ? JSON.stringify(template_settings) : null,
      updatedAt: new Date().toISOString()
    }

    res.json({
      success: true,
      message: 'Email settings updated successfully',
      data: updatedSettings
    })
  } catch (error) {
    console.error('Update email settings error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while updating email settings'
    })
  }
}

// GET /api/notifications/alerts - Dashboard alerts
const getDashboardAlerts = async (req, res) => {
  try {
    const { organization_id, user_id } = req.query

    // Mock dashboard alerts
    const alerts = [
      {
        id: 'alert-1',
        type: 'warning',
        category: 'system',
        title: 'High CPU Usage',
        message: 'Server CPU usage is at 85% for the past 30 minutes',
        priority: 'high',
        is_read: false,
        created_at: new Date(Date.now() - 1800000).toISOString(),
        action_url: '/monitoring/servers',
        action_text: 'View Monitoring',
        source: 'monitoring_system',
        source_id: 'server-1'
      },
      {
        id: 'alert-2',
        type: 'error',
        category: 'integration',
        title: 'API Connection Failed',
        message: 'Failed to connect to QuickBooks API. Please check credentials.',
        priority: 'urgent',
        is_read: false,
        created_at: new Date(Date.now() - 3600000).toISOString(),
        action_url: '/integrations/quickbooks',
        action_text: 'Check Integration',
        source: 'integration_system',
        source_id: 'quickbooks'
      },
      {
        id: 'alert-3',
        type: 'info',
        category: 'ai',
        title: 'AI Analysis Complete',
        message: 'Monthly profitability analysis has been completed. New insights available.',
        priority: 'medium',
        is_read: true,
        created_at: new Date(Date.now() - 7200000).toISOString(),
        action_url: '/ai/insights',
        action_text: 'View Insights',
        source: 'ai_system',
        source_id: 'analysis-123'
      }
    ]

    res.json({
      success: true,
      data: {
        alerts,
        summary: {
          total: alerts.length,
          unread: alerts.filter(a => !a.is_read).length,
          by_priority: {
            low: alerts.filter(a => a.priority === 'low').length,
            medium: alerts.filter(a => a.priority === 'medium').length,
            high: alerts.filter(a => a.priority === 'high').length,
            urgent: alerts.filter(a => a.priority === 'urgent').length
          },
          by_type: {
            info: alerts.filter(a => a.type === 'info').length,
            warning: alerts.filter(a => a.type === 'warning').length,
            error: alerts.filter(a => a.type === 'error').length,
            success: alerts.filter(a => a.type === 'success').length,
            alert: alerts.filter(a => a.type === 'alert').length
          }
        }
      }
    })
  } catch (error) {
    console.error('Get dashboard alerts error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching dashboard alerts'
    })
  }
}

// POST /api/notifications/test - Test notification
const testNotification = async (req, res) => {
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
      user_id,
      type = 'info',
      category = 'system',
      title,
      message,
      test_email,
      test_phone
    } = req.body

    // Mock notification test
    const testResult = {
      notification_id: crypto.randomUUID(),
      organization_id,
      user_id,
      type,
      category,
      title: title || 'Test Notification',
      message: message || 'This is a test notification to verify your notification settings.',
      test_email: test_email,
      test_phone: test_phone,
      sent_at: new Date().toISOString(),
      delivery_status: {
        email: test_email ? 'sent' : 'skipped',
        sms: test_phone ? 'sent' : 'skipped',
        push: 'sent',
        webhook: 'sent'
      },
      delivery_details: {
        email: test_email ? {
          recipient: test_email,
          subject: 'Test Notification - TechWave MSP',
          status: 'delivered',
          message_id: 'test-msg-123'
        } : null,
        sms: test_phone ? {
          recipient: test_phone,
          status: 'delivered',
          message_id: 'test-sms-123'
        } : null,
        push: {
          status: 'delivered',
          device_count: 1
        },
        webhook: {
          status: 'delivered',
          url: 'https://webhook.site/12345678',
          response_code: 200
        }
      }
    }

    res.json({
      success: true,
      message: 'Test notification sent successfully',
      data: testResult
    })
  } catch (error) {
    console.error('Test notification error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while sending test notification'
    })
  }
}

module.exports = {
  getNotifications,
  markNotificationAsRead,
  updateNotificationPreferences,
  getEmailSettings,
  updateEmailSettings,
  getDashboardAlerts,
  testNotification
}
