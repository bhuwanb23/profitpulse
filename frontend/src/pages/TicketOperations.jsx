import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/Card'
import { Button } from '../components/ui/Button'
import { Input, SearchInput } from '../components/ui/Input'
import { Badge } from '../components/ui/Badge'
import { PlusIcon, TicketIcon, UsersIcon, ChartBarIcon, TrendingUpIcon } from '../components/ui/Icons'
import { mockTickets, mockTechnicians, mockTicketCategories } from '../services/mockTickets'
import { mockClients } from '../services/mockClients'
import { Link, useSearchParams } from 'react-router-dom'

export default function TicketOperationsPage() {
	const [searchParams] = useSearchParams()
	const [activeTab, setActiveTab] = useState('new-ticket')
	const [formData, setFormData] = useState({
		title: '',
		description: '',
		priority: 'medium',
		category: 'infrastructure',
		client: '',
		assignedTo: '',
		estimatedTime: ''
	})

	// Check if we should edit an existing ticket
	const ticketToEdit = searchParams.get('ticket')
	
	useEffect(() => {
		if (ticketToEdit) {
			const ticket = mockTickets.find(t => t.id === ticketToEdit)
			if (ticket) {
				setFormData({
					title: ticket.title,
					description: ticket.description,
					priority: ticket.priority,
					category: ticket.category,
					client: ticket.clientId || '',
					assignedTo: ticket.assignedTo || '',
					estimatedTime: ticket.estimatedTime?.toString() || ''
				})
				setActiveTab('new-ticket') // Use same form for editing
			}
		}
	}, [ticketToEdit])

	const handleInputChange = (field, value) => {
		setFormData(prev => ({ ...prev, [field]: value }))
	}

	const handleSubmit = (e) => {
		e.preventDefault()
		console.log('Saving ticket:', formData)
		
		if (ticketToEdit) {
			alert(`Ticket ${ticketToEdit} updated successfully!`)
		} else {
			alert('New ticket created successfully!')
		}
		
		// Reset form
		setFormData({
			title: '',
			description: '',
			priority: 'medium',
			category: 'infrastructure',
			client: '',
			assignedTo: '',
			estimatedTime: ''
		})
	}

	const getPriorityColor = (priority) => {
		const colors = {
			low: 'default',
			medium: 'warning',
			high: 'danger',
			critical: 'danger'
		}
		return colors[priority] || 'default'
	}

	const getStatusColor = (status) => {
		const colors = {
			open: 'info',
			in_progress: 'warning',
			resolved: 'success',
			closed: 'default'
		}
		return colors[status] || 'default'
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
				<span className="text-gray-600">Ticket Operations</span>
			</div>

			{/* Header */}
			<div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
				<div>
					<h1 className="text-3xl font-bold text-gray-900">
						{ticketToEdit ? `Edit Ticket ${ticketToEdit}` : 'Ticket Operations'}
					</h1>
					<p className="text-gray-600 mt-1">
						{ticketToEdit ? 'Update ticket details and assignments' : 'Create and manage support tickets'}
					</p>
				</div>
				
				<div className="flex flex-wrap gap-3">
					<Link to="/ticket-analytics">
						<Button variant="outline" size="sm" className="flex items-center gap-2">
							<ChartBarIcon className="h-4 w-4" />
							View Analytics
						</Button>
					</Link>
					<Link to="/tickets">
						<Button variant="outline" size="sm" className="flex items-center gap-2">
							<TicketIcon className="h-4 w-4" />
							All Tickets
						</Button>
					</Link>
				</div>
			</div>

			{/* Tab Navigation */}
			<div className="bg-white rounded-xl border border-gray-200 shadow-sm">
				<div className="border-b border-gray-200">
					<nav className="flex space-x-8 px-6" aria-label="Tabs">
						<button
							onClick={() => setActiveTab('new-ticket')}
							className={`py-4 px-1 border-b-2 font-medium text-sm ${
								activeTab === 'new-ticket'
									? 'border-blue-500 text-blue-600'
									: 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
							}`}
						>
							<div className="flex items-center gap-2">
								<PlusIcon className="h-4 w-4" />
								{ticketToEdit ? 'Edit Ticket' : 'New Ticket'}
							</div>
						</button>
						<button
							onClick={() => setActiveTab('bulk-operations')}
							className={`py-4 px-1 border-b-2 font-medium text-sm ${
								activeTab === 'bulk-operations'
									? 'border-blue-500 text-blue-600'
									: 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
							}`}
						>
							<div className="flex items-center gap-2">
								<TicketIcon className="h-4 w-4" />
								Bulk Operations
							</div>
						</button>
						<button
							onClick={() => setActiveTab('templates')}
							className={`py-4 px-1 border-b-2 font-medium text-sm ${
								activeTab === 'templates'
									? 'border-blue-500 text-blue-600'
									: 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
							}`}
						>
							<div className="flex items-center gap-2">
								<ChartBarIcon className="h-4 w-4" />
								Templates
							</div>
						</button>
						<button
							onClick={() => setActiveTab('sla-monitor')}
							className={`py-4 px-1 border-b-2 font-medium text-sm ${
								activeTab === 'sla-monitor'
									? 'border-blue-500 text-blue-600'
									: 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
							}`}
						>
							<div className="flex items-center gap-2">
								<TrendingUpIcon className="h-4 w-4" />
								SLA Monitor
							</div>
						</button>
					</nav>
				</div>

				{/* Tab Content */}
				<div className="p-6">
					{activeTab === 'new-ticket' && (
						<div className="space-y-6">
							<div>
								<h2 className="text-xl font-semibold text-gray-900 mb-2">
									{ticketToEdit ? 'Edit Ticket Details' : 'Create New Ticket'}
								</h2>
								<p className="text-sm text-gray-600">
									{ticketToEdit ? 'Update the ticket information below' : 'Fill in the details to create a new support ticket'}
								</p>
							</div>

							<form onSubmit={handleSubmit} className="space-y-6">
								<div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
									{/* Left Column */}
									<div className="space-y-4">
										<div>
											<label className="block text-sm font-medium text-gray-700 mb-2">
												Ticket Title *
											</label>
											<Input
												type="text"
												value={formData.title}
												onChange={(e) => handleInputChange('title', e.target.value)}
												placeholder="Brief description of the issue"
												required
											/>
										</div>

										<div>
											<label className="block text-sm font-medium text-gray-700 mb-2">
												Priority *
											</label>
											<select
												value={formData.priority}
												onChange={(e) => handleInputChange('priority', e.target.value)}
												className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
												required
											>
												<option value="low">Low</option>
												<option value="medium">Medium</option>
												<option value="high">High</option>
												<option value="critical">Critical</option>
											</select>
										</div>

										<div>
											<label className="block text-sm font-medium text-gray-700 mb-2">
												Category *
											</label>
											<select
												value={formData.category}
												onChange={(e) => handleInputChange('category', e.target.value)}
												className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
												required
											>
												{mockTicketCategories.map(category => (
													<option key={category.id} value={category.id}>
														{category.icon} {category.name}
													</option>
												))}
											</select>
										</div>

										<div>
											<label className="block text-sm font-medium text-gray-700 mb-2">
												Estimated Time (hours)
											</label>
											<Input
												type="number"
												step="0.5"
												min="0"
												value={formData.estimatedTime}
												onChange={(e) => handleInputChange('estimatedTime', e.target.value)}
												placeholder="2.5"
											/>
										</div>
									</div>

									{/* Right Column */}
									<div className="space-y-4">
										<div>
											<label className="block text-sm font-medium text-gray-700 mb-2">
												Client *
											</label>
											<select
												value={formData.client}
												onChange={(e) => handleInputChange('client', e.target.value)}
												className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
												required
											>
												<option value="">Select a client</option>
												{mockClients.map(client => (
													<option key={client.id} value={client.id}>
														{client.name}
													</option>
												))}
											</select>
										</div>

										<div>
											<label className="block text-sm font-medium text-gray-700 mb-2">
												Assign To
											</label>
											<select
												value={formData.assignedTo}
												onChange={(e) => handleInputChange('assignedTo', e.target.value)}
												className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
											>
												<option value="">Unassigned</option>
												{mockTechnicians.map(tech => (
													<option key={tech.id} value={tech.id}>
														{tech.name} - {tech.role}
													</option>
												))}
											</select>
										</div>

										<div>
											<label className="block text-sm font-medium text-gray-700 mb-2">
												Description *
											</label>
											<textarea
												value={formData.description}
												onChange={(e) => handleInputChange('description', e.target.value)}
												placeholder="Detailed description of the issue..."
												rows={4}
												className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
												required
											/>
										</div>
									</div>
								</div>

								<div className="flex items-center justify-between pt-4 border-t border-gray-200">
									<div className="flex items-center gap-2">
										<Badge variant={getPriorityColor(formData.priority)} size="sm">
											{formData.priority} priority
										</Badge>
										{formData.category && (
											<Badge variant="info" size="sm">
												{mockTicketCategories.find(c => c.id === formData.category)?.name}
											</Badge>
										)}
									</div>
									<div className="flex gap-3">
										<Button type="button" variant="outline">
											Save as Draft
										</Button>
										<Button type="submit">
											{ticketToEdit ? 'Update Ticket' : 'Create Ticket'}
										</Button>
									</div>
								</div>
							</form>
						</div>
					)}

					{activeTab === 'bulk-operations' && (
						<div className="space-y-6">
							<div>
								<h2 className="text-xl font-semibold text-gray-900 mb-2">Bulk Operations</h2>
								<p className="text-sm text-gray-600">Perform actions on multiple tickets at once</p>
							</div>

							<div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
								<Card>
									<CardHeader>
										<CardTitle>Bulk Assignment</CardTitle>
									</CardHeader>
									<CardContent className="space-y-4">
										<div>
											<label className="block text-sm font-medium text-gray-700 mb-2">
												Assign tickets to technician
											</label>
											<select className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm">
												<option value="">Select technician</option>
												{mockTechnicians.map(tech => (
													<option key={tech.id} value={tech.id}>
														{tech.name} ({tech.activeTickets} active)
													</option>
												))}
											</select>
										</div>
										<Button className="w-full">Assign Selected Tickets</Button>
									</CardContent>
								</Card>

								<Card>
									<CardHeader>
										<CardTitle>Bulk Status Update</CardTitle>
									</CardHeader>
									<CardContent className="space-y-4">
										<div>
											<label className="block text-sm font-medium text-gray-700 mb-2">
												Update status for selected tickets
											</label>
											<select className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm">
												<option value="open">Open</option>
												<option value="in_progress">In Progress</option>
												<option value="resolved">Resolved</option>
												<option value="closed">Closed</option>
											</select>
										</div>
										<Button className="w-full">Update Status</Button>
									</CardContent>
								</Card>
							</div>
						</div>
					)}

					{activeTab === 'templates' && (
						<div className="space-y-6">
							<div>
								<h2 className="text-xl font-semibold text-gray-900 mb-2">Ticket Templates</h2>
								<p className="text-sm text-gray-600">Pre-configured templates for common issues</p>
							</div>

							<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
								{[
									{ name: 'Email Server Issue', category: 'Infrastructure', priority: 'High' },
									{ name: 'VPN Connection Problem', category: 'Network', priority: 'Medium' },
									{ name: 'Software Installation', category: 'Software', priority: 'Low' },
									{ name: 'Security Incident', category: 'Security', priority: 'Critical' },
									{ name: 'Hardware Failure', category: 'Hardware', priority: 'High' },
									{ name: 'Database Performance', category: 'Database', priority: 'Medium' },
								].map((template, index) => (
									<Card key={index} className="cursor-pointer hover:shadow-md transition-shadow">
										<CardContent className="p-4">
											<h3 className="font-medium text-gray-900 mb-2">{template.name}</h3>
											<div className="flex items-center gap-2 mb-3">
												<Badge variant="info" size="sm">{template.category}</Badge>
												<Badge variant={getPriorityColor(template.priority.toLowerCase())} size="sm">
													{template.priority}
												</Badge>
											</div>
											<Button size="sm" className="w-full">Use Template</Button>
										</CardContent>
									</Card>
								))}
							</div>
						</div>
					)}

					{activeTab === 'sla-monitor' && (
						<div className="space-y-6">
							<div>
								<h2 className="text-xl font-semibold text-gray-900 mb-2">SLA Monitor</h2>
								<p className="text-sm text-gray-600">Track SLA compliance and at-risk tickets</p>
							</div>

							<div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
								<Card>
									<CardHeader>
										<CardTitle className="text-red-600">SLA Breached Tickets</CardTitle>
									</CardHeader>
									<CardContent>
										<div className="space-y-3">
											{mockTickets.filter(t => t.slaStatus === 'breached').map(ticket => (
												<div key={ticket.id} className="flex items-center justify-between p-3 bg-red-50 rounded-lg border border-red-200">
													<div>
														<p className="font-medium text-gray-900">{ticket.id}</p>
														<p className="text-sm text-gray-600">{ticket.title}</p>
													</div>
													<Badge variant="danger" size="sm">Breached</Badge>
												</div>
											))}
										</div>
									</CardContent>
								</Card>

								<Card>
									<CardHeader>
										<CardTitle className="text-yellow-600">At Risk Tickets</CardTitle>
									</CardHeader>
									<CardContent>
										<div className="space-y-3">
											{mockTickets.filter(t => t.slaStatus === 'at_risk').map(ticket => (
												<div key={ticket.id} className="flex items-center justify-between p-3 bg-yellow-50 rounded-lg border border-yellow-200">
													<div>
														<p className="font-medium text-gray-900">{ticket.id}</p>
														<p className="text-sm text-gray-600">{ticket.title}</p>
													</div>
													<Badge variant="warning" size="sm">At Risk</Badge>
												</div>
											))}
										</div>
									</CardContent>
								</Card>
							</div>
						</div>
					)}
				</div>
			</div>

			{/* Quick Actions */}
			<div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl p-6 border border-blue-100">
				<div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
					<div>
						<h3 className="text-lg font-semibold text-gray-900 mb-1">
							Need help with ticket management?
						</h3>
						<p className="text-gray-600">
							Our team can help you optimize your ticket workflows and improve response times.
						</p>
					</div>
					<div className="flex flex-wrap gap-3">
						<Link to="/ticket-analytics">
							<Button variant="outline" size="sm">
								View Analytics
							</Button>
						</Link>
						<Button variant="primary" size="sm">
							Contact Support
						</Button>
					</div>
				</div>
			</div>
		</div>
	)
}
