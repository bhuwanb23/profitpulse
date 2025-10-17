import ClientAnalytics from '../components/clients/ClientAnalytics'
import { Button } from '../components/ui/Button'
import { Badge } from '../components/ui/Badge'
import { TrendingUpIcon, CurrencyDollarIcon, UsersIcon, ChartBarIcon } from '../components/ui/Icons'
import { useParams, Link } from 'react-router-dom'
import { mockClients } from '../services/mockClients'

export default function ClientAnalyticsPage() {
	const { id } = useParams()
	const clientId = id || 'c1'
	
	// Get client info for the header
	const client = mockClients.find(c => c.id === clientId)

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

	const getProfitabilityColor = (profitability) => {
		if (profitability >= 0.8) return 'success'
		if (profitability >= 0.7) return 'warning'
		return 'danger'
	}

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
				<span className="text-gray-600">{client?.name || 'Client'} Analytics</span>
			</div>

			{/* Enhanced Header with Client Info */}
			<div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
				<div>
					<div className="flex items-center gap-3 mb-3">
						<div className="w-12 h-12 bg-gradient-to-br from-green-500 to-green-600 rounded-xl flex items-center justify-center text-white font-semibold">
							{client?.name?.charAt(0) || 'C'}
						</div>
						<div>
							<h1 className="text-3xl font-bold text-gray-900">
								{client?.name || 'Client'} Analytics
							</h1>
							<p className="text-gray-600">Performance insights and profitability analysis</p>
						</div>
					</div>
					
					{client && (
						<div className="flex flex-wrap items-center gap-3">
							<Badge variant={getProfitabilityColor(client.profitability)} size="md">
								{client.profitability >= 0.8 ? 'High Profit' : 
								 client.profitability >= 0.7 ? 'Medium Profit' : 'Low Profit'}
							</Badge>
							<span className="text-sm text-gray-500">•</span>
							<span className="text-sm text-gray-600">{client.industry}</span>
							<span className="text-sm text-gray-500">•</span>
							<span className="text-sm text-gray-600">{client.contract} Contract</span>
						</div>
					)}
				</div>
				
				<div className="flex flex-wrap gap-3">
					<Link to={`/client-services/${clientId}`}>
						<Button variant="outline" size="sm" className="flex items-center gap-2">
							<UsersIcon className="h-4 w-4" />
							Manage Services
						</Button>
					</Link>
					<Button variant="outline" size="sm" className="flex items-center gap-2">
						<ChartBarIcon className="h-4 w-4" />
						Export Report
					</Button>
					<Button variant="primary" size="sm" className="flex items-center gap-2">
						<TrendingUpIcon className="h-4 w-4" />
						View Recommendations
					</Button>
				</div>
			</div>

			{/* Quick Stats Bar */}
			{client && (
				<div className="bg-gradient-to-r from-gray-50 to-blue-50 rounded-xl p-6 border border-gray-200">
					<div className="grid grid-cols-2 md:grid-cols-4 gap-6">
						<div className="text-center">
							<div className="flex items-center justify-center mb-2">
								<CurrencyDollarIcon className="h-5 w-5 text-green-600" />
							</div>
							<p className="text-2xl font-bold text-gray-900">{formatCurrency(client.contractValue)}</p>
							<p className="text-sm text-gray-600">Contract Value</p>
						</div>
						<div className="text-center">
							<div className="flex items-center justify-center mb-2">
								<CurrencyDollarIcon className="h-5 w-5 text-blue-600" />
							</div>
							<p className="text-2xl font-bold text-gray-900">{formatCurrency(client.mrr)}</p>
							<p className="text-sm text-gray-600">Monthly Revenue</p>
						</div>
						<div className="text-center">
							<div className="flex items-center justify-center mb-2">
								<TrendingUpIcon className="h-5 w-5 text-purple-600" />
							</div>
							<p className="text-2xl font-bold text-gray-900">{formatPercentage(client.profitability)}</p>
							<p className="text-sm text-gray-600">Profitability</p>
						</div>
						<div className="text-center">
							<div className="flex items-center justify-center mb-2">
								<UsersIcon className="h-5 w-5 text-orange-600" />
							</div>
							<p className="text-2xl font-bold text-gray-900">{client.ticketsOpen}</p>
							<p className="text-sm text-gray-600">Open Tickets</p>
						</div>
					</div>
				</div>
			)}

			{/* Analytics Component */}
			<ClientAnalytics />

			{/* Action Items */}
			<div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl p-6 border border-blue-100">
				<div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
					<div>
						<h3 className="text-lg font-semibold text-gray-900 mb-1">
							Ready to optimize performance?
						</h3>
						<p className="text-gray-600">
							Based on the analytics, we can suggest improvements to increase profitability and client satisfaction.
						</p>
					</div>
					<div className="flex flex-wrap gap-3">
						<Button variant="outline" size="sm">
							Schedule Review
						</Button>
						<Button variant="primary" size="sm">
							Get AI Recommendations
						</Button>
					</div>
				</div>
			</div>
		</div>
	)
}
