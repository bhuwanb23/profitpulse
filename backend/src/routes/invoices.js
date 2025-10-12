const express = require('express');
const router = express.Router();

// Placeholder invoice routes - will be implemented in Phase 4.1
router.get('/test', (req, res) => {
  res.json({
    success: true,
    message: 'Invoice routes are working',
    timestamp: new Date().toISOString()
  });
});

module.exports = router;
