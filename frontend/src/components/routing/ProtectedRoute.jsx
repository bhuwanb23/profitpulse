import { Navigate, Outlet, useLocation } from 'react-router-dom'
import { useAuthContext } from '../../contexts/AuthContext'

export default function ProtectedRoute() {
	const { user, loading } = useAuthContext()
	const location = useLocation()

	if (loading) {
		return (
			<div className="min-h-[60vh] grid place-items-center text-gray-500">Loading…</div>
		)
	}

	if (!user) {
		return <Navigate to="/login" state={{ from: location }} replace />
	}

	return <Outlet />
}
