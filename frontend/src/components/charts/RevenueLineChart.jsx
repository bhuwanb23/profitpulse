import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts'

export default function RevenueLineChart({ data }) {
	return (
		<div className="mt-4 h-64">
			<ResponsiveContainer width="100%" height="100%">
				<LineChart data={data} margin={{ top: 10, right: 16, bottom: 0, left: 0 }}>
					<CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
					<XAxis dataKey="label" tick={{ fontSize: 12 }} stroke="#9ca3af" />
					<YAxis tick={{ fontSize: 12 }} stroke="#9ca3af" />
					<Tooltip contentStyle={{ fontSize: 12 }} />
					<Line type="monotone" dataKey="value" stroke="#2563eb" strokeWidth={2} dot={false} />
				</LineChart>
			</ResponsiveContainer>
		</div>
	)
}
