export default function PricingRecommendations() {
	const recommendations = [
		{ 
			id: 'p1', 
			title: 'Help Desk Price Increase', 
			description: 'Raise per-user pricing from $35 to $42 based on market analysis',
			currentPrice: '$35',
			recommendedPrice: '$42',
			impact: 'high',
			confidence: 94,
			affectedClients: 18,
			monthlyIncrease: '$2,520',
			annualIncrease: '$30,240',
			icon: '🎧',
			marketPosition: 'Below Market',
			riskLevel: 'low'
		},
		{ 
			id: 'p2', 
			title: '24/7 Coverage Premium', 
			description: 'Add 10% premium for round-the-clock support services',
			currentPrice: 'Standard',
			recommendedPrice: '+10%',
			impact: 'medium',
			confidence: 87,
			affectedClients: 12,
			monthlyIncrease: '$1,800',
			annualIncrease: '$21,600',
			icon: '🌙',
			marketPosition: 'Competitive',
			riskLevel: 'low'
		},
		{ 
			id: 'p3', 
			title: 'M365 Security Bundle', 
			description: 'Bundle Microsoft 365 hardening services at $6 per user',
			currentPrice: 'N/A',
			recommendedPrice: '$6/user',
			impact: 'medium',
			confidence: 91,
			affectedClients: 15,
			monthlyIncrease: '$4,500',
			annualIncrease: '$54,000',
			icon: '🛡️',
			marketPosition: 'Premium',
			riskLevel: 'medium'
		},
		{ 
			id: 'p4', 
			title: 'Backup Service Tier', 
			description: 'Introduce premium backup tier with faster recovery SLA',
			currentPrice: '$8/GB',
			recommendedPrice: '$12/GB',
			impact: 'high',
			confidence: 89,
			affectedClients: 8,
			monthlyIncrease: '$1,920',
			annualIncrease: '$23,040',
			icon: '💾',
			marketPosition: 'Market Rate',
			riskLevel: 'medium'
		},
		{ 
			id: 'p5', 
			title: 'Cybersecurity Assessment', 
			description: 'Annual security assessment service at premium pricing',
			currentPrice: 'N/A',
			recommendedPrice: '$2,500',
			impact: 'high',
			confidence: 92,
			affectedClients: 10,
			monthlyIncrease: '$2,083',
			annualIncrease: '$25,000',
			icon: '🔒',
			marketPosition: 'Premium',
			riskLevel: 'low'
		}
	]

	const getImpactColor = (impact) => {
		const colors = {
			'high': 'bg-red-100 text-red-800',
			'medium': 'bg-yellow-100 text-yellow-800',
			'low': 'bg-green-100 text-green-800'
		}
		return colors[impact] || 'bg-gray-100 text-gray-800'
	}

	const getRiskColor = (risk) => {
		const colors = {
			'high': 'bg-red-50 text-red-700',
			'medium': 'bg-yellow-50 text-yellow-700',
			'low': 'bg-green-50 text-green-700'
		}
		return colors[risk] || 'bg-gray-50 text-gray-700'
	}

	const getMarketColor = (position) => {
		const colors = {
			'Below Market': 'bg-red-100 text-red-800',
			'Market Rate': 'bg-blue-100 text-blue-800',
			'Competitive': 'bg-green-100 text-green-800',
			'Premium': 'bg-purple-100 text-purple-800'
		}
		return colors[position] || 'bg-gray-100 text-gray-800'
	}

	const totalMonthlyIncrease = recommendations.reduce((sum, rec) => {
		return sum + parseInt(rec.monthlyIncrease.replace(/[$,]/g, ''))
	}, 0)

	const totalAnnualIncrease = recommendations.reduce((sum, rec) => {
		return sum + parseInt(rec.annualIncrease.replace(/[$,]/g, ''))
	}, 0)

	const averageConfidence = recommendations.reduce((sum, rec) => sum + rec.confidence, 0) / recommendations.length

	return (
		<section className="bg-gradient-to-br from-orange-50 to-white rounded-xl border border-gray-200 p-6 shadow-sm">
			<div className="flex items-center justify-between mb-4">
				<h2 className="text-lg font-semibold bg-gradient-to-r from-orange-600 to-red-600 bg-clip-text text-transparent">
					💰 Pricing Recommendations
				</h2>
				<div className="text-right">
					<div className="text-sm text-gray-500">Annual Potential</div>
					<div className="text-lg font-bold text-orange-600">${totalAnnualIncrease.toLocaleString()}</div>
				</div>
			</div>
			
			<div className="space-y-3 max-h-80 overflow-y-auto">
				{recommendations.map((rec) => (
					<div key={rec.id} className="bg-white rounded-lg border border-gray-200 p-3 hover:border-orange-300 transition-all hover:shadow-sm">
						<div className="flex items-center justify-between mb-2">
							<div className="flex items-center gap-2">
								<span className="text-base">{rec.icon}</span>
								<h3 className="font-medium text-gray-900 text-sm">{rec.title}</h3>
							</div>
							<div className="text-right">
								<div className="text-sm font-bold text-green-600">{rec.monthlyIncrease}</div>
								<div className="text-xs text-gray-500">monthly</div>
							</div>
						</div>
						
						<p className="text-xs text-gray-600 mb-2">{rec.description}</p>
						
						<div className="flex items-center justify-between mb-2">
							<div className="text-xs">
								<span className="text-gray-500">Price: </span>
								<span className="font-medium text-gray-900">{rec.currentPrice} → {rec.recommendedPrice}</span>
							</div>
							<span className={`px-2 py-1 rounded-full text-xs font-medium ${getMarketColor(rec.marketPosition)}`}>
								{rec.marketPosition}
							</span>
						</div>
						
						<div className="flex items-center justify-between text-xs">
							<div className="flex items-center gap-3 text-gray-500">
								<span>{rec.affectedClients} clients</span>
								<span>•</span>
								<span className={`px-1 py-0.5 rounded ${getRiskColor(rec.riskLevel)}`}>
									{rec.riskLevel} risk
								</span>
								<span>•</span>
								<span>{rec.confidence}% confidence</span>
							</div>
							<button className="bg-orange-100 text-orange-700 px-2 py-1 rounded text-xs hover:bg-orange-200 transition-colors">
								Apply
							</button>
						</div>
					</div>
				))}
			</div>
			
			<div className="mt-6 pt-4 border-t border-gray-200">
				<div className="grid grid-cols-3 gap-4 text-center">
					<div>
						<div className="text-lg font-bold text-green-600">${totalMonthlyIncrease.toLocaleString()}</div>
						<div className="text-xs text-gray-500">Monthly Increase</div>
					</div>
					<div>
						<div className="text-lg font-bold text-blue-600">{Math.round(averageConfidence)}%</div>
						<div className="text-xs text-gray-500">Avg Confidence</div>
					</div>
					<div>
						<div className="text-lg font-bold text-purple-600">{recommendations.reduce((sum, rec) => sum + rec.affectedClients, 0)}</div>
						<div className="text-xs text-gray-500">Total Clients</div>
					</div>
				</div>
			</div>
		</section>
	)
}
