import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts'
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card'
import { CalendarIcon } from '../ui/Icons'

export function ForecastChart({ data, customTooltip }) {
	return (
		<Card className="bg-gradient-to-br from-cyan-50 to-blue-50 border-cyan-200">
			<CardHeader>
				<CardTitle className="flex items-center gap-2">
					<CalendarIcon className="h-5 w-5 text-cyan-600" />
					<span className="bg-gradient-to-r from-cyan-600 to-blue-600 bg-clip-text text-transparent font-bold">
						Revenue Forecast
					</span>
				</CardTitle>
			</CardHeader>
			<CardContent>
				<div className="h-64">
					<ResponsiveContainer width="100%" height="100%">
						<AreaChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
							<defs>
								<linearGradient id="forecastGradient" x1="0" y1="0" x2="0" y2="1">
									<stop offset="5%" stopColor="#06b6d4" stopOpacity={0.8}/>
									<stop offset="95%" stopColor="#06b6d4" stopOpacity={0.2}/>
								</linearGradient>
							</defs>
							<CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" opacity={0.5} />
							<XAxis 
								dataKey="month" 
								stroke="#6b7280" 
								fontSize={11}
								tick={{ fill: '#6b7280', fontSize: 11 }}
							/>
							<YAxis 
								stroke="#6b7280" 
								fontSize={11}
								tick={{ fill: '#6b7280', fontSize: 11 }}
								tickFormatter={(value) => `$${(value / 1000).toFixed(0)}k`}
							/>
							<Tooltip content={customTooltip} />
							<Area
								type="monotone"
								dataKey="optimistic"
								stackId="1"
								stroke="#10b981"
								fill="#10b981"
								fillOpacity={0.3}
								name="Optimistic"
							/>
							<Area
								type="monotone"
								dataKey="predicted"
								stackId="2"
								stroke="#06b6d4"
								fill="url(#forecastGradient)"
								name="Predicted"
							/>
							<Area
								type="monotone"
								dataKey="pessimistic"
								stackId="3"
								stroke="#ef4444"
								fill="#ef4444"
								fillOpacity={0.3}
								name="Pessimistic"
							/>
						</AreaChart>
					</ResponsiveContainer>
				</div>
			</CardContent>
		</Card>
	)
}
