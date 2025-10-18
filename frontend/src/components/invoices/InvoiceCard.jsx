import { Link } from 'react-router-dom'
import { Card, CardContent } from '../ui/Card'
import { Button } from '../ui/Button'
import { CurrencyDollarIcon, CalendarIcon, UserIcon, CreditCardIcon, ClockIcon } from '../ui/Icons'

export function InvoiceCard({ invoice }) {
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

	const getPriorityColor = (priority) => {
		switch (priority) {
			case 'high':
				return 'bg-red-100 text-red-800'
			case 'normal':
				return 'bg-blue-100 text-blue-800'
			case 'low':
				return 'bg-gray-100 text-gray-800'
			default:
				return 'bg-gray-100 text-gray-800'
		}
	}

	const getPaymentMethodIcon = (method) => {
		switch (method) {
			case 'credit_card':
				return '💳'
			case 'bank_transfer':
				return '🏦'
			case 'wire_transfer':
				return '💸'
			case 'check':
				return '📄'
			case 'cash':
				return '💵'
			default:
				return '💳'
		}
	}

	const formatDate = (dateString) => {
		return new Date(dateString).toLocaleDateString('en-US', {
			month: 'short',
			day: 'numeric',
			year: 'numeric'
		})
	}

	const getDaysOverdue = (dueDate) => {
		const today = new Date()
		const due = new Date(dueDate)
		const diffTime = today - due
		const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
		return diffDays > 0 ? diffDays : 0
	}

	const isOverdue = invoice.status === 'overdue'
	const daysOverdue = isOverdue ? getDaysOverdue(invoice.due) : 0

	return (
		<Card className="hover:shadow-md transition-shadow duration-200 border-l-4 border-l-blue-500">
			<CardContent className="p-6">
				{/* Header */}
				<div className="flex items-start justify-between mb-4">
					<div className="flex-1">
						<div className="flex items-center gap-3 mb-2">
							<h3 className="text-lg font-semibold text-gray-900">{invoice.id}</h3>
							<span className={`px-2 py-1 text-xs font-medium rounded-full border ${getStatusColor(invoice.status)}`}>
								{invoice.status.charAt(0).toUpperCase() + invoice.status.slice(1)}
							</span>
							{invoice.priority !== 'normal' && (
								<span className={`px-2 py-1 text-xs font-medium rounded-full ${getPriorityColor(invoice.priority)}`}>
									{invoice.priority.charAt(0).toUpperCase() + invoice.priority.slice(1)}
								</span>
							)}
						</div>
						<div className="flex items-center gap-2 text-sm text-gray-600 mb-1">
							<UserIcon className="h-4 w-4" />
							<span className="font-medium">{invoice.client}</span>
						</div>
						{invoice.notes && (
							<p className="text-sm text-gray-500 line-clamp-2">{invoice.notes}</p>
						)}
					</div>
					<div className="text-right">
						<div className="text-2xl font-bold text-gray-900">
							${invoice.total.toLocaleString()}
						</div>
						<div className="text-sm text-gray-500">
							{invoice.currency}
						</div>
					</div>
				</div>

				{/* Details */}
				<div className="grid grid-cols-2 gap-4 mb-4">
					<div className="flex items-center gap-2 text-sm text-gray-600">
						<CalendarIcon className="h-4 w-4" />
						<span>Issued: {formatDate(invoice.date)}</span>
					</div>
					<div className="flex items-center gap-2 text-sm text-gray-600">
						<ClockIcon className="h-4 w-4" />
						<span>Due: {formatDate(invoice.due)}</span>
						{isOverdue && (
							<span className="text-red-600 font-medium">
								({daysOverdue} days overdue)
							</span>
						)}
					</div>
					<div className="flex items-center gap-2 text-sm text-gray-600">
						<span className="text-lg">{getPaymentMethodIcon(invoice.method)}</span>
						<span>{invoice.method.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}</span>
					</div>
					<div className="flex items-center gap-2 text-sm text-gray-600">
						<CurrencyDollarIcon className="h-4 w-4" />
						<span>{invoice.paymentTerms}</span>
					</div>
				</div>

				{/* Tags */}
				{invoice.tags && invoice.tags.length > 0 && (
					<div className="flex flex-wrap gap-2 mb-4">
						{invoice.tags.map((tag, index) => (
							<span
								key={index}
								className="px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded-full"
							>
								{tag}
							</span>
						))}
					</div>
				)}

				{/* Footer Actions */}
				<div className="flex items-center justify-between pt-4 border-t border-gray-100">
					<div className="text-xs text-gray-500">
						Created by {invoice.createdBy}
					</div>
					<div className="flex gap-2">
						<Link to={`/invoices/${invoice.id}`}>
							<Button variant="outline" size="sm">
								View Details
							</Button>
						</Link>
						<Link to={`/invoice-operations?edit=${invoice.id}`}>
							<Button variant="primary" size="sm">
								Edit
							</Button>
						</Link>
					</div>
				</div>
			</CardContent>
		</Card>
	)
}
