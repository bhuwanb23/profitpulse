import { mockBudgets } from '../../../services/mockFinancial'

export default function BudgetOverview() {
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Budget Overview</h2>
			<div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
				{mockBudgets.map(b => (
					<div key={b.id} className="border border-gray-200 rounded-lg p-4">
						<div className="text-sm font-medium">{b.name}</div>
						<div className="text-xs text-gray-500">{b.type} • {b.start} → {b.end}</div>
						<div className="mt-2 text-sm">${b.spent.toLocaleString()} / ${b.total.toLocaleString()}</div>
						<div className="mt-1 h-2 w-full bg-gray-100 rounded-full"><div className="h-2 bg-blue-600 rounded-full" style={{ width: `${Math.min(Math.round(b.spent / b.total * 100), 100)}%` }} /></div>
					</div>
				))}
			</div>
		</section>
	)
}
