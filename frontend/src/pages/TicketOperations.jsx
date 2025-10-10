import NewTicketForm from '../components/tickets/operations/NewTicketForm'
import BulkOperations from '../components/tickets/operations/BulkOperations'
import TicketTemplates from '../components/tickets/operations/TicketTemplates'
import EscalationManagement from '../components/tickets/operations/EscalationManagement'
import TicketRouting from '../components/tickets/operations/TicketRouting'
import SLAMonitor from '../components/tickets/operations/SLAMonitor'

export default function TicketOperationsPage() {
	return (
		<div className="space-y-6">
			<div className="flex items-center justify-between">
				<h1 className="text-2xl font-semibold">Ticket Operations</h1>
			</div>
			<NewTicketForm />
			<BulkOperations />
			<TicketTemplates />
			<EscalationManagement />
			<TicketRouting />
			<SLAMonitor />
		</div>
	)
}
