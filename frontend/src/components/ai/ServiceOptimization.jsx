export default function ServiceOptimization() {
	const optimizations = [
		{ 
			id: 's1', 
			title: 'Migrate Legacy AV to MDR', 
			description: 'Upgrade top 5 clients from basic antivirus to managed detection and response',
			impact: 'high',
			savings: '$18,000',
			effort: 'medium',
			timeline: '3 months',
			clients: 5,
			icon: '🛡️',
			priority: 1
		},
		{ 
			id: 's2', 
			title: 'Tiered Support SLAs', 
			description: 'Introduce premium, standard, and basic support tiers to optimize resource allocation',
			impact: 'medium',
			savings: '$12,500',
			effort: 'low',
			timeline: '6 weeks',
			clients: 15,
			icon: '⏱️',
			priority: 2
		},
		{ 
			id: 's3', 
			title: 'Standardize Backup Vendor', 
			description: 'Consolidate multiple backup solutions to single enterprise vendor',
			impact: 'medium',
			savings: '$8,200',
			effort: 'high',
			timeline: '4 months',
			clients: 12,
			icon: '💾',
			priority: 3
		},
		{ 
			id: 's4', 
			title: 'Automate Patch Management', 
			description: 'Deploy automated patching solution to reduce manual intervention',
			impact: 'high',
			savings: '$15,600',
			effort: 'medium',
			timeline: '2 months',
			clients: 20,
			icon: '🔄',
			priority: 1
		},
		{ 
			id: 's5', 
			title: 'Cloud Migration Services', 
			description: 'Offer comprehensive cloud migration packages for on-premise clients',
			impact: 'high',
			savings: '$25,000',
			effort: 'high',
			timeline: '6 months',
			clients: 8,
			icon: '☁️',
			priority: 1
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

	const getEffortColor = (effort) => {
		const colors = {
			'high': 'bg-red-50 text-red-700',
			'medium': 'bg-yellow-50 text-yellow-700',
			'low': 'bg-green-50 text-green-700'
		}
		return colors[effort] || 'bg-gray-50 text-gray-700'
	}

	const getPriorityColor = (priority) => {
		if (priority === 1) return 'bg-red-500'
		if (priority === 2) return 'bg-yellow-500'
		return 'bg-green-500'
	}

	const totalSavings = optimizations.reduce((sum, opt) => {
		return sum + parseInt(opt.savings.replace(/[$,]/g, ''))
	}, 0)

	const highPriorityCount = optimizations.filter(opt => opt.priority === 1).length

	return (
		<section className="bg-gradient-to-br from-teal-50 to-white rounded-xl border border-gray-200 p-6 shadow-sm">
			<div className="flex items-center justify-between mb-4">
				<h2 className="text-lg font-semibold bg-gradient-to-r from-teal-600 to-cyan-600 bg-clip-text text-transparent">
					⚡ Service Optimization
				</h2>
				<div className="text-right">
					<div className="text-sm text-gray-500">Total Potential</div>
					<div className="text-lg font-bold text-teal-600">${totalSavings.toLocaleString()}</div>
				</div>
			</div>
			
			<div className="space-y-3 max-h-80 overflow-y-auto">
				{optimizations.map((optimization) => (
					<div key={optimization.id} className="bg-white rounded-lg border border-gray-200 p-3 hover:border-teal-300 transition-all hover:shadow-sm">
						<div className="flex items-center justify-between mb-2">
							<div className="flex items-center gap-2">
								<span className="text-base">{optimization.icon}</span>
								<h3 className="font-medium text-gray-900 text-sm">{optimization.title}</h3>
							</div>
							<div className="flex items-center gap-2">
								<div className={`w-2 h-2 rounded-full ${getPriorityColor(optimization.priority)}`}></div>
								<span className="text-sm font-bold text-green-600">{optimization.savings}</span>
							</div>
						</div>
						
						<p className="text-xs text-gray-600 mb-2">{optimization.description}</p>
						
						<div className="flex items-center justify-between text-xs">
							<div className="flex items-center gap-3 text-gray-500">
								<span>{optimization.timeline}</span>
								<span>•</span>
								<span>{optimization.clients} clients</span>
								<span>•</span>
								<span className={`px-1 py-0.5 rounded ${getEffortColor(optimization.effort)}`}>
									{optimization.effort} effort
								</span>
							</div>
							<button className="bg-teal-100 text-teal-700 px-2 py-1 rounded text-xs hover:bg-teal-200 transition-colors">
								Plan
							</button>
						</div>
					</div>
				))}
			</div>
			
			<div className="mt-6 pt-4 border-t border-gray-200">
				<div className="grid grid-cols-3 gap-4 text-center">
					<div>
						<div className="text-lg font-bold text-red-600">{highPriorityCount}</div>
						<div className="text-xs text-gray-500">High Priority</div>
					</div>
					<div>
						<div className="text-lg font-bold text-blue-600">{optimizations.length}</div>
						<div className="text-xs text-gray-500">Total Opportunities</div>
					</div>
					<div>
						<div className="text-lg font-bold text-green-600">{optimizations.reduce((sum, opt) => sum + opt.clients, 0)}</div>
						<div className="text-xs text-gray-500">Affected Clients</div>
					</div>
				</div>
			</div>
		</section>
	)
}
