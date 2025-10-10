import { useMemo } from 'react'
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ReferenceLine } from 'recharts'

export default function ForecastingChart() {
	const data = useMemo(() => (
		[
			{ label: 'Now', revenue: 12400 },
			{ label: '+1m', revenue: 12700 },
			{ label: '+2m', revenue: 13100 },
			{ label: '+3m', revenue: 13650 },
			{ label: '+4m', revenue: 14200 },
			{ label: '+5m', revenue: 14900 },
			{ label: '+6m', revenue: 15500 },
		]
	), [])

	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Financial Forecast</h2>
			<div className="mt-4 h-72">
				<ResponsiveContainer width="100%" height="100%">
					<AreaChart data={data} margin={{ top: 10, right: 16, bottom: 0, left: 0 }}>
						<CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
						<XAxis dataKey="label" stroke="#9ca3af" />
						<YAxis stroke="#9ca3af" />
						<Tooltip />
						<ReferenceLine x="Now" stroke="#ef4444" strokeDasharray="3 3" />
						<Area type="monotone" dataKey="revenue" stroke="#2563eb" fill="#93c5fd" strokeWidth={2} />
					</AreaChart>
				</ResponsiveContainer>
			</div>
		</section>
	)
}
