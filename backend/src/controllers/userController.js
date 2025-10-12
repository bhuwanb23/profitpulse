const { User, Organization } = require('../models')
const { Op } = require('sequelize')
const bcrypt = require('bcryptjs')
const { validationResult } = require('express-validator')

// GET /api/users - List users (admin only)
const getUsers = async (req, res) => {
  try {
    const { page = 1, limit = 10, search, role, isActive } = req.query
    const offset = (page - 1) * limit

    // Build where clause
    const whereClause = {}
    if (search) {
      whereClause[Op.or] = [
        { first_name: { [Op.iLike]: `%${search}%` } },
        { last_name: { [Op.iLike]: `%${search}%` } },
        { email: { [Op.iLike]: `%${search}%` } }
      ]
    }
    if (role) whereClause.role = role
    if (isActive !== undefined) whereClause.is_active = isActive === 'true'

    const { count, rows: users } = await User.findAndCountAll({
      where: whereClause,
      include: [
        {
          model: Organization,
          as: 'organization',
          attributes: ['id', 'name', 'domain']
        }
      ],
      attributes: { exclude: ['password_hash'] },
      limit: parseInt(limit),
      offset: parseInt(offset),
      order: [['created_at', 'DESC']]
    })

    res.json({
      success: true,
      data: {
        users,
        pagination: {
          total: count,
          page: parseInt(page),
          limit: parseInt(limit),
          pages: Math.ceil(count / limit)
        }
      }
    })
  } catch (error) {
    console.error('Get users error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching users'
    })
  }
}

// GET /api/users/:id - Get user profile
const getUserById = async (req, res) => {
  try {
    const { id } = req.params

    const user = await User.findByPk(id, {
      include: [
        {
          model: Organization,
          as: 'organization',
          attributes: ['id', 'name', 'domain']
        }
      ],
      attributes: { exclude: ['password_hash'] }
    })

    if (!user) {
      return res.status(404).json({
        success: false,
        message: 'User not found'
      })
    }

    res.json({
      success: true,
      data: { user }
    })
  } catch (error) {
    console.error('Get user by ID error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching user'
    })
  }
}

// GET /api/users/me - Get current user profile
const getCurrentUser = async (req, res) => {
  try {
    // For simplified auth, get userId from query parameter or body
    const userId = req.query.userId || req.body.userId

    if (!userId) {
      return res.status(401).json({
        success: false,
        message: 'User ID required'
      })
    }

    const user = await User.findByPk(userId, {
      include: [
        {
          model: Organization,
          as: 'organization',
          attributes: ['id', 'name', 'domain']
        }
      ],
      attributes: { exclude: ['password_hash'] }
    })

    if (!user) {
      return res.status(404).json({
        success: false,
        message: 'User not found'
      })
    }

    res.json({
      success: true,
      data: { user }
    })
  } catch (error) {
    console.error('Get current user error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while fetching current user'
    })
  }
}

// PUT /api/users/:id - Update user profile
const updateUser = async (req, res) => {
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
    const { first_name, last_name, email, role, is_active, organization_id } = req.body

    const user = await User.findByPk(id)
    if (!user) {
      return res.status(404).json({
        success: false,
        message: 'User not found'
      })
    }

    // Check if email is being changed and if it's already taken
    if (email && email !== user.email) {
      const existingUser = await User.findOne({ where: { email } })
      if (existingUser) {
        return res.status(400).json({
          success: false,
          message: 'Email already exists'
        })
      }
    }

    // Update user
    await user.update({
      first_name: first_name || user.first_name,
      last_name: last_name || user.last_name,
      email: email || user.email,
      role: role || user.role,
      is_active: is_active !== undefined ? is_active : user.is_active,
      organization_id: organization_id || user.organization_id
    })

    // Fetch updated user with organization
    const updatedUser = await User.findByPk(id, {
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
      message: 'User updated successfully',
      data: { user: updatedUser }
    })
  } catch (error) {
    console.error('Update user error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while updating user'
    })
  }
}

// DELETE /api/users/:id - Delete user (admin only)
const deleteUser = async (req, res) => {
  try {
    const { id } = req.params

    const user = await User.findByPk(id)
    if (!user) {
      return res.status(404).json({
        success: false,
        message: 'User not found'
      })
    }

    // Prevent deleting the last admin user
    if (user.role === 'admin') {
      const adminCount = await User.count({ where: { role: 'admin' } })
      if (adminCount <= 1) {
        return res.status(400).json({
          success: false,
          message: 'Cannot delete the last admin user'
        })
      }
    }

    await user.destroy()

    res.json({
      success: true,
      message: 'User deleted successfully'
    })
  } catch (error) {
    console.error('Delete user error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while deleting user'
    })
  }
}

// POST /api/users/:id/change-password - Change password
const changeUserPassword = async (req, res) => {
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
    const { currentPassword, newPassword } = req.body

    const user = await User.findByPk(id)
    if (!user) {
      return res.status(404).json({
        success: false,
        message: 'User not found'
      })
    }

    // Verify current password
    const isCurrentPasswordValid = await bcrypt.compare(currentPassword, user.password_hash)
    if (!isCurrentPasswordValid) {
      return res.status(400).json({
        success: false,
        message: 'Current password is incorrect'
      })
    }

    // Hash new password
    const saltRounds = 12
    const newPasswordHash = await bcrypt.hash(newPassword, saltRounds)

    // Update password
    await user.update({ password_hash: newPasswordHash })

    res.json({
      success: true,
      message: 'Password changed successfully'
    })
  } catch (error) {
    console.error('Change password error:', error)
    res.status(500).json({
      success: false,
      message: 'Internal server error while changing password'
    })
  }
}

module.exports = {
  getUsers,
  getUserById,
  getCurrentUser,
  updateUser,
  deleteUser,
  changeUserPassword
}
