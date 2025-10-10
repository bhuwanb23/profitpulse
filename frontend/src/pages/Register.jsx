import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuthContext } from '../contexts/AuthContext'

export default function Register() {
	const { register: doRegister, error } = useAuthContext()
	const navigate = useNavigate()
	const [form, setForm] = useState({ email: '', password: '', confirm: '' })
	const [submitting, setSubmitting] = useState(false)
	const [formErrors, setFormErrors] = useState({})

	const validate = () => {
		const errs = {}
		if (!form.email) errs.email = 'Email is required'
		if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) errs.email = 'Enter a valid email'
		if (!form.password) errs.password = 'Password is required'
		if (form.password && form.password.length < 6) errs.password = 'Minimum 6 characters'
		if (form.confirm !== form.password) errs.confirm = 'Passwords do not match'
		setFormErrors(errs)
		return Object.keys(errs).length === 0
	}

	const onSubmit = async (e) => {
		e.preventDefault()
		if (!validate()) return
		setSubmitting(true)
		const res = await doRegister({ email: form.email, password: form.password })
		setSubmitting(false)
		if (res.ok) navigate('/dashboard')
	}

	return (
		<div className="min-h-screen grid place-items-center bg-gray-50 px-4">
			<form onSubmit={onSubmit} className="w-full max-w-md bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
				<h1 className="text-xl font-semibold">Create account</h1>
				<p className="text-sm text-gray-500 mt-1">Get started with SuperHack</p>
				<div className="mt-6 space-y-4">
					<div>
						<label className="block text-sm text-gray-700">Email</label>
						<input
							type="email"
							value={form.email}
							onChange={(e) => setForm((f) => ({ ...f, email: e.target.value }))}
							className={`mt-1 w-full rounded-md border px-3 py-2 text-sm ${formErrors.email ? 'border-red-400' : 'border-gray-300'}`}
							placeholder="you@example.com"
						/>
						{formErrors.email && <p className="mt-1 text-xs text-red-600">{formErrors.email}</p>}
					</div>
					<div>
						<label className="block text-sm text-gray-700">Password</label>
						<input
							type="password"
							value={form.password}
							onChange={(e) => setForm((f) => ({ ...f, password: e.target.value }))}
							className={`mt-1 w-full rounded-md border px-3 py-2 text-sm ${formErrors.password ? 'border-red-400' : 'border-gray-300'}`}
							placeholder="••••••••"
						/>
						{formErrors.password && <p className="mt-1 text-xs text-red-600">{formErrors.password}</p>}
					</div>
					<div>
						<label className="block text-sm text-gray-700">Confirm Password</label>
						<input
							type="password"
							value={form.confirm}
							onChange={(e) => setForm((f) => ({ ...f, confirm: e.target.value }))}
							className={`mt-1 w-full rounded-md border px-3 py-2 text-sm ${formErrors.confirm ? 'border-red-400' : 'border-gray-300'}`}
							placeholder="••••••••"
						/>
						{formErrors.confirm && <p className="mt-1 text-xs text-red-600">{formErrors.confirm}</p>}
					</div>
				</div>
				{error && <div className="mt-3 text-xs text-red-600">{error}</div>}
				<button type="submit" disabled={submitting} className="mt-6 w-full bg-blue-600 text-white text-sm py-2.5 rounded-md hover:bg-blue-700 disabled:opacity-60">
					{submitting ? 'Creating…' : 'Create account'}
				</button>
				<p className="text-xs text-gray-500 mt-4">
					Already have an account? <Link to="/login" className="text-blue-600 hover:underline">Sign in</Link>
				</p>
			</form>
		</div>
	)
}
