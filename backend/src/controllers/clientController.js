const { Client, Service, Ticket, Invoice, Organization } = require('../models')
const { Op } = require('sequelize')
const { validationResult } = require('express-validator')

// GET /api/clients - List clients with filters
const getClients = async (req, res) => {
  try {
    const { 
      page = 1, 
      limit = 10, 
      search, 
      industry, 
      status, 
      is_active,
      organization_id,
      sort_by = 'created_at',
      sort_order = 'DESC'
    } = req.query
    const offset = (page - 1) * limit

    // Build where clause
    const whereClause = {}
    if (search) {
      whereClause[Op.or] = [
        { name: { [Op.iLike]: `%${search}%` } },
        { email: { [Op.iLike]: `%${search}%` } },
        { contact_person: { [Op.iLike]: `%${search}%` } },
        { company: { [Op.iLike]: `%${search}%` } }
      ]
    }
    if (industry) whereClause.industry = industry
    if (status) whereClause.status = status
    if (is_active !== undefined) whereClause.is_active = is_active === 'true'
    if (organization_id) whereClause.organization_id = organization_id

    // Build order clause
    const orderClause = [[sort_by, sort_order.toUpperCase()]]

    const { count, rows: clients } = await Client.findAndCountAll({
      where: whereClause,
      include: [
        {
          model: Organization,
          as: 'organization',
          attributes: ['id', 'name', 'domain']
        },
        {
          model: Service,
          as: 'services',
          attributes: ['id', 'name', 'type', 'status', 'monthly_cost'],
          required: false
        }
      ],
      limit: parseInt(limit),
      offset: parseInt(offset),
      order: orderClause
    })

    res.json({
      success: true,
      data: {
        clients,
        pagination: {
          total: count,
          page: parseInt(page),
          limit: parseInt(limit),
          pages: Math.ceil(count / limit)
        }
      }
    })
  } catch (error) {
    console.error('Get clients error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching clients'
    })
  }
}

// POST /api/clients - Create new client
const createClient = async (req, res) => {
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
      email,
      phone,
      company,
      contact_person,
      address,
      city,
      state,
      zip_code,
      country,
      industry,
      status = 'active',
      contract_start_date,
      contract_end_date,
      monthly_budget,
      organization_id
    } = req.body

    // Check if client with same email already exists
    const existingClient = await Client.findOne({
      where: { email }
    })

    if (existingClient) {
      return res.status(400).json({
        success: false,
        message: 'Client with this email already exists'
      })
    }

    const client = await Client.create({
      name,
      email,
      phone,
      company,
      contact_person,
      address,
      city,
      state,
      zip_code,
      country,
      industry,
      status,
      contract_start_date,
      contract_end_date,
      monthly_budget,
      organization_id
    })

    // Fetch the created client with organization
    const createdClient = await Client.findByPk(client.id, {
      include: [
        {
          model: Organization,
          as: 'organization',
          attributes: ['id', 'name', 'domain']
        }
      ]
    })

    res.status(201).json({
      success: true,
      message: 'Client created successfully',
      data: { client: createdClient }
    })
  } catch (error) {
    console.error('Create client error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while creating client'
    })
  }
}

// GET /api/clients/:id - Get client details
const getClientById = async (req, res) => {
  try {
    const { id } = req.params

    const client = await Client.findByPk(id, {
      include: [
        {
          model: Organization,
          as: 'organization',
          attributes: ['id', 'name', 'domain']
        },
        {
          model: Service,
          as: 'services',
          attributes: ['id', 'name', 'type', 'status', 'monthly_cost', 'description'],
          required: false
        },
        {
          model: Ticket,
          as: 'tickets',
          attributes: ['id', 'title', 'status', 'priority', 'created_at'],
          required: false,
          limit: 10,
          order: [['created_at', 'DESC']]
        }
      ]
    })

    if (!client) {
      return res.status(404).json({
        success: false,
        message: 'Client not found'
      })
    }

    res.json({
      success: true,
      data: { client }
    })
  } catch (error) {
    console.error('Get client by ID error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching client'
    })
  }
}

// PUT /api/clients/:id - Update client
const updateClient = async (req, res) => {
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

    const client = await Client.findByPk(id)
    if (!client) {
      return res.status(404).json({
        success: false,
        message: 'Client not found'
      })
    }

    // Check if email is being changed and if it's already taken
    if (updateData.email && updateData.email !== client.email) {
      const existingClient = await Client.findOne({
        where: {
          id: { [Op.ne]: id },
          email: updateData.email
        }
      })

      if (existingClient) {
        return res.status(400).json({
          success: false,
          message: 'Client with this email already exists'
        })
      }
    }

    // Update client
    await client.update(updateData)

    // Fetch updated client with organization
    const updatedClient = await Client.findByPk(id, {
      include: [
        {
          model: Organization,
          as: 'organization',
          attributes: ['id', 'name', 'domain']
        }
      ]
    })

    res.json({
      success: true,
      message: 'Client updated successfully',
      data: { client: updatedClient }
    })
  } catch (error) {
    console.error('Update client error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while updating client'
    })
  }
}

// DELETE /api/clients/:id - Delete client
const deleteClient = async (req, res) => {
  try {
    const { id } = req.params

    const client = await Client.findByPk(id, {
      include: [
        {
          model: Service,
          as: 'services',
          required: false
        },
        {
          model: Ticket,
          as: 'tickets',
          required: false
        }
      ]
    })

    if (!client) {
      return res.status(404).json({
        success: false,
        message: 'Client not found'
      })
    }

    // Check if client has active services or tickets
    if ((client.services && client.services.length > 0) || (client.tickets && client.tickets.length > 0)) {
      return res.status(400).json({
        success: false,
        message: 'Cannot delete client with active services or tickets. Please remove all services and tickets first.'
      })
    }

    await client.destroy()

    res.json({
      success: true,
      message: 'Client deleted successfully'
    })
  } catch (error) {
    console.error('Delete client error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while deleting client'
    })
  }
}

// GET /api/clients/:id/services - Get client services
const getClientServices = async (req, res) => {
  try {
    const { id } = req.params
    const { page = 1, limit = 10, status, type } = req.query
    const offset = (page - 1) * limit

    // Check if client exists
    const client = await Client.findByPk(id)
    if (!client) {
      return res.status(404).json({
        success: false,
        message: 'Client not found'
      })
    }

    // Build where clause for services
    const whereClause = { client_id: id }
    if (status) whereClause.status = status
    if (type) whereClause.type = type

    const { count, rows: services } = await Service.findAndCountAll({
      where: whereClause,
      limit: parseInt(limit),
      offset: parseInt(offset),
      order: [['created_at', 'DESC']]
    })

    res.json({
      success: true,
      data: {
        client: { id: client.id, name: client.name },
        services,
        pagination: {
          total: count,
          page: parseInt(page),
          limit: parseInt(limit),
          pages: Math.ceil(count / limit)
        }
      }
    })
  } catch (error) {
    console.error('Get client services error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching client services'
    })
  }
}

// GET /api/clients/:id/analytics - Get client analytics
const getClientAnalytics = async (req, res) => {
  try {
    const { id } = req.params
    const { period = '30d' } = req.query

    // Check if client exists
    const client = await Client.findByPk(id)
    if (!client) {
      return res.status(404).json({
        success: false,
        message: 'Client not found'
      })
    }

    // Simplified analytics - just return basic data
    res.json({
      success: true,
      data: {
        client: { id: client.id, name: client.name },
        period,
        analytics: {
          services: {
            total: 0,
            active: 0,
            inactive: 0
          },
          tickets: {
            total: 0,
            open: 0,
            resolved: 0,
            resolution_rate: 0,
            avg_resolution_time_days: 0
          },
          revenue: {
            total: 0,
            paid: 0,
            pending: 0,
            collection_rate: 0
          }
        }
      }
    })
  } catch (error) {
    console.error('Get client analytics error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching client analytics'
    })
  }
}

// GET /api/clients/:id/profitability - Get client profitability
const getClientProfitability = async (req, res) => {
  try {
    const { id } = req.params
    const { period = '30d' } = req.query

    // Check if client exists
    const client = await Client.findByPk(id)
    if (!client) {
      return res.status(404).json({
        success: false,
        message: 'Client not found'
      })
    }

    // Simplified profitability - just return basic data
    res.json({
      success: true,
      data: {
        client: { id: client.id, name: client.name },
        period,
        profitability: {
          revenue: {
            monthly: 0,
            lifetime: 0,
            invoices: 0
          },
          costs: {
            estimated_monthly: 0
          },
          profit: {
            gross_monthly: 0,
            margin_percentage: 0,
            roi: 0
          },
          metrics: {
            services_count: 0,
            active_services: 0,
            revenue_per_service: 0
          }
        }
      }
    })
  } catch (error) {
    console.error('Get client profitability error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching client profitability'
    })
  }
}

module.exports = {
  getClients,
  createClient,
  getClientById,
  updateClient,
  deleteClient,
  getClientServices,
  getClientAnalytics,
  getClientProfitability
}
