import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { KPICard } from '../components/clients/KPICard'
import { InvoiceCard } from '../components/invoices/InvoiceCard'
import { Button } from '../components/ui/Button'
import { 
	CurrencyDollarIcon, 
	DocumentTextIcon, 
	ClockIcon, 
	ExclamationTriangleIcon,
	ChartBarIcon,
	PlusIcon,
	FunnelIcon,
	MagnifyingGlassIcon
} from '../components/ui/Icons'
import { mockInvoices, mockPaymentMethods } from '../services/mockFinancial'

export default function Invoices() {
	const [searchQuery, setSearchQuery] = useState('')
	const [statusFilter, setStatusFilter] = useState('all')
	const [clientFilter, setClientFilter] = useState('all')
	const [methodFilter, setMethodFilter] = useState('all')
	const [sortBy, setSortBy] = useState('date')
	const [sortOrder, setSortOrder] = useState('desc')

	// Calculate KPI data
	const kpiData = useMemo(() => {
		const totalInvoices = mockInvoices.length
		const paidInvoices = mockInvoices.filter(inv => inv.status === 'paid')
		const overdueInvoices = mockInvoices.filter(inv => inv.status === 'overdue')
		const draftInvoices = mockInvoices.filter(inv => inv.status === 'draft')
		
		const totalRevenue = paidInvoices.reduce((sum, inv) => sum + inv.total, 0)
		const pendingRevenue = mockInvoices
			.filter(inv => inv.status === 'sent')
			.reduce((sum, inv) => sum + inv.total, 0)
		const overdueAmount = overdueInvoices.reduce((sum, inv) => sum + inv.total, 0)
		
		const avgInvoiceValue = totalRevenue / paidInvoices.length || 0
		
		return {
			totalInvoices,
			totalRevenue,
			pendingRevenue,
			overdueAmount,
			overdueCount: overdueInvoices.length,
			draftCount: draftInvoices.length,
			avgInvoiceValue,
			paidCount: paidInvoices.length
		}
	}, [])

	// Get unique clients for filter
	const uniqueClients = useMemo(() => {
		return ['all', ...Array.from(new Set(mockInvoices.map(inv => inv.client)))]
	}, [])

	// Filter and sort invoices
	const filteredInvoices = useMemo(() => {
		let filtered = mockInvoices.filter(invoice => {
			const matchesSearch = searchQuery === '' || 
				invoice.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
				invoice.client.toLowerCase().includes(searchQuery.toLowerCase()) ||
				invoice.notes.toLowerCase().includes(searchQuery.toLowerCase())
			
			const matchesStatus = statusFilter === 'all' || invoice.status === statusFilter
			const matchesClient = clientFilter === 'all' || invoice.client === clientFilter
			const matchesMethod = methodFilter === 'all' || invoice.method === methodFilter
			
			return matchesSearch && matchesStatus && matchesClient && matchesMethod
		})

		// Sort invoices
		filtered.sort((a, b) => {
			let aValue, bValue
			
			switch (sortBy) {
				case 'date':
					aValue = new Date(a.date)
					bValue = new Date(b.date)
					break
				case 'due':
					aValue = new Date(a.due)
					bValue = new Date(b.due)
					break
				case 'total':
					aValue = a.total
					bValue = b.total
					break
				case 'client':
					aValue = a.client.toLowerCase()
					bValue = b.client.toLowerCase()
					break
				default:
					aValue = a.id
					bValue = b.id
			}
			
			if (sortOrder === 'asc') {
				return aValue > bValue ? 1 : -1
			} else {
				return aValue < bValue ? 1 : -1
			}
		})

		return filtered
	}, [searchQuery, statusFilter, clientFilter, methodFilter, sortBy, sortOrder])

	return (
		<div className="space-y-6">
			{/* Header */}
			<div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
				<div>
					<h1 className="text-3xl font-bold text-gray-900">Invoices</h1>
					<p className="text-gray-600 mt-1">Manage your billing and track payments</p>
				</div>
				
				<div className="flex flex-wrap gap-3">
					<Link to="/invoice-analytics">
						<Button variant="outline" size="sm" className="flex items-center gap-2">
							<ChartBarIcon className="h-4 w-4" />
							Analytics
						</Button>
					</Link>
					<Link to="/invoice-operations">
						<Button variant="primary" size="sm" className="flex items-center gap-2">
							<PlusIcon className="h-4 w-4" />
							New Invoice
						</Button>
					</Link>
				</div>
			</div>

			{/* KPI Cards */}
			<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 xl:grid-cols-6 gap-4">
				<KPICard
					title="Total Invoices"
					value={kpiData.totalInvoices}
					change={12.5}
					changeType="positive"
					format="number"
					icon={DocumentTextIcon}
					iconColor="blue"
				/>
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
					value={kpiData.paidCount / kpiData.totalInvoices}
					change={2.4}
					changeType="positive"
					format="percentage"
					icon={ChartBarIcon}
					iconColor="green"
				/>
			</div>

			{/* Filters and Search */}
			<div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
				<div className="flex flex-col lg:flex-row gap-4 mb-6">
					{/* Search */}
					<div className="flex-1 relative">
						<MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
						<input
							type="text"
							placeholder="Search invoices, clients, or notes..."
							value={searchQuery}
							onChange={(e) => setSearchQuery(e.target.value)}
							className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
						/>
					</div>

					{/* Filters */}
					<div className="flex flex-wrap gap-3">
						<select
							value={statusFilter}
							onChange={(e) => setStatusFilter(e.target.value)}
							className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
						>
							<option value="all">All Status</option>
							<option value="draft">Draft</option>
							<option value="sent">Sent</option>
							<option value="paid">Paid</option>
							<option value="overdue">Overdue</option>
						</select>

						<select
							value={clientFilter}
							onChange={(e) => setClientFilter(e.target.value)}
							className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
						>
							{uniqueClients.map(client => (
								<option key={client} value={client}>
									{client === 'all' ? 'All Clients' : client}
								</option>
							))}
						</select>

						<select
							value={methodFilter}
							onChange={(e) => setMethodFilter(e.target.value)}
							className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
						>
							<option value="all">All Methods</option>
							{mockPaymentMethods.map(method => (
								<option key={method.id} value={method.id}>
									{method.name}
								</option>
							))}
						</select>

						<select
							value={`${sortBy}-${sortOrder}`}
							onChange={(e) => {
								const [field, order] = e.target.value.split('-')
								setSortBy(field)
								setSortOrder(order)
							}}
							className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
						>
							<option value="date-desc">Newest First</option>
							<option value="date-asc">Oldest First</option>
							<option value="due-asc">Due Date (Earliest)</option>
							<option value="due-desc">Due Date (Latest)</option>
							<option value="total-desc">Amount (High to Low)</option>
							<option value="total-asc">Amount (Low to High)</option>
							<option value="client-asc">Client (A-Z)</option>
							<option value="client-desc">Client (Z-A)</option>
						</select>
					</div>
				</div>

				{/* Results Summary */}
				<div className="flex items-center justify-between mb-4">
					<p className="text-sm text-gray-600">
						Showing {filteredInvoices.length} of {mockInvoices.length} invoices
					</p>
					{(searchQuery || statusFilter !== 'all' || clientFilter !== 'all' || methodFilter !== 'all') && (
						<Button
							variant="outline"
							size="sm"
							onClick={() => {
								setSearchQuery('')
								setStatusFilter('all')
								setClientFilter('all')
								setMethodFilter('all')
							}}
							className="flex items-center gap-2"
						>
							<FunnelIcon className="h-4 w-4" />
							Clear Filters
						</Button>
					)}
				</div>
			</div>

			{/* Invoice Grid */}
			{filteredInvoices.length > 0 ? (
				<div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
					{filteredInvoices.map(invoice => (
						<InvoiceCard key={invoice.id} invoice={invoice} />
					))}
				</div>
			) : (
				<div className="bg-white rounded-xl border border-gray-200 p-12 shadow-sm text-center">
					<DocumentTextIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
					<h3 className="text-lg font-medium text-gray-900 mb-2">No invoices found</h3>
					<p className="text-gray-600 mb-6">
						{searchQuery || statusFilter !== 'all' || clientFilter !== 'all' || methodFilter !== 'all'
							? "Try adjusting your filters or search terms."
							: "Get started by creating your first invoice."
						}
					</p>
					<Link to="/invoice-operations">
						<Button variant="primary" className="flex items-center gap-2">
							<PlusIcon className="h-4 w-4" />
							Create Invoice
						</Button>
					</Link>
				</div>
			)}
		</div>
	)
}
