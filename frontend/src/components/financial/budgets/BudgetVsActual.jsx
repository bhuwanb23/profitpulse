import { useMemo, useState } from 'react'
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts'
import { mockBudgets, mockBudgetCategories } from '../../../services/mockFinancial'

export default function BudgetVsActual() {
	const [budgetId, setBudgetId] = useState(mockBudgets[0].id)
	const categories = mockBudgetCategories[budgetId] || []
	const data = useMemo(() => categories.map(c => ({ cat: c.name, allocated: c.alloc, spent: c.spent })), [categories])
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<div className="flex items-center justify-between">
				<h2 className="font-semibold">Budget vs Actual</h2>
				<select value={budgetId} onChange={(e) => setBudgetId(e.target.value)} className="text-sm border border-gray-300 rounded-md px-2 py-1">
					{mockBudgets.map(b => <option key={b.id} value={b.id}>{b.name}</option>)}
				</select>
			</div>
			<div className="mt-4 h-72">
				<ResponsiveContainer width="100%" height="100%">
					<BarChart data={data}>
						<CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
						<XAxis dataKey="cat" stroke="#9ca3af" />
						<YAxis stroke="#9ca3af" />
						<Tooltip />
						<Legend />
						<Bar dataKey="allocated" name="Allocated" fill="#94a3b8" />
						<Bar dataKey="spent" name="Spent" fill="#3b82f6" />
					</BarChart>
				</ResponsiveContainer>
			</div>
		</section>
	)
}
