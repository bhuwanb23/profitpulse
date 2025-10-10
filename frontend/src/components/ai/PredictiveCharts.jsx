import { useMemo } from 'react'
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts'

function MiniArea({ title, data, color }) {
	return (
		<div className="bg-white rounded-xl border border-gray-200 p-4 shadow-sm">
			<div className="text-sm font-medium">{title}</div>
			<div className="mt-2 h-40">
				<ResponsiveContainer width="100%" height="100%">
					<AreaChart data={data} margin={{ top: 6, right: 8, bottom: 0, left: 0 }}>
						<CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
						<XAxis dataKey="label" hide />
						<YAxis hide />
						<Tooltip />
						<Area type="monotone" dataKey="value" stroke={color} fill={color} fillOpacity={0.3} strokeWidth={2} />
					</AreaChart>
				</ResponsiveContainer>
			</div>
		</div>
	)
}

export default function PredictiveCharts() {
	const churn = useMemo(() => ([
		{ label: 'Now', value: 3.2 }, { label: '+1m', value: 3.1 }, { label: '+2m', value: 3.0 }, { label: '+3m', value: 2.8 },
	]), [])
	const demand = useMemo(() => ([
		{ label: 'Now', value: 100 }, { label: '+1m', value: 108 }, { label: '+2m', value: 116 }, { label: '+3m', value: 125 },
	]), [])

	return (
		<section className="grid grid-cols-1 md:grid-cols-2 gap-4">
			<MiniArea title="Predicted Churn Risk" data={churn} color="#ef4444" />
			<MiniArea title="Service Demand Forecast" data={demand} color="#3b82f6" />
		</section>
	)
}
