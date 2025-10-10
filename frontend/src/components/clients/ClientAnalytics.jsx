import { useMemo } from 'react'
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, BarChart, Bar } from 'recharts'

export default function ClientAnalytics() {
	const profitabilityTrend = useMemo(() => (
		[
			{ label: 'M-5', value: 0.70 }, { label: 'M-4', value: 0.72 }, { label: 'M-3', value: 0.74 }, { label: 'M-2', value: 0.76 }, { label: 'M-1', value: 0.78 }, { label: 'Now', value: 0.80 },
		]
	), [])

	const revenueBreakdown = useMemo(() => (
		[
			{ svc: 'Help Desk', revenue: 3500 },
			{ svc: 'Monitoring', revenue: 9000 },
			{ svc: 'Security', revenue: 1200 },
		]
	), [])

	return (
		<div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
			<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
				<h2 className="font-semibold">Profitability Trend</h2>
				<div className="mt-4 h-60">
					<ResponsiveContainer width="100%" height="100%">
						<LineChart data={profitabilityTrend}>
							<CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
							<XAxis dataKey="label" stroke="#9ca3af" />
							<YAxis domain={[0,1]} stroke="#9ca3af" />
							<Tooltip />
							<Line type="monotone" dataKey="value" stroke="#10b981" strokeWidth={2} dot={false} />
						</LineChart>
					</ResponsiveContainer>
				</div>
			</section>
			<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
				<h2 className="font-semibold">Revenue by Service</h2>
				<div className="mt-4 h-60">
					<ResponsiveContainer width="100%" height="100%">
						<BarChart data={revenueBreakdown}>
							<CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
							<XAxis dataKey="svc" stroke="#9ca3af" />
							<YAxis stroke="#9ca3af" />
							<Tooltip />
							<Bar dataKey="revenue" fill="#3b82f6" radius={[6,6,0,0]} />
						</BarChart>
					</ResponsiveContainer>
				</div>
			</section>
		</div>
	)
}
