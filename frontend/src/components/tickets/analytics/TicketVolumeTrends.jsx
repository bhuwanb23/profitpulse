import { useMemo } from 'react'
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts'

export default function TicketVolumeTrends() {
	const data = useMemo(() => (
		[
			{ month: 'Jan', opened: 45, resolved: 38 },
			{ month: 'Feb', opened: 50, resolved: 41 },
			{ month: 'Mar', opened: 62, resolved: 55 },
			{ month: 'Apr', opened: 58, resolved: 49 },
			{ month: 'May', opened: 70, resolved: 65 },
			{ month: 'Jun', opened: 64, resolved: 60 },
			{ month: 'Jul', opened: 72, resolved: 68 },
			{ month: 'Aug', opened: 69, resolved: 66 },
			{ month: 'Sep', opened: 75, resolved: 71 },
			{ month: 'Oct', opened: 80, resolved: 78 },
			{ month: 'Nov', opened: 77, resolved: 74 },
			{ month: 'Dec', opened: 82, resolved: 79 },
		]
	), [])

	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Ticket Volume Trends</h2>
			<div className="mt-4 h-72">
				<ResponsiveContainer width="100%" height="100%">
					<LineChart data={data}>
						<CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
						<XAxis dataKey="month" stroke="#9ca3af" />
						<YAxis stroke="#9ca3af" />
						<Tooltip />
						<Legend />
						<Line type="monotone" dataKey="opened" name="Opened" stroke="#ef4444" strokeWidth={2} dot={false} />
						<Line type="monotone" dataKey="resolved" name="Resolved" stroke="#10b981" strokeWidth={2} dot={false} />
					</LineChart>
				</ResponsiveContainer>
			</div>
		</section>
	)
}
