import { useState } from 'react'
import { Link } from 'react-router-dom'
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/Card'
import { Button } from '../components/ui/Button'
import { 
	DocumentTextIcon, 
	PlusIcon, 
	CurrencyDollarIcon,
	CalendarIcon,
	UserIcon,
	ClockIcon,
	CheckIcon,
	XMarkIcon
} from '../components/ui/Icons'
import { mockInvoices, mockPaymentMethods } from '../services/mockFinancial'

export default function InvoiceOperationsPage() {
	const [activeTab, setActiveTab] = useState('create')
	const [selectedInvoices, setSelectedInvoices] = useState([])
	const [formData, setFormData] = useState({
		client: '',
		date: new Date().toISOString().split('T')[0],
		due: '',
		items: [{ desc: '', qty: 1, price: 0 }],
		notes: '',
		paymentTerms: 'Net 15',
		method: 'credit_card'
	})

	const tabs = [
		{ id: 'create', label: 'Create Invoice', icon: PlusIcon },
		{ id: 'bulk', label: 'Bulk Operations', icon: DocumentTextIcon },
		{ id: 'templates', label: 'Templates', icon: CheckIcon },
		{ id: 'reminders', label: 'Payment Reminders', icon: ClockIcon }
	]

	const handleAddItem = () => {
		setFormData(prev => ({
			...prev,
			items: [...prev.items, { desc: '', qty: 1, price: 0 }]
		}))
	}

	const handleRemoveItem = (index) => {
		setFormData(prev => ({
			...prev,
			items: prev.items.filter((_, i) => i !== index)
		}))
	}

	const handleItemChange = (index, field, value) => {
		setFormData(prev => ({
			...prev,
			items: prev.items.map((item, i) => 
				i === index ? { ...item, [field]: value } : item
			)
		}))
	}

	const calculateTotal = () => {
		const subtotal = formData.items.reduce((sum, item) => sum + (item.qty * item.price), 0)
		const tax = subtotal * 0.1 // 10% tax
		return { subtotal, tax, total: subtotal + tax }
	}

	const { subtotal, tax, total } = calculateTotal()

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
				<span className="text-gray-600">Invoice Operations</span>
			</div>

			{/* Header */}
			<div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
				<div>
					<h1 className="text-3xl font-bold text-gray-900">Invoice Operations</h1>
					<p className="text-gray-600 mt-1">Create, manage, and process invoices</p>
				</div>
				
				<div className="flex flex-wrap gap-3">
					<Link to="/invoice-analytics">
						<Button variant="outline" size="sm" className="flex items-center gap-2">
							<DocumentTextIcon className="h-4 w-4" />
							View Analytics
						</Button>
					</Link>
				</div>
			</div>

			{/* Tab Navigation */}
			<div className="border-b border-gray-200">
				<nav className="flex space-x-8">
					{tabs.map(tab => {
						const Icon = tab.icon
						return (
							<button
								key={tab.id}
								onClick={() => setActiveTab(tab.id)}
								className={`flex items-center gap-2 py-2 px-1 border-b-2 font-medium text-sm ${
									activeTab === tab.id
										? 'border-blue-500 text-blue-600'
										: 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
								}`}
							>
								<Icon className="h-4 w-4" />
								{tab.label}
							</button>
						)
					})}
				</nav>
			</div>

			{/* Tab Content */}
			{activeTab === 'create' && (
				<Card>
					<CardHeader>
						<CardTitle className="flex items-center gap-2">
							<PlusIcon className="h-5 w-5 text-blue-600" />
							Create New Invoice
						</CardTitle>
					</CardHeader>
					<CardContent className="space-y-6">
						{/* Basic Information */}
						<div className="grid grid-cols-1 md:grid-cols-2 gap-6">
							<div>
								<label className="block text-sm font-medium text-gray-700 mb-2">
									Client
								</label>
								<select
									value={formData.client}
									onChange={(e) => setFormData(prev => ({ ...prev, client: e.target.value }))}
									className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
								>
									<option value="">Select a client</option>
									<option value="Acme Corp">Acme Corp</option>
									<option value="TechStart Inc">TechStart Inc</option>
									<option value="RetailMax">RetailMax</option>
									<option value="HealthCare Plus">HealthCare Plus</option>
								</select>
							</div>
							<div>
								<label className="block text-sm font-medium text-gray-700 mb-2">
									Invoice Date
								</label>
								<input
									type="date"
									value={formData.date}
									onChange={(e) => setFormData(prev => ({ ...prev, date: e.target.value }))}
									className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
								/>
							</div>
							<div>
								<label className="block text-sm font-medium text-gray-700 mb-2">
									Due Date
								</label>
								<input
									type="date"
									value={formData.due}
									onChange={(e) => setFormData(prev => ({ ...prev, due: e.target.value }))}
									className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
								/>
							</div>
							<div>
								<label className="block text-sm font-medium text-gray-700 mb-2">
									Payment Method
								</label>
								<select
									value={formData.method}
									onChange={(e) => setFormData(prev => ({ ...prev, method: e.target.value }))}
									className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
								>
									{mockPaymentMethods.map(method => (
										<option key={method.id} value={method.id}>
											{method.icon} {method.name}
										</option>
									))}
								</select>
							</div>
						</div>

						{/* Line Items */}
						<div>
							<div className="flex items-center justify-between mb-4">
								<h3 className="text-lg font-medium text-gray-900">Line Items</h3>
								<Button
									variant="outline"
									size="sm"
									onClick={handleAddItem}
									className="flex items-center gap-2"
								>
									<PlusIcon className="h-4 w-4" />
									Add Item
								</Button>
							</div>
							<div className="space-y-3">
								{formData.items.map((item, index) => (
									<div key={index} className="grid grid-cols-12 gap-3 items-center">
										<div className="col-span-6">
											<input
												type="text"
												placeholder="Description"
												value={item.desc}
												onChange={(e) => handleItemChange(index, 'desc', e.target.value)}
												className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
											/>
										</div>
										<div className="col-span-2">
											<input
												type="number"
												placeholder="Qty"
												value={item.qty}
												onChange={(e) => handleItemChange(index, 'qty', parseInt(e.target.value) || 0)}
												className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
											/>
										</div>
										<div className="col-span-3">
											<input
												type="number"
												placeholder="Price"
												value={item.price}
												onChange={(e) => handleItemChange(index, 'price', parseFloat(e.target.value) || 0)}
												className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
											/>
										</div>
										<div className="col-span-1">
											{formData.items.length > 1 && (
												<Button
													variant="outline"
													size="sm"
													onClick={() => handleRemoveItem(index)}
													className="p-2"
												>
													<XMarkIcon className="h-4 w-4" />
												</Button>
											)}
										</div>
									</div>
								))}
							</div>
						</div>

						{/* Totals */}
						<div className="bg-gray-50 rounded-lg p-4">
							<div className="space-y-2">
								<div className="flex justify-between">
									<span className="text-gray-600">Subtotal:</span>
									<span className="font-medium">${subtotal.toFixed(2)}</span>
								</div>
								<div className="flex justify-between">
									<span className="text-gray-600">Tax (10%):</span>
									<span className="font-medium">${tax.toFixed(2)}</span>
								</div>
								<div className="flex justify-between text-lg font-bold border-t pt-2">
									<span>Total:</span>
									<span>${total.toFixed(2)}</span>
								</div>
							</div>
						</div>

						{/* Notes */}
						<div>
							<label className="block text-sm font-medium text-gray-700 mb-2">
								Notes
							</label>
							<textarea
								value={formData.notes}
								onChange={(e) => setFormData(prev => ({ ...prev, notes: e.target.value }))}
								rows={3}
								className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
								placeholder="Additional notes or terms..."
							/>
						</div>

						{/* Actions */}
						<div className="flex gap-3 pt-4 border-t">
							<Button variant="outline">Save as Draft</Button>
							<Button variant="primary">Send Invoice</Button>
						</div>
					</CardContent>
				</Card>
			)}

			{activeTab === 'bulk' && (
				<Card>
					<CardHeader>
						<CardTitle className="flex items-center gap-2">
							<DocumentTextIcon className="h-5 w-5 text-purple-600" />
							Bulk Operations
						</CardTitle>
					</CardHeader>
					<CardContent>
						<div className="space-y-6">
							<div className="bg-blue-50 rounded-lg p-4">
								<h3 className="font-medium text-blue-900 mb-2">Quick Actions</h3>
								<div className="grid grid-cols-1 md:grid-cols-3 gap-3">
									<Button variant="outline" className="justify-start">
										Send Payment Reminders
									</Button>
									<Button variant="outline" className="justify-start">
										Mark as Paid
									</Button>
									<Button variant="outline" className="justify-start">
										Export Selected
									</Button>
								</div>
							</div>
							
							<div className="text-center py-8">
								<DocumentTextIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
								<h3 className="text-lg font-medium text-gray-900 mb-2">Select invoices to perform bulk operations</h3>
								<p className="text-gray-600">Go to the main invoices page to select multiple invoices for bulk actions.</p>
							</div>
						</div>
					</CardContent>
				</Card>
			)}

			{activeTab === 'templates' && (
				<Card>
					<CardHeader>
						<CardTitle className="flex items-center gap-2">
							<CheckIcon className="h-5 w-5 text-green-600" />
							Invoice Templates
						</CardTitle>
					</CardHeader>
					<CardContent>
						<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
							<div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer">
								<h3 className="font-medium text-gray-900 mb-2">Monthly Support</h3>
								<p className="text-sm text-gray-600 mb-3">Standard monthly IT support services</p>
								<div className="text-sm text-gray-500">
									<p>• Help Desk Support</p>
									<p>• System Monitoring</p>
									<p>• Emergency Response</p>
								</div>
							</div>
							<div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer">
								<h3 className="font-medium text-gray-900 mb-2">Project Setup</h3>
								<p className="text-sm text-gray-600 mb-3">One-time project implementation</p>
								<div className="text-sm text-gray-500">
									<p>• Initial Assessment</p>
									<p>• System Configuration</p>
									<p>• Training Sessions</p>
								</div>
							</div>
							<div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer">
								<h3 className="font-medium text-gray-900 mb-2">Security Audit</h3>
								<p className="text-sm text-gray-600 mb-3">Comprehensive security assessment</p>
								<div className="text-sm text-gray-500">
									<p>• Vulnerability Scan</p>
									<p>• Risk Assessment</p>
									<p>• Compliance Report</p>
								</div>
							</div>
						</div>
					</CardContent>
				</Card>
			)}

			{activeTab === 'reminders' && (
				<Card>
					<CardHeader>
						<CardTitle className="flex items-center gap-2">
							<ClockIcon className="h-5 w-5 text-orange-600" />
							Payment Reminders
						</CardTitle>
					</CardHeader>
					<CardContent>
						<div className="space-y-6">
							<div className="bg-orange-50 rounded-lg p-4">
								<h3 className="font-medium text-orange-900 mb-2">Overdue Invoices</h3>
								<p className="text-sm text-orange-700 mb-3">
									{mockInvoices.filter(i => i.status === 'overdue').length} invoices are overdue and need attention
								</p>
								<Button variant="primary" size="sm">
									Send Reminder Emails
								</Button>
							</div>

							<div className="space-y-3">
								{mockInvoices.filter(i => i.status === 'overdue').map(invoice => (
									<div key={invoice.id} className="flex items-center justify-between p-3 border border-red-200 rounded-lg bg-red-50">
										<div>
											<h4 className="font-medium text-gray-900">{invoice.id}</h4>
											<p className="text-sm text-gray-600">{invoice.client} • ${invoice.total.toLocaleString()}</p>
										</div>
										<div className="flex gap-2">
											<Button variant="outline" size="sm">
												Send Reminder
											</Button>
											<Button variant="primary" size="sm">
												Call Client
											</Button>
										</div>
									</div>
								))}
							</div>
						</div>
					</CardContent>
				</Card>
			)}
		</div>
	)
}
