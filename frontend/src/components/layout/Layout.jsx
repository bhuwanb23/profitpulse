import { useState } from 'react'
import { NavLink, Outlet } from 'react-router-dom'
import { useAuthContext } from '../../contexts/AuthContext'
import Breadcrumbs from '../navigation/Breadcrumbs'
import ErrorBoundary from '../ui/ErrorBoundary'
import BottomNav from '../navigation/BottomNav'

const navItems = [
	{ to: '/dashboard', label: 'Dashboard', icon: '🏠' },
	{ to: '/clients', label: 'Clients', icon: '👥' },
	{ to: '/tickets', label: 'Tickets', icon: '🎫' },
	{ to: '/invoices', label: 'Invoices', icon: '💰' },
	{ to: '/analytics', label: 'Analytics', icon: '📊' },
	{ to: '/reports', label: 'Reports', icon: '📑' },
	{ to: '/notifications', label: 'Notifications', icon: '🔔' },
	{ to: '/billing-analytics', label: 'Billing Analytics', icon: '💹' },
	{ to: '/budget-management', label: 'Budget Management', icon: '📘' },
	{ to: '/ai', label: 'AI Insights', icon: '🧠' },
	{ to: '/settings', label: 'Settings', icon: '⚙️' },
]

export default function Layout() {
	const [sidebarOpen, setSidebarOpen] = useState(false)
	const { user, logout } = useAuthContext()

	return (
		<div style={{ minHeight: '100vh', backgroundColor: '#f9fafb', color: '#111827', paddingBottom: '64px' }}>
			{/* Header */}
			<header style={{ position: 'sticky', top: 0, zIndex: 30, backgroundColor: 'rgba(255, 255, 255, 0.8)', backdropFilter: 'blur(10px)', borderBottom: '1px solid #e5e7eb' }}>
				<div style={{ maxWidth: '1280px', margin: '0 auto', padding: '0 16px', height: '64px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
					<button 
						style={{ display: 'none', padding: '8px', borderRadius: '4px', backgroundColor: 'transparent', border: 'none', cursor: 'pointer' }}
						onClick={() => setSidebarOpen((s) => !s)} 
						aria-label="Toggle sidebar"
					>
						☰
					</button>
					<div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
						<div style={{ height: '32px', width: '32px', borderRadius: '4px', backgroundColor: '#2563eb', color: 'white', display: 'grid', placeItems: 'center', fontWeight: 'bold' }}>SH</div>
						<span style={{ fontWeight: '600' }}>SuperHack</span>
					</div>
					<div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
						<input 
							style={{ display: 'none', width: '256px', borderRadius: '6px', border: '1px solid #d1d5db', padding: '6px 12px', fontSize: '14px' }}
							placeholder="Search..." 
						/>
						<div style={{ height: '32px', width: '32px', display: 'grid', placeItems: 'center', borderRadius: '50%', backgroundColor: '#f3f4f6' }}>🔔</div>
						<button 
							onClick={logout} 
							style={{ fontSize: '12px', padding: '6px 12px', borderRadius: '4px', backgroundColor: '#f3f4f6', border: 'none', cursor: 'pointer' }}
						>
							Logout
						</button>
						<div 
							style={{ height: '32px', width: '32px', display: 'grid', placeItems: 'center', borderRadius: '50%', backgroundColor: '#f3f4f6' }} 
							title={user?.email || ''}
						>
							👤
						</div>
					</div>
				</div>
			</header>

			{/* Body */}
			<div style={{ maxWidth: '1280px', margin: '0 auto', padding: '16px' }}>
				<Breadcrumbs />
			</div>
			<div style={{ maxWidth: '1280px', margin: '0 auto', padding: '0 16px 24px', display: 'grid', gridTemplateColumns: '220px 1fr', gap: '24px' }}>
				{/* Sidebar */}
				<aside style={{ position: 'sticky', top: '80px', alignSelf: 'start', backgroundColor: 'white', border: '1px solid #e5e7eb', borderRadius: '8px', padding: '12px', height: 'max-content' }}>
					<nav style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
						{navItems.map((item) => (
							<NavLink
								key={item.to}
								to={item.to}
								style={({ isActive }) => ({
									display: 'flex',
									alignItems: 'center',
									gap: '8px',
									padding: '8px 12px',
									borderRadius: '6px',
									fontSize: '14px',
									textDecoration: 'none',
									color: isActive ? '#1d4ed8' : '#374151',
									backgroundColor: isActive ? '#eff6ff' : 'transparent',
									border: isActive ? '1px solid #bfdbfe' : '1px solid transparent'
								})}
							>
								<span style={{ fontSize: '16px' }}>{item.icon}</span>
								<span>{item.label}</span>
							</NavLink>
						))}
					</nav>
				</aside>

				{/* Content */}
				<main style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
					<ErrorBoundary>
						<Outlet />
					</ErrorBoundary>
				</main>
			</div>

			<BottomNav />
		</div>
	)
}
