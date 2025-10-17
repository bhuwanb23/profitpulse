import { useMemo, useState } from 'react'
import { ServiceCard } from './ServiceCard'
import { SearchInput } from '../ui/Input'
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card'
import { Badge } from '../ui/Badge'
import { ChartBarIcon, FilterIcon } from '../ui/Icons'
import { mockServices, mockAssignments } from '../../services/mockClients'

export default function ServiceCatalog({ clientId, onServiceAdd }) {
	const [searchQuery, setSearchQuery] = useState('')
	const [categoryFilter, setCategoryFilter] = useState('all')

	const categories = useMemo(() => {
		const unique = [...new Set(mockServices.map(s => s.category))]
		return ['all', ...unique]
	}, [])

	const assignedServiceIds = useMemo(() => {
		if (!clientId || !mockAssignments[clientId]) return []
		return mockAssignments[clientId].map(a => a.serviceId)
	}, [clientId])

	const filteredServices = useMemo(() => {
		return mockServices.filter(service => {
			const matchesSearch = service.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
								service.category.toLowerCase().includes(searchQuery.toLowerCase())
			const matchesCategory = categoryFilter === 'all' || service.category === categoryFilter
			
			return matchesSearch && matchesCategory
		})
	}, [searchQuery, categoryFilter])

	const serviceStats = useMemo(() => {
		const totalServices = filteredServices.length
		const assignedCount = filteredServices.filter(s => assignedServiceIds.includes(s.id)).length
		const availableCount = totalServices - assignedCount
		
		return { totalServices, assignedCount, availableCount }
	}, [filteredServices, assignedServiceIds])

	const getCategoryColor = (category) => {
		const colors = {
			support: 'blue',
			maintenance: 'green',
			consulting: 'purple',
			security: 'orange'
		}
		return colors[category] || 'default'
	}

	const handleAddService = (service) => {
		onServiceAdd?.(service)
	}

	return (
		<div>
			{/* Header */}
			<div className="mb-6">
				<div className="flex items-center justify-between mb-4">
					<div>
						<h2 className="text-xl font-semibold text-gray-900">Service Catalog</h2>
						<p className="text-sm text-gray-600 mt-1">Browse and add services to this client</p>
					</div>
					<div className="flex items-center gap-2 text-sm text-gray-600">
						<span className="font-medium">{serviceStats.availableCount}</span>
						<span>available</span>
						<span className="text-gray-400">•</span>
						<span className="font-medium">{serviceStats.assignedCount}</span>
						<span>assigned</span>
					</div>
				</div>
			</div>

			{/* Search and Filters */}
				<div className="mb-6 space-y-4">
					<SearchInput
						placeholder="Search services by name or category..."
						value={searchQuery}
						onChange={(e) => setSearchQuery(e.target.value)}
						className="w-full"
					/>
					
					<div className="flex flex-wrap gap-2">
						{categories.map(category => (
							<button
								key={category}
								onClick={() => setCategoryFilter(category)}
								className={`px-3 py-1.5 text-sm rounded-lg border transition-colors ${
									categoryFilter === category
										? 'bg-blue-50 border-blue-200 text-blue-700'
										: 'bg-white border-gray-200 text-gray-600 hover:bg-gray-50'
								}`}
							>
								{category === 'all' ? 'All Categories' : category}
							</button>
						))}
					</div>
				</div>

				{/* Service Stats */}
				<div className="mb-6 grid grid-cols-2 md:grid-cols-4 gap-4">
					<div className="text-center p-3 bg-gray-50 rounded-lg">
						<p className="text-2xl font-bold text-gray-900">{serviceStats.totalServices}</p>
						<p className="text-xs text-gray-600">Total Services</p>
					</div>
					<div className="text-center p-3 bg-blue-50 rounded-lg">
						<p className="text-2xl font-bold text-blue-600">{serviceStats.availableCount}</p>
						<p className="text-xs text-gray-600">Available</p>
					</div>
					<div className="text-center p-3 bg-green-50 rounded-lg">
						<p className="text-2xl font-bold text-green-600">{serviceStats.assignedCount}</p>
						<p className="text-xs text-gray-600">Assigned</p>
					</div>
					<div className="text-center p-3 bg-purple-50 rounded-lg">
						<p className="text-2xl font-bold text-purple-600">
							{categories.length - 1}
						</p>
						<p className="text-xs text-gray-600">Categories</p>
					</div>
				</div>

				{/* Services Grid */}
				<div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-4">
					{filteredServices.map(service => (
						<ServiceCard
							key={service.id}
							service={service}
							isAssigned={assignedServiceIds.includes(service.id)}
							onAddToClient={handleAddService}
						/>
					))}
				</div>

				{/* Empty State */}
				{filteredServices.length === 0 && (
					<div className="text-center py-12">
						<ChartBarIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
						<h3 className="text-lg font-semibold text-gray-900 mb-2">No services found</h3>
						<p className="text-gray-600">
							{searchQuery || categoryFilter !== 'all'
								? 'Try adjusting your search or filters'
								: 'No services available in the catalog'}
						</p>
					</div>
				)}
		</div>
	)
}
