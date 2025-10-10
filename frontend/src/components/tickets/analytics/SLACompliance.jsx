import { useMemo } from 'react'
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts'

export default function SLACompliance() {
	const trend = useMemo(() => (
		[
			{ month: 'Jan', sla: 96 }, { month: 'Feb', sla: 97 }, { month: 'Mar', sla: 97.5 }, { month: 'Apr', sla: 98 }, { month: 'May', sla: 98.5 }, { month: 'Jun', sla: 98 },
		]
	), [])
	const current = trend[trend.length - 1].sla
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">SLA Compliance</h2>
			<div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-6 items-center">
				<div className="md:col-span-2 h-56">
					<ResponsiveContainer width="100%" height="100%">
						<LineChart data={trend}>
							<CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
							<XAxis dataKey="month" stroke="#9ca3af" />
							<YAxis unit="%" domain={[90,100]} stroke="#9ca3af" />
							<Tooltip />
							<Line type="monotone" dataKey="sla" stroke="#10b981" strokeWidth={2} dot={false} />
						</LineChart>
					</ResponsiveContainer>
				</div>
				<div>
					<div className="text-sm text-gray-500">Current</div>
					<div className="mt-1 text-3xl font-semibold">{current}%</div>
					<div className="mt-2 h-3 w-full bg-gray-100 rounded-full">
						<div className="h-3 bg-emerald-500 rounded-full" style={{ width: `${current}%` }} />
					</div>
				</div>
			</div>
		</section>
	)
}
