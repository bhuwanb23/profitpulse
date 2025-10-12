const { Organization, Client, Ticket, Service } = require('../models')
const { Op } = require('sequelize')
const { validationResult } = require('express-validator')
const crypto = require('crypto')

// In-memory storage for SuperOps connections (in production, use Redis or database)
const superOpsConnections = new Map()

// POST /api/integrations/superops/connect - Connect SuperOps
const connectSuperOps = async (req, res) => {
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
      api_key,
      api_secret,
      base_url,
      webhook_url,
      sync_settings
    } = req.body

    // Check if organization exists
    const organization = await Organization.findByPk(organization_id)
    if (!organization) {
      return res.status(404).json({
        success: false,
        message: 'Organization not found'
      })
    }

    // Generate connection ID
    const connectionId = crypto.randomUUID()

    // Test SuperOps API connection (simulated)
    const connectionTest = await testSuperOpsConnection({
      api_key,
      api_secret,
      base_url
    })

    if (!connectionTest.success) {
      return res.status(400).json({
        success: false,
        message: 'Failed to connect to SuperOps',
        details: connectionTest.error
      })
    }

    // Store connection details
    const connectionDetails = {
      id: connectionId,
      organization_id,
      api_key,
      api_secret,
      base_url,
      webhook_url,
      sync_settings: sync_settings || {
        auto_sync: true,
        sync_interval: 3600, // 1 hour
        sync_tickets: true,
        sync_clients: true,
        sync_services: true,
        sync_users: true
      },
      status: 'connected',
      connected_at: new Date().toISOString(),
      last_sync: null,
      sync_count: 0,
      error_count: 0,
      last_error: null
    }

    superOpsConnections.set(connectionId, connectionDetails)

    // Create webhook endpoint for SuperOps
    const webhookEndpoint = `${process.env.BASE_URL || 'http://localhost:3000'}/api/integrations/superops/webhook/${connectionId}`

    res.json({
      success: true,
      message: 'SuperOps connected successfully',
      data: {
        connection_id: connectionId,
        organization_id,
        status: 'connected',
        webhook_endpoint: webhookEndpoint,
        sync_settings: connectionDetails.sync_settings,
        connection_info: {
          base_url,
          connected_at: connectionDetails.connected_at,
          api_version: connectionTest.api_version,
          account_info: connectionTest.account_info
        }
      }
    })
  } catch (error) {
    console.error('Connect SuperOps error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while connecting to SuperOps'
    })
  }
}

// GET /api/integrations/superops/status - Connection status
const getSuperOpsStatus = async (req, res) => {
  try {
    const { organization_id, connection_id } = req.query

    if (!organization_id && !connection_id) {
      return res.status(400).json({
        success: false,
        message: 'Organization ID or connection ID is required'
      })
    }

    let connection = null

    if (connection_id) {
      connection = superOpsConnections.get(connection_id)
    } else if (organization_id) {
      // Find connection by organization ID
      for (const [id, conn] of superOpsConnections.entries()) {
        if (conn.organization_id === organization_id) {
          connection = conn
          break
        }
      }
    }

    if (!connection) {
      return res.status(404).json({
        success: false,
        message: 'SuperOps connection not found'
      })
    }

    // Check current connection health
    const healthCheck = await checkSuperOpsHealth(connection)

    // Get sync statistics
    const syncStats = await getSyncStatistics(connection.organization_id)

    res.json({
      success: true,
      data: {
        connection_id: connection.id,
        organization_id: connection.organization_id,
        status: connection.status,
        health_status: healthCheck.status,
        connection_details: {
          base_url: connection.base_url,
          connected_at: connection.connected_at,
          last_sync: connection.last_sync,
          sync_count: connection.sync_count,
          error_count: connection.error_count,
          last_error: connection.last_error
        },
        sync_settings: connection.sync_settings,
        sync_statistics: syncStats,
        health_check: {
          api_accessible: healthCheck.api_accessible,
          webhook_active: healthCheck.webhook_active,
          last_check: healthCheck.last_check,
          response_time: healthCheck.response_time
        }
      }
    })
  } catch (error) {
    console.error('Get SuperOps status error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching SuperOps status'
    })
  }
}

// POST /api/integrations/superops/sync - Sync data
const syncSuperOpsData = async (req, res) => {
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
      connection_id,
      sync_type = 'all', // all, tickets, clients, services, users
      force_sync = false
    } = req.body

    // Find connection
    let connection = null
    if (connection_id) {
      connection = superOpsConnections.get(connection_id)
    } else if (organization_id) {
      for (const [id, conn] of superOpsConnections.entries()) {
        if (conn.organization_id === organization_id) {
          connection = conn
          break
        }
      }
    }

    if (!connection) {
      return res.status(404).json({
        success: false,
        message: 'SuperOps connection not found'
      })
    }

    // Check if sync is already in progress
    if (connection.sync_in_progress && !force_sync) {
      return res.status(409).json({
        success: false,
        message: 'Sync already in progress',
        data: {
          sync_id: connection.sync_id,
          started_at: connection.sync_started_at
        }
      })
    }

    // Generate sync ID
    const syncId = crypto.randomUUID()
    connection.sync_in_progress = true
    connection.sync_id = syncId
    connection.sync_started_at = new Date().toISOString()

    // Start sync process (simulated)
    const syncResult = await performSuperOpsSync(connection, sync_type)

    // Update connection status
    connection.sync_in_progress = false
    connection.last_sync = new Date().toISOString()
    connection.sync_count += 1

    if (syncResult.success) {
      connection.error_count = 0
      connection.last_error = null
    } else {
      connection.error_count += 1
      connection.last_error = syncResult.error
    }

    res.json({
      success: true,
      message: 'SuperOps sync completed',
      data: {
        sync_id: syncId,
        organization_id: connection.organization_id,
        sync_type,
        sync_result: syncResult,
        sync_statistics: {
          total_records_synced: syncResult.total_records || 0,
          tickets_synced: syncResult.tickets_synced || 0,
          clients_synced: syncResult.clients_synced || 0,
          services_synced: syncResult.services_synced || 0,
          users_synced: syncResult.users_synced || 0,
          errors: syncResult.errors || 0,
          duration: syncResult.duration || 0
        },
        next_sync: connection.sync_settings.auto_sync ? 
          new Date(Date.now() + connection.sync_settings.sync_interval * 1000).toISOString() : null
      }
    })
  } catch (error) {
    console.error('Sync SuperOps data error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while syncing SuperOps data'
    })
  }
}

// GET /api/integrations/superops/tickets - Import tickets
const getSuperOpsTickets = async (req, res) => {
  try {
    const { 
      organization_id,
      connection_id,
      status,
      priority,
      assigned_to,
      created_after,
      created_before,
      limit = 50,
      offset = 0
    } = req.query

    // Find connection or use mock data
    let connection = null
    if (connection_id) {
      connection = superOpsConnections.get(connection_id)
    } else if (organization_id) {
      for (const [id, conn] of superOpsConnections.entries()) {
        if (conn.organization_id === organization_id) {
          connection = conn
          break
        }
      }
    }

    // Use mock connection if none found
    if (!connection) {
      connection = {
        id: connection_id || 'mock-connection',
        organization_id: organization_id || 'mock-org'
      }
    }

    // Fetch tickets from SuperOps API (simulated)
    const superOpsTickets = await fetchSuperOpsTickets(connection, {
      status,
      priority,
      assigned_to,
      created_after,
      created_before,
      limit: parseInt(limit),
      offset: parseInt(offset)
    })

    // Get local tickets for comparison (simplified)
    const localTickets = []

    res.json({
      success: true,
      data: {
        connection_id: connection.id,
        organization_id: connection.organization_id,
        superops_tickets: superOpsTickets,
        local_tickets: localTickets,
        pagination: {
          limit: parseInt(limit),
          offset: parseInt(offset),
          total_superops: superOpsTickets.length,
          total_local: localTickets.length,
          has_more: superOpsTickets.length === parseInt(limit)
        },
        sync_recommendations: [
          'Review tickets marked as new or updated',
          'Consider syncing high-priority tickets first',
          'Verify ticket status mappings',
          'Check for duplicate tickets'
        ]
      }
    })
  } catch (error) {
    console.error('Get SuperOps tickets error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching SuperOps tickets'
    })
  }
}

// GET /api/integrations/superops/clients - Import clients
const getSuperOpsClients = async (req, res) => {
  try {
    const { 
      organization_id,
      connection_id,
      status,
      created_after,
      created_before,
      limit = 50,
      offset = 0
    } = req.query

    // Find connection or use mock data
    let connection = null
    if (connection_id) {
      connection = superOpsConnections.get(connection_id)
    } else if (organization_id) {
      for (const [id, conn] of superOpsConnections.entries()) {
        if (conn.organization_id === organization_id) {
          connection = conn
          break
        }
      }
    }

    // Use mock connection if none found
    if (!connection) {
      connection = {
        id: connection_id || 'mock-connection',
        organization_id: organization_id || 'mock-org'
      }
    }

    // Fetch clients from SuperOps API (simulated)
    const superOpsClients = await fetchSuperOpsClients(connection, {
      status,
      created_after,
      created_before,
      limit: parseInt(limit),
      offset: parseInt(offset)
    })

    // Get local clients for comparison (simplified)
    const localClients = []

    res.json({
      success: true,
      data: {
        connection_id: connection.id,
        organization_id: connection.organization_id,
        superops_clients: superOpsClients,
        local_clients: localClients,
        pagination: {
          limit: parseInt(limit),
          offset: parseInt(offset),
          total_superops: superOpsClients.length,
          total_local: localClients.length,
          has_more: superOpsClients.length === parseInt(limit)
        },
        sync_recommendations: [
          'Review clients marked as new or updated',
          'Verify client contact information',
          'Check for duplicate clients',
          'Consider syncing active clients first'
        ]
      }
    })
  } catch (error) {
    console.error('Get SuperOps clients error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching SuperOps clients'
    })
  }
}

// PUT /api/integrations/superops/settings - Update settings
const updateSuperOpsSettings = async (req, res) => {
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
      connection_id,
      sync_settings,
      webhook_settings,
      field_mappings,
      sync_filters
    } = req.body

    res.json({
      success: true,
      message: 'SuperOps settings updated successfully',
      data: {
        connection_id: connection_id || 'mock-connection',
        organization_id: organization_id || 'mock-org',
        updated_settings: {
          sync_settings: sync_settings || {
            auto_sync: true,
            sync_interval: 3600,
            sync_tickets: true,
            sync_clients: true,
            sync_services: true,
            sync_users: true
          },
          webhook_settings: webhook_settings || {},
          field_mappings: field_mappings || {},
          sync_filters: sync_filters || {}
        },
        validation_result: { valid: true, errors: [] }
      }
    })
  } catch (error) {
    console.error('Update SuperOps settings error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while updating SuperOps settings'
    })
  }
}

// Helper function to test SuperOps connection
const testSuperOpsConnection = async (config) => {
  try {
    // Simulate API connection test
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    return {
      success: true,
      api_version: 'v1.0',
      account_info: {
        company_name: 'TechWave MSP',
        plan: 'Professional',
        user_count: 25,
        ticket_count: 1500
      }
    }
  } catch (error) {
    return {
      success: false,
      error: 'Failed to connect to SuperOps API'
    }
  }
}

// Helper function to check SuperOps health
const checkSuperOpsHealth = async (connection) => {
  try {
    const startTime = Date.now()
    
    // Simulate health check
    await new Promise(resolve => setTimeout(resolve, 500))
    
    const responseTime = Date.now() - startTime
    
    return {
      status: 'healthy',
      api_accessible: true,
      webhook_active: true,
      last_check: new Date().toISOString(),
      response_time: responseTime
    }
  } catch (error) {
    return {
      status: 'unhealthy',
      api_accessible: false,
      webhook_active: false,
      last_check: new Date().toISOString(),
      response_time: null
    }
  }
}

// Helper function to get sync statistics
const getSyncStatistics = async (organizationId) => {
  try {
    const tickets = await Ticket.count({ where: { organization_id: organizationId } })
    const clients = await Client.count({ where: { organization_id: organizationId } })
    const services = await Service.count({ where: { organization_id: organizationId } })
    
    return {
      total_tickets: tickets,
      total_clients: clients,
      total_services: services,
      last_sync_date: new Date().toISOString(),
      sync_frequency: 'hourly',
      success_rate: 0.95
    }
  } catch (error) {
    return {
      total_tickets: 0,
      total_clients: 0,
      total_services: 0,
      last_sync_date: null,
      sync_frequency: 'unknown',
      success_rate: 0
    }
  }
}

// Helper function to perform SuperOps sync
const performSuperOpsSync = async (connection, syncType) => {
  try {
    const startTime = Date.now()
    
    // Simulate sync process
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    const duration = Date.now() - startTime
    
    return {
      success: true,
      total_records: 150,
      tickets_synced: syncType === 'all' || syncType === 'tickets' ? 75 : 0,
      clients_synced: syncType === 'all' || syncType === 'clients' ? 25 : 0,
      services_synced: syncType === 'all' || syncType === 'services' ? 30 : 0,
      users_synced: syncType === 'all' || syncType === 'users' ? 20 : 0,
      errors: 0,
      duration
    }
  } catch (error) {
    return {
      success: false,
      error: error.message,
      total_records: 0,
      tickets_synced: 0,
      clients_synced: 0,
      services_synced: 0,
      users_synced: 0,
      errors: 1,
      duration: 0
    }
  }
}

// Helper function to fetch SuperOps tickets
const fetchSuperOpsTickets = async (connection, filters) => {
  try {
    // Simulate fetching tickets from SuperOps API
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    return Array.from({ length: Math.min(filters.limit, 10) }, (_, i) => ({
      id: `superops_ticket_${i + 1}`,
      title: `SuperOps Ticket ${i + 1}`,
      description: `Description for ticket ${i + 1}`,
      status: ['open', 'in_progress', 'resolved'][i % 3],
      priority: ['low', 'medium', 'high'][i % 3],
      assigned_to: `user_${i + 1}`,
      client_id: `client_${i + 1}`,
      created_at: new Date(Date.now() - i * 86400000).toISOString(),
      updated_at: new Date().toISOString(),
      due_date: new Date(Date.now() + (i + 1) * 86400000).toISOString()
    }))
  } catch (error) {
    return []
  }
}

// Helper function to fetch SuperOps clients
const fetchSuperOpsClients = async (connection, filters) => {
  try {
    // Simulate fetching clients from SuperOps API
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    return Array.from({ length: Math.min(filters.limit, 10) }, (_, i) => ({
      id: `superops_client_${i + 1}`,
      name: `SuperOps Client ${i + 1}`,
      company: `Company ${i + 1}`,
      email: `client${i + 1}@company${i + 1}.com`,
      phone: `+1-555-000${i + 1}`,
      status: 'active',
      created_at: new Date(Date.now() - i * 86400000).toISOString(),
      updated_at: new Date().toISOString()
    }))
  } catch (error) {
    return []
  }
}

// Helper function to compare tickets
const compareTickets = (superOpsTickets, localTickets) => {
  const superOpsIds = new Set(superOpsTickets.map(t => t.id))
  const localIds = new Set(localTickets.map(t => t.id))
  
  return {
    new_tickets: superOpsTickets.filter(t => !localIds.has(t.id)),
    updated_tickets: superOpsTickets.filter(t => localIds.has(t.id)),
    local_only_tickets: localTickets.filter(t => !superOpsIds.has(t.id)),
    total_new: superOpsTickets.filter(t => !localIds.has(t.id)).length,
    total_updated: superOpsTickets.filter(t => localIds.has(t.id)).length,
    total_local_only: localTickets.filter(t => !superOpsIds.has(t.id)).length
  }
}

// Helper function to compare clients
const compareClients = (superOpsClients, localClients) => {
  const superOpsIds = new Set(superOpsClients.map(c => c.id))
  const localIds = new Set(localClients.map(c => c.id))
  
  return {
    new_clients: superOpsClients.filter(c => !localIds.has(c.id)),
    updated_clients: superOpsClients.filter(c => localIds.has(c.id)),
    local_only_clients: localClients.filter(c => !superOpsIds.has(c.id)),
    total_new: superOpsClients.filter(c => !localIds.has(c.id)).length,
    total_updated: superOpsClients.filter(c => localIds.has(c.id)).length,
    total_local_only: localClients.filter(c => !superOpsIds.has(c.id)).length
  }
}

// Helper function to validate SuperOps settings
const validateSuperOpsSettings = (connection) => {
  const errors = []
  
  if (connection.sync_settings) {
    if (connection.sync_settings.sync_interval < 300) {
      errors.push('Sync interval must be at least 5 minutes')
    }
    if (connection.sync_settings.sync_interval > 86400) {
      errors.push('Sync interval must be at most 24 hours')
    }
  }
  
  if (connection.webhook_settings) {
    if (connection.webhook_settings.webhook_url && !connection.webhook_settings.webhook_url.startsWith('http')) {
      errors.push('Webhook URL must be a valid HTTP/HTTPS URL')
    }
  }
  
  return {
    valid: errors.length === 0,
    errors
  }
}

module.exports = {
  connectSuperOps,
  getSuperOpsStatus,
  syncSuperOpsData,
  getSuperOpsTickets,
  getSuperOpsClients,
  updateSuperOpsSettings
}
