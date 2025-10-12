const express = require('express');
const router = express.Router();

// Placeholder user routes - will be implemented in Phase 2.1
router.get('/test', (req, res) => {
  res.json({
    success: true,
    message: 'User routes are working',
    timestamp: new Date().toISOString()
  });
});

module.exports = router;
