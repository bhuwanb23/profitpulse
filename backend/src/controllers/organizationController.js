const { Organization, User } = require('../models')
const { Op } = require('sequelize')
const { validationResult } = require('express-validator')

// GET /api/organizations - List organizations
const getOrganizations = async (req, res) => {
  try {
    const { page = 1, limit = 10, search, subscription_plan, is_active } = req.query
    const offset = (page - 1) * limit

    // Build where clause
    const whereClause = {}
    if (search) {
      whereClause[Op.or] = [
        { name: { [Op.iLike]: `%${search}%` } },
        { domain: { [Op.iLike]: `%${search}%` } }
      ]
    }
    if (subscription_plan) whereClause.subscription_plan = subscription_plan
    if (is_active !== undefined) whereClause.is_active = is_active === 'true'

    const { count, rows: organizations } = await Organization.findAndCountAll({
      where: whereClause,
      include: [
        {
          model: User,
          as: 'users',
          attributes: ['id', 'email', 'first_name', 'last_name', 'role', 'is_active'],
          required: false
        }
      ],
      limit: parseInt(limit),
      offset: parseInt(offset),
      order: [['created_at', 'DESC']]
    })

    res.json({
      success: true,
      data: {
        organizations,
        pagination: {
          total: count,
          page: parseInt(page),
          limit: parseInt(limit),
          pages: Math.ceil(count / limit)
        }
      }
    })
  } catch (error) {
    console.error('Get organizations error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching organizations'
    })
  }
}

// POST /api/organizations - Create organization
const createOrganization = async (req, res) => {
  try {
    const errors = validationResult(req)
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        message: 'Validation failed',
        errors: errors.array()
      })
    }

    const { name, domain, subscription_plan = 'basic', is_active = true } = req.body

    // Check if organization with same name or domain already exists
    const existingOrg = await Organization.findOne({
      where: {
        [Op.or]: [
          { name },
          { domain }
        ]
      }
    })

    if (existingOrg) {
      return res.status(400).json({
        success: false,
        message: 'Organization with this name or domain already exists'
      })
    }

    const organization = await Organization.create({
      name,
      domain,
      subscription_plan,
      is_active
    })

    // Fetch the created organization with users
    const createdOrganization = await Organization.findByPk(organization.id, {
      include: [
        {
          model: User,
          as: 'users',
          attributes: ['id', 'email', 'first_name', 'last_name', 'role', 'is_active'],
          required: false
        }
      ]
    })

    res.status(201).json({
      success: true,
      message: 'Organization created successfully',
      data: { organization: createdOrganization }
    })
  } catch (error) {
    console.error('Create organization error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while creating organization'
    })
  }
}

// GET /api/organizations/:id - Get organization details
const getOrganizationById = async (req, res) => {
  try {
    const { id } = req.params

    const organization = await Organization.findByPk(id, {
      include: [
        {
          model: User,
          as: 'users',
          attributes: ['id', 'email', 'first_name', 'last_name', 'role', 'is_active'],
          required: false
        }
      ]
    })

    if (!organization) {
      return res.status(404).json({
        success: false,
        message: 'Organization not found'
      })
    }

    res.json({
      success: true,
      data: { organization }
    })
  } catch (error) {
    console.error('Get organization by ID error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching organization'
    })
  }
}

// PUT /api/organizations/:id - Update organization
const updateOrganization = async (req, res) => {
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
    const { name, domain, subscription_plan, is_active } = req.body

    const organization = await Organization.findByPk(id)
    if (!organization) {
      return res.status(404).json({
        success: false,
        message: 'Organization not found'
      })
    }

    // Check if name or domain is being changed and if it's already taken
    if ((name && name !== organization.name) || (domain && domain !== organization.domain)) {
      const existingOrg = await Organization.findOne({
        where: {
          id: { [Op.ne]: id },
          [Op.or]: [
            ...(name && name !== organization.name ? [{ name }] : []),
            ...(domain && domain !== organization.domain ? [{ domain }] : [])
          ]
        }
      })

      if (existingOrg) {
        return res.status(400).json({
          success: false,
          message: 'Organization with this name or domain already exists'
        })
      }
    }

    // Update organization
    await organization.update({
      name: name || organization.name,
      domain: domain || organization.domain,
      subscription_plan: subscription_plan || organization.subscription_plan,
      is_active: is_active !== undefined ? is_active : organization.is_active
    })

    // Fetch updated organization with users
    const updatedOrganization = await Organization.findByPk(id, {
      include: [
        {
          model: User,
          as: 'users',
          attributes: ['id', 'email', 'first_name', 'last_name', 'role', 'is_active'],
          required: false
        }
      ]
    })

    res.json({
      success: true,
      message: 'Organization updated successfully',
      data: { organization: updatedOrganization }
    })
  } catch (error) {
    console.error('Update organization error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while updating organization'
    })
  }
}

// DELETE /api/organizations/:id - Delete organization
const deleteOrganization = async (req, res) => {
  try {
    const { id } = req.params

    const organization = await Organization.findByPk(id, {
      include: [
        {
          model: User,
          as: 'users',
          required: false
        }
      ]
    })

    if (!organization) {
      return res.status(404).json({
        success: false,
        message: 'Organization not found'
      })
    }

    // Check if organization has users
    if (organization.users && organization.users.length > 0) {
      return res.status(400).json({
        success: false,
        message: 'Cannot delete organization with existing users. Please remove all users first.'
      })
    }

    await organization.destroy()

    res.json({
      success: true,
      message: 'Organization deleted successfully'
    })
  } catch (error) {
    console.error('Delete organization error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while deleting organization'
    })
  }
}

// POST /api/organizations/:id/members - Add organization member
const addOrganizationMember = async (req, res) => {
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
    const { user_id, role = 'user' } = req.body

    // Check if organization exists
    const organization = await Organization.findByPk(id)
    if (!organization) {
      return res.status(404).json({
        success: false,
        message: 'Organization not found'
      })
    }

    // Check if user exists
    const user = await User.findByPk(user_id)
    if (!user) {
      return res.status(404).json({
        success: false,
        message: 'User not found'
      })
    }

    // Check if user is already a member of this organization
    if (user.organization_id === id) {
      return res.status(400).json({
        success: false,
        message: 'User is already a member of this organization'
      })
    }

    // Update user's organization and role
    await user.update({
      organization_id: id,
      role: role
    })

    // Fetch updated user with organization
    const updatedUser = await User.findByPk(user_id, {
      include: [
        {
          model: Organization,
          as: 'organization',
          attributes: ['id', 'name', 'domain']
        }
      ],
      attributes: { exclude: ['password_hash'] }
    })

    res.json({
      success: true,
      message: 'User added to organization successfully',
      data: { user: updatedUser }
    })
  } catch (error) {
    console.error('Add organization member error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while adding organization member'
    })
  }
}

// DELETE /api/organizations/:id/members/:userId - Remove member
const removeOrganizationMember = async (req, res) => {
  try {
    const { id, userId } = req.params

    // Check if organization exists
    const organization = await Organization.findByPk(id)
    if (!organization) {
      return res.status(404).json({
        success: false,
        message: 'Organization not found'
      })
    }

    // Check if user exists
    const user = await User.findByPk(userId)
    if (!user) {
      return res.status(404).json({
        success: false,
        message: 'User not found'
      })
    }

    // Check if user is a member of this organization
    if (user.organization_id !== id) {
      return res.status(400).json({
        success: false,
        message: 'User is not a member of this organization'
      })
    }

    // Remove user from organization
    await user.update({
      organization_id: null,
      role: 'user' // Reset to default role
    })

    res.json({
      success: true,
      message: 'User removed from organization successfully'
    })
  } catch (error) {
    console.error('Remove organization member error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while removing organization member'
    })
  }
}

module.exports = {
  getOrganizations,
  createOrganization,
  getOrganizationById,
  updateOrganization,
  deleteOrganization,
  addOrganizationMember,
  removeOrganizationMember
}
