import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip, Legend } from 'recharts'
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card'
import { UserIcon } from '../ui/Icons'

export function CustomerSegmentsChart({ data }) {
	return (
		<Card className="bg-gradient-to-br from-orange-50 to-red-50 border-orange-200">
			<CardHeader>
				<CardTitle className="flex items-center gap-2">
					<UserIcon className="h-5 w-5 text-orange-600" />
					<span className="bg-gradient-to-r from-orange-600 to-red-600 bg-clip-text text-transparent font-bold">
						Customer Segments
					</span>
				</CardTitle>
			</CardHeader>
			<CardContent>
				<div className="h-64">
					<ResponsiveContainer width="100%" height="100%">
						<PieChart width={400} height={300}>
							<Pie
								data={data || []}
								cx="50%"
								cy="50%"
								outerRadius={85}
								innerRadius={50}
								paddingAngle={3}
								dataKey="value"
								nameKey="name"
							>
								{(data || []).map((entry, index) => (
									<Cell 
										key={`cell-${index}`} 
										fill={entry.fill || '#8884d8'}
										stroke={entry.fill || '#8884d8'}
										strokeWidth={2}
									/>
								))}
							</Pie>
							<Tooltip 
								formatter={(value, name, props) => [
									`${value}% (${props.payload?.count || 0} customers)`,
									name
								]}
								contentStyle={{ 
									backgroundColor: 'rgba(255, 255, 255, 0.95)', 
									border: '1px solid #e5e7eb',
									borderRadius: '8px',
									backdropFilter: 'blur(8px)'
								}}
							/>
							<Legend 
								verticalAlign="bottom" 
								height={36}
								formatter={(value, entry) => (
									<span style={{ color: entry.color, fontWeight: 'bold' }}>
										{value}
									</span>
								)}
							/>
						</PieChart>
					</ResponsiveContainer>
				</div>
			</CardContent>
		</Card>
	)
}
