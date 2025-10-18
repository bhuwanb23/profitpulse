import { useMemo } from 'react'
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, BarChart, Bar, PieChart, Pie, Cell, AreaChart, Area } from 'recharts'
import { KPICard } from '../components/clients/KPICard'
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/Card'
import { Button } from '../components/ui/Button'
import { TrendingUpIcon, CurrencyDollarIcon, DocumentTextIcon, ChartBarIcon, ClockIcon, ExclamationTriangleIcon } from '../components/ui/Icons'
import { mockInvoices, mockInvoiceCategories, mockPaymentMethods } from '../services/mockFinancial'
import { Link } from 'react-router-dom'

export default function InvoiceAnalyticsPage() {
	// Calculate analytics data from mock invoices
	const analyticsData = useMemo(() => {
		// Revenue trends (last 6 months)
		const revenueTrends = [
			{ month: 'Jan', revenue: 8800, invoices: 1, avgValue: 8800 },
			{ month: 'Feb', revenue: 1650, invoices: 1, avgValue: 1650 },
			{ month: 'Mar', revenue: 0, invoices: 0, avgValue: 0 },
			{ month: 'Apr', revenue: 16495, invoices: 3, avgValue: 5498 },
			{ month: 'May', revenue: 6380, invoices: 1, avgValue: 6380 },
			{ month: 'Jun', revenue: 0, invoices: 0, avgValue: 0 },
		]

		// Status breakdown
		const statusStats = [
			{ status: 'Paid', count: mockInvoices.filter(i => i.status === 'paid').length, color: '#10b981' },
			{ status: 'Sent', count: mockInvoices.filter(i => i.status === 'sent').length, color: '#3b82f6' },
			{ status: 'Overdue', count: mockInvoices.filter(i => i.status === 'overdue').length, color: '#ef4444' },
			{ status: 'Draft', count: mockInvoices.filter(i => i.status === 'draft').length, color: '#6b7280' },
		]

		// Payment method breakdown
		const methodStats = mockPaymentMethods.map(method => {
			const methodInvoices = mockInvoices.filter(i => i.method === method.id)
			return {
				name: method.name,
				count: methodInvoices.length,
				revenue: methodInvoices.reduce((sum, i) => sum + i.total, 0),
				color: method.id === 'credit_card' ? '#3b82f6' :
					   method.id === 'bank_transfer' ? '#10b981' :
					   method.id === 'wire_transfer' ? '#8b5cf6' :
					   method.id === 'check' ? '#f59e0b' : '#6b7280'
			}
		}).filter(method => method.count > 0)

		// Client revenue breakdown
		const clientStats = Array.from(new Set(mockInvoices.map(i => i.client))).map(client => {
			const clientInvoices = mockInvoices.filter(i => i.client === client)
			const paidInvoices = clientInvoices.filter(i => i.status === 'paid')
			return {
				name: client,
				invoices: clientInvoices.length,
				revenue: paidInvoices.reduce((sum, i) => sum + i.total, 0),
				pending: clientInvoices.filter(i => i.status === 'sent').reduce((sum, i) => sum + i.total, 0),
				overdue: clientInvoices.filter(i => i.status === 'overdue').reduce((sum, i) => sum + i.total, 0)
			}
		}).sort((a, b) => b.revenue - a.revenue).slice(0, 6)

		// Monthly collection performance
		const collectionStats = [
			{ month: 'Jan', collected: 8800, outstanding: 0, collectionRate: 100 },
			{ month: 'Feb', collected: 0, outstanding: 1650, collectionRate: 0 },
			{ month: 'Mar', collected: 0, outstanding: 0, collectionRate: 0 },
			{ month: 'Apr', collected: 3740, outstanding: 12155, collectionRate: 23.5 },
			{ month: 'May', collected: 6380, outstanding: 0, collectionRate: 100 },
			{ month: 'Jun', collected: 0, outstanding: 2420, collectionRate: 0 },
		]

		return {
			revenueTrends,
			statusStats,
			methodStats,
			clientStats,
			collectionStats
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
				<div className="bg-white p-3 border border-gray-200 rounded-lg shadow-lg">
					<p className="font-medium text-gray-900">{label}</p>
					{payload.map((entry, index) => (
						<p key={index} className="text-sm" style={{ color: entry.color }}>
							{entry.name}: {entry.name.includes('Rate') ? `${entry.value}%` : 
								entry.name.includes('Revenue') || entry.name.includes('collected') || entry.name.includes('outstanding') ? 
								formatCurrency(entry.value) : entry.value}
						</p>
					))}
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

			{/* Main Chart - Revenue Trends */}
			<Card>
				<CardHeader>
					<CardTitle className="flex items-center gap-2">
						<TrendingUpIcon className="h-5 w-5 text-green-600" />
						Revenue & Invoice Trends
					</CardTitle>
				</CardHeader>
				<CardContent>
					<div className="h-64 sm:h-72 lg:h-80">
						<ResponsiveContainer width="100%" height="100%">
							<LineChart data={analyticsData.revenueTrends} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
								<defs>
									<linearGradient id="revenueGradient" x1="0" y1="0" x2="0" y2="1">
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
									tickFormatter={(value) => `$${(value / 1000).toFixed(0)}k`}
								/>
								<Tooltip content={<CustomTooltip />} />
								<Area
									type="monotone"
									dataKey="revenue"
									stroke="#10b981"
									strokeWidth={3}
									fill="url(#revenueGradient)"
									name="Revenue"
								/>
								<Line
									type="monotone"
									dataKey="invoices"
									stroke="#3b82f6"
									strokeWidth={2}
									dot={{ fill: '#3b82f6', strokeWidth: 2, r: 4 }}
									name="Invoice Count"
									yAxisId="right"
								/>
							</LineChart>
						</ResponsiveContainer>
					</div>
				</CardContent>
			</Card>

			{/* Charts Row */}
			<div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
				{/* Invoice Status Breakdown */}
				<Card>
					<CardHeader>
						<CardTitle className="flex items-center gap-2">
							<ChartBarIcon className="h-5 w-5 text-blue-600" />
							Invoice Status Distribution
						</CardTitle>
					</CardHeader>
					<CardContent>
						<div className="h-64 sm:h-72">
							<ResponsiveContainer width="100%" height="100%">
								<PieChart>
									<Pie
										data={analyticsData.statusStats}
										cx="50%"
										cy="50%"
										outerRadius={80}
										innerRadius={40}
										paddingAngle={2}
										dataKey="count"
										label={({status, percent}) => `${status} ${(percent * 100).toFixed(0)}%`}
										labelLine={false}
									>
										{analyticsData.statusStats.map((entry, index) => (
											<Cell key={`cell-${index}`} fill={entry.color} />
										))}
									</Pie>
									<Tooltip 
										formatter={(value) => [value, 'Invoices']}
										labelFormatter={(label) => `Status: ${label}`}
									/>
								</PieChart>
							</ResponsiveContainer>
						</div>
						<div className="mt-4 space-y-3">
							{analyticsData.statusStats.map((item, index) => (
								<div key={index} className="flex items-center justify-between p-2 rounded-lg hover:bg-gray-50">
									<div className="flex items-center gap-3">
										<div 
											className="w-4 h-4 rounded-full" 
											style={{ backgroundColor: item.color }}
										/>
										<span className="text-sm font-medium text-gray-900">{item.status}</span>
									</div>
									<div className="text-right">
										<span className="text-sm font-bold text-gray-900">
											{item.count}
										</span>
										<span className="text-xs text-gray-500 ml-1">invoices</span>
									</div>
								</div>
							))}
						</div>
					</CardContent>
				</Card>

				{/* Payment Methods */}
				<Card>
					<CardHeader>
						<CardTitle className="flex items-center gap-2">
							<CurrencyDollarIcon className="h-5 w-5 text-purple-600" />
							Payment Methods
						</CardTitle>
					</CardHeader>
					<CardContent>
						<div className="h-64 sm:h-72">
							<ResponsiveContainer width="100%" height="100%">
								<BarChart data={analyticsData.methodStats} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
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
										tickFormatter={(value) => `$${(value / 1000).toFixed(0)}k`}
									/>
									<Tooltip content={<CustomTooltip />} />
									<Bar
										dataKey="revenue"
										radius={[4, 4, 0, 0]}
										name="Revenue"
									>
										{analyticsData.methodStats.map((entry, index) => (
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
				{/* Top Clients by Revenue */}
				<Card>
					<CardHeader>
						<CardTitle className="flex items-center gap-2">
							<DocumentTextIcon className="h-5 w-5 text-orange-600" />
							Top Clients by Revenue
						</CardTitle>
					</CardHeader>
					<CardContent>
						<div className="h-56 sm:h-64">
							<ResponsiveContainer width="100%" height="100%">
								<BarChart data={analyticsData.clientStats} layout="horizontal" margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
									<CartesianGrid strokeDasharray="3 3" stroke="#f3f4f6" />
									<XAxis 
										type="number" 
										stroke="#6b7280" 
										fontSize={11}
										tick={{ fill: '#6b7280', fontSize: 11 }}
										tickFormatter={(value) => `$${(value / 1000).toFixed(0)}k`}
									/>
									<YAxis 
										dataKey="name" 
										type="category" 
										stroke="#6b7280" 
										fontSize={10}
										tick={{ fill: '#6b7280', fontSize: 10 }}
										width={100}
									/>
									<Tooltip content={<CustomTooltip />} />
									<Bar
										dataKey="revenue"
										fill="#f59e0b"
										radius={[0, 4, 4, 0]}
										name="Revenue"
									/>
								</BarChart>
							</ResponsiveContainer>
						</div>
					</CardContent>
				</Card>

				{/* Collection Performance */}
				<Card>
					<CardHeader>
						<CardTitle className="flex items-center gap-2">
							<ChartBarIcon className="h-5 w-5 text-green-600" />
							Collection Performance
						</CardTitle>
					</CardHeader>
					<CardContent>
						<div className="h-56 sm:h-64">
							<ResponsiveContainer width="100%" height="100%">
								<BarChart data={analyticsData.collectionStats} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
									<CartesianGrid strokeDasharray="3 3" stroke="#f3f4f6" />
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
									<Bar
										dataKey="collected"
										fill="#10b981"
										radius={[4, 4, 0, 0]}
										name="Collected"
									/>
									<Bar
										dataKey="outstanding"
										fill="#ef4444"
										radius={[4, 4, 0, 0]}
										name="Outstanding"
									/>
								</BarChart>
							</ResponsiveContainer>
						</div>
					</CardContent>
				</Card>
			</div>

			{/* Action Items */}
			<div className="bg-gradient-to-r from-green-50 to-blue-50 rounded-xl p-6 border border-green-100">
				<div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
					<div>
						<h3 className="text-lg font-semibold text-gray-900 mb-1">
							Ready to optimize your billing process?
						</h3>
						<p className="text-gray-600">
							Based on the analytics, we can help you improve collection rates and reduce payment delays.
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
