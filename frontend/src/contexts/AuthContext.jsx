import { createContext, useContext, useEffect, useMemo, useState } from 'react'
import api from '../services/api'

const STORAGE_KEY = 'token'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
	const [user, setUser] = useState(null)
	const [token, setToken] = useState(localStorage.getItem(STORAGE_KEY) || null)
	const [loading, setLoading] = useState(true)
	const [error, setError] = useState(null)

	useEffect(() => {
		async function bootstrap() {
			try {
				setLoading(true)
				if (token) {
					// Optionally fetch profile
					setUser({ email: 'user@example.com' })
				}
			} catch (e) {
				setUser(null)
			} finally {
				setLoading(false)
			}
		}
		bootstrap()
	}, [token])

	const login = async (credentials) => {
		setError(null)
		try {
			// const { data } = await api.post('/auth/login', credentials)
			// Mocked response for now
			const data = { token: 'mock-token', user: { email: credentials.email } }
			localStorage.setItem(STORAGE_KEY, data.token)
			setToken(data.token)
			setUser(data.user)
			return { ok: true }
		} catch (e) {
			setError(e?.response?.data?.message || 'Login failed')
			return { ok: false, error: e }
		}
	}

	const register = async (payload) => {
		setError(null)
		try {
			// const { data } = await api.post('/auth/register', payload)
			const data = { token: 'mock-token', user: { email: payload.email } }
			localStorage.setItem(STORAGE_KEY, data.token)
			setToken(data.token)
			setUser(data.user)
			return { ok: true }
		} catch (e) {
			setError(e?.response?.data?.message || 'Registration failed')
			return { ok: false, error: e }
		}
	}

	const logout = () => {
		localStorage.removeItem(STORAGE_KEY)
		setToken(null)
		setUser(null)
	}

	const value = useMemo(() => ({ user, token, loading, error, login, register, logout }), [user, token, loading, error])

	return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuthContext() {
	return useContext(AuthContext)
}
