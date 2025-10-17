import { Badge } from '../ui/Badge'
import { Button } from '../ui/Button'
import { TicketIcon, UsersIcon, CurrencyDollarIcon, DotsVerticalIcon } from '../ui/Icons'
import { Link } from 'react-router-dom'
import { mockTechnicians, mockTicketCategories } from '../../services/mockTickets'

export function TicketCard({ ticket }) {
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

	const getSLAColor = (slaStatus) => {
		const colors = {
			met: 'success',
			on_track: 'info',
			at_risk: 'warning',
			breached: 'danger'
		}
		return colors[slaStatus] || 'default'
	}

	const getCategoryInfo = (categoryId) => {
		return mockTicketCategories.find(cat => cat.id === categoryId) || 
			   { name: categoryId, color: 'default', icon: '📋' }
	}

	const getAssignedTechnician = (techId) => {
		return mockTechnicians.find(tech => tech.id === techId)
	}

	const formatDate = (dateString) => {
		return new Date(dateString).toLocaleDateString('en-US', {
			month: 'short',
			day: 'numeric',
			hour: '2-digit',
			minute: '2-digit'
		})
	}

	const formatTimeSpent = (hours) => {
		if (hours === 0) return 'No time logged'
		return `${hours}h logged`
	}

	const categoryInfo = getCategoryInfo(ticket.category)
	const assignedTech = getAssignedTechnician(ticket.assignedTo)

	return (
		<div className="bg-white rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-shadow duration-200">
			{/* Header */}
			<div className="p-6 pb-4">
				<div className="flex items-start justify-between mb-3">
					<div className="flex-1">
						<div className="flex items-center gap-3 mb-2">
							<div className={`w-10 h-10 rounded-lg flex items-center justify-center text-white font-semibold text-sm ${
								ticket.priority === 'critical' ? 'bg-red-600' :
								ticket.priority === 'high' ? 'bg-orange-500' :
								ticket.priority === 'medium' ? 'bg-yellow-500' :
								'bg-gray-500'
							}`}>
								{categoryInfo.icon}
							</div>
							<div className="flex-1">
								<h3 className="font-semibold text-gray-900 text-lg leading-tight">{ticket.title}</h3>
								<p className="text-sm text-gray-500">{ticket.id} • {ticket.client}</p>
							</div>
						</div>
					</div>
					<div className="flex items-center gap-2">
						<Badge variant={getPriorityColor(ticket.priority)} size="sm">
							{ticket.priority}
						</Badge>
						<button className="p-1 hover:bg-gray-100 rounded-md transition-colors">
							<DotsVerticalIcon className="h-4 w-4 text-gray-400" />
						</button>
					</div>
				</div>

				{/* Description */}
				<p className="text-sm text-gray-600 leading-relaxed mb-4 line-clamp-2">
					{ticket.description}
				</p>
			</div>

			{/* Metrics */}
			<div className="px-6 pb-4">
				<div className="grid grid-cols-2 gap-4">
					{/* Status & SLA */}
					<div className="space-y-3">
						<div className="flex items-center gap-2">
							<span className="text-xs text-gray-500 uppercase tracking-wide">Status</span>
							<Badge variant={getStatusColor(ticket.status)} size="sm">
								{ticket.status.replace('_', ' ')}
							</Badge>
						</div>
						<div className="flex items-center gap-2">
							<span className="text-xs text-gray-500 uppercase tracking-wide">SLA</span>
							<Badge variant={getSLAColor(ticket.slaStatus)} size="sm">
								{ticket.slaStatus.replace('_', ' ')}
							</Badge>
						</div>
					</div>

					{/* Time & Assignment */}
					<div className="space-y-3">
						<div>
							<p className="text-xs text-gray-500 uppercase tracking-wide">Time Spent</p>
							<p className="text-sm font-medium text-gray-900">{formatTimeSpent(ticket.timeSpent)}</p>
						</div>
						<div>
							<p className="text-xs text-gray-500 uppercase tracking-wide">Assigned To</p>
							<p className="text-sm font-medium text-gray-900">
								{assignedTech ? assignedTech.name : 'Unassigned'}
							</p>
						</div>
					</div>
				</div>
			</div>

			{/* Tags */}
			{ticket.tags && ticket.tags.length > 0 && (
				<div className="px-6 pb-4">
					<div className="flex flex-wrap gap-1">
						{ticket.tags.slice(0, 3).map((tag, index) => (
							<span 
								key={index}
								className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-md"
							>
								{tag}
							</span>
						))}
						{ticket.tags.length > 3 && (
							<span className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-md">
								+{ticket.tags.length - 3} more
							</span>
						)}
					</div>
				</div>
			)}

			{/* Footer */}
			<div className="px-6 py-4 bg-gray-50 rounded-b-xl border-t border-gray-100">
				<div className="flex items-center justify-between">
					<div className="text-xs text-gray-500">
						Created {formatDate(ticket.createdAt)}
					</div>
					<div className="flex gap-2">
						<Link to={`/tickets/${ticket.id}`}>
							<Button variant="ghost" size="sm">
								View Details
							</Button>
						</Link>
						<Link to={`/ticket-operations?ticket=${ticket.id}`}>
							<Button variant="primary" size="sm">
								Edit
							</Button>
						</Link>
					</div>
				</div>
			</div>
		</div>
	)
}
