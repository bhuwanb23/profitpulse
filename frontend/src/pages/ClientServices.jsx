import { useState, useEffect, useMemo } from 'react'
import ServiceCatalog from '../components/clients/ServiceCatalog'
import ClientServices from '../components/clients/ClientServices'
import { Button } from '../components/ui/Button'
import { Badge } from '../components/ui/Badge'
import { UsersIcon, ChartBarIcon, CurrencyDollarIcon } from '../components/ui/Icons'
import { useParams, Link } from 'react-router-dom'
import { mockClients, mockAssignments, mockServices } from '../services/mockClients'

export default function ClientServicesPage() {
	const { id } = useParams()
	const clientId = id || 'c1'
	const [refreshKey, setRefreshKey] = useState(0)
	const [activeTab, setActiveTab] = useState('assigned') // 'assigned' or 'catalog'
	
	// Get client info for the header
	const client = mockClients.find(c => c.id === clientId)
	
	const handleServiceAdd = (service) => {
		// In a real app, this would make an API call to add the service
		console.log('Adding service to client:', { clientId, service })
		
		// For now, we'll just show a success message and refresh the components
		alert(`${service.name} has been added to ${client?.name || 'the client'}!`)
		
		// Force refresh of components by updating key
		setRefreshKey(prev => prev + 1)
		
		// Switch to assigned services tab to show the new service
		setActiveTab('assigned')
	}

	const formatCurrency = (amount) => {
		return new Intl.NumberFormat('en-US', {
			style: 'currency',
			currency: 'USD',
			minimumFractionDigits: 0
		}).format(amount)
	}

	const formatPercentage = (value) => {
		return `${(value * 100).toFixed(1)}%`
	}

	// Calculate tab counts
	const tabCounts = useMemo(() => {
		const assignedCount = mockAssignments[clientId]?.length || 0
		const availableCount = mockServices.filter(service => 
			!mockAssignments[clientId]?.some(assignment => assignment.serviceId === service.id)
		).length
		
		return { assignedCount, availableCount }
	}, [clientId, refreshKey])

	// Listen for tab switch events
	useEffect(() => {
		const handleSwitchToCatalog = () => {
			setActiveTab('catalog')
		}

		window.addEventListener('switchToServiceCatalog', handleSwitchToCatalog)
		
		return () => {
			window.removeEventListener('switchToServiceCatalog', handleSwitchToCatalog)
		}
	}, [])

	return (
		<div className="space-y-6">
			{/* Back to Clients Link */}
			<div className="flex items-center gap-2 text-sm">
				<Link 
					to="/clients" 
					className="text-blue-600 hover:text-blue-800 flex items-center gap-1"
				>
					← Back to Clients
				</Link>
				<span className="text-gray-400">•</span>
				<span className="text-gray-600">{client?.name || 'Client'} Services</span>
			</div>

			{/* Header with Client Info */}
			<div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
				<div>
					<div className="flex items-center gap-3 mb-2">
						<div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl flex items-center justify-center text-white font-semibold">
							{client?.name?.charAt(0) || 'C'}
						</div>
						<div>
							<h1 className="text-3xl font-bold text-gray-900">
								{client?.name || 'Client'} Services
							</h1>
							<p className="text-gray-600">Manage service assignments and catalog</p>
						</div>
					</div>
				</div>
				
				{client && (
					<div className="flex flex-wrap gap-4">
						<div className="bg-white rounded-lg border border-gray-200 px-4 py-2">
							<div className="flex items-center gap-2">
								<UsersIcon className="h-4 w-4 text-blue-600" />
								<span className="text-sm text-gray-600">Industry:</span>
								<span className="font-medium text-gray-900">{client.industry}</span>
							</div>
						</div>
						<div className="bg-white rounded-lg border border-gray-200 px-4 py-2">
							<div className="flex items-center gap-2">
								<CurrencyDollarIcon className="h-4 w-4 text-green-600" />
								<span className="text-sm text-gray-600">MRR:</span>
								<span className="font-medium text-gray-900">{formatCurrency(client.mrr)}</span>
							</div>
						</div>
						<div className="bg-white rounded-lg border border-gray-200 px-4 py-2">
							<div className="flex items-center gap-2">
								<ChartBarIcon className="h-4 w-4 text-purple-600" />
								<span className="text-sm text-gray-600">Profitability:</span>
								<span className="font-medium text-gray-900">{formatPercentage(client.profitability)}</span>
							</div>
						</div>
					</div>
				)}
			</div>

			{/* Tab Navigation */}
			<div className="bg-white rounded-xl border border-gray-200 shadow-sm">
				<div className="border-b border-gray-200">
					<nav className="flex space-x-8 px-6" aria-label="Tabs">
						<button
							onClick={() => setActiveTab('assigned')}
							className={`py-4 px-1 border-b-2 font-medium text-sm ${
								activeTab === 'assigned'
									? 'border-blue-500 text-blue-600'
									: 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
							}`}
						>
							<div className="flex items-center gap-2">
								<UsersIcon className="h-4 w-4" />
								Assigned Services
								<span className={`px-2 py-1 text-xs rounded-full ${
									activeTab === 'assigned'
										? 'bg-blue-100 text-blue-600'
										: 'bg-gray-100 text-gray-600'
								}`}>
									{tabCounts.assignedCount}
								</span>
							</div>
						</button>
						<button
							onClick={() => setActiveTab('catalog')}
							className={`py-4 px-1 border-b-2 font-medium text-sm ${
								activeTab === 'catalog'
									? 'border-blue-500 text-blue-600'
									: 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
							}`}
						>
							<div className="flex items-center gap-2">
								<ChartBarIcon className="h-4 w-4" />
								Service Catalog
								<span className={`px-2 py-1 text-xs rounded-full ${
									activeTab === 'catalog'
										? 'bg-blue-100 text-blue-600'
										: 'bg-gray-100 text-gray-600'
								}`}>
									{tabCounts.availableCount}
								</span>
							</div>
						</button>
					</nav>
				</div>

				{/* Tab Content */}
				<div className="p-6">
					{activeTab === 'assigned' && (
						<div>
							<ClientServices 
								key={`services-${refreshKey}`}
								clientId={clientId} 
							/>
						</div>
					)}
					
					{activeTab === 'catalog' && (
						<div>
							<ServiceCatalog 
								key={`catalog-${refreshKey}`}
								clientId={clientId} 
								onServiceAdd={handleServiceAdd}
							/>
						</div>
					)}
				</div>
			</div>

			{/* Quick Actions */}
			<div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl p-6 border border-blue-100">
				<div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
					<div>
						<h3 className="text-lg font-semibold text-gray-900 mb-1">
							Need help with service configuration?
						</h3>
						<p className="text-gray-600">
							Our team can help optimize your service assignments for maximum profitability.
						</p>
					</div>
					<div className="flex flex-wrap gap-3">
						<Link to={`/client-analytics/${clientId}`}>
							<Button variant="outline" size="sm">
								View Analytics
							</Button>
						</Link>
						<Button variant="primary" size="sm">
							Contact Support
						</Button>
					</div>
				</div>
			</div>
		</div>
	)
}
