const express = require('express');
const router = express.Router();
const { 
  register, 
  login, 
  getProfile, 
  logout, 
  verifyUser,
  requestPasswordReset,
  resetPassword,
  changePassword
} = require('../controllers/authController');
const { 
  registerValidation, 
  loginValidation 
} = require('../validators/authValidator');

// Public routes
router.post('/register', registerValidation, register);
router.post('/login', loginValidation, login);

// Password reset routes (public)
router.post('/forgot-password', requestPasswordReset);
router.post('/reset-password', resetPassword);

// User routes (simplified for testing)
router.get('/profile/:userId', getProfile);
router.get('/verify/:userId', verifyUser);
router.post('/logout', logout);
router.post('/change-password', changePassword);

// Test route
router.get('/test', (req, res) => {
  res.json({
    success: true,
    message: 'Auth routes are working',
    timestamp: new Date().toISOString()
  });
});

module.exports = router;
