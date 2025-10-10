import { useMemo, useState } from 'react'

const baseItems = [
	{ id: 'r1', title: 'Increase Help Desk Pricing', impact: 'high', confidence: 0.85, type: 'pricing' },
	{ id: 'r2', title: 'Add Network Monitoring', impact: 'medium', confidence: 0.75, type: 'service' },
	{ id: 'r3', title: 'Optimize Software Licenses', impact: 'low', confidence: 0.70, type: 'budget' },
	{ id: 'r4', title: 'Security Assessment Upsell', impact: 'medium', confidence: 0.73, type: 'service' },
]

const impactClasses = { high: 'bg-red-50 text-red-700', medium: 'bg-amber-50 text-amber-700', low: 'bg-gray-100' }

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

	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<div className="flex items-center justify-between">
				<h2 className="font-semibold">AI Recommendations</h2>
				<div className="flex gap-2 text-sm">
					<select value={filterImpact} onChange={(e) => setFilterImpact(e.target.value)} className="border border-gray-300 rounded-md px-2 py-1">
						<option value="all">All impacts</option>
						<option value="high">High</option>
						<option value="medium">Medium</option>
						<option value="low">Low</option>
					</select>
					<select value={filterType} onChange={(e) => setFilterType(e.target.value)} className="border border-gray-300 rounded-md px-2 py-1">
						<option value="all">All types</option>
						<option value="pricing">Pricing</option>
						<option value="service">Service</option>
						<option value="budget">Budget</option>
					</select>
					<select value={filterStatus} onChange={(e) => setFilterStatus(e.target.value)} className="border border-gray-300 rounded-md px-2 py-1">
						<option value="open">Open</option>
						<option value="accepted">Accepted</option>
						<option value="dismissed">Dismissed</option>
						<option value="all">All</option>
					</select>
				</div>
			</div>
			<ul className="mt-3 space-y-3">
				{filtered.map((rec) => (
					<li key={rec.id} className="p-3 border border-gray-200 rounded-lg">
						<div className="flex items-center justify-between">
							<div>
								<p className="font-medium text-sm">{rec.title}</p>
								<div className="mt-1 flex items-center gap-2">
									<span className={`text-[10px] px-2 py-0.5 rounded ${impactClasses[rec.impact]}`}>{rec.impact}</span>
									<span className="text-[10px] px-2 py-0.5 rounded bg-blue-50 text-blue-700">conf {(rec.confidence*100).toFixed(0)}%</span>
									<span className="text-[10px] px-2 py-0.5 rounded bg-gray-100">{rec.type}</span>
								</div>
							</div>
							<div className="flex items-center gap-2">
								<button onClick={() => accept(rec.id)} className="text-xs px-3 py-1.5 rounded bg-blue-600 text-white hover:bg-blue-700">Accept</button>
								<button onClick={() => dismiss(rec.id)} className="text-xs px-3 py-1.5 rounded bg-gray-100 hover:bg-gray-200">Dismiss</button>
							</div>
						</div>
					</li>
				))}
				{filtered.length === 0 && <li className="text-sm text-gray-500">No recommendations.</li>}
			</ul>
			<div className="mt-5">
				<h3 className="font-medium text-sm">History</h3>
				<ul className="mt-2 space-y-2">
					{history.length === 0 && <li className="text-xs text-gray-500">No history yet.</li>}
					{history.map(h => (
						<li key={h.id} className="text-xs text-gray-700">[{new Date(h.at).toLocaleString()}] {h.action} — {h.title}</li>
					))}
				</ul>
			</div>
		</section>
	)
}
