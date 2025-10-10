import { useMemo } from 'react'
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts'
import { mockInvoices } from '../../../services/mockFinancial'

function monthKey(dateStr) {
	const d = new Date(dateStr)
	return d.toLocaleString('en', { month: 'short' })
}

export default function RevenueTrends() {
	const data = useMemo(() => {
		const map = new Map()
		mockInvoices.forEach(inv => {
			const k = monthKey(inv.date)
			map.set(k, (map.get(k) || 0) + inv.total)
		})
		return Array.from(map.entries()).map(([label, value]) => ({ label, value })).slice(0, 12)
	}, [])

	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Revenue Trends</h2>
			<div className="mt-4 h-72">
				<ResponsiveContainer width="100%" height="100%">
					<LineChart data={data}>
						<CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
						<XAxis dataKey="label" stroke="#9ca3af" />
						<YAxis stroke="#9ca3af" />
						<Tooltip />
						<Line type="monotone" dataKey="value" stroke="#2563eb" strokeWidth={2} dot={false} />
					</LineChart>
				</ResponsiveContainer>
			</div>
		</section>
	)
}
