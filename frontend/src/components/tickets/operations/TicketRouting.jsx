import { useState } from 'react'

export default function TicketRouting() {
	const [rules, setRules] = useState([
		{ id: 1, match: 'category:security', routeTo: 'Security Team' },
		{ id: 2, match: 'priority:critical', routeTo: 'On-call Engineer' },
	])
	const [newRule, setNewRule] = useState({ match: '', routeTo: '' })

	const addRule = (e) => {
		e.preventDefault()
		if (!newRule.match || !newRule.routeTo) return
		setRules(prev => [...prev, { id: Date.now(), ...newRule }])
		setNewRule({ match: '', routeTo: '' })
	}

	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Ticket Routing Rules</h2>
			<form onSubmit={addRule} className="mt-3 flex flex-wrap gap-2 items-end text-sm">
				<div>
					<label className="block text-gray-600 text-xs">Match</label>
					<input value={newRule.match} onChange={(e) => setNewRule(prev => ({ ...prev, match: e.target.value }))} className="mt-1 w-64 rounded-md border border-gray-300 px-3 py-2 text-sm" placeholder="e.g., category:network" />
				</div>
				<div>
					<label className="block text-gray-600 text-xs">Route To</label>
					<input value={newRule.routeTo} onChange={(e) => setNewRule(prev => ({ ...prev, routeTo: e.target.value }))} className="mt-1 w-64 rounded-md border border-gray-300 px-3 py-2 text-sm" placeholder="Team or technician" />
				</div>
				<button type="submit" className="bg-blue-600 text-white px-3 py-1.5 rounded-md hover:bg-blue-700">Add Rule</button>
			</form>
			<ul className="mt-4 divide-y">
				{rules.map(r => (
					<li key={r.id} className="py-2 text-sm flex items-center justify-between">
						<div>
							<div className="font-medium">{r.match}</div>
							<div className="text-xs text-gray-500">→ {r.routeTo}</div>
						</div>
					</li>
				))}
			</ul>
		</section>
	)
}
