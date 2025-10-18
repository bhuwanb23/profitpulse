import { ResponsiveContainer, RadialBarChart, RadialBar, Legend, Tooltip } from 'recharts'
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card'
import { TrendingUpIcon } from '../ui/Icons'

export function PerformanceMetricsChart({ data, customTooltip }) {
	return (
		<Card className="bg-gradient-to-br from-purple-50 to-pink-50 border-purple-200">
			<CardHeader>
				<CardTitle className="flex items-center gap-2">
					<TrendingUpIcon className="h-5 w-5 text-purple-600" />
					<span className="bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent font-bold">
						Performance Metrics
					</span>
				</CardTitle>
			</CardHeader>
			<CardContent>
				<div className="h-64">
					<ResponsiveContainer width="100%" height="100%">
						<RadialBarChart 
							cx="50%" 
							cy="50%" 
							innerRadius="20%" 
							outerRadius="90%" 
							data={data}
						>
							<RadialBar
								minAngle={15}
								label={{ position: 'insideStart', fill: '#fff', fontSize: 10 }}
								background
								clockWise
								dataKey="value"
							/>
							<Legend 
								iconSize={8}
								layout="vertical"
								verticalAlign="bottom"
								align="center"
								formatter={(value, entry) => (
									<span style={{ color: entry.color, fontSize: '10px', fontWeight: 'bold' }}>
										{value}: {entry.payload.value}%
									</span>
								)}
							/>
							<Tooltip content={customTooltip} />
						</RadialBarChart>
					</ResponsiveContainer>
				</div>
			</CardContent>
		</Card>
	)
}
