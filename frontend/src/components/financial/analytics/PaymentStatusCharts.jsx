import { useMemo } from 'react'
import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip, Legend } from 'recharts'
import { mockInvoices } from '../../../services/mockFinancial'

const COLORS = { draft: '#9ca3af', sent: '#60a5fa', paid: '#10b981', overdue: '#ef4444' }

export default function PaymentStatusCharts() {
	const data = useMemo(() => {
		const counts = { draft: 0, sent: 0, paid: 0, overdue: 0 }
		mockInvoices.forEach(i => { counts[i.status] = (counts[i.status] || 0) + 1 })
		return Object.entries(counts).map(([name, value]) => ({ name, value }))
	}, [])
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Payment Status</h2>
			<div className="mt-4 h-72">
				<ResponsiveContainer width="100%" height="100%">
					<PieChart>
						<Pie data={data} dataKey="value" nameKey="name" outerRadius={100}>
							{data.map((e) => <Cell key={e.name} fill={COLORS[e.name] || '#ccc'} />)}
						</Pie>
						<Tooltip />
						<Legend />
					</PieChart>
				</ResponsiveContainer>
			</div>
		</section>
	)
}
