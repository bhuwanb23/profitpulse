import { TrendingUpIcon, TrendingDownIcon } from '../ui/Icons'

export function KPICard({ 
	title, 
	value, 
	change, 
	changeType = 'neutral', 
	icon: Icon, 
	iconColor = 'blue',
	format = 'number',
	className = ""
}) {
	const formatValue = (val) => {
		switch (format) {
			case 'currency':
				return new Intl.NumberFormat('en-US', {
					style: 'currency',
					currency: 'USD',
					minimumFractionDigits: 0
				}).format(val)
			case 'percentage':
				return `${(val * 100).toFixed(1)}%`
			case 'number':
			default:
				return val.toLocaleString()
		}
	}

	const getChangeColor = (type) => {
		switch (type) {
			case 'positive':
				return 'text-green-600'
			case 'negative':
				return 'text-red-600'
			default:
				return 'text-gray-600'
		}
	}

	const getIconBgColor = (color) => {
		const colors = {
			blue: 'bg-blue-100',
			green: 'bg-green-100',
			purple: 'bg-purple-100',
			orange: 'bg-orange-100',
			red: 'bg-red-100',
			yellow: 'bg-yellow-100'
		}
		return colors[color] || colors.blue
	}

	const getIconTextColor = (color) => {
		const colors = {
			blue: 'text-blue-600',
			green: 'text-green-600',
			purple: 'text-purple-600',
			orange: 'text-orange-600',
			red: 'text-red-600',
			yellow: 'text-yellow-600'
		}
		return colors[color] || colors.blue
	}

	return (
		<div className={`bg-white rounded-xl border border-gray-200 shadow-sm p-6 ${className}`}>
			<div className="flex items-center justify-between">
				<div className="flex-1">
					<div className="flex items-center gap-3 mb-3">
						{Icon && (
							<div className={`p-2 rounded-lg ${getIconBgColor(iconColor)}`}>
								<Icon className={`h-5 w-5 ${getIconTextColor(iconColor)}`} />
							</div>
						)}
						<p className="text-sm font-medium text-gray-600">{title}</p>
					</div>
					<p className="text-2xl font-bold text-gray-900 mb-2">
						{formatValue(value)}
					</p>
					{change !== undefined && (
						<div className="flex items-center gap-1">
							{changeType === 'positive' && <TrendingUpIcon className="h-4 w-4 text-green-600" />}
							{changeType === 'negative' && <TrendingDownIcon className="h-4 w-4 text-red-600" />}
							<span className={`text-sm font-medium ${getChangeColor(changeType)}`}>
								{change > 0 ? '+' : ''}{change}%
							</span>
							<span className="text-sm text-gray-500">vs last month</span>
						</div>
					)}
				</div>
			</div>
		</div>
	)
}
