const express = require('express');
const router = express.Router();
const { 
  register, 
  login, 
  getProfile, 
  logout, 
  refreshToken 
} = require('../controllers/authController');
const { authenticateToken } = require('../middleware/auth');
const { 
  registerValidation, 
  loginValidation 
} = require('../validators/authValidator');

// Public routes
router.post('/register', register);
router.post('/login', loginValidation, login);

// Protected routes
router.get('/profile', authenticateToken, getProfile);
router.post('/logout', authenticateToken, logout);
router.post('/refresh', authenticateToken, refreshToken);

// Test route
router.get('/test', (req, res) => {
  res.json({
    success: true,
    message: 'Auth routes are working',
    timestamp: new Date().toISOString()
  });
});

module.exports = router;
