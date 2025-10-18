import { useMemo } from 'react'
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts'

export default function ComparativeAnalysis() {
	const comparisonData = useMemo(() => [
		{
			metric: 'Revenue',
			thisMonth: 124000,
			lastMonth: 116000,
			change: 6.9,
			unit: '$'
		},
		{
			metric: 'Tickets',
			thisMonth: 482,
			lastMonth: 505,
			change: -4.6,
			unit: ''
		},
		{
			metric: 'Profitability',
			thisMonth: 17.2,
			lastMonth: 15.8,
			change: 8.9,
			unit: '%'
		},
		{
			metric: 'Customer Satisfaction',
			thisMonth: 94.8,
			lastMonth: 92.1,
			change: 2.9,
			unit: '%'
		}
	], [])

	const formatValue = (value, unit) => {
		if (unit === '$') return `$${(value/1000).toFixed(0)}k`
		if (unit === '%') return `${value}%`
		return value.toString()
	}

	return (
		<section className="bg-gradient-to-br from-emerald-50 to-white rounded-xl border border-gray-200 p-6 shadow-sm">
			<h2 className="text-lg font-semibold bg-gradient-to-r from-emerald-600 to-teal-600 bg-clip-text text-transparent mb-4">
				Comparative Analysis
			</h2>
			
			{/* Chart Visualization */}
			<div className="bg-white rounded-lg border border-gray-200 p-4 mb-4">
				<h3 className="text-sm font-medium text-gray-700 mb-3">Month-over-Month Comparison</h3>
				<div className="h-48">
					<ResponsiveContainer width="100%" height="100%">
						<BarChart data={comparisonData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
							<CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
							<XAxis dataKey="metric" stroke="#9ca3af" fontSize={12} />
							<YAxis stroke="#9ca3af" fontSize={12} />
							<Tooltip 
								formatter={(value, name) => [
									name === 'thisMonth' ? 'This Month' : 'Last Month',
									value
								]}
								contentStyle={{ 
									backgroundColor: 'rgba(255, 255, 255, 0.95)', 
									border: '1px solid #e5e7eb',
									borderRadius: '8px',
									backdropFilter: 'blur(8px)'
								}} 
							/>
							<Legend />
							<Bar dataKey="thisMonth" fill="#10b981" name="This Month" radius={[2, 2, 0, 0]} />
							<Bar dataKey="lastMonth" fill="#6b7280" name="Last Month" radius={[2, 2, 0, 0]} />
						</BarChart>
					</ResponsiveContainer>
				</div>
			</div>
			
			{/* Detailed Comparison Cards */}
			<div className="grid grid-cols-1 md:grid-cols-2 gap-4">
				<div className="bg-gradient-to-br from-emerald-100 to-emerald-50 rounded-lg border border-emerald-200 p-4">
					<div className="flex items-center justify-between mb-3">
						<h3 className="font-medium text-emerald-800">This Month</h3>
						<span className="px-2 py-1 bg-emerald-200 text-emerald-800 text-xs font-medium rounded-full">
							Current
						</span>
					</div>
					<div className="space-y-3">
						{comparisonData.map((item, index) => (
							<div key={index} className="flex items-center justify-between">
								<span className="text-sm text-emerald-700">{item.metric}:</span>
								<span className="font-semibold text-emerald-900">
									{formatValue(item.thisMonth, item.unit)}
								</span>
							</div>
						))}
					</div>
				</div>
				
				<div className="bg-gradient-to-br from-gray-100 to-gray-50 rounded-lg border border-gray-200 p-4">
					<div className="flex items-center justify-between mb-3">
						<h3 className="font-medium text-gray-800">Last Month</h3>
						<span className="px-2 py-1 bg-gray-200 text-gray-800 text-xs font-medium rounded-full">
							Previous
						</span>
					</div>
					<div className="space-y-3">
						{comparisonData.map((item, index) => (
							<div key={index} className="flex items-center justify-between">
								<span className="text-sm text-gray-700">{item.metric}:</span>
								<span className="font-semibold text-gray-900">
									{formatValue(item.lastMonth, item.unit)}
								</span>
							</div>
						))}
					</div>
				</div>
			</div>
			
			{/* Change Summary */}
			<div className="mt-4 bg-white rounded-lg border border-gray-200 p-4">
				<h3 className="text-sm font-medium text-gray-700 mb-3">Performance Changes</h3>
				<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
					{comparisonData.map((item, index) => (
						<div key={index} className="flex items-center justify-between p-2 bg-gray-50 rounded-lg">
							<span className="text-xs text-gray-600">{item.metric}</span>
							<span className={`text-xs font-semibold px-2 py-1 rounded-full ${
								item.change > 0 
									? 'bg-green-100 text-green-800' 
									: 'bg-red-100 text-red-800'
							}`}>
								{item.change > 0 ? '+' : ''}{item.change.toFixed(1)}%
							</span>
						</div>
					))}
				</div>
			</div>
		</section>
	)
}
