export default function LeakAlerts() {
	const leaks = [
		{ title: 'Unbilled hours (TechStart)', amount: 1500, severity: 'high', confidence: 95, impact: 'Critical' },
		{ title: 'Underpriced service (Acme)', amount: 900, severity: 'medium', confidence: 87, impact: 'High' },
		{ title: 'Unused licenses (RetailMax)', amount: 450, severity: 'low', confidence: 92, impact: 'Medium' },
		{ title: 'Contract renewal opportunity', amount: 2200, severity: 'high', confidence: 89, impact: 'Critical' }
	]
	
	const getSeverityColor = (severity) => {
		const colors = {
			'high': 'bg-red-100 text-red-800 border-red-200',
			'medium': 'bg-yellow-100 text-yellow-800 border-yellow-200',
			'low': 'bg-green-100 text-green-800 border-green-200'
		}
		return colors[severity] || 'bg-gray-100 text-gray-800 border-gray-200'
	}

	const getImpactColor = (impact) => {
		const colors = {
			'Critical': 'bg-red-50 text-red-700',
			'High': 'bg-orange-50 text-orange-700',
			'Medium': 'bg-yellow-50 text-yellow-700'
		}
		return colors[impact] || 'bg-gray-50 text-gray-700'
	}

	const totalPotential = leaks.reduce((sum, leak) => sum + leak.amount, 0)

	return (
		<section className="bg-gradient-to-br from-red-50 to-white rounded-xl border border-gray-200 p-6 shadow-sm">
			<div className="flex items-center justify-between mb-4">
				<h2 className="text-lg font-semibold bg-gradient-to-r from-red-600 to-orange-600 bg-clip-text text-transparent">
					🚨 Revenue Leak Alerts
				</h2>
				<div className="text-right">
					<div className="text-sm text-gray-500">Total Potential</div>
					<div className="text-lg font-bold text-red-600">${totalPotential.toLocaleString()}</div>
				</div>
			</div>
			
			<div className="space-y-3 max-h-80 overflow-y-auto">
				{leaks.map((leak, index) => (
					<div key={index} className={`p-4 rounded-lg border-2 transition-all hover:shadow-sm ${getSeverityColor(leak.severity)}`}>
						<div className="flex items-start justify-between mb-3">
							<div className="flex-1">
								<h3 className="font-medium text-gray-900 text-sm">{leak.title}</h3>
								<p className="text-xs text-gray-600 mt-1">Potential recovery: ${leak.amount.toLocaleString()}</p>
							</div>
							<div className="flex items-center gap-2">
								<span className={`px-2 py-1 rounded-full text-xs font-medium ${getImpactColor(leak.impact)}`}>
									{leak.impact}
								</span>
							</div>
						</div>
						
						<div className="flex items-center justify-between">
							<div className="flex items-center gap-2">
								<span className="text-xs text-gray-500">AI Confidence:</span>
								<div className="w-16 bg-gray-200 rounded-full h-1.5">
									<div 
										className="h-1.5 rounded-full bg-red-500 transition-all duration-300" 
										style={{ width: `${leak.confidence}%` }}
									></div>
								</div>
								<span className="text-xs font-medium text-gray-700">{leak.confidence}%</span>
							</div>
							<button className="text-xs bg-red-100 text-red-700 px-3 py-1 rounded hover:bg-red-200 transition-colors">
								Investigate
							</button>
						</div>
					</div>
				))}
			</div>
			
			<div className="mt-4 pt-4 border-t border-gray-200">
				<button className="w-full bg-gradient-to-r from-red-600 to-orange-600 text-white py-2 px-4 rounded-lg text-sm font-medium hover:from-red-700 hover:to-orange-700 transition-all">
					View All Revenue Leaks
				</button>
			</div>
		</section>
	)
}
