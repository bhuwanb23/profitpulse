const express = require('express')
const router = express.Router()
const {
  getUsers,
  getUserById,
  getCurrentUser,
  updateUser,
  deleteUser,
  changeUserPassword
} = require('../controllers/userController')
const {
  updateUserValidation,
  changePasswordValidation,
  userIdValidation,
  getUsersValidation
} = require('../validators/userValidator')
const { requireRole } = require('../middleware/rbac')

// GET /api/users - List users (admin only) - temporarily without auth for testing
router.get('/', 
  getUsersValidation,
  getUsers
)

// GET /api/users/me - Get current user profile
router.get('/me', getCurrentUser)

// GET /api/users/:id - Get user profile
router.get('/:id', 
  userIdValidation,
  getUserById
)

// PUT /api/users/:id - Update user profile
router.put('/:id', 
  updateUserValidation,
  updateUser
)

// DELETE /api/users/:id - Delete user (admin only) - temporarily without auth for testing
router.delete('/:id', 
  userIdValidation,
  deleteUser
)

// POST /api/users/:id/change-password - Change password
router.post('/:id/change-password', 
  changePasswordValidation,
  changeUserPassword
)

module.exports = router