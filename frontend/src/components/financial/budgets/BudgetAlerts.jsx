import { useMemo } from 'react'
import { mockBudgets, mockBudgetCategories } from '../../../services/mockFinancial'

export default function BudgetAlerts() {
	const alerts = useMemo(() => {
		const items = []
		mockBudgets.forEach(b => {
			const pct = b.spent / b.total
			if (pct >= 1) items.push({ type: 'critical', text: `${b.name} is overspent.` })
			else if (pct >= 0.8) items.push({ type: 'warning', text: `${b.name} reached ${(pct*100).toFixed(0)}% of budget.` })
			(mockBudgetCategories[b.id] || []).forEach(c => {
				const cp = c.spent / c.alloc
				if (cp >= 1) items.push({ type: 'critical', text: `${b.name} • ${c.name} overspent.` })
				else if (cp >= 0.9) items.push({ type: 'warning', text: `${b.name} • ${c.name} at ${(cp*100).toFixed(0)}%.` })
			})
		})
		return items
	}, [])

	const style = (t) => t === 'critical' ? 'bg-red-50 text-red-700 border-red-200' : 'bg-amber-50 text-amber-700 border-amber-200'

	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Budget Alerts</h2>
			<ul className="mt-3 space-y-2">
				{alerts.length === 0 && <li className="text-sm text-gray-500">No alerts.</li>}
				{alerts.map((a, i) => (
					<li key={i} className={`text-sm px-3 py-2 rounded border ${style(a.type)}`}>{a.text}</li>
				))}
			</ul>
		</section>
	)
}
