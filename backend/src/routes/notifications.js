const express = require('express')
const router = express.Router()
const {
  getNotifications,
  markNotificationAsRead,
  updateNotificationPreferences,
  getEmailSettings,
  updateEmailSettings,
  getDashboardAlerts,
  testNotification
} = require('../controllers/notificationController')
const {
  getNotificationsValidation,
  markNotificationAsReadValidation,
  updateNotificationPreferencesValidation,
  getEmailSettingsValidation,
  updateEmailSettingsValidation,
  getDashboardAlertsValidation,
  testNotificationValidation
} = require('../validators/notificationValidator')

// GET /api/notifications - List notifications
router.get('/', 
  getNotificationsValidation,
  getNotifications
)

// PUT /api/notifications/:id/read - Mark as read
router.put('/:id/read', 
  markNotificationAsReadValidation,
  markNotificationAsRead
)

// POST /api/notifications/preferences - Update preferences
router.post('/preferences', 
  updateNotificationPreferencesValidation,
  updateNotificationPreferences
)

// GET /api/notifications/email-settings - Email settings
router.get('/email-settings', 
  getEmailSettingsValidation,
  getEmailSettings
)

// PUT /api/notifications/email-settings - Update email settings
router.put('/email-settings', 
  updateEmailSettingsValidation,
  updateEmailSettings
)

// GET /api/notifications/alerts - Dashboard alerts
router.get('/alerts', 
  getDashboardAlertsValidation,
  getDashboardAlerts
)

// POST /api/notifications/test - Test notification
router.post('/test', 
  testNotificationValidation,
  testNotification
)

module.exports = router