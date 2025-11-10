const client = require('./client');

// Export both for compatibility
module.exports = client;  // Default export (for most controllers)
module.exports.client = client;  // Named export (for aiController)
module.exports.default = client;  // ES6 style default