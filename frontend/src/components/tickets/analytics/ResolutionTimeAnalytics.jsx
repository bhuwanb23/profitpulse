import { useMemo } from 'react'
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts'

export default function ResolutionTimeAnalytics() {
	const data = useMemo(() => (
		[
			{ month: 'Jan', hours: 4.2 },
			{ month: 'Feb', hours: 3.9 },
			{ month: 'Mar', hours: 3.6 },
			{ month: 'Apr', hours: 3.4 },
			{ month: 'May', hours: 3.1 },
			{ month: 'Jun', hours: 3.0 },
			{ month: 'Jul', hours: 2.9 },
			{ month: 'Aug', hours: 2.8 },
			{ month: 'Sep', hours: 2.7 },
			{ month: 'Oct', hours: 2.6 },
			{ month: 'Nov', hours: 2.7 },
			{ month: 'Dec', hours: 2.5 },
		]
	), [])

	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Resolution Time Analytics</h2>
			<div className="mt-4 h-72">
				<ResponsiveContainer width="100%" height="100%">
					<AreaChart data={data}>
						<CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
						<XAxis dataKey="month" stroke="#9ca3af" />
						<YAxis unit="h" stroke="#9ca3af" />
						<Tooltip />
						<Area type="monotone" dataKey="hours" stroke="#3b82f6" fill="#93c5fd" strokeWidth={2} />
					</AreaChart>
				</ResponsiveContainer>
			</div>
		</section>
	)
}
