const { Service, Client, Organization } = require('../models')
const { Op } = require('sequelize')
const { validationResult } = require('express-validator')

// GET /api/services - List services
const getServices = async (req, res) => {
  try {
    const { 
      page = 1, 
      limit = 10, 
      search, 
      category, 
      type,
      status,
      is_active,
      organization_id,
      client_id,
      sort_by = 'created_at',
      sort_order = 'DESC'
    } = req.query
    const offset = (page - 1) * limit

    // Build where clause
    const whereClause = {}
    if (search) {
      whereClause[Op.or] = [
        { name: { [Op.iLike]: `%${search}%` } },
        { description: { [Op.iLike]: `%${search}%` } },
        { category: { [Op.iLike]: `%${search}%` } }
      ]
    }
    if (category) whereClause.category = category
    if (type) whereClause.type = type
    if (status) whereClause.status = status
    if (is_active !== undefined) whereClause.is_active = is_active === 'true'
    if (organization_id) whereClause.organization_id = organization_id
    if (client_id) whereClause.client_id = client_id

    // Build order clause
    const orderClause = [[sort_by, sort_order.toUpperCase()]]

    const { count, rows: services } = await Service.findAndCountAll({
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
          attributes: ['id', 'name', 'email', 'company'],
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
    console.error('Get services error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching services'
    })
  }
}

// POST /api/services - Create service
const createService = async (req, res) => {
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
      description,
      category,
      type = 'basic',
      status = 'active',
      base_price,
      monthly_cost,
      billing_type = 'monthly',
      organization_id,
      client_id
    } = req.body

    // Check if service with same name already exists in the organization
    if (organization_id) {
      const existingService = await Service.findOne({
        where: { 
          name,
          organization_id
        }
      })

      if (existingService) {
        return res.status(400).json({
          success: false,
          message: 'Service with this name already exists in the organization'
        })
      }
    }

    const service = await Service.create({
      name,
      description,
      category,
      type,
      status,
      base_price,
      monthly_cost,
      billing_type,
      organization_id,
      client_id
    })

    // Fetch the created service with associations
    const createdService = await Service.findByPk(service.id, {
      include: [
        {
          model: Organization,
          as: 'organization',
          attributes: ['id', 'name', 'domain']
        },
        {
          model: Client,
          as: 'client',
          attributes: ['id', 'name', 'email', 'company'],
          required: false
        }
      ]
    })

    res.status(201).json({
      success: true,
      message: 'Service created successfully',
      data: { service: createdService }
    })
  } catch (error) {
    console.error('Create service error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while creating service'
    })
  }
}

// GET /api/services/:id - Get service details
const getServiceById = async (req, res) => {
  try {
    const { id } = req.params

    const service = await Service.findByPk(id, {
      include: [
        {
          model: Organization,
          as: 'organization',
          attributes: ['id', 'name', 'domain']
        },
        {
          model: Client,
          as: 'client',
          attributes: ['id', 'name', 'email', 'company', 'contact_person', 'phone'],
          required: false
        }
      ]
    })

    if (!service) {
      return res.status(404).json({
        success: false,
        message: 'Service not found'
      })
    }

    res.json({
      success: true,
      data: { service }
    })
  } catch (error) {
    console.error('Get service by ID error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching service'
    })
  }
}

// PUT /api/services/:id - Update service
const updateService = async (req, res) => {
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

    const service = await Service.findByPk(id)
    if (!service) {
      return res.status(404).json({
        success: false,
        message: 'Service not found'
      })
    }

    // Check if name is being changed and if it's already taken in the organization
    if (updateData.name && updateData.name !== service.name) {
      const existingService = await Service.findOne({
        where: {
          id: { [Op.ne]: id },
          name: updateData.name,
          organization_id: service.organization_id
        }
      })

      if (existingService) {
        return res.status(400).json({
          success: false,
          message: 'Service with this name already exists in the organization'
        })
      }
    }

    // Update service
    await service.update(updateData)

    // Fetch updated service with associations
    const updatedService = await Service.findByPk(id, {
      include: [
        {
          model: Organization,
          as: 'organization',
          attributes: ['id', 'name', 'domain']
        },
        {
          model: Client,
          as: 'client',
          attributes: ['id', 'name', 'email', 'company'],
          required: false
        }
      ]
    })

    res.json({
      success: true,
      message: 'Service updated successfully',
      data: { service: updatedService }
    })
  } catch (error) {
    console.error('Update service error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while updating service'
    })
  }
}

// DELETE /api/services/:id - Delete service
const deleteService = async (req, res) => {
  try {
    const { id } = req.params

    const service = await Service.findByPk(id)
    if (!service) {
      return res.status(404).json({
        success: false,
        message: 'Service not found'
      })
    }

    // Check if service is assigned to any clients
    if (service.client_id) {
      return res.status(400).json({
        success: false,
        message: 'Cannot delete service that is assigned to a client. Please unassign the service first.'
      })
    }

    await service.destroy()

    res.json({
      success: true,
      message: 'Service deleted successfully'
    })
  } catch (error) {
    console.error('Delete service error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while deleting service'
    })
  }
}

// POST /api/services/:id/assign - Assign service to client
const assignServiceToClient = async (req, res) => {
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
    const { client_id } = req.body

    // Check if service exists
    const service = await Service.findByPk(id)
    if (!service) {
      return res.status(404).json({
        success: false,
        message: 'Service not found'
      })
    }

    // Check if client exists
    const client = await Client.findByPk(client_id)
    if (!client) {
      return res.status(404).json({
        success: false,
        message: 'Client not found'
      })
    }

    // Check if service is already assigned to a client
    if (service.client_id) {
      return res.status(400).json({
        success: false,
        message: 'Service is already assigned to a client. Please unassign it first.'
      })
    }

    // Check if client belongs to the same organization as the service
    if (client.organization_id !== service.organization_id) {
      return res.status(400).json({
        success: false,
        message: 'Client and service must belong to the same organization'
      })
    }

    // Assign service to client
    await service.update({ client_id })

    // Fetch updated service with client information
    const updatedService = await Service.findByPk(id, {
      include: [
        {
          model: Organization,
          as: 'organization',
          attributes: ['id', 'name', 'domain']
        },
        {
          model: Client,
          as: 'client',
          attributes: ['id', 'name', 'email', 'company', 'contact_person', 'phone']
        }
      ]
    })

    res.json({
      success: true,
      message: 'Service assigned to client successfully',
      data: { service: updatedService }
    })
  } catch (error) {
    console.error('Assign service to client error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while assigning service to client'
    })
  }
}

// PUT /api/services/:id/pricing - Update service pricing
const updateServicePricing = async (req, res) => {
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
    const { base_price, monthly_cost, billing_type } = req.body

    const service = await Service.findByPk(id)
    if (!service) {
      return res.status(404).json({
        success: false,
        message: 'Service not found'
      })
    }

    // Update pricing information
    const updateData = {}
    if (base_price !== undefined) updateData.base_price = base_price
    if (monthly_cost !== undefined) updateData.monthly_cost = monthly_cost
    if (billing_type !== undefined) updateData.billing_type = billing_type

    await service.update(updateData)

    // Fetch updated service with associations
    const updatedService = await Service.findByPk(id, {
      include: [
        {
          model: Organization,
          as: 'organization',
          attributes: ['id', 'name', 'domain']
        },
        {
          model: Client,
          as: 'client',
          attributes: ['id', 'name', 'email', 'company'],
          required: false
        }
      ]
    })

    res.json({
      success: true,
      message: 'Service pricing updated successfully',
      data: { service: updatedService }
    })
  } catch (error) {
    console.error('Update service pricing error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while updating service pricing'
    })
  }
}

module.exports = {
  getServices,
  createService,
  getServiceById,
  updateService,
  deleteService,
  assignServiceToClient,
  updateServicePricing
}
