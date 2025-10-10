import { useMemo, useState } from 'react'
import { mockBudgets, mockExpenses, mockBudgetCategories } from '../../../services/mockFinancial'

export default function ExpenseCategorization() {
	const [rows, setRows] = useState(mockExpenses)
	const setRow = (i, patch) => setRows(prev => prev.map((r, idx) => (i === idx ? { ...r, ...patch } : r)))
	const save = () => {
		console.log('Save expenses (mock)', rows)
		alert('Expenses saved (mock).')
	}
	const budgets = useMemo(() => mockBudgets.map(b => ({ id: b.id, name: b.name })), [])
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<div className="flex items-center justify-between">
				<h2 className="font-semibold">Expense Categorization</h2>
				<button onClick={save} className="text-xs px-3 py-1.5 rounded bg-blue-600 text-white hover:bg-blue-700">Save</button>
			</div>
			<div className="mt-3 overflow-x-auto">
				<table className="min-w-full text-sm">
					<thead>
						<tr className="text-left text-gray-500">
							<th className="py-2">Date</th>
							<th className="py-2">Vendor</th>
							<th className="py-2">Budget</th>
							<th className="py-2">Category</th>
							<th className="py-2 text-right">Amount</th>
						</tr>
					</thead>
					<tbody className="divide-y">
						{rows.map((r, i) => (
							<tr key={r.id}>
								<td className="py-2">{r.date}</td>
								<td>{r.vendor}</td>
								<td>
									<select value={r.budget} onChange={(e) => setRow(i, { budget: e.target.value })} className="rounded-md border border-gray-300 px-2 py-1">
										{budgets.map(b => <option key={b.id} value={b.id}>{b.name}</option>)}
									</select>
								</td>
								<td>
									<select value={r.category} onChange={(e) => setRow(i, { category: e.target.value })} className="rounded-md border border-gray-300 px-2 py-1">
										{(mockBudgetCategories[r.budget] || []).map(c => <option key={c.name} value={c.name}>{c.name}</option>)}
									</select>
								</td>
								<td className="text-right">${r.amount.toLocaleString()}</td>
							</tr>
						))}
					</tbody>
				</table>
			</div>
		</section>
	)
}
