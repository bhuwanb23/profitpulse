import { useMemo } from 'react'
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts'

export default function TechnicianPerformance() {
	const data = useMemo(() => (
		[
			{ tech: 'John', resolved: 38, avgHrs: 2.8 },
			{ tech: 'Sarah', resolved: 41, avgHrs: 3.1 },
			{ tech: 'Mike', resolved: 55, avgHrs: 2.6 },
		]
	), [])

	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Technician Performance</h2>
			<div className="mt-4 h-72">
				<ResponsiveContainer width="100%" height="100%">
					<BarChart data={data}>
						<CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
						<XAxis dataKey="tech" stroke="#9ca3af" />
						<YAxis yAxisId="left" stroke="#9ca3af" />
						<YAxis yAxisId="right" orientation="right" stroke="#9ca3af" />
						<Tooltip />
						<Legend />
						<Bar yAxisId="left" dataKey="resolved" name="Resolved" fill="#3b82f6" />
						<Bar yAxisId="right" dataKey="avgHrs" name="Avg Hours" fill="#f59e0b" />
					</BarChart>
				</ResponsiveContainer>
			</div>
		</section>
	)
}
