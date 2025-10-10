import { useMemo } from 'react'
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts'

export default function CategoryBreakdown() {
	const data = useMemo(() => (
		[
			{ category: 'infrastructure', count: 18 },
			{ category: 'network', count: 22 },
			{ category: 'software', count: 14 },
			{ category: 'security', count: 11 },
			{ category: 'database', count: 9 },
		]
	), [])

	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Category Breakdown</h2>
			<div className="mt-4 h-72">
				<ResponsiveContainer width="100%" height="100%">
					<BarChart data={data}>
						<CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
						<XAxis dataKey="category" stroke="#9ca3af" />
						<YAxis stroke="#9ca3af" />
						<Tooltip />
						<Bar dataKey="count" fill="#10b981" radius={[6,6,0,0]} />
					</BarChart>
				</ResponsiveContainer>
			</div>
		</section>
	)
}
