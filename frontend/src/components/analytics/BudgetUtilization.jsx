import { useMemo } from 'react'
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts'

export default function BudgetUtilization() {
	const data = useMemo(() => (
		[
			{ name: 'Q1', personnel: 45, equipment: 18, software: 12 },
			{ name: 'Q2', personnel: 52, equipment: 9, software: 14 },
			{ name: 'Q3', personnel: 48, equipment: 15, software: 17 },
			{ name: 'Q4', personnel: 50, equipment: 20, software: 10 },
		]
	), [])

	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Budget Utilization</h2>
			<div className="mt-4 h-72">
				<ResponsiveContainer width="100%" height="100%">
					<BarChart data={data} margin={{ top: 10, right: 16, bottom: 0, left: 0 }}>
						<CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
						<XAxis dataKey="name" stroke="#9ca3af" />
						<YAxis unit="%" stroke="#9ca3af" />
						<Tooltip />
						<Legend />
						<Bar dataKey="personnel" stackId="a" name="Personnel" fill="#3b82f6" />
						<Bar dataKey="equipment" stackId="a" name="Equipment" fill="#8b5cf6" />
						<Bar dataKey="software" stackId="a" name="Software" fill="#10b981" />
					</BarChart>
				</ResponsiveContainer>
			</div>
		</section>
	)
}
