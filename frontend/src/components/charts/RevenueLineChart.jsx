import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, AreaChart, Area } from 'recharts'

export default function RevenueLineChart({ data, showArea = false, height = 250 }) {
	const ChartComponent = showArea ? AreaChart : LineChart
	
	return (
		<div className={`w-full ${showArea ? 'h-80' : `h-${height}`}`}>
			<ResponsiveContainer width="100%" height="100%">
				<ChartComponent data={data} margin={{ top: 10, right: 16, bottom: 10, left: 0 }}>
					<defs>
						<linearGradient id="revenueGradient" x1="0" y1="0" x2="0" y2="1">
							<stop offset="5%" stopColor="#3B82F6" stopOpacity={0.8}/>
							<stop offset="95%" stopColor="#3B82F6" stopOpacity={0.1}/>
						</linearGradient>
					</defs>
					<CartesianGrid strokeDasharray="3 3" stroke="#F3F4F6" />
					<XAxis 
						dataKey="label" 
						axisLine={false}
						tickLine={false}
						tick={{ fontSize: 12, fill: '#6B7280' }} 
					/>
					<YAxis 
						axisLine={false}
						tickLine={false}
						tick={{ fontSize: 12, fill: '#6B7280' }}
						tickFormatter={(value) => `$${(value / 1000).toFixed(0)}k`}
					/>
					<Tooltip 
						contentStyle={{
							backgroundColor: 'white',
							border: '1px solid #E5E7EB',
							borderRadius: '8px',
							boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
							fontSize: '12px'
						}}
						formatter={(value) => [`$${value.toLocaleString()}`, 'Revenue']}
					/>
					{showArea ? (
						<Area
							type="monotone"
							dataKey="value"
							stroke="#3B82F6"
							strokeWidth={2}
							fill="url(#revenueGradient)"
						/>
					) : (
						<Line 
							type="monotone" 
							dataKey="value" 
							stroke="#3B82F6" 
							strokeWidth={3} 
							dot={{ fill: '#3B82F6', strokeWidth: 2, r: 4 }}
							activeDot={{ r: 6, stroke: '#3B82F6', strokeWidth: 2 }}
						/>
					)}
				</ChartComponent>
			</ResponsiveContainer>
		</div>
	)
}
