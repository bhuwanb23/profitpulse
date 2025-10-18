export default function ProfitabilityGenome() {
	const genomeData = [
		{ 
			category: 'Labor Efficiency', 
			score: 87, 
			trend: 'up', 
			impact: 'high',
			color: 'emerald',
			icon: '👥',
			details: 'Utilization rate 87%, 13% above target'
		},
		{ 
			category: 'Service Mix', 
			score: 92, 
			trend: 'up', 
			impact: 'high',
			color: 'blue',
			icon: '🛠️',
			details: 'High-margin services 65% of portfolio'
		},
		{ 
			category: 'Pricing Strategy', 
			score: 74, 
			trend: 'stable', 
			impact: 'medium',
			color: 'amber',
			icon: '💰',
			details: 'Market competitive, 8% below premium'
		},
		{ 
			category: 'Ticket Efficiency', 
			score: 89, 
			trend: 'up', 
			impact: 'medium',
			color: 'rose',
			icon: '🎫',
			details: 'Resolution time 15% faster than SLA'
		},
		{ 
			category: 'Project Margins', 
			score: 78, 
			trend: 'down', 
			impact: 'high',
			color: 'indigo',
			icon: '📋',
			details: 'Average margin 23%, down 3% QoQ'
		},
		{ 
			category: 'SaaS Optimization', 
			score: 95, 
			trend: 'up', 
			impact: 'low',
			color: 'cyan',
			icon: '☁️',
			details: 'License utilization 95%, well optimized'
		}
	]

	const getScoreColor = (score) => {
		if (score >= 90) return 'text-green-600'
		if (score >= 80) return 'text-blue-600'
		if (score >= 70) return 'text-yellow-600'
		return 'text-red-600'
	}

	const getTrendIcon = (trend) => {
		if (trend === 'up') return '📈'
		if (trend === 'down') return '📉'
		return '➡️'
	}

	const getImpactColor = (impact) => {
		const colors = {
			'high': 'bg-red-100 text-red-800',
			'medium': 'bg-yellow-100 text-yellow-800',
			'low': 'bg-green-100 text-green-800'
		}
		return colors[impact] || 'bg-gray-100 text-gray-800'
	}

	const getColorClasses = (color) => {
		const colors = {
			emerald: 'from-emerald-50 to-white border-emerald-200',
			blue: 'from-blue-50 to-white border-blue-200',
			amber: 'from-amber-50 to-white border-amber-200',
			rose: 'from-rose-50 to-white border-rose-200',
			indigo: 'from-indigo-50 to-white border-indigo-200',
			cyan: 'from-cyan-50 to-white border-cyan-200'
		}
		return colors[color] || 'from-gray-50 to-white border-gray-200'
	}

	const averageScore = genomeData.reduce((sum, item) => sum + item.score, 0) / genomeData.length

	return (
		<section className="bg-gradient-to-br from-purple-50 to-white rounded-xl border border-gray-200 p-6 shadow-sm">
			<div className="flex items-center justify-between mb-4">
				<h2 className="text-lg font-semibold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
					🧬 Profitability Genome
				</h2>
				<div className="text-right">
					<div className="text-sm text-gray-500">Overall Health</div>
					<div className={`text-lg font-bold ${getScoreColor(averageScore)}`}>{Math.round(averageScore)}%</div>
				</div>
			</div>
			
			<div className="space-y-3">
				{genomeData.map((item, index) => (
					<div key={index} className="bg-white rounded-lg border border-gray-200 p-4 hover:border-purple-300 transition-all hover:shadow-sm">
						<div className="flex items-center justify-between mb-2">
							<div className="flex items-center gap-2">
								<span className="text-base">{item.icon}</span>
								<h3 className="font-medium text-gray-900 text-sm">{item.category}</h3>
							</div>
							<div className="flex items-center gap-2">
								<span className={`text-xl font-bold ${getScoreColor(item.score)}`}>{item.score}%</span>
								<span className="text-sm">{getTrendIcon(item.trend)}</span>
							</div>
						</div>
						
						<div className="flex items-center justify-between mb-2">
							<div className="w-full bg-gray-200 rounded-full h-2 mr-3">
								<div 
									className={`h-2 rounded-full transition-all duration-500 ${
										item.score >= 90 ? 'bg-green-500' : 
										item.score >= 80 ? 'bg-blue-500' : 
										item.score >= 70 ? 'bg-yellow-500' : 'bg-red-500'
									}`}
									style={{ width: `${item.score}%` }}
								></div>
							</div>
							<span className={`px-2 py-1 rounded-full text-xs font-medium ${getImpactColor(item.impact)}`}>
								{item.impact}
							</span>
						</div>
						
						<p className="text-xs text-gray-600">{item.details}</p>
					</div>
				))}
			</div>
			
			<div className="mt-6 pt-4 border-t border-gray-200">
				<div className="grid grid-cols-3 gap-4 text-center">
					<div>
						<div className="text-lg font-bold text-green-600">4</div>
						<div className="text-xs text-gray-500">Healthy Areas</div>
					</div>
					<div>
						<div className="text-lg font-bold text-yellow-600">1</div>
						<div className="text-xs text-gray-500">Needs Attention</div>
					</div>
					<div>
						<div className="text-lg font-bold text-red-600">1</div>
						<div className="text-xs text-gray-500">Critical Areas</div>
					</div>
				</div>
			</div>
		</section>
	)
}
