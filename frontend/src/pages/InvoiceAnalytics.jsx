import { useMemo } from 'react'
import { 
	ResponsiveContainer, 
	LineChart, 
	Line, 
	XAxis, 
	YAxis, 
	CartesianGrid, 
	Tooltip, 
	BarChart, 
	Bar, 
	PieChart, 
	Pie, 
	Cell, 
	AreaChart, 
	Area,
	ComposedChart,
	RadialBarChart,
	RadialBar,
	Legend
} from 'recharts'
import { KPICard } from '../components/clients/KPICard'
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/Card'
import { Button } from '../components/ui/Button'
import { TrendingUpIcon, CurrencyDollarIcon, DocumentTextIcon, ChartBarIcon, ClockIcon, ExclamationTriangleIcon } from '../components/ui/Icons'
import { mockInvoices, mockInvoiceCategories, mockPaymentMethods } from '../services/mockFinancial'
import { Link } from 'react-router-dom'

export default function InvoiceAnalyticsPage() {
	// Calculate enhanced analytics data
	const analyticsData = useMemo(() => {
		// Enhanced revenue trends with more data points
		const revenueTrends = [
			{ 
				month: 'Jan', 
				revenue: 8800, 
				invoices: 1, 
				avgValue: 8800,
				target: 12000,
				growth: 15.2,
				collections: 8800,
				outstanding: 0
			},
			{ 
				month: 'Feb', 
				revenue: 1650, 
				invoices: 1, 
				avgValue: 1650,
				target: 12000,
				growth: -81.3,
				collections: 0,
				outstanding: 1650
			},
			{ 
				month: 'Mar', 
				revenue: 0, 
				invoices: 0, 
				avgValue: 0,
				target: 12000,
				growth: -100,
				collections: 0,
				outstanding: 0
			},
			{ 
				month: 'Apr', 
				revenue: 16495, 
				invoices: 3, 
				avgValue: 5498,
				target: 12000,
				growth: 37.5,
				collections: 3740,
				outstanding: 12755
			},
			{ 
				month: 'May', 
				revenue: 6380, 
				invoices: 1, 
				avgValue: 6380,
				target: 12000,
				growth: -61.3,
				collections: 6380,
				outstanding: 0
			},
			{ 
				month: 'Jun', 
				revenue: 2420, 
				invoices: 1, 
				avgValue: 2420,
				target: 12000,
				growth: -62.1,
				collections: 0,
				outstanding: 2420
			},
		]

		// Enhanced status breakdown with percentages and values
		const statusStats = [
			{ 
				name: 'Paid', 
				count: mockInvoices.filter(i => i.status === 'paid').length,
				value: mockInvoices.filter(i => i.status === 'paid').reduce((sum, i) => sum + i.total, 0),
				fill: '#10b981',
				percentage: 0
			},
			{ 
				name: 'Sent', 
				count: mockInvoices.filter(i => i.status === 'sent').length,
				value: mockInvoices.filter(i => i.status === 'sent').reduce((sum, i) => sum + i.total, 0),
				fill: '#3b82f6',
				percentage: 0
			},
			{ 
				name: 'Overdue', 
				count: mockInvoices.filter(i => i.status === 'overdue').length,
				value: mockInvoices.filter(i => i.status === 'overdue').reduce((sum, i) => sum + i.total, 0),
				fill: '#ef4444',
				percentage: 0
			},
			{ 
				name: 'Draft', 
				count: mockInvoices.filter(i => i.status === 'draft').length,
				value: mockInvoices.filter(i => i.status === 'draft').reduce((sum, i) => sum + i.total, 0),
				fill: '#6b7280',
				percentage: 0
			},
		]

		// Calculate percentages for status stats
		const totalValue = statusStats.reduce((sum, stat) => sum + stat.value, 0)
		statusStats.forEach(stat => {
			stat.percentage = totalValue > 0 ? (stat.value / totalValue) * 100 : 0
		})

		// Enhanced payment method breakdown
		const methodStats = [
			{
				name: 'Credit Card',
				count: mockInvoices.filter(i => i.method === 'credit_card').length,
				revenue: mockInvoices.filter(i => i.method === 'credit_card').reduce((sum, i) => sum + i.total, 0),
				fill: '#3b82f6',
				trend: 12.5
			},
			{
				name: 'Bank Transfer',
				count: mockInvoices.filter(i => i.method === 'bank_transfer').length,
				revenue: mockInvoices.filter(i => i.method === 'bank_transfer').reduce((sum, i) => sum + i.total, 0),
				fill: '#10b981',
				trend: 8.3
			},
			{
				name: 'Wire Transfer',
				count: mockInvoices.filter(i => i.method === 'wire_transfer').length,
				revenue: mockInvoices.filter(i => i.method === 'wire_transfer').reduce((sum, i) => sum + i.total, 0),
				fill: '#8b5cf6',
				trend: 15.7
			}
		].filter(method => method.count > 0)

		// Enhanced client revenue breakdown with growth metrics
		const clientStats = Array.from(new Set(mockInvoices.map(i => i.client))).map((client, index) => {
			const clientInvoices = mockInvoices.filter(i => i.client === client)
			const paidInvoices = clientInvoices.filter(i => i.status === 'paid')
			const revenue = paidInvoices.reduce((sum, i) => sum + i.total, 0)
			return {
				name: client.length > 12 ? client.substring(0, 12) + '...' : client,
				fullName: client,
				invoices: clientInvoices.length,
				revenue: revenue,
				pending: clientInvoices.filter(i => i.status === 'sent').reduce((sum, i) => sum + i.total, 0),
				overdue: clientInvoices.filter(i => i.status === 'overdue').reduce((sum, i) => sum + i.total, 0),
				growth: [15.2, -8.3, 22.7, 5.1, -12.4, 18.9, 7.2, 31.5][index] || 0,
				fill: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4', '#84cc16', '#f97316'][index] || '#6b7280'
			}
		}).sort((a, b) => b.revenue - a.revenue).slice(0, 6)

		// Enhanced collection performance with aging analysis
		const collectionStats = [
			{ month: 'Jan', collected: 8800, outstanding: 0, collectionRate: 100, aging30: 0, aging60: 0, aging90: 0 },
			{ month: 'Feb', collected: 0, outstanding: 1650, collectionRate: 0, aging30: 1650, aging60: 0, aging90: 0 },
			{ month: 'Mar', collected: 0, outstanding: 0, collectionRate: 0, aging30: 0, aging60: 0, aging90: 0 },
			{ month: 'Apr', collected: 3740, outstanding: 12155, collectionRate: 23.5, aging30: 8000, aging60: 3155, aging90: 1000 },
			{ month: 'May', collected: 6380, outstanding: 0, collectionRate: 100, aging30: 0, aging60: 0, aging90: 0 },
			{ month: 'Jun', collected: 0, outstanding: 2420, collectionRate: 0, aging30: 2420, aging60: 0, aging90: 0 },
		]

		// Performance metrics for radial charts
		const performanceMetrics = [
			{ name: 'Collection Rate', value: 62.5, fill: '#10b981', target: 85 },
			{ name: 'On-Time Payment', value: 45.8, fill: '#3b82f6', target: 70 },
			{ name: 'Customer Satisfaction', value: 78.3, fill: '#f59e0b', target: 90 },
			{ name: 'Revenue Growth', value: 23.7, fill: '#8b5cf6', target: 30 }
		]

		return {
			revenueTrends,
			statusStats,
			methodStats,
			clientStats,
			collectionStats,
			performanceMetrics
		}
	}, [])

	// Calculate KPI data
	const kpiData = useMemo(() => {
		const totalInvoices = mockInvoices.length
		const paidInvoices = mockInvoices.filter(i => i.status === 'paid')
		const overdueInvoices = mockInvoices.filter(i => i.status === 'overdue')
		const sentInvoices = mockInvoices.filter(i => i.status === 'sent')
		
		const totalRevenue = paidInvoices.reduce((sum, i) => sum + i.total, 0)
		const pendingRevenue = sentInvoices.reduce((sum, i) => sum + i.total, 0)
		const overdueAmount = overdueInvoices.reduce((sum, i) => sum + i.total, 0)
		const avgInvoiceValue = totalRevenue / paidInvoices.length || 0
		const collectionRate = (paidInvoices.length / totalInvoices) * 100
		const avgPaymentTime = 12.5 // Mock average payment time in days

		return {
			totalRevenue,
			pendingRevenue,
			overdueAmount,
			avgInvoiceValue,
			collectionRate,
			avgPaymentTime,
			totalInvoices,
			paidCount: paidInvoices.length
		}
	}, [])

	const formatCurrency = (amount) => {
		return new Intl.NumberFormat('en-US', {
			style: 'currency',
			currency: 'USD'
		}).format(amount)
	}

	const CustomTooltip = ({ active, payload, label }) => {
		if (active && payload && payload.length) {
			return (
				<div className="bg-white/95 backdrop-blur-sm p-4 border border-gray-200 rounded-xl shadow-xl">
					<p className="font-semibold text-gray-900 mb-2">{label}</p>
					{payload.map((entry, index) => (
						<div key={index} className="flex items-center gap-2 mb-1">
							<div 
								className="w-3 h-3 rounded-full" 
								style={{ backgroundColor: entry.color }}
							/>
							<span className="text-sm font-medium" style={{ color: entry.color }}>
								{entry.name}: {entry.name.includes('Rate') || entry.name.includes('Growth') ? `${entry.value}%` : 
									entry.name.includes('Revenue') || entry.name.includes('collected') || entry.name.includes('outstanding') || entry.name.includes('target') ? 
									formatCurrency(entry.value) : entry.value}
							</span>
						</div>
					))}
				</div>
			)
		}
		return null
	}

	const CustomPieTooltip = ({ active, payload }) => {
		if (active && payload && payload.length) {
			const data = payload[0].payload
			return (
				<div className="bg-white/95 backdrop-blur-sm p-4 border border-gray-200 rounded-xl shadow-xl">
					<p className="font-semibold text-gray-900 mb-2">{data.name}</p>
					<div className="space-y-1">
						<div className="flex justify-between gap-4">
							<span className="text-sm text-gray-600">Count:</span>
							<span className="text-sm font-medium">{data.count}</span>
						</div>
						<div className="flex justify-between gap-4">
							<span className="text-sm text-gray-600">Value:</span>
							<span className="text-sm font-medium">{formatCurrency(data.value)}</span>
						</div>
						<div className="flex justify-between gap-4">
							<span className="text-sm text-gray-600">Percentage:</span>
							<span className="text-sm font-medium">{data.percentage.toFixed(1)}%</span>
						</div>
					</div>
				</div>
			)
		}
		return null
	}

	return (
		<div className="space-y-6">
			{/* Back to Invoices Link */}
			<div className="flex items-center gap-2 text-sm">
				<Link 
					to="/invoices" 
					className="text-blue-600 hover:text-blue-800 flex items-center gap-1"
				>
					← Back to Invoices
				</Link>
				<span className="text-gray-400">•</span>
				<span className="text-gray-600">Invoice Analytics</span>
			</div>

			{/* Header */}
			<div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
				<div>
					<h1 className="text-3xl font-bold text-gray-900">Invoice Analytics</h1>
					<p className="text-gray-600 mt-1">Financial insights and billing performance</p>
				</div>
				
				<div className="flex flex-wrap gap-3">
					<Link to="/invoice-operations">
						<Button variant="outline" size="sm" className="flex items-center gap-2">
							<DocumentTextIcon className="h-4 w-4" />
							Create Invoice
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
					title="Total Revenue"
					value={kpiData.totalRevenue}
					change={8.3}
					changeType="positive"
					format="currency"
					icon={CurrencyDollarIcon}
					iconColor="green"
				/>
				<KPICard
					title="Pending Revenue"
					value={kpiData.pendingRevenue}
					change={-5.2}
					changeType="negative"
					format="currency"
					icon={ClockIcon}
					iconColor="orange"
				/>
				<KPICard
					title="Overdue Amount"
					value={kpiData.overdueAmount}
					change={15.7}
					changeType="negative"
					format="currency"
					icon={ExclamationTriangleIcon}
					iconColor="red"
				/>
				<KPICard
					title="Avg Invoice Value"
					value={kpiData.avgInvoiceValue}
					change={3.1}
					changeType="positive"
					format="currency"
					icon={CurrencyDollarIcon}
					iconColor="purple"
				/>
				<KPICard
					title="Collection Rate"
					value={kpiData.collectionRate / 100}
					change={2.4}
					changeType="positive"
					format="percentage"
					icon={ChartBarIcon}
					iconColor="blue"
				/>
				<KPICard
					title="Avg Payment Time"
					value={kpiData.avgPaymentTime}
					change={-1.8}
					changeType="positive"
					format="number"
					icon={ClockIcon}
					iconColor="green"
				/>
			</div>

			{/* Hero Chart - Enhanced Revenue & Performance Dashboard */}
			<Card className="bg-gradient-to-br from-blue-50 via-white to-purple-50 border-blue-200">
				<CardHeader className="pb-2">
					<CardTitle className="flex items-center justify-between">
						<div className="flex items-center gap-2">
							<TrendingUpIcon className="h-6 w-6 text-blue-600" />
							<span className="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
								Revenue Performance Dashboard
							</span>
						</div>
						<div className="flex items-center gap-2 text-sm">
							<div className="flex items-center gap-1">
								<div className="w-3 h-3 rounded-full bg-gradient-to-r from-green-400 to-green-600"></div>
								<span className="text-gray-600">Revenue</span>
							</div>
							<div className="flex items-center gap-1">
								<div className="w-3 h-3 rounded-full bg-gradient-to-r from-blue-400 to-blue-600"></div>
								<span className="text-gray-600">Target</span>
							</div>
							<div className="flex items-center gap-1">
								<div className="w-3 h-3 rounded-full bg-gradient-to-r from-orange-400 to-orange-600"></div>
								<span className="text-gray-600">Collections</span>
							</div>
						</div>
					</CardTitle>
				</CardHeader>
				<CardContent>
					<div className="h-80 lg:h-96">
						<ResponsiveContainer width="100%" height="100%">
							<ComposedChart data={analyticsData.revenueTrends} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
								<defs>
									<linearGradient id="revenueGradient" x1="0" y1="0" x2="0" y2="1">
										<stop offset="5%" stopColor="#10b981" stopOpacity={0.8}/>
										<stop offset="50%" stopColor="#10b981" stopOpacity={0.4}/>
										<stop offset="95%" stopColor="#10b981" stopOpacity={0.1}/>
									</linearGradient>
									<linearGradient id="targetGradient" x1="0" y1="0" x2="0" y2="1">
										<stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
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
								<Tooltip content={<CustomTooltip />} />
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
									dataKey="target"
									stroke="#3b82f6"
									strokeWidth={2}
									strokeDasharray="5 5"
									fill="url(#targetGradient)"
									name="Target"
								/>
								<Bar
									dataKey="collections"
									fill="#f59e0b"
									radius={[4, 4, 0, 0]}
									name="Collections"
									opacity={0.7}
								/>
								<Line
									type="monotone"
									dataKey="outstanding"
									stroke="#ef4444"
									strokeWidth={3}
									dot={{ fill: '#ef4444', strokeWidth: 2, r: 5 }}
									name="Outstanding"
								/>
							</ComposedChart>
						</ResponsiveContainer>
					</div>
				</CardContent>
			</Card>

			{/* Enhanced Charts Grid */}
			<div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
				{/* Modern Donut Chart - Invoice Status */}
				<Card className="bg-gradient-to-br from-purple-50 to-pink-50 border-purple-200">
					<CardHeader>
						<CardTitle className="flex items-center gap-2">
							<ChartBarIcon className="h-5 w-5 text-purple-600" />
							<span className="bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent font-bold">
								Invoice Status
							</span>
						</CardTitle>
					</CardHeader>
					<CardContent>
						<div className="h-64">
							<ResponsiveContainer width="100%" height="100%">
								<PieChart width={400} height={300}>
									<Pie
										data={analyticsData.statusStats || []}
										cx="50%"
										cy="50%"
										outerRadius={85}
										innerRadius={50}
										paddingAngle={3}
										dataKey="value"
										nameKey="name"
									>
										{(analyticsData.statusStats || []).map((entry, index) => (
											<Cell 
												key={`cell-${index}`} 
												fill={entry.fill || '#8884d8'}
												stroke={entry.fill || '#8884d8'}
												strokeWidth={2}
											/>
										))}
									</Pie>
									<Tooltip content={<CustomPieTooltip />} />
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

				{/* Performance Metrics - Radial Chart */}
				<Card className="bg-gradient-to-br from-green-50 to-emerald-50 border-green-200">
					<CardHeader>
						<CardTitle className="flex items-center gap-2">
							<TrendingUpIcon className="h-5 w-5 text-green-600" />
							<span className="bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent font-bold">
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
									data={analyticsData.performanceMetrics}
								>
									<RadialBar
										minAngle={15}
										label={{ position: 'insideStart', fill: '#fff', fontSize: 12 }}
										background
										clockWise
										dataKey="value"
									/>
									<Legend 
										iconSize={10}
										layout="vertical"
										verticalAlign="bottom"
										align="center"
										formatter={(value, entry) => (
											<span style={{ color: entry.color, fontSize: '12px', fontWeight: 'bold' }}>
												{value}: {entry.payload.value}%
											</span>
										)}
									/>
									<Tooltip content={<CustomTooltip />} />
								</RadialBarChart>
							</ResponsiveContainer>
						</div>
					</CardContent>
				</Card>

				{/* Top Clients - Enhanced Bar Chart */}
				<Card className="bg-gradient-to-br from-orange-50 to-red-50 border-orange-200">
					<CardHeader>
						<CardTitle className="flex items-center gap-2">
							<CurrencyDollarIcon className="h-5 w-5 text-orange-600" />
							<span className="bg-gradient-to-r from-orange-600 to-red-600 bg-clip-text text-transparent font-bold">
								Top Clients
							</span>
						</CardTitle>
					</CardHeader>
					<CardContent>
						<div className="h-64">
							<ResponsiveContainer width="100%" height="100%">
								<BarChart 
									data={analyticsData.clientStats} 
									layout="horizontal"
									margin={{ top: 5, right: 30, left: 5, bottom: 5 }}
								>
									<CartesianGrid strokeDasharray="3 3" stroke="#f3f4f6" />
									<XAxis 
										type="number" 
										stroke="#6b7280" 
										fontSize={10}
										tickFormatter={(value) => `$${(value / 1000).toFixed(0)}k`}
									/>
									<YAxis 
										dataKey="name" 
										type="category" 
										stroke="#6b7280" 
										fontSize={10}
										width={80}
									/>
									<Tooltip content={<CustomTooltip />} />
									<Bar
										dataKey="revenue"
										radius={[0, 8, 8, 0]}
										name="Revenue"
									>
										{analyticsData.clientStats.map((entry, index) => (
											<Cell key={`cell-${index}`} fill={entry.fill} />
										))}
									</Bar>
								</BarChart>
							</ResponsiveContainer>
						</div>
					</CardContent>
				</Card>
			</div>

			{/* Payment Methods & Collection Analysis */}
			<div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
				{/* Payment Methods - Enhanced */}
				<Card className="bg-gradient-to-br from-indigo-50 to-blue-50 border-indigo-200">
					<CardHeader>
						<CardTitle className="flex items-center gap-2">
							<CurrencyDollarIcon className="h-5 w-5 text-indigo-600" />
							<span className="bg-gradient-to-r from-indigo-600 to-blue-600 bg-clip-text text-transparent font-bold">
								Payment Methods
							</span>
						</CardTitle>
					</CardHeader>
					<CardContent>
						<div className="h-64">
							<ResponsiveContainer width="100%" height="100%">
								<BarChart data={analyticsData.methodStats} margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
									<defs>
										<linearGradient id="methodGradient1" x1="0" y1="0" x2="0" y2="1">
											<stop offset="5%" stopColor="#3b82f6" stopOpacity={0.8}/>
											<stop offset="95%" stopColor="#3b82f6" stopOpacity={0.3}/>
										</linearGradient>
										<linearGradient id="methodGradient2" x1="0" y1="0" x2="0" y2="1">
											<stop offset="5%" stopColor="#10b981" stopOpacity={0.8}/>
											<stop offset="95%" stopColor="#10b981" stopOpacity={0.3}/>
										</linearGradient>
										<linearGradient id="methodGradient3" x1="0" y1="0" x2="0" y2="1">
											<stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.8}/>
											<stop offset="95%" stopColor="#8b5cf6" stopOpacity={0.3}/>
										</linearGradient>
									</defs>
									<CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" opacity={0.5} />
									<XAxis 
										dataKey="name" 
										stroke="#6b7280" 
										fontSize={11}
										tick={{ fill: '#6b7280', fontSize: 11 }}
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
									<Tooltip content={<CustomTooltip />} />
									<Bar
										dataKey="revenue"
										radius={[8, 8, 0, 0]}
										name="Revenue"
									>
										{analyticsData.methodStats.map((entry, index) => (
											<Cell 
												key={`cell-${index}`} 
												fill={`url(#methodGradient${index + 1})`}
											/>
										))}
									</Bar>
								</BarChart>
							</ResponsiveContainer>
						</div>
					</CardContent>
				</Card>

				{/* Collection Performance - Enhanced Area Chart */}
				<Card className="bg-gradient-to-br from-emerald-50 to-teal-50 border-emerald-200">
					<CardHeader>
						<CardTitle className="flex items-center gap-2">
							<ClockIcon className="h-5 w-5 text-emerald-600" />
							<span className="bg-gradient-to-r from-emerald-600 to-teal-600 bg-clip-text text-transparent font-bold">
								Collection Performance
							</span>
						</CardTitle>
					</CardHeader>
					<CardContent>
						<div className="h-64">
							<ResponsiveContainer width="100%" height="100%">
								<AreaChart data={analyticsData.collectionStats} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
									<defs>
										<linearGradient id="collectedGradient" x1="0" y1="0" x2="0" y2="1">
											<stop offset="5%" stopColor="#10b981" stopOpacity={0.8}/>
											<stop offset="95%" stopColor="#10b981" stopOpacity={0.2}/>
										</linearGradient>
										<linearGradient id="outstandingGradient" x1="0" y1="0" x2="0" y2="1">
											<stop offset="5%" stopColor="#ef4444" stopOpacity={0.8}/>
											<stop offset="95%" stopColor="#ef4444" stopOpacity={0.2}/>
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
									<Tooltip content={<CustomTooltip />} />
									<Area
										type="monotone"
										dataKey="collected"
										stackId="1"
										stroke="#10b981"
										strokeWidth={2}
										fill="url(#collectedGradient)"
										name="Collected"
									/>
									<Area
										type="monotone"
										dataKey="outstanding"
										stackId="2"
										stroke="#ef4444"
										strokeWidth={2}
										fill="url(#outstandingGradient)"
										name="Outstanding"
									/>
								</AreaChart>
							</ResponsiveContainer>
						</div>
					</CardContent>
				</Card>
			</div>

			{/* Action Items */}
			<div className="bg-gradient-to-r from-blue-50 via-indigo-50 to-purple-50 rounded-xl p-6 border border-blue-200 shadow-sm">
				<div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
					<div>
						<h3 className="text-lg font-semibold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-1">
							🚀 Ready to optimize your billing process?
						</h3>
						<p className="text-gray-600">
							Based on the analytics, we can help you improve collection rates and reduce payment delays with AI-powered insights.
						</p>
					</div>
					<div className="flex flex-wrap gap-3">
						<Button variant="outline" size="sm" className="bg-white/50 backdrop-blur-sm">
							📅 Schedule Review
						</Button>
						<Button variant="primary" size="sm" className="bg-gradient-to-r from-blue-600 to-purple-600 text-white">
							🤖 Get AI Recommendations
						</Button>
					</div>
				</div>
			</div>
		</div>
	)
}
