import { useMemo, useState } from 'react'

const baseItems = [
	{ id: 'r1', title: 'Increase Help Desk Pricing', impact: 'high', confidence: 0.85, type: 'pricing', savings: '$15,000', description: 'Market analysis shows 20% pricing increase opportunity' },
	{ id: 'r2', title: 'Add Network Monitoring', impact: 'medium', confidence: 0.75, type: 'service', savings: '$8,500', description: 'Upsell opportunity for 60% of existing clients' },
	{ id: 'r3', title: 'Optimize Software Licenses', impact: 'low', confidence: 0.70, type: 'budget', savings: '$3,200', description: 'Reduce unused licenses and consolidate vendors' },
	{ id: 'r4', title: 'Security Assessment Upsell', impact: 'medium', confidence: 0.73, type: 'service', savings: '$12,000', description: 'High demand service with 85% close rate' },
	{ id: 'r5', title: 'Automate Routine Tasks', impact: 'high', confidence: 0.88, type: 'efficiency', savings: '$22,000', description: 'Reduce manual work by 40% through automation' },
]

export default function AIRecommendationPanel() {
	const [filterImpact, setFilterImpact] = useState('all')
	const [filterType, setFilterType] = useState('all')
	const [filterStatus, setFilterStatus] = useState('open')
	const [history, setHistory] = useState([])
	const [items, setItems] = useState(baseItems.map(i => ({ ...i, status: 'open' })))

	const filtered = useMemo(() => items.filter(i => {
		const fi = filterImpact === 'all' || i.impact === filterImpact
		const ft = filterType === 'all' || i.type === filterType
		const fs = filterStatus === 'all' || i.status === filterStatus
		return fi && ft && fs
	}), [items, filterImpact, filterType, filterStatus])

	const accept = (id) => {
		setItems(prev => prev.map(i => i.id === id ? { ...i, status: 'accepted' } : i))
		const rec = items.find(i => i.id === id)
		if (rec) setHistory(prev => [{ id: `${id}-${Date.now()}`, action: 'accepted', title: rec.title, at: new Date().toISOString() }, ...prev])
	}
	const dismiss = (id) => {
		setItems(prev => prev.map(i => i.id === id ? { ...i, status: 'dismissed' } : i))
		const rec = items.find(i => i.id === id)
		if (rec) setHistory(prev => [{ id: `${id}-${Date.now()}`, action: 'dismissed', title: rec.title, at: new Date().toISOString() }, ...prev])
	}

	const getImpactColor = (impact) => {
		const colors = {
			'high': 'bg-red-100 text-red-800',
			'medium': 'bg-yellow-100 text-yellow-800',
			'low': 'bg-green-100 text-green-800'
		}
		return colors[impact] || 'bg-gray-100 text-gray-800'
	}

	const getTypeColor = (type) => {
		const colors = {
			'pricing': 'bg-purple-100 text-purple-800',
			'service': 'bg-blue-100 text-blue-800',
			'budget': 'bg-orange-100 text-orange-800',
			'efficiency': 'bg-indigo-100 text-indigo-800'
		}
		return colors[type] || 'bg-gray-100 text-gray-800'
	}

	const totalPotentialSavings = filtered.reduce((sum, item) => {
		const amount = parseInt(item.savings.replace(/[$,]/g, ''))
		return sum + amount
	}, 0)

	return (
		<section className="bg-gradient-to-br from-indigo-50 to-white rounded-xl border border-gray-200 p-6 shadow-sm">
			<div className="flex items-center justify-between mb-4">
				<div>
					<h2 className="text-lg font-semibold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
						🎯 AI Recommendations
					</h2>
					<p className="text-sm text-gray-500">Potential savings: ${totalPotentialSavings.toLocaleString()}</p>
				</div>
				<div className="flex gap-2 text-sm">
					<select value={filterImpact} onChange={(e) => setFilterImpact(e.target.value)} className="border border-gray-300 rounded-lg px-3 py-1 bg-white">
						<option value="all">All impacts</option>
						<option value="high">High</option>
						<option value="medium">Medium</option>
						<option value="low">Low</option>
					</select>
					<select value={filterType} onChange={(e) => setFilterType(e.target.value)} className="border border-gray-300 rounded-lg px-3 py-1 bg-white">
						<option value="all">All types</option>
						<option value="pricing">Pricing</option>
						<option value="service">Service</option>
						<option value="budget">Budget</option>
						<option value="efficiency">Efficiency</option>
					</select>
				</div>
			</div>
			
			<div className="space-y-4 max-h-80 overflow-y-auto">
				{filtered.map((rec) => (
					<div key={rec.id} className="bg-white rounded-lg border border-gray-200 p-4 hover:border-indigo-300 transition-all hover:shadow-sm">
						<div className="flex items-start justify-between mb-3">
							<div className="flex-1">
								<h3 className="font-medium text-gray-900 text-sm">{rec.title}</h3>
								<p className="text-xs text-gray-600 mt-1">{rec.description}</p>
								<p className="text-xs text-green-600 font-medium mt-1">Potential savings: {rec.savings}</p>
							</div>
							<div className="flex items-center gap-2">
								<span className={`px-2 py-1 rounded-full text-xs font-medium ${getImpactColor(rec.impact)}`}>
									{rec.impact}
								</span>
								<span className={`px-2 py-1 rounded-full text-xs font-medium ${getTypeColor(rec.type)}`}>
									{rec.type}
								</span>
							</div>
						</div>
						
						<div className="flex items-center justify-between">
							<div className="flex items-center gap-2">
								<span className="text-xs text-gray-500">Confidence:</span>
								<div className="w-16 bg-gray-200 rounded-full h-1.5">
									<div 
										className="h-1.5 rounded-full bg-indigo-500 transition-all duration-300" 
										style={{ width: `${rec.confidence * 100}%` }}
									></div>
								</div>
								<span className="text-xs font-medium text-gray-700">{Math.round(rec.confidence * 100)}%</span>
							</div>
							<div className="flex items-center gap-2">
								<button onClick={() => accept(rec.id)} className="text-xs px-3 py-1 rounded bg-green-600 text-white hover:bg-green-700 transition-colors">
									Accept
								</button>
								<button onClick={() => dismiss(rec.id)} className="text-xs px-3 py-1 rounded bg-gray-200 text-gray-700 hover:bg-gray-300 transition-colors">
									Dismiss
								</button>
							</div>
						</div>
					</div>
				))}
				{filtered.length === 0 && <div className="text-sm text-gray-500 text-center py-8">No recommendations match your filters.</div>}
			</div>
			
			{history.length > 0 && (
				<div className="mt-6 pt-4 border-t border-gray-200">
					<h3 className="font-medium text-sm text-gray-700 mb-3">Recent Actions</h3>
					<div className="space-y-2 max-h-32 overflow-y-auto">
						{history.slice(0, 3).map(h => (
							<div key={h.id} className="flex items-center gap-2 text-xs text-gray-600 bg-gray-50 rounded p-2">
								<span className={`w-2 h-2 rounded-full ${h.action === 'accepted' ? 'bg-green-500' : 'bg-red-500'}`}></span>
								<span className="font-medium">{h.action === 'accepted' ? 'Accepted' : 'Dismissed'}</span>
								<span>•</span>
								<span className="flex-1">{h.title}</span>
								<span>{new Date(h.at).toLocaleDateString()}</span>
							</div>
						))}
					</div>
				</div>
			)}
		</section>
	)
}
