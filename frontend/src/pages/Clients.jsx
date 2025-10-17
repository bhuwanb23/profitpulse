import { useState, useMemo } from 'react'
import { ClientCard } from '../components/clients/ClientCard'
import { Button } from '../components/ui/Button'
import { SearchInput } from '../components/ui/Input'
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/Card'
import { PlusIcon, FilterIcon, UsersIcon, CurrencyDollarIcon, TrendingUpIcon } from '../components/ui/Icons'
import { mockClients } from '../services/mockClients'

export default function Clients() {
	const [searchQuery, setSearchQuery] = useState('')
	const [industryFilter, setIndustryFilter] = useState('all')
	const [contractFilter, setContractFilter] = useState('all')
	const [sortBy, setSortBy] = useState('name')

	// Get unique industries for filter
	const industries = useMemo(() => {
		const unique = [...new Set(mockClients.map(client => client.industry))]
		return ['all', ...unique]
	}, [])

	// Filter and sort clients
	const filteredClients = useMemo(() => {
		let filtered = mockClients.filter(client => {
			const matchesSearch = client.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
								client.industry.toLowerCase().includes(searchQuery.toLowerCase())
			const matchesIndustry = industryFilter === 'all' || client.industry === industryFilter
			const matchesContract = contractFilter === 'all' || client.contract === contractFilter
			
			return matchesSearch && matchesIndustry && matchesContract
		})

		// Sort clients
		filtered.sort((a, b) => {
			switch (sortBy) {
				case 'name':
					return a.name.localeCompare(b.name)
				case 'profitability':
					return b.profitability - a.profitability
				case 'mrr':
					return b.mrr - a.mrr
				case 'contractValue':
					return b.contractValue - a.contractValue
				default:
					return 0
			}
		})

		return filtered
	}, [searchQuery, industryFilter, contractFilter, sortBy])

	// Calculate summary stats
	const stats = useMemo(() => {
		const totalClients = filteredClients.length
		const totalMRR = filteredClients.reduce((sum, client) => sum + client.mrr, 0)
		const avgProfitability = filteredClients.reduce((sum, client) => sum + client.profitability, 0) / totalClients || 0
		const totalContractValue = filteredClients.reduce((sum, client) => sum + client.contractValue, 0)

		return {
			totalClients,
			totalMRR,
			avgProfitability,
			totalContractValue
		}
	}, [filteredClients])

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

	return (
		<div className="space-y-6">
			{/* Header */}
			<div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
				<div>
					<h1 className="text-3xl font-bold text-gray-900">Clients</h1>
					<p className="text-gray-600 mt-1">Manage your client relationships and track performance</p>
				</div>
				<Button className="flex items-center gap-2">
					<PlusIcon className="h-4 w-4" />
					New Client
				</Button>
			</div>

			{/* Stats Overview */}
			<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
				<Card>
					<CardContent className="p-6">
						<div className="flex items-center gap-4">
							<div className="p-3 bg-blue-100 rounded-lg">
								<UsersIcon className="h-6 w-6 text-blue-600" />
							</div>
							<div>
								<p className="text-sm text-gray-600">Total Clients</p>
								<p className="text-2xl font-bold text-gray-900">{stats.totalClients}</p>
							</div>
						</div>
					</CardContent>
				</Card>

				<Card>
					<CardContent className="p-6">
						<div className="flex items-center gap-4">
							<div className="p-3 bg-green-100 rounded-lg">
								<CurrencyDollarIcon className="h-6 w-6 text-green-600" />
							</div>
							<div>
								<p className="text-sm text-gray-600">Total MRR</p>
								<p className="text-2xl font-bold text-gray-900">{formatCurrency(stats.totalMRR)}</p>
							</div>
						</div>
					</CardContent>
				</Card>

				<Card>
					<CardContent className="p-6">
						<div className="flex items-center gap-4">
							<div className="p-3 bg-purple-100 rounded-lg">
								<TrendingUpIcon className="h-6 w-6 text-purple-600" />
							</div>
							<div>
								<p className="text-sm text-gray-600">Avg Profitability</p>
								<p className="text-2xl font-bold text-gray-900">{formatPercentage(stats.avgProfitability)}</p>
							</div>
						</div>
					</CardContent>
				</Card>

				<Card>
					<CardContent className="p-6">
						<div className="flex items-center gap-4">
							<div className="p-3 bg-orange-100 rounded-lg">
								<CurrencyDollarIcon className="h-6 w-6 text-orange-600" />
							</div>
							<div>
								<p className="text-sm text-gray-600">Contract Value</p>
								<p className="text-2xl font-bold text-gray-900">{formatCurrency(stats.totalContractValue)}</p>
							</div>
						</div>
					</CardContent>
				</Card>
			</div>

			{/* Filters and Search */}
			<Card>
				<CardContent className="p-6">
					<div className="flex flex-col lg:flex-row gap-4">
						<div className="flex-1">
							<SearchInput
								placeholder="Search clients by name or industry..."
								value={searchQuery}
								onChange={(e) => setSearchQuery(e.target.value)}
								className="w-full"
							/>
						</div>
						<div className="flex flex-wrap gap-3">
							<select
								value={industryFilter}
								onChange={(e) => setIndustryFilter(e.target.value)}
								className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
							>
								{industries.map(industry => (
									<option key={industry} value={industry}>
										{industry === 'all' ? 'All Industries' : industry}
									</option>
								))}
							</select>
							<select
								value={contractFilter}
								onChange={(e) => setContractFilter(e.target.value)}
								className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
							>
								<option value="all">All Contracts</option>
								<option value="Annual">Annual</option>
								<option value="Monthly">Monthly</option>
							</select>
							<select
								value={sortBy}
								onChange={(e) => setSortBy(e.target.value)}
								className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
							>
								<option value="name">Sort by Name</option>
								<option value="profitability">Sort by Profitability</option>
								<option value="mrr">Sort by MRR</option>
								<option value="contractValue">Sort by Contract Value</option>
							</select>
						</div>
					</div>
				</CardContent>
			</Card>

			{/* Client Grid */}
			<div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
				{filteredClients.map(client => (
					<ClientCard key={client.id} client={client} />
				))}
			</div>

			{/* Empty State */}
			{filteredClients.length === 0 && (
				<Card>
					<CardContent className="p-12 text-center">
						<UsersIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
						<h3 className="text-lg font-semibold text-gray-900 mb-2">No clients found</h3>
						<p className="text-gray-600 mb-6">
							{searchQuery || industryFilter !== 'all' || contractFilter !== 'all'
								? 'Try adjusting your search or filters'
								: 'Get started by adding your first client'}
						</p>
						<Button>
							<PlusIcon className="h-4 w-4 mr-2" />
							Add Client
						</Button>
					</CardContent>
				</Card>
			)}
		</div>
	)
}

