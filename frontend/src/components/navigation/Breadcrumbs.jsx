import { NavLink, useLocation } from 'react-router-dom'

const labelMap = {
	'': 'Dashboard',
	dashboard: 'Dashboard',
	clients: 'Clients',
	tickets: 'Tickets',
	invoices: 'Invoices',
	analytics: 'Analytics',
	settings: 'Settings',
}

export default function Breadcrumbs() {
	const location = useLocation()
	const segments = location.pathname.replace(/^\/+|\/+$/g, '').split('/')

	const items = segments[0] === '' ? [''] : segments

	return (
		<nav className="text-sm text-gray-500" aria-label="Breadcrumb">
			<ol className="flex items-center gap-2 flex-wrap">
				{items.map((seg, idx) => {
					const to = '/' + items.slice(0, idx + 1).filter(Boolean).join('/')
					const isLast = idx === items.length - 1
					const label = labelMap[seg] || (seg.charAt(0).toUpperCase() + seg.slice(1))
					return (
						<li key={to} className="flex items-center gap-2">
							{idx > 0 && <span className="text-gray-300">/</span>}
							{isLast ? (
								<span className="text-gray-700">{label}</span>
							) : (
								<NavLink to={to || '/dashboard'} className="hover:text-gray-700">
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
