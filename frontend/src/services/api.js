import axios from 'axios'
import { v4 as uuidv4 } from 'uuid'
import { CONFIG } from './config'

const DEFAULT_TIMEOUT_MS = 15000
const MAX_RETRY_ATTEMPTS = 2

const api = axios.create({
	baseURL: CONFIG.apiUrl,
	timeout: DEFAULT_TIMEOUT_MS,
	headers: {
		'X-Requested-With': 'XMLHttpRequest',
	},
})

api.interceptors.request.use((config) => {
	// Auth token
	const token = localStorage.getItem('token')
	if (token) {
		config.headers.Authorization = `Bearer ${token}`
	}

	// Correlation ID
	if (!config.headers['X-Correlation-ID']) {
		config.headers['X-Correlation-ID'] = uuidv4()
	}

	return config
})

api.interceptors.response.use(
	(res) => {
		// Log backend request id in dev
		const reqId = res.headers?.['x-request-id']
		if (import.meta.env.DEV && reqId) {
			// eslint-disable-next-line no-console
			console.debug('[API]', res.config.method?.toUpperCase(), res.config.url, '→', res.status, 'reqId:', reqId)
		}
		return res
	},
	async (error) => {
		const { config, response, code, message } = error || {}

		// Normalize error shape
		const normalized = {
			status: response?.status ?? null,
			code: code || response?.data?.code || null,
			message: response?.data?.message || message || 'Network error',
			details: response?.data?.errors || null,
			requestId: response?.headers?.['x-request-id'] || null,
		}

		// 401 → clear creds and redirect to login
		if (response?.status === 401) {
			localStorage.removeItem('token')
			// optional: preserve current path for post-login redirect
			if (window.location.pathname !== '/login') {
				window.location.replace('/login')
			}
			return Promise.reject(normalized)
		}

		// Simple retry for transient errors (429 / network timeouts)
		const shouldRetry =
			response?.status === 429 ||
			code === 'ECONNABORTED' ||
			message?.toLowerCase?.().includes('network')

		if (shouldRetry && config && !config._retry) {
			config._retry = 0
		}

		if (shouldRetry && config && config._retry < MAX_RETRY_ATTEMPTS) {
			config._retry += 1
			const delayMs = Math.min(1000 * 2 ** (config._retry - 1), 4000)
			await new Promise((r) => setTimeout(r, delayMs))
			return api(config)
		}

		return Promise.reject(normalized)
	}
)

export default api
