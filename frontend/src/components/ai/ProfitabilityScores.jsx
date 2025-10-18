export default function ProfitabilityScores() {
	const items = [
		{ client: 'Acme Corp', score: 0.85, revenue: 45000, trend: 'up', category: 'Enterprise' },
		{ client: 'TechStart Inc', score: 0.78, revenue: 32000, trend: 'stable', category: 'Mid-Market' },
		{ client: 'RetailMax Ltd', score: 0.62, revenue: 18000, trend: 'down', category: 'Small Business' },
		{ client: 'HealthPlus', score: 0.80, revenue: 38000, trend: 'up', category: 'Enterprise' },
		{ client: 'FinanceFirst', score: 0.74, revenue: 28000, trend: 'stable', category: 'Mid-Market' },
	]

	const getScoreColor = (score) => {
		if (score >= 0.8) return 'bg-green-500'
		if (score >= 0.7) return 'bg-yellow-500'
		return 'bg-red-500'
	}

	const getTrendIcon = (trend) => {
		if (trend === 'up') return '📈'
		if (trend === 'down') return '📉'
		return '➡️'
	}

	const getCategoryColor = (category) => {
		const colors = {
			'Enterprise': 'bg-purple-100 text-purple-800',
			'Mid-Market': 'bg-blue-100 text-blue-800',
			'Small Business': 'bg-green-100 text-green-800'
		}
		return colors[category] || 'bg-gray-100 text-gray-800'
	}

	const averageScore = items.reduce((sum, item) => sum + item.score, 0) / items.length

	return (
		<section className="bg-gradient-to-br from-green-50 to-white rounded-xl border border-gray-200 p-6 shadow-sm">
			<div className="flex items-center justify-between mb-4">
				<h2 className="text-lg font-semibold bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">
					💰 Profitability Scores
				</h2>
				<div className="text-right">
					<div className="text-sm text-gray-500">Average Score</div>
					<div className="text-lg font-bold text-green-600">{Math.round(averageScore * 100)}%</div>
				</div>
			</div>
			
			<div className="space-y-4 max-h-80 overflow-y-auto">
				{items.map((item, index) => (
					<div key={index} className="bg-white rounded-lg border border-gray-200 p-4 hover:border-green-300 transition-all hover:shadow-sm">
						<div className="flex items-center justify-between mb-3">
							<div className="flex items-center gap-3">
								<div className="flex-1">
									<h3 className="font-medium text-gray-900 text-sm">{item.client}</h3>
									<p className="text-xs text-gray-500">Revenue: ${item.revenue.toLocaleString()}</p>
								</div>
							</div>
							<div className="flex items-center gap-2">
								<span className={`px-2 py-1 rounded-full text-xs font-medium ${getCategoryColor(item.category)}`}>
									{item.category}
								</span>
								<span className="text-lg">{getTrendIcon(item.trend)}</span>
							</div>
						</div>
						
						<div className="flex items-center gap-3">
							<div className="flex-1 h-3 bg-gray-200 rounded-full overflow-hidden">
								<div 
									className={`h-3 rounded-full transition-all duration-500 ${getScoreColor(item.score)}`}
									style={{ width: `${item.score * 100}%` }}
								></div>
							</div>
							<div className="w-12 text-right">
								<span className="text-sm font-bold text-gray-900">{Math.round(item.score * 100)}%</span>
							</div>
						</div>
						
						<div className="mt-2 flex items-center justify-between text-xs text-gray-500">
							<span>Profitability Index</span>
							<span className={`font-medium ${
								item.score >= 0.8 ? 'text-green-600' : 
								item.score >= 0.7 ? 'text-yellow-600' : 'text-red-600'
							}`}>
								{item.score >= 0.8 ? 'Excellent' : item.score >= 0.7 ? 'Good' : 'Needs Attention'}
							</span>
						</div>
					</div>
				))}
			</div>
			
			<div className="mt-4 pt-4 border-t border-gray-200">
				<button className="w-full bg-gradient-to-r from-green-600 to-emerald-600 text-white py-2 px-4 rounded-lg text-sm font-medium hover:from-green-700 hover:to-emerald-700 transition-all">
					Optimize All Clients
				</button>
			</div>
		</section>
	)
}
