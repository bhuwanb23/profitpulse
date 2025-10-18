export default function MarketInsights() {
	const marketData = [
		{
			category: 'Market Trends',
			icon: '📈',
			insights: [
				{ 
					trend: 'SMB Security Services Growth', 
					value: '13-15% CAGR', 
					impact: 'high',
					description: 'Strong demand for managed security services',
					opportunity: 'Expand security portfolio'
				},
				{ 
					trend: 'Cloud Backup Adoption', 
					value: '+9% YoY', 
					impact: 'medium',
					description: 'Businesses migrating from on-premise backup',
					opportunity: 'Cloud backup upsell'
				},
				{ 
					trend: 'Zero Trust Architecture', 
					value: '+22% YoY', 
					impact: 'high',
					description: 'Enterprise adoption accelerating',
					opportunity: 'Zero trust consulting'
				}
			]
		},
		{
			category: 'Competitive Intelligence',
			icon: '🎯',
			insights: [
				{ 
					trend: 'Competitor A Strategy', 
					value: 'MDR+NDR Bundle', 
					impact: 'high',
					description: 'Aggressive pricing on security bundles',
					opportunity: 'Counter with value-add services'
				},
				{ 
					trend: 'Competitor B Focus', 
					value: 'vCISO Services', 
					impact: 'medium',
					description: 'Heavy investment in virtual CISO offerings',
					opportunity: 'Develop vCISO capability'
				},
				{ 
					trend: 'Competitor C Innovation', 
					value: 'AI Automation', 
					impact: 'high',
					description: 'Reducing ticket MTTR through automation',
					opportunity: 'Invest in automation tools'
				}
			]
		},
		{
			category: 'Industry Benchmarks',
			icon: '📊',
			insights: [
				{ 
					trend: 'Average MSP Margin', 
					value: '18-25%', 
					impact: 'medium',
					description: 'Industry standard profitability range',
					opportunity: 'Optimize service mix'
				},
				{ 
					trend: 'Client Retention Rate', 
					value: '92% Average', 
					impact: 'high',
					description: 'Top MSPs maintain 95%+ retention',
					opportunity: 'Improve client success'
				},
				{ 
					trend: 'Service Desk Response', 
					value: '< 15 min SLA', 
					impact: 'medium',
					description: 'Industry standard for Tier 1 response',
					opportunity: 'Optimize response times'
				}
			]
		},
		{
			category: 'Emerging Opportunities',
			icon: '🚀',
			insights: [
				{ 
					trend: 'AI/ML Security Tools', 
					value: '+35% Demand', 
					impact: 'high',
					description: 'Growing demand for AI-powered security',
					opportunity: 'Partner with AI security vendors'
				},
				{ 
					trend: 'Compliance as a Service', 
					value: 'High Growth', 
					impact: 'medium',
					description: 'Regulatory compliance outsourcing trend',
					opportunity: 'Develop compliance practice'
				},
				{ 
					trend: 'Remote Work Security', 
					value: 'Sustained Demand', 
					impact: 'high',
					description: 'Permanent shift to hybrid work models',
					opportunity: 'Endpoint security focus'
				}
			]
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

	const getCategoryColor = (category) => {
		const colors = {
			'Market Trends': 'from-blue-50 to-white border-blue-200',
			'Competitive Intelligence': 'from-red-50 to-white border-red-200',
			'Industry Benchmarks': 'from-green-50 to-white border-green-200',
			'Emerging Opportunities': 'from-purple-50 to-white border-purple-200'
		}
		return colors[category] || 'from-gray-50 to-white border-gray-200'
	}

	const totalOpportunities = marketData.reduce((sum, category) => sum + category.insights.length, 0)
	const highImpactCount = marketData.reduce((sum, category) => {
		return sum + category.insights.filter(insight => insight.impact === 'high').length
	}, 0)

	return (
		<section className="bg-gradient-to-br from-indigo-50 to-white rounded-xl border border-gray-200 p-6 shadow-sm">
			<div className="flex items-center justify-between mb-4">
				<h2 className="text-lg font-semibold bg-gradient-to-r from-indigo-600 to-blue-600 bg-clip-text text-transparent">
					🌐 Market Insights
				</h2>
				<div className="text-right">
					<div className="text-sm text-gray-500">High Impact</div>
					<div className="text-lg font-bold text-indigo-600">{highImpactCount} Insights</div>
				</div>
			</div>
			
			<div className="space-y-3 max-h-80 overflow-y-auto">
				{marketData.map((category, categoryIndex) => (
					<div key={categoryIndex} className="bg-white rounded-lg border border-gray-200 p-3 hover:border-indigo-300 transition-all hover:shadow-sm">
						<div className="flex items-center justify-between mb-2">
							<div className="flex items-center gap-2">
								<span className="text-base">{category.icon}</span>
								<h3 className="font-medium text-gray-900 text-sm">{category.category}</h3>
							</div>
							<span className="text-xs text-gray-500">{category.insights.length} insights</span>
						</div>
						
						<div className="space-y-2">
							{category.insights.slice(0, 2).map((insight, insightIndex) => (
								<div key={insightIndex} className="bg-gray-50 rounded p-2">
									<div className="flex items-center justify-between mb-1">
										<h4 className="font-medium text-gray-900 text-xs">{insight.trend}</h4>
										<div className="flex items-center gap-1">
											<span className="text-xs font-bold text-indigo-600">{insight.value}</span>
											<span className={`px-1 py-0.5 rounded text-xs font-medium ${getImpactColor(insight.impact)}`}>
												{insight.impact}
											</span>
										</div>
									</div>
									<p className="text-xs text-gray-600">{insight.description}</p>
									<div className="text-xs text-indigo-700 mt-1">
										<span className="font-medium">→</span> {insight.opportunity}
									</div>
								</div>
							))}
							{category.insights.length > 2 && (
								<div className="text-center">
									<button className="text-xs text-indigo-600 hover:text-indigo-800 font-medium">
										+{category.insights.length - 2} more insights
									</button>
								</div>
							)}
						</div>
					</div>
				))}
			</div>
			
			<div className="mt-6 pt-4 border-t border-gray-200">
				<div className="grid grid-cols-3 gap-4 text-center">
					<div>
						<div className="text-lg font-bold text-blue-600">{totalOpportunities}</div>
						<div className="text-xs text-gray-500">Total Insights</div>
					</div>
					<div>
						<div className="text-lg font-bold text-red-600">{highImpactCount}</div>
						<div className="text-xs text-gray-500">High Impact</div>
					</div>
					<div>
						<div className="text-lg font-bold text-green-600">4</div>
						<div className="text-xs text-gray-500">Categories</div>
					</div>
				</div>
			</div>
		</section>
	)
}
