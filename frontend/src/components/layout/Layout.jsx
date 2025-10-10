import { useState } from 'react'
import { NavLink, Outlet } from 'react-router-dom'
import { useAuthContext } from '../../contexts/AuthContext'
import Breadcrumbs from '../navigation/Breadcrumbs'
import ErrorBoundary from '../ui/ErrorBoundary'

const navItems = [
	{ to: '/dashboard', label: 'Dashboard', icon: '🏠' },
	{ to: '/clients', label: 'Clients', icon: '👥' },
	{ to: '/tickets', label: 'Tickets', icon: '🎫' },
	{ to: '/invoices', label: 'Invoices', icon: '💰' },
	{ to: '/analytics', label: 'Analytics', icon: '📊' },
	{ to: '/reports', label: 'Reports', icon: '📑' },
	{ to: '/billing-analytics', label: 'Billing Analytics', icon: '💹' },
	{ to: '/budget-management', label: 'Budget Management', icon: '📘' },
	{ to: '/ai', label: 'AI Insights', icon: '🧠' },
	{ to: '/settings', label: 'Settings', icon: '⚙️' },
]

export default function Layout() {
	const [sidebarOpen, setSidebarOpen] = useState(false)
	const { user, logout } = useAuthContext()

	return (
		<div className="min-h-screen bg-gray-50 text-gray-900">
			{/* Header */}
			<header className="sticky top-0 z-30 bg-white/80 backdrop-blur border-b border-gray-200">
				<div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
					<button className="md:hidden p-2 rounded hover:bg-gray-100" onClick={() => setSidebarOpen((s) => !s)} aria-label="Toggle sidebar">☰</button>
					<div className="flex items-center gap-3">
						<div className="h-8 w-8 rounded bg-blue-600 text-white grid place-items-center font-bold">SH</div>
						<span className="font-semibold">SuperHack</span>
					</div>
					<div className="flex items-center gap-2">
						<input className="hidden sm:block w-64 rounded-md border border-gray-300 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Search..." />
						<div className="h-8 w-8 grid place-items-center rounded-full bg-gray-100">🔔</div>
						<button onClick={logout} className="text-xs px-3 py-1.5 rounded bg-gray-100 hover:bg-gray-200">Logout</button>
						<div className="h-8 w-8 grid place-items-center rounded-full bg-gray-100" title={user?.email || ''}>👤</div>
					</div>
				</div>
			</header>

			{/* Body */}
			<div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
				<Breadcrumbs />
			</div>
			<div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-6 grid grid-cols-1 md:grid-cols-[220px_1fr] gap-6">
				{/* Sidebar */}
				<aside className={`md:sticky md:top-20 md:self-start bg-white border border-gray-200 rounded-lg p-3 h-max ${sidebarOpen ? 'block' : 'hidden'} md:block`}>
					<nav className="space-y-1">
						{navItems.map((item) => (
							<NavLink
								key={item.to}
								to={item.to}
								className={({ isActive }) => `flex items-center gap-2 px-3 py-2 rounded-md text-sm transition-colors ${isActive ? 'bg-blue-50 text-blue-700 border border-blue-200' : 'hover:bg-gray-50'}`}
							>
								<span className="text-base">{item.icon}</span>
								<span>{item.label}</span>
							</NavLink>
						))}
					</nav>
				</aside>

				{/* Content */}
				<main className="space-y-6">
					<ErrorBoundary>
						<Outlet />
					</ErrorBoundary>
				</main>
			</div>
		</div>
	)
}
