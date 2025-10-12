const { Ticket, Client, User, Organization } = require('../models')
const { Op } = require('sequelize')
const { validationResult } = require('express-validator')

// POST /api/tickets/bulk - Bulk ticket operations
const bulkTicketOperations = async (req, res) => {
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
      operation, // 'create', 'update', 'delete', 'assign', 'status_change'
      tickets,
      filters,
      updates
    } = req.body

    let results = {
      success: [],
      failed: [],
      total_processed: 0,
      total_success: 0,
      total_failed: 0
    }

    switch (operation) {
      case 'create':
        // Bulk create tickets
        for (const ticketData of tickets) {
          try {
            const ticketNumber = `TKT-${Date.now()}-${Math.random().toString(36).substr(2, 4).toUpperCase()}`
            const ticket = await Ticket.create({
              ...ticketData,
              ticket_number: ticketNumber
            })
            results.success.push({
              id: ticket.id,
              ticket_number: ticket.ticket_number,
              title: ticket.title
            })
            results.total_success++
          } catch (error) {
            results.failed.push({
              data: ticketData,
              error: error.message
            })
            results.total_failed++
          }
          results.total_processed++
        }
        break

      case 'update':
        // Bulk update tickets
        for (const updateData of tickets) {
          try {
            const { id, ...updateFields } = updateData
            const ticket = await Ticket.findByPk(id)
            if (!ticket) {
              results.failed.push({
                id,
                error: 'Ticket not found'
              })
              results.total_failed++
            } else {
              await ticket.update(updateFields)
              results.success.push({
                id: ticket.id,
                ticket_number: ticket.ticket_number,
                title: ticket.title
              })
              results.total_success++
            }
          } catch (error) {
            results.failed.push({
              id: updateData.id,
              error: error.message
            })
            results.total_failed++
          }
          results.total_processed++
        }
        break

      case 'delete':
        // Bulk delete tickets
        for (const ticketId of tickets) {
          try {
            const ticket = await Ticket.findByPk(ticketId)
            if (!ticket) {
              results.failed.push({
                id: ticketId,
                error: 'Ticket not found'
              })
              results.total_failed++
            } else {
              await ticket.destroy()
              results.success.push({
                id: ticketId,
                ticket_number: ticket.ticket_number,
                title: ticket.title
              })
              results.total_success++
            }
          } catch (error) {
            results.failed.push({
              id: ticketId,
              error: error.message
            })
            results.total_failed++
          }
          results.total_processed++
        }
        break

      case 'assign':
        // Bulk assign tickets
        for (const assignment of tickets) {
          try {
            const { ticket_id, assigned_to } = assignment
            const ticket = await Ticket.findByPk(ticket_id)
            if (!ticket) {
              results.failed.push({
                ticket_id,
                error: 'Ticket not found'
              })
              results.total_failed++
            } else {
              await ticket.update({ assigned_to })
              results.success.push({
                id: ticket.id,
                ticket_number: ticket.ticket_number,
                assigned_to
              })
              results.total_success++
            }
          } catch (error) {
            results.failed.push({
              ticket_id: assignment.ticket_id,
              error: error.message
            })
            results.total_failed++
          }
          results.total_processed++
        }
        break

      case 'status_change':
        // Bulk status change
        for (const statusChange of tickets) {
          try {
            const { ticket_id, status, resolution_notes } = statusChange
            const ticket = await Ticket.findByPk(ticket_id)
            if (!ticket) {
              results.failed.push({
                ticket_id,
                error: 'Ticket not found'
              })
              results.total_failed++
            } else {
              const updateData = { status }
              if (resolution_notes) updateData.resolution_notes = resolution_notes
              if (status === 'resolved' || status === 'closed') {
                updateData.resolved_at = new Date()
              }
              await ticket.update(updateData)
              results.success.push({
                id: ticket.id,
                ticket_number: ticket.ticket_number,
                status
              })
              results.total_success++
            }
          } catch (error) {
            results.failed.push({
              ticket_id: statusChange.ticket_id,
              error: error.message
            })
            results.total_failed++
          }
          results.total_processed++
        }
        break

      default:
        return res.status(400).json({
          success: false,
          message: 'Invalid operation. Supported operations: create, update, delete, assign, status_change'
        })
    }

    res.json({
      success: true,
      message: `Bulk ${operation} operation completed`,
      data: results
    })
  } catch (error) {
    console.error('Bulk ticket operations error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while performing bulk operations'
    })
  }
}

// GET /api/tickets/templates - Ticket templates
const getTicketTemplates = async (req, res) => {
  try {
    const { 
      organization_id,
      category,
      search
    } = req.query

    // In a real application, you would have a TicketTemplate model
    // For now, we'll return predefined templates
    const templates = [
      {
        id: 'template-1',
        name: 'Server Performance Issue',
        category: 'Performance',
        description: 'Template for server performance related tickets',
        priority: 'high',
        estimated_hours: 4,
        template_fields: {
          title: 'Server Performance Issue - {server_name}',
          description: 'Client reporting slow server response times affecting productivity.\n\nServer: {server_name}\nIssue: {issue_description}\nImpact: {impact_level}',
          category: 'Performance',
          priority: 'high',
          estimated_hours: 4
        },
        organization_id: organization_id || null,
        created_at: new Date(),
        updated_at: new Date()
      },
      {
        id: 'template-2',
        name: 'Network Connectivity',
        category: 'Network',
        description: 'Template for network connectivity issues',
        priority: 'medium',
        estimated_hours: 2,
        template_fields: {
          title: 'Network Connectivity Issue - {location}',
          description: 'Network connectivity problems reported.\n\nLocation: {location}\nDevices Affected: {device_count}\nSymptoms: {symptoms}',
          category: 'Network',
          priority: 'medium',
          estimated_hours: 2
        },
        organization_id: organization_id || null,
        created_at: new Date(),
        updated_at: new Date()
      },
      {
        id: 'template-3',
        name: 'Software Installation',
        category: 'Software',
        description: 'Template for software installation requests',
        priority: 'low',
        estimated_hours: 1,
        template_fields: {
          title: 'Software Installation Request - {software_name}',
          description: 'Request for software installation.\n\nSoftware: {software_name}\nVersion: {version}\nTarget Systems: {target_systems}',
          category: 'Software',
          priority: 'low',
          estimated_hours: 1
        },
        organization_id: organization_id || null,
        created_at: new Date(),
        updated_at: new Date()
      }
    ]

    // Filter templates based on query parameters
    let filteredTemplates = templates
    if (category) {
      filteredTemplates = filteredTemplates.filter(t => t.category.toLowerCase() === category.toLowerCase())
    }
    if (search) {
      filteredTemplates = filteredTemplates.filter(t => 
        t.name.toLowerCase().includes(search.toLowerCase()) ||
        t.description.toLowerCase().includes(search.toLowerCase())
      )
    }

    res.json({
      success: true,
      data: {
        templates: filteredTemplates,
        total: filteredTemplates.length
      }
    })
  } catch (error) {
    console.error('Get ticket templates error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching ticket templates'
    })
  }
}

// POST /api/tickets/templates - Create template
const createTicketTemplate = async (req, res) => {
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
      name,
      category,
      description,
      priority,
      estimated_hours,
      template_fields,
      organization_id
    } = req.body

    // In a real application, you would save this to a TicketTemplate model
    const template = {
      id: `template-${Date.now()}`,
      name,
      category,
      description,
      priority,
      estimated_hours,
      template_fields,
      organization_id,
      created_at: new Date(),
      updated_at: new Date()
    }

    res.status(201).json({
      success: true,
      message: 'Ticket template created successfully',
      data: { template }
    })
  } catch (error) {
    console.error('Create ticket template error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while creating ticket template'
    })
  }
}

// POST /api/tickets/:id/escalate - Escalate ticket
const escalateTicket = async (req, res) => {
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
    const { 
      escalation_reason,
      escalated_to,
      priority_increase = true,
      notify_stakeholders = true
    } = req.body

    const ticket = await Ticket.findByPk(id)
    if (!ticket) {
      return res.status(404).json({
        success: false,
        message: 'Ticket not found'
      })
    }

    // Check if ticket is already escalated
    if (ticket.priority === 'critical') {
      return res.status(400).json({
        success: false,
        message: 'Ticket is already at maximum priority level'
      })
    }

    // Determine new priority based on current priority
    const priorityLevels = {
      'low': 'medium',
      'medium': 'high',
      'high': 'urgent',
      'urgent': 'critical'
    }

    const newPriority = priorityLevels[ticket.priority] || 'high'
    
    // Update ticket with escalation
    const updateData = {
      priority: newPriority,
      escalated_at: new Date(),
      escalation_reason,
      escalated_to,
      last_activity: new Date()
    }

    await ticket.update(updateData)

    res.json({
      success: true,
      message: 'Ticket escalated successfully',
      data: {
        ticket: {
          id: ticket.id,
          ticket_number: ticket.ticket_number,
          title: ticket.title,
          priority: newPriority,
          escalated_at: updateData.escalated_at
        }
      }
    })
  } catch (error) {
    console.error('Escalate ticket error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while escalating ticket'
    })
  }
}

// GET /api/tickets/routing - Ticket routing rules
const getTicketRoutingRules = async (req, res) => {
  try {
    const { organization_id } = req.query

    // In a real application, you would have a TicketRoutingRule model
    // For now, we'll return predefined routing rules
    const routingRules = [
      {
        id: 'rule-1',
        name: 'Critical Priority Auto-Assignment',
        description: 'Automatically assign critical priority tickets to senior technicians',
        conditions: {
          priority: 'critical',
          category: { $in: ['Performance', 'Security', 'Network'] }
        },
        actions: {
          assign_to_role: 'senior_technician',
          set_priority: 'critical',
          notify_immediately: true
        },
        organization_id: organization_id || null,
        is_active: true,
        created_at: new Date(),
        updated_at: new Date()
      },
      {
        id: 'rule-2',
        name: 'Network Issues Routing',
        description: 'Route network-related tickets to network specialists',
        conditions: {
          category: 'Network',
          priority: { $in: ['high', 'urgent', 'critical'] }
        },
        actions: {
          assign_to_role: 'network_specialist',
          add_tags: ['network', 'connectivity'],
          set_sla_target: 4
        },
        organization_id: organization_id || null,
        is_active: true,
        created_at: new Date(),
        updated_at: new Date()
      },
      {
        id: 'rule-3',
        name: 'Software Installation Queue',
        description: 'Route software installation requests to software team',
        conditions: {
          category: 'Software',
          title: { $regex: 'installation|install|setup' }
        },
        actions: {
          assign_to_role: 'software_technician',
          set_priority: 'low',
          add_tags: ['software', 'installation']
        },
        organization_id: organization_id || null,
        is_active: true,
        created_at: new Date(),
        updated_at: new Date()
      },
      {
        id: 'rule-4',
        name: 'Client-Specific Routing',
        description: 'Route tickets from specific clients to dedicated technicians',
        conditions: {
          client_id: { $in: ['vip-client-1', 'vip-client-2'] }
        },
        actions: {
          assign_to_user: 'dedicated-technician-id',
          set_priority: 'high',
          notify_client: true
        },
        organization_id: organization_id || null,
        is_active: true,
        created_at: new Date(),
        updated_at: new Date()
      }
    ]

    res.json({
      success: true,
      data: {
        routing_rules: routingRules,
        total: routingRules.length,
        active_rules: routingRules.filter(rule => rule.is_active).length
      }
    })
  } catch (error) {
    console.error('Get ticket routing rules error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching routing rules'
    })
  }
}

// GET /api/tickets/sla-monitor - SLA monitoring
const getSLAMonitoring = async (req, res) => {
  try {
    const { 
      organization_id,
      period = '24h' // 1h, 6h, 24h, 7d
    } = req.query

    // Calculate time threshold based on period
    const now = new Date()
    let timeThreshold
    switch (period) {
      case '1h':
        timeThreshold = new Date(now.getTime() - (1 * 60 * 60 * 1000))
        break
      case '6h':
        timeThreshold = new Date(now.getTime() - (6 * 60 * 60 * 1000))
        break
      case '24h':
        timeThreshold = new Date(now.getTime() - (24 * 60 * 60 * 1000))
        break
      case '7d':
        timeThreshold = new Date(now.getTime() - (7 * 24 * 60 * 60 * 1000))
        break
      default:
        timeThreshold = new Date(now.getTime() - (24 * 60 * 60 * 1000))
    }

    // Build where clause
    const whereClause = {
      created_at: { [Op.gte]: timeThreshold },
      status: { [Op.in]: ['open', 'in_progress', 'pending'] }
    }
    if (organization_id) whereClause.organization_id = organization_id

    // Get tickets that are approaching or have breached SLA
    const tickets = await Ticket.findAll({
      where: whereClause,
      include: [
        {
          model: Organization,
          as: 'organization',
          attributes: ['id', 'name']
        },
        {
          model: Client,
          as: 'client',
          attributes: ['id', 'name', 'company']
        }
      ]
    })

    // Define SLA targets (in hours)
    const slaTargets = {
      critical: 4,
      urgent: 8,
      high: 24,
      medium: 72,
      low: 168
    }

    // Analyze SLA status for each ticket
    const slaAnalysis = tickets.map(ticket => {
      const created = new Date(ticket.created_at)
      const hoursElapsed = (now - created) / (1000 * 60 * 60)
      const slaTarget = slaTargets[ticket.priority] || slaTargets.medium
      const hoursRemaining = slaTarget - hoursElapsed
      const slaStatus = hoursRemaining <= 0 ? 'breached' : 
                       hoursRemaining <= (slaTarget * 0.2) ? 'critical' :
                       hoursRemaining <= (slaTarget * 0.5) ? 'warning' : 'ok'

      return {
        ticket_id: ticket.id,
        ticket_number: ticket.ticket_number,
        title: ticket.title,
        priority: ticket.priority,
        status: ticket.status,
        client_name: ticket.client ? ticket.client.name : 'Unknown',
        client_company: ticket.client ? ticket.client.company : 'Unknown',
        created_at: ticket.created_at,
        assigned_to: ticket.assigned_to,
        sla_target_hours: slaTarget,
        hours_elapsed: Math.round(hoursElapsed * 100) / 100,
        hours_remaining: Math.round(hoursRemaining * 100) / 100,
        sla_status: slaStatus,
        sla_percentage: Math.round((hoursElapsed / slaTarget) * 100)
      }
    })

    // Categorize by SLA status
    const slaStatusCounts = {
      ok: slaAnalysis.filter(t => t.sla_status === 'ok').length,
      warning: slaAnalysis.filter(t => t.sla_status === 'warning').length,
      critical: slaAnalysis.filter(t => t.sla_status === 'critical').length,
      breached: slaAnalysis.filter(t => t.sla_status === 'breached').length
    }

    // Get priority breakdown
    const priorityBreakdown = {}
    slaAnalysis.forEach(ticket => {
      if (!priorityBreakdown[ticket.priority]) {
        priorityBreakdown[ticket.priority] = {
          total: 0,
          breached: 0,
          critical: 0,
          warning: 0,
          ok: 0
        }
      }
      priorityBreakdown[ticket.priority].total++
      priorityBreakdown[ticket.priority][ticket.sla_status]++
    })

    res.json({
      success: true,
      data: {
        period,
        time_threshold: timeThreshold,
        sla_targets: slaTargets,
        summary: {
          total_tickets: tickets.length,
          sla_status_counts: slaStatusCounts,
          breached_percentage: tickets.length > 0 ? 
            Math.round((slaStatusCounts.breached / tickets.length) * 100) : 0,
          critical_percentage: tickets.length > 0 ? 
            Math.round((slaStatusCounts.critical / tickets.length) * 100) : 0
        },
        priority_breakdown: priorityBreakdown,
        tickets: slaAnalysis.sort((a, b) => {
          // Sort by SLA status priority (breached first, then critical, etc.)
          const statusPriority = { breached: 0, critical: 1, warning: 2, ok: 3 }
          return statusPriority[a.sla_status] - statusPriority[b.sla_status]
        })
      }
    })
  } catch (error) {
    console.error('Get SLA monitoring error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching SLA monitoring data'
    })
  }
}

module.exports = {
  bulkTicketOperations,
  getTicketTemplates,
  createTicketTemplate,
  escalateTicket,
  getTicketRoutingRules,
  getSLAMonitoring
}
