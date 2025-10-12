const express = require('express');
const router = express.Router();

// Placeholder budget routes - will be implemented in Phase 4.3
router.get('/test', (req, res) => {
  res.json({
    success: true,
    message: 'Budget routes are working',
    timestamp: new Date().toISOString()
  });
});

module.exports = router;
