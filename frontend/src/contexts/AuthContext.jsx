import { createContext, useContext, useEffect, useMemo, useState } from 'react'
import api from '../services/api'

const STORAGE_KEY = 'user'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
	const [user, setUser] = useState(null)
	const [loading, setLoading] = useState(true)
	const [error, setError] = useState(null)

	useEffect(() => {
		async function bootstrap() {
			try {
				setLoading(true)
				const storedUser = localStorage.getItem(STORAGE_KEY)
				if (storedUser) {
					const userData = JSON.parse(storedUser)
					setUser(userData)
					// Verify user is still valid by checking profile
					try {
						const { data } = await api.get(`/auth/profile/${userData.id}`)
						setUser(data.data.user)
					} catch (e) {
						// User might be invalid, clear it
						localStorage.removeItem(STORAGE_KEY)
						setUser(null)
					}
				}
			} catch (e) {
				// Clear invalid data
				localStorage.removeItem(STORAGE_KEY)
				setUser(null)
			} finally {
				setLoading(false)
			}
		}
		bootstrap()
	}, [])

	const login = async (credentials) => {
		setError(null)
		try {
			console.log('Login attempt with:', credentials)
			console.log('API base URL:', api.defaults.baseURL)
			const { data } = await api.post('/auth/login', credentials)
			console.log('Login successful:', data)
			localStorage.setItem(STORAGE_KEY, JSON.stringify(data.data.user))
			setUser(data.data.user)
			return { ok: true }
		} catch (e) {
			console.error('Login failed:', e)
			console.error('Error response:', e?.response?.data)
			setError(e?.response?.data?.message || 'Login failed')
			return { ok: false, error: e }
		}
	}

	const register = async (payload) => {
		setError(null)
		try {
			const { data } = await api.post('/auth/register', payload)
			localStorage.setItem(STORAGE_KEY, JSON.stringify(data.data.user))
			setUser(data.data.user)
			return { ok: true }
		} catch (e) {
			setError(e?.response?.data?.message || 'Registration failed')
			return { ok: false, error: e }
		}
	}

	const logout = () => {
		localStorage.removeItem(STORAGE_KEY)
		setUser(null)
	}

	const value = useMemo(() => ({ user, loading, error, login, register, logout }), [user, loading, error])

	return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuthContext() {
	return useContext(AuthContext)
}
