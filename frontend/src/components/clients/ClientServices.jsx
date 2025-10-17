import { useState, useMemo } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card'
import { Button } from '../ui/Button'
import { Badge } from '../ui/Badge'
import { Input } from '../ui/Input'
import { UsersIcon, CurrencyDollarIcon, TicketIcon } from '../ui/Icons'
import { mockAssignments, mockServices } from '../../services/mockClients'

export default function ClientServices({ clientId = 'c1' }) {
	const [assignments, setAssignments] = useState(
		(mockAssignments[clientId] || []).map(a => {
			const service = mockServices.find(s => s.id === a.serviceId)
			return { 
				...a, 
				name: service?.name || a.serviceId, 
				billing: service?.billing || '-', 
				category: service?.category || 'unknown',
				basePrice: service?.basePrice || 0,
				serviceId: a.serviceId 
			}
		})
	)

	const [hasChanges, setHasChanges] = useState(false)

	const updateAssignment = (index, updates) => {
		setAssignments(prev => prev.map((assignment, i) => 
			i === index ? { ...assignment, ...updates } : assignment
		))
		setHasChanges(true)
	}

	const removeAssignment = (index) => {
		setAssignments(prev => prev.filter((_, i) => i !== index))
		setHasChanges(true)
	}

	const calculateTotal = (assignment) => {
		const baseTotal = assignment.customPrice * assignment.quantity
		const frequencyMultiplier = {
			monthly: 12,
			quarterly: 4,
			annually: 1
		}
		return baseTotal * (frequencyMultiplier[assignment.frequency] || 1)
	}

	const totals = useMemo(() => {
		const monthlyTotal = assignments.reduce((sum, assignment) => {
			const total = calculateTotal(assignment)
			const frequencyDivisor = {
				monthly: 1,
				quarterly: 3,
				annually: 12
			}
			return sum + (total / (frequencyDivisor[assignment.frequency] || 1))
		}, 0)

		const annualTotal = assignments.reduce((sum, assignment) => {
			return sum + calculateTotal(assignment)
		}, 0)

		return { monthlyTotal, annualTotal }
	}, [assignments])

	const onSave = () => {
		// Mock save: here you would POST to API
		console.log('Saving assignments', assignments)
		setHasChanges(false)
		// Show success notification
		alert('Service assignments saved successfully!')
	}

	const getCategoryColor = (category) => {
		const colors = {
			support: 'blue',
			maintenance: 'green',
			consulting: 'purple',
			security: 'orange'
		}
		return colors[category] || 'default'
	}

	const formatCurrency = (amount) => {
		return new Intl.NumberFormat('en-US', {
			style: 'currency',
			currency: 'USD',
			minimumFractionDigits: 0
		}).format(amount)
	}

	return (
		<div>
			{/* Header with Save Button */}
			<div className="flex items-center justify-between mb-6">
				<div>
					<h2 className="text-xl font-semibold text-gray-900">Assigned Services</h2>
					<p className="text-sm text-gray-600 mt-1">Manage services assigned to this client</p>
				</div>
				<div className="flex items-center gap-3">
					{hasChanges && (
						<span className="text-sm text-amber-600 font-medium">
							Unsaved changes
						</span>
					)}
					<Button 
						onClick={onSave} 
						disabled={!hasChanges}
						size="sm"
					>
						Save Changes
					</Button>
				</div>
			</div>
				{/* Summary Cards */}
				<div className="mb-6 grid grid-cols-1 md:grid-cols-3 gap-4">
					<div className="bg-blue-50 rounded-lg p-4">
						<div className="flex items-center gap-3">
							<div className="p-2 bg-blue-100 rounded-lg">
								<TicketIcon className="h-5 w-5 text-blue-600" />
							</div>
							<div>
								<p className="text-sm text-gray-600">Active Services</p>
								<p className="text-xl font-bold text-gray-900">{assignments.length}</p>
							</div>
						</div>
					</div>
					<div className="bg-green-50 rounded-lg p-4">
						<div className="flex items-center gap-3">
							<div className="p-2 bg-green-100 rounded-lg">
								<CurrencyDollarIcon className="h-5 w-5 text-green-600" />
							</div>
							<div>
								<p className="text-sm text-gray-600">Monthly Revenue</p>
								<p className="text-xl font-bold text-gray-900">{formatCurrency(totals.monthlyTotal)}</p>
							</div>
						</div>
					</div>
					<div className="bg-purple-50 rounded-lg p-4">
						<div className="flex items-center gap-3">
							<div className="p-2 bg-purple-100 rounded-lg">
								<CurrencyDollarIcon className="h-5 w-5 text-purple-600" />
							</div>
							<div>
								<p className="text-sm text-gray-600">Annual Revenue</p>
								<p className="text-xl font-bold text-gray-900">{formatCurrency(totals.annualTotal)}</p>
							</div>
						</div>
					</div>
				</div>

				{/* Services Table */}
				{assignments.length > 0 ? (
					<div className="overflow-x-auto">
						<table className="min-w-full">
							<thead>
								<tr className="border-b border-gray-200">
									<th className="text-left py-3 px-4 font-medium text-gray-900">Service</th>
									<th className="text-left py-3 px-4 font-medium text-gray-900">Category</th>
									<th className="text-left py-3 px-4 font-medium text-gray-900">Quantity</th>
									<th className="text-left py-3 px-4 font-medium text-gray-900">Frequency</th>
									<th className="text-left py-3 px-4 font-medium text-gray-900">Price</th>
									<th className="text-left py-3 px-4 font-medium text-gray-900">Total</th>
									<th className="text-left py-3 px-4 font-medium text-gray-900">Actions</th>
								</tr>
							</thead>
							<tbody className="divide-y divide-gray-200">
								{assignments.map((assignment, index) => (
									<tr key={`${assignment.serviceId}-${index}`} className="hover:bg-gray-50">
										<td className="py-4 px-4">
											<div>
												<p className="font-medium text-gray-900">{assignment.name}</p>
												<p className="text-sm text-gray-500">{assignment.billing}</p>
											</div>
										</td>
										<td className="py-4 px-4">
											<Badge variant={getCategoryColor(assignment.category)} size="sm">
												{assignment.category}
											</Badge>
										</td>
										<td className="py-4 px-4">
											<Input
												type="number"
												min={0}
												value={assignment.quantity}
												onChange={(e) => updateAssignment(index, { quantity: Number(e.target.value) })}
												className="w-20"
											/>
										</td>
										<td className="py-4 px-4">
											<select
												value={assignment.frequency}
												onChange={(e) => updateAssignment(index, { frequency: e.target.value })}
												className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
											>
												<option value="monthly">Monthly</option>
												<option value="quarterly">Quarterly</option>
												<option value="annually">Annually</option>
											</select>
										</td>
										<td className="py-4 px-4">
											<div className="flex items-center gap-2">
												<span className="text-gray-500">$</span>
												<Input
													type="number"
													min={0}
													value={assignment.customPrice}
													onChange={(e) => updateAssignment(index, { customPrice: Number(e.target.value) })}
													className="w-24"
												/>
											</div>
										</td>
										<td className="py-4 px-4">
											<div>
												<p className="font-medium text-gray-900">
													{formatCurrency(calculateTotal(assignment))}
												</p>
												<p className="text-sm text-gray-500">per year</p>
											</div>
										</td>
										<td className="py-4 px-4">
											<Button
												variant="danger"
												size="sm"
												onClick={() => removeAssignment(index)}
											>
												Remove
											</Button>
										</td>
									</tr>
								))}
							</tbody>
						</table>
					</div>
				) : (
					<div className="text-center py-12">
						<UsersIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
						<h3 className="text-lg font-semibold text-gray-900 mb-2">No services assigned</h3>
						<p className="text-gray-600 mb-6">
							Add services from the catalog to get started with this client.
						</p>
						<Button 
							onClick={() => window.dispatchEvent(new CustomEvent('switchToServiceCatalog'))}
							variant="primary"
						>
							Browse Service Catalog
						</Button>
					</div>
				)}
		</div>
	)
}
