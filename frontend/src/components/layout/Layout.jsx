import { useState } from 'react'
import { NavLink, Outlet, useLocation } from 'react-router-dom'
import { useAuthContext } from '../../contexts/AuthContext'
import Breadcrumbs from '../navigation/Breadcrumbs'
import ErrorBoundary from '../ui/ErrorBoundary'
import BottomNav from '../navigation/BottomNav'


export default function Layout() {
	const [sidebarOpen, setSidebarOpen] = useState(false)
	const { user, logout } = useAuthContext()
	const location = useLocation()

	// Check if we're on a client-related page
	const isClientPage = location.pathname.startsWith('/client')
	const clientId = location.pathname.match(/\/client-(?:analytics|services)\/(.+)/)?.[1]

	// Check if we're on a ticket-related page
	const isTicketPage = location.pathname.startsWith('/ticket')

	// Enhanced navigation items with categories
	const getNavigationItems = () => {
		const categories = [
			{
				title: 'Overview',
				items: [
					{ to: '/dashboard', label: 'Dashboard', icon: '🏠', gradient: 'from-blue-500 to-purple-600' },
					{ to: '/analytics', label: 'Analytics', icon: '📊', gradient: 'from-green-500 to-teal-600' },
					{ to: '/reports', label: 'Reports', icon: '📑', gradient: 'from-orange-500 to-red-600' },
				]
			},
			{
				title: 'Client Management',
				items: [
					{ to: '/clients', label: 'Clients', icon: '👥', gradient: 'from-indigo-500 to-blue-600' },
				]
			},
			{
				title: 'Operations',
				items: [
					{ to: '/tickets', label: 'Tickets', icon: '🎫', gradient: 'from-purple-500 to-pink-600' },
					{ to: '/invoices', label: 'Invoices', icon: '💰', gradient: 'from-yellow-500 to-orange-600' },
				]
			},
			{
				title: 'Financial',
				items: [
					{ to: '/billing-analytics', label: 'Billing Analytics', icon: '💹', gradient: 'from-emerald-500 to-green-600' },
					{ to: '/budget-management', label: 'Budget Management', icon: '📘', gradient: 'from-cyan-500 to-blue-600' },
				]
			},
			{
				title: 'Intelligence',
				items: [
					{ to: '/ai', label: 'AI Insights', icon: '🧠', gradient: 'from-violet-500 to-purple-600' },
					{ to: '/notifications', label: 'Notifications', icon: '🔔', gradient: 'from-pink-500 to-rose-600' },
				]
			},
			{
				title: 'System',
				items: [
					{ to: '/settings', label: 'Settings', icon: '⚙️', gradient: 'from-gray-500 to-slate-600' },
				]
			}
		]

		// Add dynamic sub-items
		if (isClientPage && clientId) {
			categories[1].items.push(
				{ to: `/client-analytics/${clientId}`, label: 'Client Analytics', icon: '📊', isSubItem: true, gradient: 'from-blue-400 to-indigo-500' },
				{ to: `/client-services/${clientId}`, label: 'Client Services', icon: '⚙️', isSubItem: true, gradient: 'from-teal-400 to-cyan-500' }
			)
		}

		if (isTicketPage) {
			categories[2].items.push(
				{ to: '/ticket-analytics', label: 'Ticket Analytics', icon: '📈', isSubItem: true, gradient: 'from-purple-400 to-pink-500' },
				{ to: '/ticket-operations', label: 'Ticket Operations', icon: '⚙️', isSubItem: true, gradient: 'from-indigo-400 to-purple-500' }
			)
		}

		const isInvoicePage = location.pathname.startsWith('/invoice')
		if (isInvoicePage) {
			categories[2].items.push(
				{ to: '/invoice-analytics', label: 'Invoice Analytics', icon: '📊', isSubItem: true, gradient: 'from-yellow-400 to-orange-500' },
				{ to: '/invoice-operations', label: 'Invoice Operations', icon: '⚙️', isSubItem: true, gradient: 'from-orange-400 to-red-500' }
			)
		}

		return categories
	}

	const navigationCategories = getNavigationItems()

	return (
		<div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 text-gray-900 pb-16">
			{/* Modern Header */}
			<header className="sticky top-0 z-30 bg-white/80 backdrop-blur-xl border-b border-gray-200/50 shadow-sm">
				<div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
					<button 
						className="lg:hidden p-2 rounded-lg bg-gray-100 hover:bg-gray-200 transition-colors"
						onClick={() => setSidebarOpen((s) => !s)} 
						aria-label="Toggle sidebar"
					>
						<span className="text-lg">☰</span>
					</button>
					
					{/* Logo */}
					<div className="flex items-center gap-3">
						<div className="h-10 w-10 rounded-xl bg-gradient-to-br from-blue-600 to-purple-700 text-white flex items-center justify-center font-bold text-lg shadow-lg">
							SH
						</div>
						<div className="hidden sm:block">
							<h1 className="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
								SuperHack
							</h1>
							<p className="text-xs text-gray-500">MSP Management Platform</p>
						</div>
					</div>

					{/* Header Actions */}
					<div className="flex items-center gap-3">
						<div className="hidden md:flex items-center gap-2">
							<input 
								className="w-64 px-4 py-2 rounded-xl border border-gray-200 bg-white/50 backdrop-blur-sm text-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-300"
								placeholder="Search anything..." 
							/>
						</div>
						
						<button className="relative p-2 rounded-xl bg-gradient-to-br from-blue-50 to-indigo-100 hover:from-blue-100 hover:to-indigo-200 transition-all duration-200">
							<span className="text-lg">🔔</span>
							<div className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full"></div>
						</button>
						
						<button 
							onClick={logout} 
							className="px-4 py-2 rounded-xl bg-gradient-to-r from-gray-100 to-gray-200 hover:from-gray-200 hover:to-gray-300 text-sm font-medium transition-all duration-200"
						>
							Logout
						</button>
						
						<div 
							className="h-10 w-10 rounded-xl bg-gradient-to-br from-purple-100 to-pink-100 flex items-center justify-center cursor-pointer hover:from-purple-200 hover:to-pink-200 transition-all duration-200" 
							title={user?.email || ''}
						>
							<span className="text-lg">👤</span>
						</div>
					</div>
				</div>
			</header>

			{/* Main Layout */}
			<div className="max-w-7xl mx-auto px-6 py-6">
				<div className="mb-6">
					<Breadcrumbs />
				</div>
				
				<div className="grid grid-cols-1 lg:grid-cols-[280px_1fr] gap-6">
					{/* Beautiful Sidebar */}
					<aside className="lg:sticky lg:top-24 lg:self-start">
						<div className="bg-white/70 backdrop-blur-xl rounded-2xl border border-gray-200/50 shadow-xl p-6">
							<nav className="space-y-6">
								{navigationCategories.map((category, categoryIndex) => (
									<div key={categoryIndex} className="space-y-2">
										<h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider px-3">
											{category.title}
										</h3>
										<div className="space-y-1">
											{category.items.map((item) => (
												<NavLink
													key={item.to}
													to={item.to}
													className={({ isActive }) => 
														`group flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 ${
															item.isSubItem ? 'ml-4 pl-6 border-l-2 border-gray-200' : ''
														} ${
															isActive 
																? `bg-gradient-to-r ${item.gradient} text-white shadow-lg transform scale-[1.02]` 
																: 'text-gray-700 hover:bg-gray-100/80 hover:text-gray-900'
														}`
													}
												>
													{({ isActive }) => (
														<>
															<span className={`text-lg transition-transform duration-200 ${isActive ? '' : 'group-hover:scale-110'}`}>
																{item.icon}
															</span>
															<span className="truncate">{item.label}</span>
															{isActive && (
																<div className="ml-auto w-2 h-2 bg-white/30 rounded-full"></div>
															)}
														</>
													)}
												</NavLink>
											))}
										</div>
									</div>
								))}
							</nav>
							
							{/* Sidebar Footer */}
							<div className="mt-8 pt-6 border-t border-gray-200/50">
								<div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-4">
									<div className="flex items-center gap-3">
										<div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
											<span className="text-white text-sm">✨</span>
										</div>
										<div>
											<p className="text-sm font-medium text-gray-900">Pro Tips</p>
											<p className="text-xs text-gray-600">Explore AI insights</p>
										</div>
									</div>
								</div>
							</div>
						</div>
					</aside>

					{/* Content Area */}
					<main className="min-h-[calc(100vh-200px)]">
						<ErrorBoundary>
							<Outlet />
						</ErrorBoundary>
					</main>
				</div>
			</div>

			<BottomNav />
		</div>
	)
}
