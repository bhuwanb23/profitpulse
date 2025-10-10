import { useMemo } from 'react'
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts'
import { mockInvoices } from '../../../services/mockFinancial'

export default function PaymentMethodAnalytics() {
	const data = useMemo(() => {
		const counts = new Map()
		mockInvoices.forEach(i => counts.set(i.method, (counts.get(i.method) || 0) + 1))
		return Array.from(counts.entries()).map(([method, count]) => ({ method, count }))
	}, [])
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Payment Method Analytics</h2>
			<div className="mt-4 h-60">
				<ResponsiveContainer width="100%" height="100%">
					<BarChart data={data}>
						<CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
						<XAxis dataKey="method" stroke="#9ca3af" />
						<YAxis stroke="#9ca3af" />
						<Tooltip />
						<Bar dataKey="count" fill="#8b5cf6" radius={[6,6,0,0]} />
					</BarChart>
				</ResponsiveContainer>
			</div>
		</section>
	)
}
