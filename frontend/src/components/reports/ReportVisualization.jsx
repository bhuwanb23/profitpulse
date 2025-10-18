import { useState, useMemo } from 'react'
import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip, Legend, BarChart, Bar, XAxis, YAxis, CartesianGrid } from 'recharts'

export default function ReportVisualization() {
	const [mode, setMode] = useState('chart')
	const [chartType, setChartType] = useState('pie')

	const chartData = useMemo(() => [
		{ name: 'Revenue', value: 124000, percentage: 45.2, color: '#3b82f6' },
		{ name: 'Expenses', value: 68000, percentage: 24.8, color: '#ef4444' },
		{ name: 'Profit', value: 56000, percentage: 20.4, color: '#10b981' },
		{ name: 'Tax', value: 26000, percentage: 9.6, color: '#f59e0b' }
	], [])

	const tableData = useMemo(() => [
		{ metric: 'Total Revenue', value: '$124,000', change: '+12.5%', status: 'positive' },
		{ metric: 'Active Tickets', value: '482', change: '+8.3%', status: 'positive' },
		{ metric: 'Profitability', value: '17.2%', change: '+2.1%', status: 'positive' },
		{ metric: 'Customer Satisfaction', value: '94.8%', change: '+1.2%', status: 'positive' },
		{ metric: 'Response Time', value: '2.3h', change: '-15.4%', status: 'positive' },
		{ metric: 'Resolution Rate', value: '89.6%', change: '+5.7%', status: 'positive' }
	], [])

	const renderChart = () => {
		if (chartType === 'pie') {
			return (
				<ResponsiveContainer width="100%" height="100%">
					<PieChart width={400} height={300}>
						<Pie
							data={chartData || []}
							cx="50%"
							cy="50%"
							innerRadius={40}
							outerRadius={80}
							paddingAngle={2}
							dataKey="value"
							nameKey="name"
						>
							{(chartData || []).map((entry, index) => (
								<Cell key={`cell-${index}`} fill={entry.color || '#8884d8'} />
							))}
						</Pie>
						<Tooltip 
							formatter={(value) => [`$${(value/1000).toFixed(0)}k`, 'Value']}
							contentStyle={{ 
								backgroundColor: 'rgba(255, 255, 255, 0.95)', 
								border: '1px solid #e5e7eb',
								borderRadius: '8px',
								backdropFilter: 'blur(8px)'
							}} 
						/>
						<Legend />
					</PieChart>
				</ResponsiveContainer>
			)
		} else {
			return (
				<ResponsiveContainer width="100%" height="100%">
					<BarChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
						<CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
						<XAxis dataKey="name" stroke="#9ca3af" fontSize={12} />
						<YAxis stroke="#9ca3af" fontSize={12} />
						<Tooltip 
							formatter={(value) => [`$${(value/1000).toFixed(0)}k`, 'Value']}
							contentStyle={{ 
								backgroundColor: 'rgba(255, 255, 255, 0.95)', 
								border: '1px solid #e5e7eb',
								borderRadius: '8px',
								backdropFilter: 'blur(8px)'
							}} 
						/>
						<Bar dataKey="value" fill="#3b82f6" radius={[4, 4, 0, 0]} />
					</BarChart>
				</ResponsiveContainer>
			)
		}
	}

	return (
		<section className="bg-gradient-to-br from-purple-50 to-white rounded-xl border border-gray-200 p-6 shadow-sm">
			<h2 className="text-lg font-semibold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent mb-4">
				Data Visualization
			</h2>
			
			{/* Mode and Chart Type Controls */}
			<div className="flex flex-wrap gap-3 mb-4">
				<div className="flex gap-2 text-sm">
					<button 
						onClick={()=>setMode('chart')} 
						className={`px-3 py-1.5 rounded-lg font-medium transition-all ${mode==='chart'?'bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-sm':'bg-gray-100 hover:bg-gray-200 text-gray-700'}`}
					>
						Chart
					</button>
					<button 
						onClick={()=>setMode('table')} 
						className={`px-3 py-1.5 rounded-lg font-medium transition-all ${mode==='table'?'bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-sm':'bg-gray-100 hover:bg-gray-200 text-gray-700'}`}
					>
						Table
					</button>
					<button 
						onClick={()=>setMode('both')} 
						className={`px-3 py-1.5 rounded-lg font-medium transition-all ${mode==='both'?'bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-sm':'bg-gray-100 hover:bg-gray-200 text-gray-700'}`}
					>
						Both
					</button>
				</div>
				
				{(mode === 'chart' || mode === 'both') && (
					<div className="flex gap-2 text-sm">
						<button 
							onClick={()=>setChartType('pie')} 
							className={`px-3 py-1.5 rounded-lg font-medium transition-all ${chartType==='pie'?'bg-blue-600 text-white':'bg-gray-100 hover:bg-gray-200 text-gray-700'}`}
						>
							Pie Chart
						</button>
						<button 
							onClick={()=>setChartType('bar')} 
							className={`px-3 py-1.5 rounded-lg font-medium transition-all ${chartType==='bar'?'bg-blue-600 text-white':'bg-gray-100 hover:bg-gray-200 text-gray-700'}`}
						>
							Bar Chart
						</button>
					</div>
				)}
			</div>
			
			{/* Content Area */}
			<div className="grid grid-cols-1 md:grid-cols-2 gap-6">
				{(mode==='chart' || mode==='both') && (
					<div className="bg-white rounded-lg border border-gray-200 p-4">
						<h3 className="text-sm font-medium text-gray-700 mb-3">Financial Overview</h3>
						<div className="h-64">
							{renderChart()}
						</div>
					</div>
				)}
				
				{(mode==='table' || mode==='both') && (
					<div className="bg-white rounded-lg border border-gray-200 p-4">
						<h3 className="text-sm font-medium text-gray-700 mb-3">Performance Metrics</h3>
						<div className="overflow-x-auto">
							<table className="w-full text-sm">
								<thead className="text-left text-gray-500 border-b border-gray-200">
									<tr>
										<th className="py-2 font-medium">Metric</th>
										<th className="py-2 font-medium">Value</th>
										<th className="py-2 font-medium">Change</th>
									</tr>
								</thead>
								<tbody className="divide-y divide-gray-100">
									{tableData.map((row, index) => (
										<tr key={index} className="hover:bg-gray-50">
											<td className="py-3 font-medium text-gray-900">{row.metric}</td>
											<td className="py-3 text-gray-700">{row.value}</td>
											<td className="py-3">
												<span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
													row.status === 'positive' 
														? 'bg-green-100 text-green-800' 
														: 'bg-red-100 text-red-800'
												}`}>
													{row.change}
												</span>
											</td>
										</tr>
									))}
								</tbody>
							</table>
						</div>
					</div>
				)}
			</div>
		</section>
	)
}
