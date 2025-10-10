import { useMemo, useState } from 'react'
import { useParams } from 'react-router-dom'
import { mockTickets, mockTechnicians, mockTimeEntries } from '../../services/mockTickets'

export default function TicketDetail() {
	const { id } = useParams()
	const ticket = useMemo(() => mockTickets.find(t => t.id === id), [id])
	const [status, setStatus] = useState(ticket?.status || 'open')
	const [priority, setPriority] = useState(ticket?.priority || 'medium')
	const [assignedTo, setAssignedTo] = useState(ticket?.assignedTo || '')
	const [timeEntries, setTimeEntries] = useState(mockTimeEntries[id] || [])
	const [newEntry, setNewEntry] = useState({ hours: '', note: '' })

	if (!ticket) return <div className="text-sm text-gray-500">Ticket not found.</div>

	const onSaveMeta = () => {
		console.log('Saving ticket meta', { status, priority, assignedTo })
		alert('Ticket updated (mock).')
	}

	const addTime = (e) => {
		e.preventDefault()
		const entry = { at: new Date().toISOString().slice(0,16).replace('T',' '), technician: assignedTo || 'u3', hours: Number(newEntry.hours), note: newEntry.note }
		setTimeEntries(prev => [...prev, entry])
		setNewEntry({ hours: '', note: '' })
	}

	return (
		<div className="space-y-6">
			<div className="flex items-center justify-between">
				<div>
					<h1 className="text-2xl font-semibold">{ticket.id} — {ticket.title}</h1>
					<p className="text-sm text-gray-500">{ticket.client} • {ticket.category}</p>
				</div>
				<button onClick={onSaveMeta} className="bg-blue-600 text-white text-sm px-3 py-2 rounded-md hover:bg-blue-700">Save</button>
			</div>

			<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
				<h2 className="font-semibold">Details</h2>
				<div className="mt-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 text-sm">
					<div>
						<label className="block text-gray-600 text-xs">Status</label>
						<select value={status} onChange={(e) => setStatus(e.target.value)} className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 text-sm">
							<option value="open">open</option>
							<option value="in_progress">in_progress</option>
							<option value="resolved">resolved</option>
							<option value="closed">closed</option>
						</select>
					</div>
					<div>
						<label className="block text-gray-600 text-xs">Priority</label>
						<select value={priority} onChange={(e) => setPriority(e.target.value)} className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 text-sm">
							<option value="low">low</option>
							<option value="medium">medium</option>
							<option value="high">high</option>
							<option value="critical">critical</option>
						</select>
					</div>
					<div>
						<label className="block text-gray-600 text-xs">Assign to</label>
						<select value={assignedTo} onChange={(e) => setAssignedTo(e.target.value)} className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 text-sm">
							<option value="">Unassigned</option>
							{mockTechnicians.map(t => <option key={t.id} value={t.id}>{t.name}</option>)}
						</select>
					</div>
					<div>
						<label className="block text-gray-600 text-xs">Created</label>
						<div className="mt-2">{ticket.createdAt}</div>
					</div>
				</div>
				<div className="mt-4">
					<label className="block text-gray-600 text-xs">Description</label>
					<p className="mt-1 text-sm text-gray-700">{ticket.description}</p>
				</div>
			</section>

			<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
				<h2 className="font-semibold">Time Tracking</h2>
				<form onSubmit={addTime} className="mt-3 flex flex-wrap gap-2 items-end">
					<div>
						<label className="block text-gray-600 text-xs">Hours</label>
						<input type="number" step="0.1" min={0} value={newEntry.hours} onChange={(e) => setNewEntry(prev => ({ ...prev, hours: e.target.value }))} className="mt-1 w-24 rounded-md border border-gray-300 px-3 py-2 text-sm" />
					</div>
					<div className="flex-1 min-w-[240px]">
						<label className="block text-gray-600 text-xs">Note</label>
						<input value={newEntry.note} onChange={(e) => setNewEntry(prev => ({ ...prev, note: e.target.value }))} className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 text-sm" placeholder="What did you work on?" />
					</div>
					<button type="submit" className="text-xs px-3 py-2 rounded bg-blue-600 text-white hover:bg-blue-700">Add Time</button>
				</form>
				<ul className="mt-4 divide-y">
					{timeEntries.map((e, i) => (
						<li key={i} className="py-2 text-sm flex items-center justify-between">
							<div>
								<div className="font-medium">{e.hours}h — {e.note}</div>
								<div className="text-xs text-gray-500">{e.at}</div>
							</div>
							<span className="text-xs px-2 py-1 rounded bg-gray-100">{e.technician}</span>
						</li>
					))}
				</ul>
			</section>
		</div>
	)
}
