export default function PredictiveAnalytics() {
	const predictions = [
		{
			title: 'Revenue Forecasting',
			icon: '📈',
			prediction: '+8.4% MoM',
			confidence: 92,
			details: 'Projected next 6 months growth',
			trend: 'positive',
			color: 'blue'
		},
		{
			title: 'Client Churn Risk',
			icon: '⚠️',
			prediction: '3 High Risk',
			confidence: 87,
			details: 'Acme Co (12%), Globex (9%), Umbrella (7%)',
			trend: 'negative',
			color: 'red'
		},
		{
			title: 'Service Demand',
			icon: '🔮',
			prediction: 'MDR +45%',
			confidence: 89,
			details: 'Top rising: MDR, Cloud Backup, Security',
			trend: 'positive',
			color: 'emerald'
		},
		{
			title: 'Budget Optimization',
			icon: '💡',
			prediction: '$2K/mo Savings',
			confidence: 94,
			details: 'Unused SaaS seats, vendor consolidation',
			trend: 'positive',
			color: 'purple'
		},
		{
			title: 'Market Trends',
			icon: '📊',
			prediction: '+14% YoY',
			confidence: 85,
			details: 'SMB security spending acceleration',
			trend: 'positive',
			color: 'amber'
		},
		{
			title: 'Growth Opportunities',
			icon: '🚀',
			prediction: '18 Upsells',
			confidence: 91,
			details: 'M365 Hardening (11), NDR Bundle (7)',
			trend: 'positive',
			color: 'indigo'
		}
	]

	const getColorClasses = (color, trend) => {
		const colors = {
			blue: trend === 'positive' ? 'from-blue-500 to-blue-600' : 'from-blue-400 to-blue-500',
			red: 'from-red-500 to-red-600',
			emerald: 'from-emerald-500 to-emerald-600',
			purple: 'from-purple-500 to-purple-600',
			amber: 'from-amber-500 to-amber-600',
			indigo: 'from-indigo-500 to-indigo-600'
		}
		return colors[color] || 'from-gray-500 to-gray-600'
	}

	const getBgColor = (color) => {
		const colors = {
			blue: 'from-blue-50 to-white',
			red: 'from-red-50 to-white',
			emerald: 'from-emerald-50 to-white',
			purple: 'from-purple-50 to-white',
			amber: 'from-amber-50 to-white',
			indigo: 'from-indigo-50 to-white'
		}
		return colors[color] || 'from-gray-50 to-white'
	}

	const averageConfidence = predictions.reduce((sum, p) => sum + p.confidence, 0) / predictions.length

	return (
		<section className="bg-gradient-to-br from-cyan-50 to-white rounded-xl border border-gray-200 p-6 shadow-sm">
			<div className="flex items-center justify-between mb-4">
				<h2 className="text-lg font-semibold bg-gradient-to-r from-cyan-600 to-blue-600 bg-clip-text text-transparent">
					🔮 Predictive Analytics
				</h2>
				<div className="text-right">
					<div className="text-sm text-gray-500">Avg Confidence</div>
					<div className="text-lg font-bold text-cyan-600">{Math.round(averageConfidence)}%</div>
				</div>
			</div>
			
			<div className="grid grid-cols-1 md:grid-cols-2 gap-4">
				{predictions.map((prediction, index) => (
					<div key={index} className={`bg-gradient-to-br ${getBgColor(prediction.color)} rounded-lg border border-gray-200 p-4 hover:shadow-sm transition-all`}>
						<div className="flex items-start justify-between mb-3">
							<div className="flex items-center gap-2">
								<span className="text-lg">{prediction.icon}</span>
								<h3 className="font-medium text-gray-900 text-sm">{prediction.title}</h3>
							</div>
							<div className={`px-2 py-1 rounded-full text-xs font-medium ${
								prediction.trend === 'positive' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
							}`}>
								{prediction.trend === 'positive' ? '📈' : '📉'}
							</div>
						</div>
						
						<div className="mb-3">
							<div className="text-lg font-bold text-gray-900">{prediction.prediction}</div>
							<p className="text-xs text-gray-600 mt-1">{prediction.details}</p>
						</div>
						
						<div className="flex items-center justify-between">
							<div className="flex items-center gap-2">
								<span className="text-xs text-gray-500">Confidence:</span>
								<div className="w-16 bg-gray-200 rounded-full h-1.5">
									<div 
										className={`h-1.5 rounded-full bg-gradient-to-r ${getColorClasses(prediction.color, prediction.trend)} transition-all duration-300`}
										style={{ width: `${prediction.confidence}%` }}
									></div>
								</div>
								<span className="text-xs font-medium text-gray-700">{prediction.confidence}%</span>
							</div>
							<button className={`text-xs bg-gradient-to-r ${getColorClasses(prediction.color, prediction.trend)} text-white px-3 py-1 rounded hover:opacity-90 transition-opacity`}>
								Details
							</button>
						</div>
					</div>
				))}
			</div>
			
			<div className="mt-6 pt-4 border-t border-gray-200">
				<div className="grid grid-cols-3 gap-4 text-center">
					<div>
						<div className="text-lg font-bold text-green-600">+$156K</div>
						<div className="text-xs text-gray-500">Predicted Revenue</div>
					</div>
					<div>
						<div className="text-lg font-bold text-blue-600">94%</div>
						<div className="text-xs text-gray-500">Model Accuracy</div>
					</div>
					<div>
						<div className="text-lg font-bold text-purple-600">18</div>
						<div className="text-xs text-gray-500">Opportunities</div>
					</div>
				</div>
			</div>
		</section>
	)
}
