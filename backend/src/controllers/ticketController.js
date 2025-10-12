const { Ticket, Client, User, Organization } = require('../models')
const { Op } = require('sequelize')
const { validationResult } = require('express-validator')

// GET /api/tickets - List tickets with filters
const getTickets = async (req, res) => {
  try {
    const { 
      page = 1, 
      limit = 10, 
      search, 
      status,
      priority,
      category,
      assigned_to,
      client_id,
      organization_id,
      created_from,
      created_to,
      sort_by = 'created_at',
      sort_order = 'DESC'
    } = req.query
    const offset = (page - 1) * limit

    // Build where clause
    const whereClause = {}
    if (search) {
      whereClause[Op.or] = [
        { title: { [Op.iLike]: `%${search}%` } },
        { description: { [Op.iLike]: `%${search}%` } },
        { ticket_number: { [Op.iLike]: `%${search}%` } }
      ]
    }
    if (status) whereClause.status = status
    if (priority) whereClause.priority = priority
    if (category) whereClause.category = category
    if (assigned_to) whereClause.assigned_to = assigned_to
    if (client_id) whereClause.client_id = client_id
    if (organization_id) whereClause.organization_id = organization_id
    
    // Date range filtering
    if (created_from || created_to) {
      whereClause.created_at = {}
      if (created_from) whereClause.created_at[Op.gte] = new Date(created_from)
      if (created_to) whereClause.created_at[Op.lte] = new Date(created_to)
    }

    // Build order clause
    const orderClause = [[sort_by, sort_order.toUpperCase()]]

    const { count, rows: tickets } = await Ticket.findAndCountAll({
      where: whereClause,
      include: [
        {
          model: Organization,
          as: 'organization',
          attributes: ['id', 'name', 'domain']
        },
        {
          model: Client,
          as: 'client',
          attributes: ['id', 'name', 'email', 'company']
        }
      ],
      limit: parseInt(limit),
      offset: parseInt(offset),
      order: orderClause
    })

    res.json({
      success: true,
      data: {
        tickets,
        pagination: {
          total: count,
          page: parseInt(page),
          limit: parseInt(limit),
          pages: Math.ceil(count / limit)
        }
      }
    })
  } catch (error) {
    console.error('Get tickets error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching tickets'
    })
  }
}

// POST /api/tickets - Create new ticket
const createTicket = async (req, res) => {
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
      title,
      description,
      priority = 'medium',
      category,
      status = 'open',
      client_id,
      organization_id,
      assigned_to,
      due_date,
      estimated_hours,
      created_by
    } = req.body

    // Check if client exists and belongs to organization
    if (client_id) {
      const client = await Client.findOne({
        where: { 
          id: client_id,
          organization_id: organization_id
        }
      })
      if (!client) {
        return res.status(400).json({
          success: false,
          message: 'Client not found or does not belong to the organization'
        })
      }
    }

    // Check if assigned user exists and belongs to organization
    if (assigned_to) {
      const user = await User.findOne({
        where: { 
          id: assigned_to,
          organization_id: organization_id
        }
      })
      if (!user) {
        return res.status(400).json({
          success: false,
          message: 'Assigned user not found or does not belong to the organization'
        })
      }
    }

    // Generate ticket number
    const ticketNumber = `TKT-${Date.now()}-${Math.random().toString(36).substr(2, 4).toUpperCase()}`

    const ticket = await Ticket.create({
      title,
      description,
      priority,
      category,
      status,
      client_id,
      organization_id,
      assigned_to,
      due_date: due_date ? new Date(due_date) : null,
      estimated_hours,
      ticket_number: ticketNumber,
      created_by
    })

    // Fetch the created ticket with basic associations
    const createdTicket = await Ticket.findByPk(ticket.id, {
      include: [
        {
          model: Organization,
          as: 'organization',
          attributes: ['id', 'name', 'domain']
        },
        {
          model: Client,
          as: 'client',
          attributes: ['id', 'name', 'email', 'company']
        }
      ]
    })

    res.status(201).json({
      success: true,
      message: 'Ticket created successfully',
      data: { ticket: createdTicket }
    })
  } catch (error) {
    console.error('Create ticket error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while creating ticket'
    })
  }
}

// GET /api/tickets/:id - Get ticket details
const getTicketById = async (req, res) => {
  try {
    const { id } = req.params

    const ticket = await Ticket.findByPk(id, {
      include: [
        {
          model: Organization,
          as: 'organization',
          attributes: ['id', 'name', 'domain']
        },
        {
          model: Client,
          as: 'client',
          attributes: ['id', 'name', 'email', 'company']
        }
      ]
    })

    if (!ticket) {
      return res.status(404).json({
        success: false,
        message: 'Ticket not found'
      })
    }

    res.json({
      success: true,
      data: { ticket }
    })
  } catch (error) {
    console.error('Get ticket by ID error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching ticket'
    })
  }
}

// PUT /api/tickets/:id - Update ticket
const updateTicket = async (req, res) => {
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
    const updateData = req.body

    const ticket = await Ticket.findByPk(id)
    if (!ticket) {
      return res.status(404).json({
        success: false,
        message: 'Ticket not found'
      })
    }

    // Validate client if being updated
    if (updateData.client_id && updateData.client_id !== ticket.client_id) {
      const client = await Client.findOne({
        where: { 
          id: updateData.client_id,
          organization_id: ticket.organization_id
        }
      })
      if (!client) {
        return res.status(400).json({
          success: false,
          message: 'Client not found or does not belong to the organization'
        })
      }
    }

    // Validate assigned user if being updated
    if (updateData.assigned_to && updateData.assigned_to !== ticket.assigned_to) {
      const user = await User.findOne({
        where: { 
          id: updateData.assigned_to,
          organization_id: ticket.organization_id
        }
      })
      if (!user) {
        return res.status(400).json({
          success: false,
          message: 'Assigned user not found or does not belong to the organization'
        })
      }
    }

    // Update ticket
    await ticket.update(updateData)

    // Fetch updated ticket with basic associations
    const updatedTicket = await Ticket.findByPk(id, {
      include: [
        {
          model: Organization,
          as: 'organization',
          attributes: ['id', 'name', 'domain']
        },
        {
          model: Client,
          as: 'client',
          attributes: ['id', 'name', 'email', 'company']
        }
      ]
    })

    res.json({
      success: true,
      message: 'Ticket updated successfully',
      data: { ticket: updatedTicket }
    })
  } catch (error) {
    console.error('Update ticket error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while updating ticket'
    })
  }
}

// DELETE /api/tickets/:id - Delete ticket
const deleteTicket = async (req, res) => {
  try {
    const { id } = req.params

    const ticket = await Ticket.findByPk(id)
    if (!ticket) {
      return res.status(404).json({
        success: false,
        message: 'Ticket not found'
      })
    }

    await ticket.destroy()

    res.json({
      success: true,
      message: 'Ticket deleted successfully'
    })
  } catch (error) {
    console.error('Delete ticket error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while deleting ticket'
    })
  }
}

// POST /api/tickets/:id/assign - Assign ticket to technician
const assignTicket = async (req, res) => {
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
    const { assigned_to } = req.body

    const ticket = await Ticket.findByPk(id)
    if (!ticket) {
      return res.status(404).json({
        success: false,
        message: 'Ticket not found'
      })
    }

    // Check if user exists and belongs to organization
    const user = await User.findOne({
      where: { 
        id: assigned_to,
        organization_id: ticket.organization_id
      }
    })
    if (!user) {
      return res.status(400).json({
        success: false,
        message: 'User not found or does not belong to the organization'
      })
    }

    // Update ticket assignment
    await ticket.update({ assigned_to })

    // Fetch updated ticket with basic associations
    const updatedTicket = await Ticket.findByPk(id, {
      include: [
        {
          model: Organization,
          as: 'organization',
          attributes: ['id', 'name', 'domain']
        },
        {
          model: Client,
          as: 'client',
          attributes: ['id', 'name', 'email', 'company']
        }
      ]
    })

    res.json({
      success: true,
      message: 'Ticket assigned successfully',
      data: { ticket: updatedTicket }
    })
  } catch (error) {
    console.error('Assign ticket error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while assigning ticket'
    })
  }
}

// PUT /api/tickets/:id/status - Update ticket status
const updateTicketStatus = async (req, res) => {
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
    const { status, resolution_notes } = req.body

    const ticket = await Ticket.findByPk(id)
    if (!ticket) {
      return res.status(404).json({
        success: false,
        message: 'Ticket not found'
      })
    }

    // Update ticket status
    const updateData = { status }
    if (resolution_notes) updateData.resolution_notes = resolution_notes
    
    // Set resolved_at if status is resolved/closed
    if (status === 'resolved' || status === 'closed') {
      updateData.resolved_at = new Date()
    }

    await ticket.update(updateData)

    // Fetch updated ticket with basic associations
    const updatedTicket = await Ticket.findByPk(id, {
      include: [
        {
          model: Organization,
          as: 'organization',
          attributes: ['id', 'name', 'domain']
        },
        {
          model: Client,
          as: 'client',
          attributes: ['id', 'name', 'email', 'company']
        }
      ]
    })

    res.json({
      success: true,
      message: 'Ticket status updated successfully',
      data: { ticket: updatedTicket }
    })
  } catch (error) {
    console.error('Update ticket status error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while updating ticket status'
    })
  }
}

// POST /api/tickets/:id/time - Log time spent
const logTimeSpent = async (req, res) => {
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
      hours_spent, 
      description, 
      user_id, 
      date_worked = new Date().toISOString().split('T')[0] 
    } = req.body

    const ticket = await Ticket.findByPk(id)
    if (!ticket) {
      return res.status(404).json({
        success: false,
        message: 'Ticket not found'
      })
    }

    // Check if user exists and belongs to organization
    if (user_id) {
      const user = await User.findOne({
        where: { 
          id: user_id,
          organization_id: ticket.organization_id
        }
      })
      if (!user) {
        return res.status(400).json({
          success: false,
          message: 'User not found or does not belong to the organization'
        })
      }
    }

    // Update ticket with time logged
    const currentTimeSpent = ticket.time_spent || 0
    const newTimeSpent = currentTimeSpent + parseFloat(hours_spent)
    
    await ticket.update({ 
      time_spent: newTimeSpent,
      last_activity: new Date()
    })

    // In a real application, you might want to create a separate TimeLog model
    // For now, we'll just update the ticket with the total time

    // Fetch updated ticket with basic associations
    const updatedTicket = await Ticket.findByPk(id, {
      include: [
        {
          model: Organization,
          as: 'organization',
          attributes: ['id', 'name', 'domain']
        },
        {
          model: Client,
          as: 'client',
          attributes: ['id', 'name', 'email', 'company']
        }
      ]
    })

    res.json({
      success: true,
      message: 'Time logged successfully',
      data: { 
        ticket: updatedTicket,
        time_logged: {
          hours_spent,
          description,
          user_id,
          date_worked,
          total_time_spent: newTimeSpent
        }
      }
    })
  } catch (error) {
    console.error('Log time spent error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while logging time'
    })
  }
}

module.exports = {
  getTickets,
  createTicket,
  getTicketById,
  updateTicket,
  deleteTicket,
  assignTicket,
  updateTicketStatus,
  logTimeSpent
}
