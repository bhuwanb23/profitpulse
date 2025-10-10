import { Routes, Route } from 'react-router-dom'
import TicketList from '../components/tickets/TicketList'
import TicketDetail from '../components/tickets/TicketDetail'

export default function Tickets() {
	return (
		<div className="space-y-6">
			<div className="flex items-center justify-between">
				<h1 className="text-2xl font-semibold">Tickets</h1>
				<div className="flex gap-2">
					<button className="bg-blue-600 text-white text-sm px-3 py-2 rounded-md hover:bg-blue-700">+ New Ticket</button>
				</div>
			</div>
			<Routes>
				<Route index element={<TicketList />} />
				<Route path=":id" element={<TicketDetail />} />
			</Routes>
		</div>
	)
}
