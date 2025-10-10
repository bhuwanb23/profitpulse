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
		<nav className="fixed bottom-0 left-0 right-0 z-40 bg-white border-t border-gray-200 md:hidden">
			<ul className="grid grid-cols-5">
				{items.map(i => (
					<li key={i.to}>
						<NavLink to={i.to} className={({ isActive }) => `flex flex-col items-center justify-center py-2 text-xs ${isActive ? 'text-blue-600' : 'text-gray-600'}`}>
							<span className="text-base">{i.icon}</span>
							<span>{i.label}</span>
						</NavLink>
					</li>
				))}
			</ul>
		</nav>
	)
}
