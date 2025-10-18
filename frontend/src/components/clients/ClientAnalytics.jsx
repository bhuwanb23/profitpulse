import { useMemo } from 'react'
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, BarChart, Bar, PieChart, Pie, Cell, AreaChart, Area } from 'recharts'
import { KPICard } from './KPICard'
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card'
import { TrendingUpIcon, CurrencyDollarIcon, UsersIcon, TicketIcon, ChartBarIcon } from '../ui/Icons'

export default function ClientAnalytics() {
	const profitabilityTrend = useMemo(() => [
		{ month: 'Jan', profitability: 0.70, revenue: 45000, costs: 32000 },
		{ month: 'Feb', profitability: 0.72, revenue: 47000, costs: 33000 },
		{ month: 'Mar', profitability: 0.74, revenue: 49000, costs: 34000 },
		{ month: 'Apr', profitability: 0.76, revenue: 51000, costs: 35000 },
		{ month: 'May', profitability: 0.78, revenue: 53000, costs: 36000 },
		{ month: 'Jun', profitability: 0.80, revenue: 55000, costs: 37000 },
	], [])

	const revenueBreakdown = useMemo(() => [
		{ service: 'Help Desk', revenue: 18500, percentage: 33.6, color: '#3b82f6' },
		{ service: 'Monitoring', revenue: 22000, percentage: 40.0, color: '#10b981' },
		{ service: 'Security', revenue: 8500, percentage: 15.5, color: '#f59e0b' },
		{ service: 'Consulting', revenue: 6000, percentage: 10.9, color: '#8b5cf6' },
	], [])

	const clientSatisfaction = useMemo(() => [
		{ month: 'Jan', score: 4.2, tickets: 45 },
		{ month: 'Feb', score: 4.3, tickets: 38 },
		{ month: 'Mar', score: 4.1, tickets: 52 },
		{ month: 'Apr', score: 4.4, tickets: 41 },
		{ month: 'May', score: 4.5, tickets: 35 },
		{ month: 'Jun', score: 4.6, tickets: 28 },
	], [])

	const kpiData = useMemo(() => ({
		totalRevenue: 55000,
		revenueChange: 12.5,
		profitMargin: 0.80,
		profitChange: 8.3,
		activeClients: 24,
		clientChange: 4.2,
		avgTickets: 28,
		ticketChange: -15.2
	}), [])

	const formatCurrency = (value) => `$${value.toLocaleString()}`
	const formatPercentage = (value) => `${(value * 100).toFixed(1)}%`

	const CustomTooltip = ({ active, payload, label }) => {
		if (active && payload && payload.length) {
			return (
				<div className="bg-white p-3 border border-gray-200 rounded-lg shadow-lg">
					<p className="font-medium text-gray-900">{label}</p>
					{payload.map((entry, index) => (
						<p key={index} className="text-sm" style={{ color: entry.color }}>
							{entry.name}: {entry.name.includes('Revenue') || entry.name.includes('Costs') 
								? formatCurrency(entry.value) 
								: entry.name === 'Profitability' 
								? formatPercentage(entry.value)
								: entry.value}
						</p>
					))}
				</div>
			)
		}
		return null
	}

	return (
		<div className="space-y-6">
			{/* KPI Cards */}
			<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
				<KPICard
					title="Total Revenue"
					value={kpiData.totalRevenue}
					change={kpiData.revenueChange}
					changeType="positive"
					format="currency"
					icon={CurrencyDollarIcon}
					iconColor="green"
				/>
				<KPICard
					title="Profit Margin"
					value={kpiData.profitMargin}
					change={kpiData.profitChange}
					changeType="positive"
					format="percentage"
					icon={TrendingUpIcon}
					iconColor="blue"
				/>
				<KPICard
					title="Active Clients"
					value={kpiData.activeClients}
					change={kpiData.clientChange}
					changeType="positive"
					format="number"
					icon={UsersIcon}
					iconColor="purple"
				/>
				<KPICard
					title="Avg Monthly Tickets"
					value={kpiData.avgTickets}
					change={kpiData.ticketChange}
					changeType="negative"
					format="number"
					icon={TicketIcon}
					iconColor="orange"
				/>
			</div>

			{/* Charts Row 1 */}
			<div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
				{/* Profitability & Revenue Trend */}
				<Card>
					<CardHeader>
						<CardTitle className="flex items-center gap-2">
							<TrendingUpIcon className="h-5 w-5 text-blue-600" />
							Profitability & Revenue Trend
						</CardTitle>
					</CardHeader>
					<CardContent>
						<div className="h-80">
							<ResponsiveContainer width="100%" height="100%">
								<AreaChart data={profitabilityTrend}>
									<defs>
										<linearGradient id="profitGradient" x1="0" y1="0" x2="0" y2="1">
											<stop offset="5%" stopColor="#10b981" stopOpacity={0.3}/>
											<stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
										</linearGradient>
									</defs>
									<CartesianGrid strokeDasharray="3 3" stroke="#f3f4f6" />
									<XAxis dataKey="month" stroke="#6b7280" fontSize={12} />
									<YAxis yAxisId="left" orientation="left" stroke="#6b7280" fontSize={12} />
									<YAxis yAxisId="right" orientation="right" stroke="#6b7280" fontSize={12} />
									<Tooltip content={<CustomTooltip />} />
									<Area
										yAxisId="right"
										type="monotone"
										dataKey="profitability"
										stroke="#10b981"
										strokeWidth={3}
										fill="url(#profitGradient)"
										name="Profitability"
									/>
									<Line
										yAxisId="left"
										type="monotone"
										dataKey="revenue"
										stroke="#3b82f6"
										strokeWidth={2}
										dot={{ fill: '#3b82f6', strokeWidth: 2, r: 4 }}
										name="Revenue"
									/>
								</AreaChart>
							</ResponsiveContainer>
						</div>
					</CardContent>
				</Card>

				{/* Revenue by Service */}
				<Card>
					<CardHeader>
						<CardTitle className="flex items-center gap-2">
							<ChartBarIcon className="h-5 w-5 text-purple-600" />
							Revenue by Service
						</CardTitle>
					</CardHeader>
					<CardContent>
						<div className="h-80">
							<ResponsiveContainer width="100%" height="100%">
								<PieChart width={400} height={350}>
									<Pie
										data={revenueBreakdown || []}
										cx="50%"
										cy="50%"
										outerRadius={100}
										innerRadius={40}
										paddingAngle={2}
										dataKey="revenue"
										nameKey="service"
									>
										{(revenueBreakdown || []).map((entry, index) => (
											<Cell key={`cell-${index}`} fill={entry.color || '#8884d8'} />
										))}
									</Pie>
									<Tooltip 
										formatter={(value) => [formatCurrency(value), 'Revenue']}
										labelFormatter={(label) => `Service: ${label}`}
										contentStyle={{ 
											backgroundColor: 'rgba(255, 255, 255, 0.95)', 
											border: '1px solid #e5e7eb',
											borderRadius: '8px',
											backdropFilter: 'blur(8px)'
										}}
									/>
								</PieChart>
							</ResponsiveContainer>
						</div>
						<div className="mt-4 space-y-2">
							{revenueBreakdown.map((item, index) => (
								<div key={index} className="flex items-center justify-between">
									<div className="flex items-center gap-2">
										<div 
											className="w-3 h-3 rounded-full" 
											style={{ backgroundColor: item.color }}
										/>
										<span className="text-sm text-gray-600">{item.service}</span>
									</div>
									<div className="text-right">
										<span className="text-sm font-medium text-gray-900">
											{formatCurrency(item.revenue)}
										</span>
										<span className="text-xs text-gray-500 ml-2">
											{item.percentage}%
										</span>
									</div>
								</div>
							))}
						</div>
					</CardContent>
				</Card>
			</div>

			{/* Charts Row 2 */}
			<div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
				{/* Client Satisfaction */}
				<Card>
					<CardHeader>
						<CardTitle className="flex items-center gap-2">
							<UsersIcon className="h-5 w-5 text-green-600" />
							Client Satisfaction Score
						</CardTitle>
					</CardHeader>
					<CardContent>
						<div className="h-64">
							<ResponsiveContainer width="100%" height="100%">
								<LineChart data={clientSatisfaction}>
									<CartesianGrid strokeDasharray="3 3" stroke="#f3f4f6" />
									<XAxis dataKey="month" stroke="#6b7280" fontSize={12} />
									<YAxis domain={[3.5, 5]} stroke="#6b7280" fontSize={12} />
									<Tooltip content={<CustomTooltip />} />
									<Line
										type="monotone"
										dataKey="score"
										stroke="#10b981"
										strokeWidth={3}
										dot={{ fill: '#10b981', strokeWidth: 2, r: 5 }}
										name="Satisfaction Score"
									/>
								</LineChart>
							</ResponsiveContainer>
						</div>
					</CardContent>
				</Card>

				{/* Monthly Tickets */}
				<Card>
					<CardHeader>
						<CardTitle className="flex items-center gap-2">
							<TicketIcon className="h-5 w-5 text-orange-600" />
							Monthly Support Tickets
						</CardTitle>
					</CardHeader>
					<CardContent>
						<div className="h-64">
							<ResponsiveContainer width="100%" height="100%">
								<BarChart data={clientSatisfaction}>
									<CartesianGrid strokeDasharray="3 3" stroke="#f3f4f6" />
									<XAxis dataKey="month" stroke="#6b7280" fontSize={12} />
									<YAxis stroke="#6b7280" fontSize={12} />
									<Tooltip content={<CustomTooltip />} />
									<Bar
										dataKey="tickets"
										fill="#f59e0b"
										radius={[4, 4, 0, 0]}
										name="Tickets"
									/>
								</BarChart>
							</ResponsiveContainer>
						</div>
					</CardContent>
				</Card>
			</div>
		</div>
	)
}
