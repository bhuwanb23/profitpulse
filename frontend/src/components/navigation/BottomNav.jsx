import { NavLink } from 'react-router-dom'

const items = [
	{ to: '/dashboard', label: 'Home', icon: '🏠' },
	{ to: '/clients', label: 'Clients', icon: '👥' },
	{ to: '/tickets', label: 'Tickets', icon: '🎫' },
	{ to: '/reports', label: 'Reports', icon: '📑' },
	{ to: '/ai', label: 'AI', icon: '🧠' },
]

export default function BottomNav() {
	return (
		<nav style={{ position: 'fixed', bottom: 0, left: 0, right: 0, zIndex: 40, backgroundColor: 'white', borderTop: '1px solid #e5e7eb', display: 'none' }}>
			<ul style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)' }}>
				{items.map(i => (
					<li key={i.to}>
						<NavLink 
							to={i.to} 
							style={({ isActive }) => ({
								display: 'flex',
								flexDirection: 'column',
								alignItems: 'center',
								justifyContent: 'center',
								padding: '8px 0',
								fontSize: '12px',
								textDecoration: 'none',
								color: isActive ? '#2563eb' : '#6b7280'
							})}
						>
							<span style={{ fontSize: '16px' }}>{i.icon}</span>
							<span>{i.label}</span>
						</NavLink>
					</li>
				))}
			</ul>
		</nav>
	)
}
