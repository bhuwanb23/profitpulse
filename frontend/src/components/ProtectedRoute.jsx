import { useAuthContext } from '../contexts/AuthContext'
import { Navigate, Outlet } from 'react-router-dom'

export default function ProtectedRoute() {
  const { user, loading } = useAuthContext()

  if (loading) {
    return (
      <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <div style={{ width: '32px', height: '32px', border: '2px solid #e5e7eb', borderTop: '2px solid #4f46e5', borderRadius: '50%', animation: 'spin 1s linear infinite' }}></div>
      </div>
    )
  }

  if (!user) {
    return <Navigate to="/login" replace />
  }

  return <Outlet />
}
