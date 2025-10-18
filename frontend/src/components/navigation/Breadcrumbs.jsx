import { NavLink, useLocation } from 'react-router-dom'

const labelMap = {
	'': 'Dashboard',
	dashboard: 'Dashboard',
	clients: 'Clients',
	'client-analytics': 'Client Analytics',
	'client-services': 'Client Services',
	tickets: 'Tickets',
	'ticket-analytics': 'Ticket Analytics',
	'ticket-operations': 'Ticket Operations',
	invoices: 'Invoices',
	'invoice-analytics': 'Invoice Analytics',
	'invoice-operations': 'Invoice Operations',
	analytics: 'Analytics',
	'billing-analytics': 'Billing Analytics',
	'budget-management': 'Budget Management',
	reports: 'Reports',
	notifications: 'Notifications',
	ai: 'AI Insights',
	settings: 'Settings',
}

export default function Breadcrumbs() {
	const location = useLocation()
	const segments = location.pathname.replace(/^\/+|\/+$/g, '').split('/')

	const items = segments[0] === '' ? [''] : segments

	return (
		<nav style={{ fontSize: '14px', color: '#6b7280' }} aria-label="Breadcrumb">
			<ol style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
				{items.map((seg, idx) => {
					const to = '/' + items.slice(0, idx + 1).filter(Boolean).join('/')
					const isLast = idx === items.length - 1
					const label = labelMap[seg] || (seg.charAt(0).toUpperCase() + seg.slice(1))
					return (
						<li key={to} style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
							{idx > 0 && <span style={{ color: '#d1d5db' }}>/</span>}
							{isLast ? (
								<span style={{ color: '#374151' }}>{label}</span>
							) : (
								<NavLink 
									to={to || '/dashboard'} 
									style={{ color: '#6b7280', textDecoration: 'none' }}
								>
									{label}
								</NavLink>
							)}
						</li>
					)
				})}
			</ol>
		</nav>
	)
}
