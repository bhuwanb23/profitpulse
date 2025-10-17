import { useMemo, useState } from 'react'
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, AreaChart, Area, BarChart, Bar, PieChart, Pie, Cell } from 'recharts'
import QuickActions from '../components/dashboard/QuickActions'

const StatCard = ({ title, value, change, positive, icon, color = 'blue' }) => {
	const colorClasses = {
		blue: 'from-blue-500 to-blue-600',
		green: 'from-green-500 to-green-600',
		orange: 'from-orange-500 to-orange-600',
		purple: 'from-purple-500 to-purple-600',
		red: 'from-red-500 to-red-600'
	}
	
	return (
		<div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm hover:shadow-md transition-shadow duration-200">
			<div className="flex items-center justify-between">
				<div className="flex-1">
					<p className="text-sm font-medium text-gray-600 mb-1">{title}</p>
					<p className="text-2xl font-bold text-gray-900">{value}</p>
					<div className={`flex items-center mt-2 text-sm ${positive ? 'text-green-600' : 'text-red-600'}`}>
						<span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${positive ? 'bg-green-100' : 'bg-red-100'}`}>
							{positive ? '↗' : '↘'} {change}
						</span>
					</div>
				</div>
				<div className={`p-3 rounded-lg bg-gradient-to-r ${colorClasses[color]}`}>
					{icon}
				</div>
			</div>
		</div>
	)
}

export default function Dashboard() {
	const [timeRange, setTimeRange] = useState('12months')
	
	const stats = useMemo(() => ([
		{ 
			title: 'Total Revenue', 
			value: '$88,400', 
			change: '12.4%', 
			positive: true, 
			icon: <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20"><path d="M8.433 7.418c.155-.103.346-.196.567-.267v1.698a2.305 2.305 0 01-.567-.267C8.07 8.34 8 8.114 8 8c0-.114.07-.34.433-.582zM11 12.849v-1.698c.22.071.412.164.567.267.364.243.433.468.433.582 0 .114-.07.34-.433.582a2.305 2.305 0 01-.567.267z"/><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-13a1 1 0 10-2 0v.092a4.535 4.535 0 00-1.676.662C6.602 6.234 6 7.009 6 8c0 .99.602 1.765 1.324 2.246.48.32 1.054.545 1.676.662v1.941c-.391-.127-.68-.317-.843-.504a1 1 0 10-1.51 1.31c.562.649 1.413 1.076 2.353 1.253V15a1 1 0 102 0v-.092a4.535 4.535 0 001.676-.662C13.398 13.766 14 12.991 14 12c0-.99-.602-1.765-1.324-2.246A4.535 4.535 0 0011 9.092V7.151c.391.127.68.317.843.504a1 1 0 101.511-1.31c-.563-.649-1.413-1.076-2.354-1.253V5z" clipRule="evenodd"/></svg>,
			color: 'green'
		},
		{ 
			title: 'Active Clients', 
			value: '42', 
			change: '3.8%', 
			positive: true, 
			icon: <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20"><path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3z"/></svg>,
			color: 'blue'
		},
		{ 
			title: 'Open Tickets', 
			value: '17', 
			change: '5.1%', 
			positive: false, 
			icon: <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd"/></svg>,
			color: 'orange'
		},
		{ 
			title: 'Profitability', 
			value: '31.2%', 
			change: '1.2%', 
			positive: true, 
			icon: <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11.707 4.707a1 1 0 00-1.414-1.414L10 9.586 8.707 8.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"/></svg>,
			color: 'purple'
		},
	]), [])

	const revenueData = useMemo(() => (
		[
			{ month: 'Jan', revenue: 6400, profit: 3200 },
			{ month: 'Feb', revenue: 7200, profit: 3600 },
			{ month: 'Mar', revenue: 8800, profit: 4400 },
			{ month: 'Apr', revenue: 7600, profit: 3800 },
			{ month: 'May', revenue: 9100, profit: 4550 },
			{ month: 'Jun', revenue: 9800, profit: 4900 },
			{ month: 'Jul', revenue: 10400, profit: 5200 },
			{ month: 'Aug', revenue: 9900, profit: 4950 },
			{ month: 'Sep', revenue: 11200, profit: 5600 },
			{ month: 'Oct', revenue: 12400, profit: 6200 },
			{ month: 'Nov', revenue: 11800, profit: 5900 },
			{ month: 'Dec', revenue: 13100, profit: 6550 },
		]
	), [])

	const ticketData = useMemo(() => (
		[
			{ name: 'Open', value: 17, color: '#EF4444' },
			{ name: 'In Progress', value: 23, color: '#F59E0B' },
			{ name: 'Resolved', value: 45, color: '#10B981' },
			{ name: 'Closed', value: 15, color: '#6B7280' },
		]
	), [])

	const clientSatisfactionData = useMemo(() => (
		[
			{ month: 'Jan', satisfaction: 85 },
			{ month: 'Feb', satisfaction: 87 },
			{ month: 'Mar', satisfaction: 89 },
			{ month: 'Apr', satisfaction: 86 },
			{ month: 'May', satisfaction: 91 },
			{ month: 'Jun', satisfaction: 88 },
			{ month: 'Jul', satisfaction: 92 },
			{ month: 'Aug', satisfaction: 90 },
			{ month: 'Sep', satisfaction: 94 },
			{ month: 'Oct', satisfaction: 93 },
			{ month: 'Nov', satisfaction: 95 },
			{ month: 'Dec', satisfaction: 96 },
		]
	), [])

	return (
		<div className="min-h-screen bg-gray-50">
			<div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
				{/* Header */}
				<div className="mb-8">
					<div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
						<div>
							<h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
							<p className="mt-2 text-gray-600">Welcome back! Here's what's happening with your business.</p>
						</div>
						<div className="mt-4 sm:mt-0">
							<button className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-200">
								<svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
								</svg>
								Generate Report
							</button>
						</div>
					</div>
				</div>

				{/* Stats Grid */}
				<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
					{stats.map((stat) => (
						<StatCard key={stat.title} {...stat} />
					))}
				</div>

				{/* Main Content Grid */}
				<div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
					{/* Revenue Chart */}
					<div className="lg:col-span-2 bg-white rounded-xl shadow-sm border border-gray-200 p-6">
						<div className="flex items-center justify-between mb-6">
							<h2 className="text-xl font-semibold text-gray-900">Revenue Analytics</h2>
							<select 
								value={timeRange}
								onChange={(e) => setTimeRange(e.target.value)}
								className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
							>
								<option value="30days">Last 30 days</option>
								<option value="6months">Last 6 months</option>
								<option value="12months">Last 12 months</option>
							</select>
						</div>
						<div className="h-80">
							<ResponsiveContainer width="100%" height="100%">
								<AreaChart data={revenueData}>
									<defs>
										<linearGradient id="revenueGradient" x1="0" y1="0" x2="0" y2="1">
											<stop offset="5%" stopColor="#3B82F6" stopOpacity={0.8}/>
											<stop offset="95%" stopColor="#3B82F6" stopOpacity={0.1}/>
										</linearGradient>
										<linearGradient id="profitGradient" x1="0" y1="0" x2="0" y2="1">
											<stop offset="5%" stopColor="#10B981" stopOpacity={0.8}/>
											<stop offset="95%" stopColor="#10B981" stopOpacity={0.1}/>
										</linearGradient>
									</defs>
									<CartesianGrid strokeDasharray="3 3" stroke="#F3F4F6" />
									<XAxis 
										dataKey="month" 
										axisLine={false}
										tickLine={false}
										tick={{ fill: '#6B7280', fontSize: 12 }}
									/>
									<YAxis 
										axisLine={false}
										tickLine={false}
										tick={{ fill: '#6B7280', fontSize: 12 }}
										tickFormatter={(value) => `$${(value / 1000).toFixed(0)}k`}
									/>
									<Tooltip 
										contentStyle={{
											backgroundColor: 'white',
											border: '1px solid #E5E7EB',
											borderRadius: '8px',
											boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
										}}
										formatter={(value, name) => [`$${value.toLocaleString()}`, name === 'revenue' ? 'Revenue' : 'Profit']}
									/>
									<Area
										type="monotone"
										dataKey="revenue"
										stroke="#3B82F6"
										strokeWidth={2}
										fill="url(#revenueGradient)"
									/>
									<Area
										type="monotone"
										dataKey="profit"
										stroke="#10B981"
										strokeWidth={2}
										fill="url(#profitGradient)"
									/>
								</AreaChart>
							</ResponsiveContainer>
						</div>
					</div>

					{/* AI Recommendations */}
					<div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
						<h2 className="text-xl font-semibold text-gray-900 mb-6">AI Recommendations</h2>
						<div className="space-y-4">
							{[
								{ title: 'Increase Help Desk Pricing', impact: 'High', score: 0.85, icon: '💰' },
								{ title: 'Add Network Monitoring', impact: 'Medium', score: 0.75, icon: '🔍' },
								{ title: 'Optimize Software Licenses', impact: 'Low', score: 0.70, icon: '⚙️' },
							].map((rec) => (
								<div key={rec.title} className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors duration-200">
									<div className="flex items-start justify-between">
										<div className="flex items-start space-x-3">
											<span className="text-lg">{rec.icon}</span>
											<div>
												<h3 className="font-medium text-sm text-gray-900">{rec.title}</h3>
												<p className="text-xs text-gray-500 mt-1">Impact: {rec.impact}</p>
											</div>
										</div>
										<div className="text-right">
											<div className="text-xs font-medium text-blue-600">
												{(rec.score * 100).toFixed(0)}% confidence
											</div>
											<div className="w-16 bg-gray-200 rounded-full h-1.5 mt-1">
												<div 
													className="bg-blue-600 h-1.5 rounded-full" 
													style={{ width: `${rec.score * 100}%` }}
												></div>
											</div>
										</div>
									</div>
								</div>
							))}
						</div>
					</div>
				</div>

				{/* Quick Actions */}
				<QuickActions />

				{/* Bottom Grid */}
				<div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
					{/* Ticket Status */}
					<div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
						<h2 className="text-xl font-semibold text-gray-900 mb-6">Ticket Status Overview</h2>
						<div className="h-64">
							<ResponsiveContainer width="100%" height="100%">
								<PieChart>
									<Pie
										data={ticketData}
										cx="50%"
										cy="50%"
										innerRadius={60}
										outerRadius={100}
										paddingAngle={5}
										dataKey="value"
									>
										{ticketData.map((entry, index) => (
											<Cell key={`cell-${index}`} fill={entry.color} />
										))}
									</Pie>
									<Tooltip />
								</PieChart>
							</ResponsiveContainer>
						</div>
						<div className="grid grid-cols-2 gap-4 mt-4">
							{ticketData.map((item) => (
								<div key={item.name} className="flex items-center space-x-2">
									<div 
										className="w-3 h-3 rounded-full" 
										style={{ backgroundColor: item.color }}
									></div>
									<span className="text-sm text-gray-600">{item.name}: {item.value}</span>
								</div>
							))}
						</div>
					</div>

					{/* Client Satisfaction */}
					<div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
						<h2 className="text-xl font-semibold text-gray-900 mb-6">Client Satisfaction Trend</h2>
						<div className="h-64">
							<ResponsiveContainer width="100%" height="100%">
								<LineChart data={clientSatisfactionData}>
									<CartesianGrid strokeDasharray="3 3" stroke="#F3F4F6" />
									<XAxis 
										dataKey="month" 
										axisLine={false}
										tickLine={false}
										tick={{ fill: '#6B7280', fontSize: 12 }}
									/>
									<YAxis 
										axisLine={false}
										tickLine={false}
										tick={{ fill: '#6B7280', fontSize: 12 }}
										domain={[80, 100]}
									/>
									<Tooltip 
										contentStyle={{
											backgroundColor: 'white',
											border: '1px solid #E5E7EB',
											borderRadius: '8px',
											boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
										}}
										formatter={(value) => [`${value}%`, 'Satisfaction']}
									/>
									<Line
										type="monotone"
										dataKey="satisfaction"
										stroke="#10B981"
										strokeWidth={3}
										dot={{ fill: '#10B981', strokeWidth: 2, r: 4 }}
										activeDot={{ r: 6, stroke: '#10B981', strokeWidth: 2 }}
									/>
								</LineChart>
							</ResponsiveContainer>
						</div>
					</div>
				</div>

				{/* Recent Activity */}
				<div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
					<h2 className="text-xl font-semibold text-gray-900 mb-6">Recent Activity</h2>
					<div className="space-y-4">
						{[
							{ id: 'TKT-001', title: 'Email server down', status: 'Resolved', time: '2 hours ago', client: 'Acme Corp' },
							{ id: 'TKT-002', title: 'VPN connection issues', status: 'In Progress', time: '4 hours ago', client: 'TechStart Inc' },
							{ id: 'TKT-003', title: 'Software installation request', status: 'Open', time: '6 hours ago', client: 'Global Solutions' },
							{ id: 'TKT-004', title: 'Network performance optimization', status: 'Resolved', time: '8 hours ago', client: 'Innovation Labs' },
						].map((ticket) => (
							<div key={ticket.id} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors duration-200">
								<div className="flex items-center space-x-4">
									<div className={`w-3 h-3 rounded-full ${
										ticket.status === 'Resolved' ? 'bg-green-500' :
										ticket.status === 'In Progress' ? 'bg-yellow-500' : 'bg-red-500'
									}`}></div>
									<div>
										<h3 className="font-medium text-gray-900">{ticket.title}</h3>
										<p className="text-sm text-gray-500">{ticket.id} • {ticket.client}</p>
									</div>
								</div>
								<div className="text-right">
									<span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
										ticket.status === 'Resolved' ? 'bg-green-100 text-green-800' :
										ticket.status === 'In Progress' ? 'bg-yellow-100 text-yellow-800' : 'bg-red-100 text-red-800'
									}`}>
										{ticket.status}
									</span>
									<p className="text-xs text-gray-500 mt-1">{ticket.time}</p>
								</div>
							</div>
						))}
					</div>
				</div>
			</div>
		</div>
	)
}
