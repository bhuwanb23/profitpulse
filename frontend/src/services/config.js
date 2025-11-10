export const CONFIG = {
	apiUrl: import.meta.env.VITE_API_URL || 'http://localhost:3000/api',
	appName: import.meta.env.VITE_APP_NAME || 'SuperHack',
	appVersion: import.meta.env.VITE_APP_VERSION || '0.1.0',
}

// Dev/Prod hints for missing API URL
if (import.meta.env.PROD && !import.meta.env.VITE_API_URL) {
	// Fail-safe: this should already be caught at build-time in vite.config.js
	// but keep a runtime guard for safety.
	console.error('[Config] VITE_API_URL is not set in production! Falling back to http://localhost:3000/api')
}