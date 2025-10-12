/**
 * Role-Based Access Control Middleware
 */

/**
 * Check if user has required role
 */
const requireRole = (roles) => {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({
        success: false,
        message: 'Authentication required'
      });
    }

    const userRole = req.user.role;
    const allowedRoles = Array.isArray(roles) ? roles : [roles];

    if (!allowedRoles.includes(userRole)) {
      return res.status(403).json({
        success: false,
        message: 'Insufficient permissions',
        required: allowedRoles,
        current: userRole
      });
    }

    next();
  };
};

/**
 * Check if user is admin
 */
const requireAdmin = requireRole('admin');

/**
 * Check if user is admin or finance
 */
const requireAdminOrFinance = requireRole(['admin', 'finance']);

/**
 * Check if user is admin or ops
 */
const requireAdminOrOps = requireRole(['admin', 'ops']);

/**
 * Check if user can access organization data
 */
const requireOrganizationAccess = (req, res, next) => {
  if (!req.user) {
    return res.status(401).json({
      success: false,
      message: 'Authentication required'
    });
  }

  // Admin can access any organization
  if (req.user.role === 'admin') {
    return next();
  }

  // Check if user belongs to the organization
  const organizationId = req.params.organizationId || req.body.organizationId || req.query.organizationId;
  
  if (!organizationId) {
    return res.status(400).json({
      success: false,
      message: 'Organization ID required'
    });
  }

  // In a real implementation, you'd check if user.organization_id matches organizationId
  // For now, we'll allow access if user has organization_id
  if (req.user.organizationId && req.user.organizationId === organizationId) {
    return next();
  }

  return res.status(403).json({
    success: false,
    message: 'Access denied to this organization'
  });
};

module.exports = {
  requireRole,
  requireAdmin,
  requireAdminOrFinance,
  requireAdminOrOps,
  requireOrganizationAccess
};
