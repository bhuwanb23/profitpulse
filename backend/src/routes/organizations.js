const express = require('express')
const router = express.Router()
const {
  getOrganizations,
  createOrganization,
  getOrganizationById,
  updateOrganization,
  deleteOrganization,
  addOrganizationMember,
  removeOrganizationMember
} = require('../controllers/organizationController')
const {
  createOrganizationValidation,
  updateOrganizationValidation,
  organizationIdValidation,
  getOrganizationsValidation,
  addMemberValidation,
  removeMemberValidation
} = require('../validators/organizationValidator')
const { requireRole } = require('../middleware/rbac')

// GET /api/organizations - List organizations
router.get('/', 
  getOrganizationsValidation,
  getOrganizations
)

// POST /api/organizations - Create organization - temporarily without auth for testing
router.post('/', 
  createOrganizationValidation,
  createOrganization
)

// GET /api/organizations/:id - Get organization details
router.get('/:id', 
  organizationIdValidation,
  getOrganizationById
)

// PUT /api/organizations/:id - Update organization - temporarily without auth for testing
router.put('/:id', 
  updateOrganizationValidation,
  updateOrganization
)

// DELETE /api/organizations/:id - Delete organization - temporarily without auth for testing
router.delete('/:id', 
  organizationIdValidation,
  deleteOrganization
)

// POST /api/organizations/:id/members - Add organization member - temporarily without auth for testing
router.post('/:id/members', 
  addMemberValidation,
  addOrganizationMember
)

// DELETE /api/organizations/:id/members/:userId - Remove member - temporarily without auth for testing
router.delete('/:id/members/:userId', 
  removeMemberValidation,
  removeOrganizationMember
)

module.exports = router