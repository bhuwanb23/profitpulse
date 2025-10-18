import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Cell } from 'recharts'
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card'
import { ChartBarIcon } from '../ui/Icons'

export function DepartmentChart({ data, customTooltip }) {
	return (
		<Card className="bg-gradient-to-br from-emerald-50 to-teal-50 border-emerald-200">
			<CardHeader>
				<CardTitle className="flex items-center gap-2">
					<ChartBarIcon className="h-5 w-5 text-emerald-600" />
					<span className="bg-gradient-to-r from-emerald-600 to-teal-600 bg-clip-text text-transparent font-bold">
						Department Performance
					</span>
				</CardTitle>
			</CardHeader>
			<CardContent>
				<div className="h-64">
					<ResponsiveContainer width="100%" height="100%">
						<BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
							<CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" opacity={0.5} />
							<XAxis 
								dataKey="name" 
								stroke="#6b7280" 
								fontSize={10}
								tick={{ fill: '#6b7280', fontSize: 10 }}
								angle={-45}
								textAnchor="end"
								height={60}
							/>
							<YAxis 
								stroke="#6b7280" 
								fontSize={11}
								tick={{ fill: '#6b7280', fontSize: 11 }}
								tickFormatter={(value) => `$${(value / 1000).toFixed(0)}k`}
							/>
							<Tooltip content={customTooltip} />
							<Bar
								dataKey="revenue"
								radius={[8, 8, 0, 0]}
								name="Revenue"
							>
								{data.map((entry, index) => (
									<Cell key={`cell-${index}`} fill={entry.fill} />
								))}
							</Bar>
						</BarChart>
					</ResponsiveContainer>
				</div>
			</CardContent>
		</Card>
	)
}
