import { useParams, Link } from 'react-router-dom'
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/Card'
import { Button } from '../components/ui/Button'
import { 
	DocumentTextIcon, 
	CalendarIcon, 
	UserIcon, 
	CurrencyDollarIcon,
	ClockIcon,
	CreditCardIcon
} from '../components/ui/Icons'
import { mockInvoices, mockInvoiceItems } from '../services/mockFinancial'

export default function InvoiceDetailPage() {
	const { id } = useParams()
	const invoice = mockInvoices.find(inv => inv.id === id)
	const items = mockInvoiceItems[id] || []

	if (!invoice) {
		return (
			<div className="space-y-6">
				<div className="text-center py-12">
					<DocumentTextIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
					<h2 className="text-xl font-semibold text-gray-900 mb-2">Invoice Not Found</h2>
					<p className="text-gray-600 mb-6">The invoice you're looking for doesn't exist.</p>
					<Link to="/invoices">
						<Button variant="primary">Back to Invoices</Button>
					</Link>
				</div>
			</div>
		)
	}

	const getStatusColor = (status) => {
		switch (status) {
			case 'paid':
				return 'bg-green-50 text-green-700 border-green-200'
			case 'sent':
				return 'bg-blue-50 text-blue-700 border-blue-200'
			case 'overdue':
				return 'bg-red-50 text-red-700 border-red-200'
			case 'draft':
				return 'bg-gray-50 text-gray-700 border-gray-200'
			default:
				return 'bg-gray-50 text-gray-700 border-gray-200'
		}
	}

	const formatDate = (dateString) => {
		return new Date(dateString).toLocaleDateString('en-US', {
			year: 'numeric',
			month: 'long',
			day: 'numeric'
		})
	}

	const formatCurrency = (amount) => {
		return new Intl.NumberFormat('en-US', {
			style: 'currency',
			currency: 'USD'
		}).format(amount)
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
				<span className="text-gray-600">{invoice.id}</span>
			</div>

			{/* Header */}
			<div className="flex flex-col lg:flex-row lg:items-start justify-between gap-6">
				<div>
					<div className="flex items-center gap-3 mb-2">
						<h1 className="text-3xl font-bold text-gray-900">{invoice.id}</h1>
						<span className={`px-3 py-1 text-sm font-medium rounded-full border ${getStatusColor(invoice.status)}`}>
							{invoice.status.charAt(0).toUpperCase() + invoice.status.slice(1)}
						</span>
					</div>
					<p className="text-gray-600">Invoice details and line items</p>
				</div>
				
				<div className="flex flex-wrap gap-3">
					<Button variant="outline" size="sm">
						Download PDF
					</Button>
					<Button variant="outline" size="sm">
						Send Email
					</Button>
					<Link to={`/invoice-operations?edit=${invoice.id}`}>
						<Button variant="primary" size="sm">
							Edit Invoice
						</Button>
					</Link>
				</div>
			</div>

			<div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
				{/* Invoice Details */}
				<div className="lg:col-span-2 space-y-6">
					{/* Basic Information */}
					<Card>
						<CardHeader>
							<CardTitle className="flex items-center gap-2">
								<DocumentTextIcon className="h-5 w-5 text-blue-600" />
								Invoice Information
							</CardTitle>
						</CardHeader>
						<CardContent>
							<div className="grid grid-cols-1 md:grid-cols-2 gap-6">
								<div className="space-y-4">
									<div className="flex items-center gap-3">
										<UserIcon className="h-5 w-5 text-gray-400" />
										<div>
											<p className="text-sm text-gray-500">Client</p>
											<p className="font-medium text-gray-900">{invoice.client}</p>
										</div>
									</div>
									<div className="flex items-center gap-3">
										<CalendarIcon className="h-5 w-5 text-gray-400" />
										<div>
											<p className="text-sm text-gray-500">Invoice Date</p>
											<p className="font-medium text-gray-900">{formatDate(invoice.date)}</p>
										</div>
									</div>
									<div className="flex items-center gap-3">
										<ClockIcon className="h-5 w-5 text-gray-400" />
										<div>
											<p className="text-sm text-gray-500">Due Date</p>
											<p className="font-medium text-gray-900">{formatDate(invoice.due)}</p>
										</div>
									</div>
								</div>
								<div className="space-y-4">
									<div className="flex items-center gap-3">
										<CreditCardIcon className="h-5 w-5 text-gray-400" />
										<div>
											<p className="text-sm text-gray-500">Payment Method</p>
											<p className="font-medium text-gray-900">
												{invoice.method.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
											</p>
										</div>
									</div>
									<div className="flex items-center gap-3">
										<CurrencyDollarIcon className="h-5 w-5 text-gray-400" />
										<div>
											<p className="text-sm text-gray-500">Payment Terms</p>
											<p className="font-medium text-gray-900">{invoice.paymentTerms}</p>
										</div>
									</div>
									{invoice.paidAt && (
										<div className="flex items-center gap-3">
											<CalendarIcon className="h-5 w-5 text-green-400" />
											<div>
												<p className="text-sm text-gray-500">Paid Date</p>
												<p className="font-medium text-green-700">{formatDate(invoice.paidAt)}</p>
											</div>
										</div>
									)}
								</div>
							</div>
							{invoice.notes && (
								<div className="mt-6 pt-6 border-t border-gray-200">
									<p className="text-sm text-gray-500 mb-2">Notes</p>
									<p className="text-gray-900">{invoice.notes}</p>
								</div>
							)}
						</CardContent>
					</Card>

					{/* Line Items */}
					<Card>
						<CardHeader>
							<CardTitle>Line Items</CardTitle>
						</CardHeader>
						<CardContent>
							<div className="overflow-x-auto">
								<table className="w-full">
									<thead>
										<tr className="border-b border-gray-200">
											<th className="text-left py-3 px-2 font-medium text-gray-900">Description</th>
											<th className="text-center py-3 px-2 font-medium text-gray-900">Qty</th>
											<th className="text-right py-3 px-2 font-medium text-gray-900">Price</th>
											<th className="text-right py-3 px-2 font-medium text-gray-900">Total</th>
										</tr>
									</thead>
									<tbody className="divide-y divide-gray-200">
										{items.map((item, index) => (
											<tr key={index}>
												<td className="py-3 px-2">
													<div>
														<p className="font-medium text-gray-900">{item.desc}</p>
														{item.category && (
															<p className="text-sm text-gray-500">{item.category}</p>
														)}
													</div>
												</td>
												<td className="py-3 px-2 text-center text-gray-900">{item.qty}</td>
												<td className="py-3 px-2 text-right text-gray-900">{formatCurrency(item.price)}</td>
												<td className="py-3 px-2 text-right font-medium text-gray-900">
													{formatCurrency(item.qty * item.price)}
												</td>
											</tr>
										))}
									</tbody>
								</table>
							</div>
						</CardContent>
					</Card>
				</div>

				{/* Summary */}
				<div className="space-y-6">
					{/* Amount Summary */}
					<Card>
						<CardHeader>
							<CardTitle className="flex items-center gap-2">
								<CurrencyDollarIcon className="h-5 w-5 text-green-600" />
								Amount Summary
							</CardTitle>
						</CardHeader>
						<CardContent>
							<div className="space-y-3">
								<div className="flex justify-between">
									<span className="text-gray-600">Subtotal:</span>
									<span className="font-medium">{formatCurrency(invoice.subtotal)}</span>
								</div>
								{invoice.discount > 0 && (
									<div className="flex justify-between text-green-600">
										<span>Discount ({invoice.discount}%):</span>
										<span>-{formatCurrency(invoice.subtotal * (invoice.discount / 100))}</span>
									</div>
								)}
								<div className="flex justify-between">
									<span className="text-gray-600">Tax:</span>
									<span className="font-medium">{formatCurrency(invoice.tax)}</span>
								</div>
								<div className="flex justify-between text-lg font-bold border-t pt-3">
									<span>Total:</span>
									<span>{formatCurrency(invoice.total)}</span>
								</div>
							</div>
						</CardContent>
					</Card>

					{/* Tags */}
					{invoice.tags && invoice.tags.length > 0 && (
						<Card>
							<CardHeader>
								<CardTitle>Tags</CardTitle>
							</CardHeader>
							<CardContent>
								<div className="flex flex-wrap gap-2">
									{invoice.tags.map((tag, index) => (
										<span
											key={index}
											className="px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded-full"
										>
											{tag}
										</span>
									))}
								</div>
							</CardContent>
						</Card>
					)}

					{/* Actions */}
					<Card>
						<CardHeader>
							<CardTitle>Quick Actions</CardTitle>
						</CardHeader>
						<CardContent className="space-y-3">
							{invoice.status === 'draft' && (
								<Button variant="primary" className="w-full">
									Send Invoice
								</Button>
							)}
							{invoice.status === 'sent' && (
								<Button variant="primary" className="w-full">
									Mark as Paid
								</Button>
							)}
							{invoice.status === 'overdue' && (
								<Button variant="primary" className="w-full">
									Send Reminder
								</Button>
							)}
							<Button variant="outline" className="w-full">
								Duplicate Invoice
							</Button>
							<Button variant="outline" className="w-full">
								Print Invoice
							</Button>
						</CardContent>
					</Card>
				</div>
			</div>
		</div>
	)
}
