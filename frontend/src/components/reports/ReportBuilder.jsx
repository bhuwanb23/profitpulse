import { useState, useMemo } from 'react'
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, BarChart, Bar } from 'recharts'

export default function ReportBuilder() {
	const [dateRange, setDateRange] = useState('last_30')
	const [metrics, setMetrics] = useState({ revenue: true, tickets: true, profitability: false })
	const [groupBy, setGroupBy] = useState('month')
	const [chartType, setChartType] = useState('line')

	// Sample data for preview
	const previewData = useMemo(() => {
		const data = [
			{ period: 'Week 1', revenue: 28400, tickets: 145, profitability: 18.2 },
			{ period: 'Week 2', revenue: 32100, tickets: 167, profitability: 21.5 },
			{ period: 'Week 3', revenue: 29800, tickets: 152, profitability: 19.8 },
			{ period: 'Week 4', revenue: 35600, tickets: 189, profitability: 23.1 }
		]
		return data
	}, [])

	const renderChart = () => {
		if (chartType === 'line') {
			return (
				<ResponsiveContainer width="100%" height="100%">
					<LineChart data={previewData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
						<CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
						<XAxis dataKey="period" stroke="#9ca3af" fontSize={12} />
						<YAxis stroke="#9ca3af" fontSize={12} />
						<Tooltip 
							contentStyle={{ 
								backgroundColor: 'rgba(255, 255, 255, 0.95)', 
								border: '1px solid #e5e7eb',
								borderRadius: '8px',
								backdropFilter: 'blur(8px)'
							}} 
						/>
						<Legend />
						{metrics.revenue && <Line type="monotone" dataKey="revenue" stroke="#3b82f6" strokeWidth={2} name="Revenue ($)" />}
						{metrics.tickets && <Line type="monotone" dataKey="tickets" stroke="#10b981" strokeWidth={2} name="Tickets" />}
						{metrics.profitability && <Line type="monotone" dataKey="profitability" stroke="#f59e0b" strokeWidth={2} name="Profitability (%)" />}
					</LineChart>
				</ResponsiveContainer>
			)
		} else {
			return (
				<ResponsiveContainer width="100%" height="100%">
					<BarChart data={previewData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
						<CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
						<XAxis dataKey="period" stroke="#9ca3af" fontSize={12} />
						<YAxis stroke="#9ca3af" fontSize={12} />
						<Tooltip 
							contentStyle={{ 
								backgroundColor: 'rgba(255, 255, 255, 0.95)', 
								border: '1px solid #e5e7eb',
								borderRadius: '8px',
								backdropFilter: 'blur(8px)'
							}} 
						/>
						<Legend />
						{metrics.revenue && <Bar dataKey="revenue" fill="#3b82f6" name="Revenue ($)" />}
						{metrics.tickets && <Bar dataKey="tickets" fill="#10b981" name="Tickets" />}
						{metrics.profitability && <Bar dataKey="profitability" fill="#f59e0b" name="Profitability (%)" />}
					</BarChart>
				</ResponsiveContainer>
			)
		}
	}

	return (
		<section className="bg-gradient-to-br from-blue-50 to-white rounded-xl border border-gray-200 p-6 shadow-sm">
			<h2 className="text-lg font-semibold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-4">
				Custom Report Builder
			</h2>
			
			{/* Configuration Controls */}
			<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 text-sm mb-6">
				<label className="block">
					<span className="text-gray-600 font-medium">Date Range</span>
					<select 
						className="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent" 
						value={dateRange} 
						onChange={(e)=>setDateRange(e.target.value)}
					>
						<option value="last_7">Last 7 days</option>
						<option value="last_30">Last 30 days</option>
						<option value="last_quarter">Last quarter</option>
						<option value="ytd">Year to date</option>
					</select>
				</label>
				
				<label className="block">
					<span className="text-gray-600 font-medium">Chart Type</span>
					<select 
						className="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent" 
						value={chartType} 
						onChange={(e)=>setChartType(e.target.value)}
					>
						<option value="line">Line Chart</option>
						<option value="bar">Bar Chart</option>
					</select>
				</label>
				
				<label className="block">
					<span className="text-gray-600 font-medium">Group By</span>
					<select 
						className="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent" 
						value={groupBy} 
						onChange={(e)=>setGroupBy(e.target.value)}
					>
						<option value="day">Day</option>
						<option value="week">Week</option>
						<option value="month">Month</option>
						<option value="quarter">Quarter</option>
					</select>
				</label>
				
				<div>
					<span className="text-gray-600 font-medium">Metrics</span>
					<div className="mt-1 space-y-2">
						<label className="flex items-center gap-2">
							<input 
								type="checkbox" 
								checked={metrics.revenue} 
								onChange={()=>setMetrics(m=>({ ...m, revenue: !m.revenue }))}
								className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
							/> 
							<span className="text-sm">Revenue</span>
						</label>
						<label className="flex items-center gap-2">
							<input 
								type="checkbox" 
								checked={metrics.tickets} 
								onChange={()=>setMetrics(m=>({ ...m, tickets: !m.tickets }))}
								className="rounded border-gray-300 text-green-600 focus:ring-green-500"
							/> 
							<span className="text-sm">Tickets</span>
						</label>
						<label className="flex items-center gap-2">
							<input 
								type="checkbox" 
								checked={metrics.profitability} 
								onChange={()=>setMetrics(m=>({ ...m, profitability: !m.profitability }))}
								className="rounded border-gray-300 text-orange-600 focus:ring-orange-500"
							/> 
							<span className="text-sm">Profitability</span>
						</label>
					</div>
				</div>
			</div>
			
			{/* Chart Preview */}
			<div className="bg-white rounded-lg border border-gray-200 p-4 mb-4">
				<h3 className="text-sm font-medium text-gray-700 mb-3">Live Preview</h3>
				<div className="h-64">
					{renderChart()}
				</div>
			</div>
			
			{/* Action Buttons */}
			<div className="flex flex-wrap gap-3">
				<button className="px-4 py-2 rounded-lg bg-gradient-to-r from-blue-600 to-blue-700 text-white text-sm font-medium hover:from-blue-700 hover:to-blue-800 transition-all shadow-sm">
					Generate Report
				</button>
				<button className="px-4 py-2 rounded-lg bg-gradient-to-r from-gray-100 to-gray-200 text-gray-700 text-sm font-medium hover:from-gray-200 hover:to-gray-300 transition-all">
					Save as Template
				</button>
				<button className="px-4 py-2 rounded-lg border border-gray-300 text-gray-700 text-sm font-medium hover:bg-gray-50 transition-colors">
					Export Preview
				</button>
			</div>
		</section>
	)
}
