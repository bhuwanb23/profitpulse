import { useMemo } from 'react'
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, BarChart, Bar, PieChart, Pie, Cell, AreaChart, Area } from 'recharts'
import { KPICard } from '../components/clients/KPICard'
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/Card'
import { Button } from '../components/ui/Button'
import { TrendingUpIcon, TicketIcon, UsersIcon, ChartBarIcon, CurrencyDollarIcon } from '../components/ui/Icons'
import { mockTickets, mockTechnicians, mockTicketCategories } from '../services/mockTickets'
import { Link } from 'react-router-dom'

export default function TicketAnalyticsPage() {
	// Calculate analytics data from mock tickets
	const analyticsData = useMemo(() => {
		// Volume trends (last 6 months)
		const volumeTrends = [
			{ month: 'Jan', tickets: 45, resolved: 42, avgTime: 4.2 },
			{ month: 'Feb', tickets: 52, resolved: 48, avgTime: 3.8 },
			{ month: 'Mar', tickets: 38, resolved: 40, avgTime: 4.5 },
			{ month: 'Apr', tickets: 61, resolved: 55, avgTime: 3.9 },
			{ month: 'May', tickets: 48, resolved: 51, avgTime: 4.1 },
			{ month: 'Jun', tickets: 55, resolved: 49, avgTime: 4.3 },
		]

		// Category breakdown
		const categoryStats = mockTicketCategories.map(category => {
			const categoryTickets = mockTickets.filter(t => t.category === category.id)
			return {
				name: category.name,
				count: categoryTickets.length,
				resolved: categoryTickets.filter(t => t.status === 'resolved').length,
				avgTime: categoryTickets.reduce((sum, t) => sum + (t.timeSpent || 0), 0) / categoryTickets.length || 0,
				color: category.color === 'blue' ? '#3b82f6' :
					   category.color === 'green' ? '#10b981' :
					   category.color === 'purple' ? '#8b5cf6' :
					   category.color === 'red' ? '#ef4444' :
					   category.color === 'orange' ? '#f59e0b' : '#6b7280'
			}
		}).filter(cat => cat.count > 0)

		// Technician performance
		const techPerformance = mockTechnicians.map(tech => {
			const techTickets = mockTickets.filter(t => t.assignedTo === tech.id)
			const resolvedTickets = techTickets.filter(t => t.status === 'resolved')
			return {
				name: tech.name,
				assigned: techTickets.length,
				resolved: resolvedTickets.length,
				avgTime: resolvedTickets.reduce((sum, t) => sum + (t.timeSpent || 0), 0) / resolvedTickets.length || 0,
				satisfaction: resolvedTickets.reduce((sum, t) => sum + (t.satisfaction || 0), 0) / resolvedTickets.length || 0
			}
		})

		// SLA compliance
		const slaStats = [
			{ status: 'Met', count: mockTickets.filter(t => t.slaStatus === 'met').length, color: '#10b981' },
			{ status: 'On Track', count: mockTickets.filter(t => t.slaStatus === 'on_track').length, color: '#3b82f6' },
			{ status: 'At Risk', count: mockTickets.filter(t => t.slaStatus === 'at_risk').length, color: '#f59e0b' },
			{ status: 'Breached', count: mockTickets.filter(t => t.slaStatus === 'breached').length, color: '#ef4444' },
		]

		// Priority distribution
		const priorityStats = [
			{ priority: 'Critical', count: mockTickets.filter(t => t.priority === 'critical').length, color: '#dc2626' },
			{ priority: 'High', count: mockTickets.filter(t => t.priority === 'high').length, color: '#ea580c' },
			{ priority: 'Medium', count: mockTickets.filter(t => t.priority === 'medium').length, color: '#ca8a04' },
			{ priority: 'Low', count: mockTickets.filter(t => t.priority === 'low').length, color: '#65a30d' },
		]

		return {
			volumeTrends,
			categoryStats,
			techPerformance,
			slaStats,
			priorityStats
		}
	}, [])

	// Calculate KPI data
	const kpiData = useMemo(() => {
		const totalTickets = mockTickets.length
		const resolvedTickets = mockTickets.filter(t => t.status === 'resolved')
		const openTickets = mockTickets.filter(t => t.status === 'open' || t.status === 'in_progress')
		const avgResolutionTime = resolvedTickets.reduce((sum, t) => sum + (t.timeSpent || 0), 0) / resolvedTickets.length || 0
		const slaCompliance = (mockTickets.filter(t => t.slaStatus === 'met').length / totalTickets) * 100
		const avgSatisfaction = resolvedTickets.filter(t => t.satisfaction).reduce((sum, t) => sum + t.satisfaction, 0) / resolvedTickets.filter(t => t.satisfaction).length || 0

		return {
			totalTickets,
			openTickets: openTickets.length,
			avgResolutionTime,
			slaCompliance,
			avgSatisfaction,
			resolutionRate: (resolvedTickets.length / totalTickets) * 100
		}
	}, [])

	const formatHours = (hours) => {
		if (hours < 1) return `${Math.round(hours * 60)}m`
		return `${hours.toFixed(1)}h`
	}

	const CustomTooltip = ({ active, payload, label }) => {
		if (active && payload && payload.length) {
			return (
				<div className="bg-white p-3 border border-gray-200 rounded-lg shadow-lg">
					<p className="font-medium text-gray-900">{label}</p>
					{payload.map((entry, index) => (
						<p key={index} className="text-sm" style={{ color: entry.color }}>
							{entry.name}: {entry.name.includes('Time') ? formatHours(entry.value) : entry.value}
						</p>
					))}
				</div>
			)
		}
		return null
	}

	return (
		<div className="space-y-6">
			{/* Back to Tickets Link */}
			<div className="flex items-center gap-2 text-sm">
				<Link 
					to="/tickets" 
					className="text-blue-600 hover:text-blue-800 flex items-center gap-1"
				>
					← Back to Tickets
				</Link>
				<span className="text-gray-400">•</span>
				<span className="text-gray-600">Ticket Analytics</span>
			</div>

			{/* Header */}
			<div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
				<div>
					<h1 className="text-3xl font-bold text-gray-900">Ticket Analytics</h1>
					<p className="text-gray-600 mt-1">Performance insights and support metrics</p>
				</div>
				
				<div className="flex flex-wrap gap-3">
					<Link to="/ticket-operations">
						<Button variant="outline" size="sm" className="flex items-center gap-2">
							<TicketIcon className="h-4 w-4" />
							Manage Tickets
						</Button>
					</Link>
					<Button variant="outline" size="sm" className="flex items-center gap-2">
						<ChartBarIcon className="h-4 w-4" />
						Export Report
					</Button>
					<Button variant="primary" size="sm" className="flex items-center gap-2">
						<TrendingUpIcon className="h-4 w-4" />
						View Insights
					</Button>
				</div>
			</div>

			{/* KPI Cards */}
			<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 xl:grid-cols-6 gap-4">
				<KPICard
					title="Total Tickets"
					value={kpiData.totalTickets}
					change={8.2}
					changeType="positive"
					format="number"
					icon={TicketIcon}
					iconColor="blue"
				/>
				<KPICard
					title="Open Tickets"
					value={kpiData.openTickets}
					change={-12.5}
					changeType="negative"
					format="number"
					icon={TicketIcon}
					iconColor="red"
				/>
				<KPICard
					title="Avg Resolution Time"
					value={kpiData.avgResolutionTime}
					change={-5.8}
					changeType="positive"
					format="number"
					icon={TrendingUpIcon}
					iconColor="green"
				/>
				<KPICard
					title="SLA Compliance"
					value={kpiData.slaCompliance / 100}
					change={3.2}
					changeType="positive"
					format="percentage"
					icon={ChartBarIcon}
					iconColor="purple"
				/>
				<KPICard
					title="Resolution Rate"
					value={kpiData.resolutionRate / 100}
					change={4.1}
					changeType="positive"
					format="percentage"
					icon={TrendingUpIcon}
					iconColor="green"
				/>
				<KPICard
					title="Avg Satisfaction"
					value={kpiData.avgSatisfaction}
					change={2.3}
					changeType="positive"
					format="number"
					icon={UsersIcon}
					iconColor="orange"
				/>
			</div>

			{/* Main Chart - Ticket Volume Trends */}
			<Card>
				<CardHeader>
					<CardTitle className="flex items-center gap-2">
						<TrendingUpIcon className="h-5 w-5 text-blue-600" />
						Ticket Volume & Resolution Trends
					</CardTitle>
				</CardHeader>
				<CardContent>
					<div className="h-64 sm:h-72 lg:h-80">
						<ResponsiveContainer width="100%" height="100%">
							<LineChart data={analyticsData.volumeTrends} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
								<defs>
									<linearGradient id="ticketGradient" x1="0" y1="0" x2="0" y2="1">
										<stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
										<stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
									</linearGradient>
									<linearGradient id="resolvedGradient" x1="0" y1="0" x2="0" y2="1">
										<stop offset="5%" stopColor="#10b981" stopOpacity={0.3}/>
										<stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
									</linearGradient>
								</defs>
								<CartesianGrid strokeDasharray="3 3" stroke="#f3f4f6" />
								<XAxis 
									dataKey="month" 
									stroke="#6b7280" 
									fontSize={11}
									tick={{ fill: '#6b7280', fontSize: 11 }}
									tickMargin={5}
								/>
								<YAxis 
									stroke="#6b7280" 
									fontSize={11}
									tick={{ fill: '#6b7280', fontSize: 11 }}
									tickMargin={5}
								/>
								<Tooltip content={<CustomTooltip />} />
								<Area
									type="monotone"
									dataKey="tickets"
									stroke="#3b82f6"
									strokeWidth={3}
									fill="url(#ticketGradient)"
									name="New Tickets"
								/>
								<Area
									type="monotone"
									dataKey="resolved"
									stroke="#10b981"
									strokeWidth={3}
									fill="url(#resolvedGradient)"
									name="Resolved Tickets"
								/>
							</LineChart>
						</ResponsiveContainer>
					</div>
				</CardContent>
			</Card>

			{/* Charts Row */}
			<div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
				{/* Category Breakdown */}
				<Card>
					<CardHeader>
						<CardTitle className="flex items-center gap-2">
							<ChartBarIcon className="h-5 w-5 text-purple-600" />
							Tickets by Category
						</CardTitle>
					</CardHeader>
					<CardContent>
						<div className="h-64 sm:h-72">
							<ResponsiveContainer width="100%" height="100%">
								<PieChart>
									<Pie
										data={analyticsData.categoryStats}
										cx="50%"
										cy="50%"
										outerRadius={80}
										innerRadius={40}
										paddingAngle={2}
										dataKey="count"
										label={({name, percent}) => `${name} ${(percent * 100).toFixed(0)}%`}
										labelLine={false}
									>
										{analyticsData.categoryStats.map((entry, index) => (
											<Cell key={`cell-${index}`} fill={entry.color} />
										))}
									</Pie>
									<Tooltip 
										formatter={(value) => [value, 'Tickets']}
										labelFormatter={(label) => `Category: ${label}`}
									/>
								</PieChart>
							</ResponsiveContainer>
						</div>
						<div className="mt-4 space-y-3">
							{analyticsData.categoryStats.map((item, index) => (
								<div key={index} className="flex items-center justify-between p-2 rounded-lg hover:bg-gray-50">
									<div className="flex items-center gap-3">
										<div 
											className="w-4 h-4 rounded-full" 
											style={{ backgroundColor: item.color }}
										/>
										<span className="text-sm font-medium text-gray-900">{item.name}</span>
									</div>
									<div className="text-right">
										<span className="text-sm font-bold text-gray-900">
											{item.count}
										</span>
										<span className="text-xs text-gray-500 ml-1">tickets</span>
									</div>
								</div>
							))}
						</div>
					</CardContent>
				</Card>

				{/* Priority Distribution */}
				<Card>
					<CardHeader>
						<CardTitle className="flex items-center gap-2">
							<TicketIcon className="h-5 w-5 text-orange-600" />
							Priority Distribution
						</CardTitle>
					</CardHeader>
					<CardContent>
						<div className="h-64 sm:h-72">
							<ResponsiveContainer width="100%" height="100%">
								<BarChart data={analyticsData.priorityStats} layout="horizontal" margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
									<CartesianGrid strokeDasharray="3 3" stroke="#f3f4f6" />
									<XAxis 
										type="number" 
										stroke="#6b7280" 
										fontSize={11}
										tick={{ fill: '#6b7280', fontSize: 11 }}
									/>
									<YAxis 
										dataKey="priority" 
										type="category" 
										stroke="#6b7280" 
										fontSize={11}
										tick={{ fill: '#6b7280', fontSize: 11 }}
										width={70}
									/>
									<Tooltip content={<CustomTooltip />} />
									<Bar
										dataKey="count"
										radius={[0, 4, 4, 0]}
										name="Tickets"
									>
										{analyticsData.priorityStats.map((entry, index) => (
											<Cell key={`cell-${index}`} fill={entry.color} />
										))}
									</Bar>
								</BarChart>
							</ResponsiveContainer>
						</div>
					</CardContent>
				</Card>
			</div>

			{/* Charts Row 2 */}
			<div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
				{/* Technician Performance */}
				<Card>
					<CardHeader>
						<CardTitle className="flex items-center gap-2">
							<UsersIcon className="h-5 w-5 text-green-600" />
							Technician Performance
						</CardTitle>
					</CardHeader>
					<CardContent>
						<div className="h-56 sm:h-64">
							<ResponsiveContainer width="100%" height="100%">
								<BarChart data={analyticsData.techPerformance} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
									<CartesianGrid strokeDasharray="3 3" stroke="#f3f4f6" />
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
									/>
									<Tooltip content={<CustomTooltip />} />
									<Bar
										dataKey="resolved"
										fill="#10b981"
										radius={[4, 4, 0, 0]}
										name="Resolved Tickets"
									/>
								</BarChart>
							</ResponsiveContainer>
						</div>
					</CardContent>
				</Card>

				{/* SLA Compliance */}
				<Card>
					<CardHeader>
						<CardTitle className="flex items-center gap-2">
							<ChartBarIcon className="h-5 w-5 text-orange-600" />
							SLA Compliance Status
						</CardTitle>
					</CardHeader>
					<CardContent>
						<div className="h-56 sm:h-64">
							<ResponsiveContainer width="100%" height="100%">
								<BarChart data={analyticsData.slaStats} layout="horizontal" margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
									<CartesianGrid strokeDasharray="3 3" stroke="#f3f4f6" />
									<XAxis 
										type="number" 
										stroke="#6b7280" 
										fontSize={11}
										tick={{ fill: '#6b7280', fontSize: 11 }}
									/>
									<YAxis 
										dataKey="status" 
										type="category" 
										stroke="#6b7280" 
										fontSize={11}
										tick={{ fill: '#6b7280', fontSize: 11 }}
										width={80}
									/>
									<Tooltip content={<CustomTooltip />} />
									<Bar
										dataKey="count"
										fill="#f59e0b"
										radius={[0, 4, 4, 0]}
										name="Tickets"
									/>
								</BarChart>
							</ResponsiveContainer>
						</div>
					</CardContent>
				</Card>
			</div>

			{/* Action Items */}
			<div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl p-6 border border-blue-100">
				<div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
					<div>
						<h3 className="text-lg font-semibold text-gray-900 mb-1">
							Ready to optimize your support operations?
						</h3>
						<p className="text-gray-600">
							Based on the analytics, we can suggest improvements to reduce resolution times and improve customer satisfaction.
						</p>
					</div>
					<div className="flex flex-wrap gap-3">
						<Button variant="outline" size="sm">
							Schedule Review
						</Button>
						<Button variant="primary" size="sm">
							Get AI Recommendations
						</Button>
					</div>
				</div>
			</div>
		</div>
	)
}
