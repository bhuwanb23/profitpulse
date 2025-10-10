import { useMemo } from 'react'
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts'

export default function ProfitabilityChart() {
	const data = useMemo(() => (
		[
			{ client: 'Acme', margin: 32 },
			{ client: 'TechStart', margin: 27 },
			{ client: 'RetailMax', margin: 18 },
			{ client: 'HealthPlus', margin: 30 },
			{ client: 'FinanceFirst', margin: 24 },
		]
	), [])

	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Profitability Analysis</h2>
			<div className="mt-4 h-72">
				<ResponsiveContainer width="100%" height="100%">
					<BarChart data={data} margin={{ top: 10, right: 16, bottom: 0, left: 0 }}>
						<CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
						<XAxis dataKey="client" stroke="#9ca3af" />
						<YAxis unit="%" stroke="#9ca3af" />
						<Tooltip />
						<Bar dataKey="margin" fill="#f59e0b" radius={[6,6,0,0]} />
					</BarChart>
				</ResponsiveContainer>
			</div>
		</section>
	)
}
