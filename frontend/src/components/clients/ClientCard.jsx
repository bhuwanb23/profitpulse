import { Badge } from '../ui/Badge'
import { Button } from '../ui/Button'
import { UsersIcon, CurrencyDollarIcon, TrendingUpIcon, TrendingDownIcon, TicketIcon, DotsVerticalIcon } from '../ui/Icons'
import { Link } from 'react-router-dom'

export function ClientCard({ client }) {
	const getProfitabilityColor = (profitability) => {
		if (profitability >= 0.8) return 'success'
		if (profitability >= 0.7) return 'warning'
		return 'danger'
	}

	const getContractStatus = (client) => {
		if (client.contract === 'Annual') return 'info'
		return 'purple'
	}

	const formatCurrency = (amount) => {
		return new Intl.NumberFormat('en-US', {
			style: 'currency',
			currency: 'USD',
			minimumFractionDigits: 0
		}).format(amount)
	}

	const formatPercentage = (value) => {
		return `${(value * 100).toFixed(0)}%`
	}

	return (
		<div className="bg-white rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-shadow duration-200">
			{/* Header */}
			<div className="p-6 pb-4">
				<div className="flex items-start justify-between">
					<div className="flex-1">
						<div className="flex items-center gap-3 mb-2">
							<div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center text-white font-semibold text-sm">
								{client.name.charAt(0)}
							</div>
							<div>
								<h3 className="font-semibold text-gray-900 text-lg">{client.name}</h3>
								<p className="text-sm text-gray-500">{client.industry}</p>
							</div>
						</div>
					</div>
					<div className="flex items-center gap-2">
						<Badge variant={getContractStatus(client)} size="sm">
							{client.contract}
						</Badge>
						<button className="p-1 hover:bg-gray-100 rounded-md transition-colors">
							<DotsVerticalIcon className="h-4 w-4 text-gray-400" />
						</button>
					</div>
				</div>
			</div>

			{/* Metrics */}
			<div className="px-6 pb-4">
				<div className="grid grid-cols-2 gap-4">
					{/* Profitability */}
					<div className="flex items-center gap-3">
						<div className={`p-2 rounded-lg ${
							client.profitability >= 0.8 ? 'bg-green-100' : 
							client.profitability >= 0.7 ? 'bg-yellow-100' : 'bg-red-100'
						}`}>
							{client.profitability >= 0.7 ? (
								<TrendingUpIcon className={`h-4 w-4 ${
									client.profitability >= 0.8 ? 'text-green-600' : 'text-yellow-600'
								}`} />
							) : (
								<TrendingDownIcon className="h-4 w-4 text-red-600" />
							)}
						</div>
						<div>
							<p className="text-xs text-gray-500 uppercase tracking-wide">Profitability</p>
							<p className="font-semibold text-gray-900">{formatPercentage(client.profitability)}</p>
						</div>
					</div>

					{/* MRR */}
					<div className="flex items-center gap-3">
						<div className="p-2 bg-blue-100 rounded-lg">
							<CurrencyDollarIcon className="h-4 w-4 text-blue-600" />
						</div>
						<div>
							<p className="text-xs text-gray-500 uppercase tracking-wide">MRR</p>
							<p className="font-semibold text-gray-900">{formatCurrency(client.mrr)}</p>
						</div>
					</div>

					{/* Contract Value */}
					<div className="flex items-center gap-3">
						<div className="p-2 bg-purple-100 rounded-lg">
							<UsersIcon className="h-4 w-4 text-purple-600" />
						</div>
						<div>
							<p className="text-xs text-gray-500 uppercase tracking-wide">Contract Value</p>
							<p className="font-semibold text-gray-900">{formatCurrency(client.contractValue)}</p>
						</div>
					</div>

					{/* Open Tickets */}
					<div className="flex items-center gap-3">
						<div className="p-2 bg-orange-100 rounded-lg">
							<TicketIcon className="h-4 w-4 text-orange-600" />
						</div>
						<div>
							<p className="text-xs text-gray-500 uppercase tracking-wide">Open Tickets</p>
							<p className="font-semibold text-gray-900">{client.ticketsOpen}</p>
						</div>
					</div>
				</div>
			</div>

			{/* Footer */}
			<div className="px-6 py-4 bg-gray-50 rounded-b-xl border-t border-gray-100">
				<div className="flex items-center justify-between">
					<Badge variant={getProfitabilityColor(client.profitability)} size="sm">
						{client.profitability >= 0.8 ? 'High Profit' : 
						 client.profitability >= 0.7 ? 'Medium Profit' : 'Low Profit'}
					</Badge>
					<div className="flex gap-2">
						<Link to={`/client-analytics/${client.id}`}>
							<Button variant="ghost" size="sm">
								Analytics
							</Button>
						</Link>
						<Link to={`/client-services/${client.id}`}>
							<Button variant="primary" size="sm">
								Services
							</Button>
						</Link>
					</div>
				</div>
			</div>
		</div>
	)
}
