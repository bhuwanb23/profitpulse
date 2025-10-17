import { useState, useMemo } from 'react'
import { TicketCard } from '../components/tickets/TicketCard'
import { Button } from '../components/ui/Button'
import { SearchInput } from '../components/ui/Input'
import { Card, CardContent } from '../components/ui/Card'
import { PlusIcon, TicketIcon, UsersIcon, TrendingUpIcon, ChartBarIcon } from '../components/ui/Icons'
import { mockTickets, mockTicketCategories, mockTechnicians } from '../services/mockTickets'
import { Link } from 'react-router-dom'

export default function Tickets() {
	const [searchQuery, setSearchQuery] = useState('')
	const [statusFilter, setStatusFilter] = useState('all')
	const [priorityFilter, setPriorityFilter] = useState('all')
	const [categoryFilter, setCategoryFilter] = useState('all')
	const [assigneeFilter, setAssigneeFilter] = useState('all')
	const [sortBy, setSortBy] = useState('created')

	// Filter and sort tickets
	const filteredTickets = useMemo(() => {
		let filtered = mockTickets.filter(ticket => {
			const matchesSearch = ticket.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
								ticket.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
								ticket.client.toLowerCase().includes(searchQuery.toLowerCase()) ||
								ticket.description.toLowerCase().includes(searchQuery.toLowerCase())
			
			const matchesStatus = statusFilter === 'all' || ticket.status === statusFilter
			const matchesPriority = priorityFilter === 'all' || ticket.priority === priorityFilter
			const matchesCategory = categoryFilter === 'all' || ticket.category === categoryFilter
			const matchesAssignee = assigneeFilter === 'all' || 
								   (assigneeFilter === 'unassigned' && !ticket.assignedTo) ||
								   ticket.assignedTo === assigneeFilter
			
			return matchesSearch && matchesStatus && matchesPriority && matchesCategory && matchesAssignee
		})

		// Sort tickets
		filtered.sort((a, b) => {
			switch (sortBy) {
				case 'created':
					return new Date(b.createdAt) - new Date(a.createdAt)
				case 'updated':
					return new Date(b.updatedAt) - new Date(a.updatedAt)
				case 'priority':
					const priorityOrder = { critical: 4, high: 3, medium: 2, low: 1 }
					return priorityOrder[b.priority] - priorityOrder[a.priority]
				case 'sla':
					const slaOrder = { breached: 4, at_risk: 3, on_track: 2, met: 1 }
					return slaOrder[b.slaStatus] - slaOrder[a.slaStatus]
				default:
					return 0
			}
		})

		return filtered
	}, [searchQuery, statusFilter, priorityFilter, categoryFilter, assigneeFilter, sortBy])

	// Calculate summary stats
	const stats = useMemo(() => {
		const totalTickets = filteredTickets.length
		const openTickets = filteredTickets.filter(t => t.status === 'open').length
		const inProgressTickets = filteredTickets.filter(t => t.status === 'in_progress').length
		const criticalTickets = filteredTickets.filter(t => t.priority === 'critical' || t.priority === 'high').length
		const slaBreached = filteredTickets.filter(t => t.slaStatus === 'breached').length
		const avgResolutionTime = filteredTickets
			.filter(t => t.status === 'resolved' && t.resolvedAt)
			.reduce((sum, t) => {
				const created = new Date(t.createdAt)
				const resolved = new Date(t.resolvedAt)
				return sum + (resolved - created) / (1000 * 60 * 60) // hours
			}, 0) / filteredTickets.filter(t => t.status === 'resolved').length || 0

		return {
			totalTickets,
			openTickets,
			inProgressTickets,
			criticalTickets,
			slaBreached,
			avgResolutionTime
		}
	}, [filteredTickets])

	const formatHours = (hours) => {
		if (hours < 1) return `${Math.round(hours * 60)}m`
		return `${hours.toFixed(1)}h`
	}

	return (
		<div className="space-y-6">
			{/* Header */}
			<div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
				<div>
					<h1 className="text-3xl font-bold text-gray-900">Support Tickets</h1>
					<p className="text-gray-600 mt-1">Manage and track support requests</p>
				</div>
				<div className="flex gap-3">
					<Link to="/ticket-analytics">
						<Button variant="outline" className="flex items-center gap-2">
							<ChartBarIcon className="h-4 w-4" />
							Analytics
						</Button>
					</Link>
					<Link to="/ticket-operations">
						<Button className="flex items-center gap-2">
							<PlusIcon className="h-4 w-4" />
							New Ticket
						</Button>
					</Link>
				</div>
			</div>

			{/* Stats Overview */}
			<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 xl:grid-cols-6 gap-4">
				<Card>
					<CardContent className="p-4">
						<div className="flex items-center gap-3">
							<div className="p-2 bg-blue-100 rounded-lg">
								<TicketIcon className="h-5 w-5 text-blue-600" />
							</div>
							<div>
								<p className="text-sm text-gray-600">Total</p>
								<p className="text-xl font-bold text-gray-900">{stats.totalTickets}</p>
							</div>
						</div>
					</CardContent>
				</Card>

				<Card>
					<CardContent className="p-4">
						<div className="flex items-center gap-3">
							<div className="p-2 bg-red-100 rounded-lg">
								<TicketIcon className="h-5 w-5 text-red-600" />
							</div>
							<div>
								<p className="text-sm text-gray-600">Open</p>
								<p className="text-xl font-bold text-gray-900">{stats.openTickets}</p>
							</div>
						</div>
					</CardContent>
				</Card>

				<Card>
					<CardContent className="p-4">
						<div className="flex items-center gap-3">
							<div className="p-2 bg-yellow-100 rounded-lg">
								<TrendingUpIcon className="h-5 w-5 text-yellow-600" />
							</div>
							<div>
								<p className="text-sm text-gray-600">In Progress</p>
								<p className="text-xl font-bold text-gray-900">{stats.inProgressTickets}</p>
							</div>
						</div>
					</CardContent>
				</Card>

				<Card>
					<CardContent className="p-4">
						<div className="flex items-center gap-3">
							<div className="p-2 bg-orange-100 rounded-lg">
								<TicketIcon className="h-5 w-5 text-orange-600" />
							</div>
							<div>
								<p className="text-sm text-gray-600">Critical</p>
								<p className="text-xl font-bold text-gray-900">{stats.criticalTickets}</p>
							</div>
						</div>
					</CardContent>
				</Card>

				<Card>
					<CardContent className="p-4">
						<div className="flex items-center gap-3">
							<div className="p-2 bg-red-100 rounded-lg">
								<TicketIcon className="h-5 w-5 text-red-600" />
							</div>
							<div>
								<p className="text-sm text-gray-600">SLA Breached</p>
								<p className="text-xl font-bold text-gray-900">{stats.slaBreached}</p>
							</div>
						</div>
					</CardContent>
				</Card>

				<Card>
					<CardContent className="p-4">
						<div className="flex items-center gap-3">
							<div className="p-2 bg-green-100 rounded-lg">
								<TrendingUpIcon className="h-5 w-5 text-green-600" />
							</div>
							<div>
								<p className="text-sm text-gray-600">Avg Resolution</p>
								<p className="text-xl font-bold text-gray-900">{formatHours(stats.avgResolutionTime)}</p>
							</div>
						</div>
					</CardContent>
				</Card>
			</div>

			{/* Filters and Search */}
			<Card>
				<CardContent className="p-6">
					<div className="space-y-4">
						<SearchInput
							placeholder="Search tickets by title, ID, client, or description..."
							value={searchQuery}
							onChange={(e) => setSearchQuery(e.target.value)}
							className="w-full"
						/>
						
						<div className="flex flex-wrap gap-3">
							<select
								value={statusFilter}
								onChange={(e) => setStatusFilter(e.target.value)}
								className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
							>
								<option value="all">All Statuses</option>
								<option value="open">Open</option>
								<option value="in_progress">In Progress</option>
								<option value="resolved">Resolved</option>
								<option value="closed">Closed</option>
							</select>

							<select
								value={priorityFilter}
								onChange={(e) => setPriorityFilter(e.target.value)}
								className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
							>
								<option value="all">All Priorities</option>
								<option value="critical">Critical</option>
								<option value="high">High</option>
								<option value="medium">Medium</option>
								<option value="low">Low</option>
							</select>

							<select
								value={categoryFilter}
								onChange={(e) => setCategoryFilter(e.target.value)}
								className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
							>
								<option value="all">All Categories</option>
								{mockTicketCategories.map(category => (
									<option key={category.id} value={category.id}>
										{category.name}
									</option>
								))}
							</select>

							<select
								value={assigneeFilter}
								onChange={(e) => setAssigneeFilter(e.target.value)}
								className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
							>
								<option value="all">All Assignees</option>
								<option value="unassigned">Unassigned</option>
								{mockTechnicians.map(tech => (
									<option key={tech.id} value={tech.id}>
										{tech.name}
									</option>
								))}
							</select>

							<select
								value={sortBy}
								onChange={(e) => setSortBy(e.target.value)}
								className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
							>
								<option value="created">Sort by Created</option>
								<option value="updated">Sort by Updated</option>
								<option value="priority">Sort by Priority</option>
								<option value="sla">Sort by SLA Status</option>
							</select>
						</div>
					</div>
				</CardContent>
			</Card>

			{/* Tickets Grid */}
			<div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
				{filteredTickets.map(ticket => (
					<TicketCard key={ticket.id} ticket={ticket} />
				))}
			</div>

			{/* Empty State */}
			{filteredTickets.length === 0 && (
				<Card>
					<CardContent className="p-12 text-center">
						<TicketIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
						<h3 className="text-lg font-semibold text-gray-900 mb-2">No tickets found</h3>
						<p className="text-gray-600 mb-6">
							{searchQuery || statusFilter !== 'all' || priorityFilter !== 'all' || categoryFilter !== 'all' || assigneeFilter !== 'all'
								? 'Try adjusting your search or filters'
								: 'Get started by creating your first support ticket'}
						</p>
						<Link to="/ticket-operations">
							<Button>
								<PlusIcon className="h-4 w-4 mr-2" />
								Create Ticket
							</Button>
						</Link>
					</CardContent>
				</Card>
			)}
		</div>
	)
}
