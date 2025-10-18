import { ResponsiveContainer, ComposedChart, Area, Line, Bar, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts'
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card'
import { TrendingUpIcon } from '../ui/Icons'

export function RevenueChart({ data, customTooltip }) {
	return (
		<Card className="bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 border-blue-200">
			<CardHeader className="pb-2">
				<CardTitle className="flex items-center justify-between">
					<div className="flex items-center gap-2">
						<TrendingUpIcon className="h-6 w-6 text-blue-600" />
						<span className="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
							Revenue & Profitability Analysis
						</span>
					</div>
					<div className="flex items-center gap-2 text-sm">
						<div className="flex items-center gap-1">
							<div className="w-3 h-3 rounded-full bg-gradient-to-r from-green-400 to-green-600"></div>
							<span className="text-gray-600">Revenue</span>
						</div>
						<div className="flex items-center gap-1">
							<div className="w-3 h-3 rounded-full bg-gradient-to-r from-blue-400 to-blue-600"></div>
							<span className="text-gray-600">Profit</span>
						</div>
						<div className="flex items-center gap-1">
							<div className="w-3 h-3 rounded-full bg-gradient-to-r from-purple-400 to-purple-600"></div>
							<span className="text-gray-600">Target</span>
						</div>
					</div>
				</CardTitle>
			</CardHeader>
			<CardContent>
				<div className="h-80 lg:h-96">
					<ResponsiveContainer width="100%" height="100%">
						<ComposedChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
							<defs>
								<linearGradient id="revenueGradient" x1="0" y1="0" x2="0" y2="1">
									<stop offset="5%" stopColor="#10b981" stopOpacity={0.8}/>
									<stop offset="50%" stopColor="#10b981" stopOpacity={0.4}/>
									<stop offset="95%" stopColor="#10b981" stopOpacity={0.1}/>
								</linearGradient>
								<linearGradient id="profitGradient" x1="0" y1="0" x2="0" y2="1">
									<stop offset="5%" stopColor="#3b82f6" stopOpacity={0.8}/>
									<stop offset="50%" stopColor="#3b82f6" stopOpacity={0.4}/>
									<stop offset="95%" stopColor="#3b82f6" stopOpacity={0.1}/>
								</linearGradient>
							</defs>
							<CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" opacity={0.5} />
							<XAxis 
								dataKey="month" 
								stroke="#6b7280" 
								fontSize={12}
								tick={{ fill: '#6b7280', fontSize: 12 }}
								tickMargin={10}
							/>
							<YAxis 
								stroke="#6b7280" 
								fontSize={11}
								tick={{ fill: '#6b7280', fontSize: 11 }}
								tickMargin={10}
								tickFormatter={(value) => `$${(value / 1000).toFixed(0)}k`}
							/>
							<Tooltip content={customTooltip} />
							<Area
								type="monotone"
								dataKey="revenue"
								stroke="#10b981"
								strokeWidth={4}
								fill="url(#revenueGradient)"
								name="Revenue"
							/>
							<Area
								type="monotone"
								dataKey="profit"
								stroke="#3b82f6"
								strokeWidth={3}
								fill="url(#profitGradient)"
								name="Profit"
							/>
							<Line
								type="monotone"
								dataKey="target"
								stroke="#8b5cf6"
								strokeWidth={2}
								strokeDasharray="5 5"
								dot={{ fill: '#8b5cf6', strokeWidth: 2, r: 4 }}
								name="Target"
							/>
							<Bar
								dataKey="customers"
								fill="#f59e0b"
								radius={[2, 2, 0, 0]}
								name="Customers"
								opacity={0.6}
								yAxisId="right"
							/>
						</ComposedChart>
					</ResponsiveContainer>
				</div>
			</CardContent>
		</Card>
	)
}
