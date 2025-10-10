import { useMemo } from 'react'
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts'

export default function CSATScores() {
	const dist = useMemo(() => (
		[
			{ score: '1★', count: 2 },
			{ score: '2★', count: 4 },
			{ score: '3★', count: 9 },
			{ score: '4★', count: 22 },
			{ score: '5★', count: 38 },
		]
	), [])
	const avg = 4.3
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Customer Satisfaction (CSAT)</h2>
			<div className="mt-2 text-sm">Average: <span className="font-medium">{avg}/5</span></div>
			<div className="mt-3 h-60">
				<ResponsiveContainer width="100%" height="100%">
					<BarChart data={dist}>
						<CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
						<XAxis dataKey="score" stroke="#9ca3af" />
						<YAxis stroke="#9ca3af" />
						<Tooltip />
						<Bar dataKey="count" fill="#8b5cf6" radius={[6,6,0,0]} />
					</BarChart>
				</ResponsiveContainer>
			</div>
		</section>
	)
}
