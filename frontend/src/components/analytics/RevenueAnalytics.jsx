import { useMemo, useState } from 'react'
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts'

export default function RevenueAnalytics() {
	const [period, setPeriod] = useState('12m')

	const data = useMemo(() => (
		[
			{ label: 'Jan', mrr: 5400, oneOff: 1000 },
			{ label: 'Feb', mrr: 5600, oneOff: 1600 },
			{ label: 'Mar', mrr: 6000, oneOff: 2800 },
			{ label: 'Apr', mrr: 6100, oneOff: 1500 },
			{ label: 'May', mrr: 6400, oneOff: 2700 },
			{ label: 'Jun', mrr: 6600, oneOff: 3200 },
			{ label: 'Jul', mrr: 6900, oneOff: 3500 },
			{ label: 'Aug', mrr: 7000, oneOff: 2900 },
			{ label: 'Sep', mrr: 7400, oneOff: 3800 },
			{ label: 'Oct', mrr: 7900, oneOff: 4500 },
			{ label: 'Nov', mrr: 8100, oneOff: 3700 },
			{ label: 'Dec', mrr: 8400, oneOff: 4700 },
		]
	), [])

	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<div className="flex items-center justify-between">
				<h2 className="font-semibold">Revenue Analytics</h2>
				<select value={period} onChange={(e) => setPeriod(e.target.value)} className="text-sm border border-gray-300 rounded-md px-2 py-1">
					<option value="12m">Last 12 months</option>
					<option value="6m">Last 6 months</option>
					<option value="30d">Last 30 days</option>
				</select>
			</div>
			<div className="mt-4 h-72">
				<ResponsiveContainer width="100%" height="100%">
					<LineChart data={data} margin={{ top: 10, right: 16, bottom: 0, left: 0 }}>
						<CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
						<XAxis dataKey="label" stroke="#9ca3af" />
						<YAxis stroke="#9ca3af" />
						<Tooltip />
						<Legend />
						<Line type="monotone" dataKey="mrr" name="MRR" stroke="#2563eb" strokeWidth={2} dot={false} />
						<Line type="monotone" dataKey="oneOff" name="One-off" stroke="#10b981" strokeWidth={2} dot={false} />
					</LineChart>
				</ResponsiveContainer>
			</div>
		</section>
	)
}
