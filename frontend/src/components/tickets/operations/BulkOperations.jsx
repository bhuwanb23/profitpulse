import { useMemo, useState } from 'react'
import { mockTickets, mockTechnicians } from '../../../services/mockTickets'

export default function BulkOperations() {
	const [selected, setSelected] = useState([])
	const [action, setAction] = useState('close')
	const [assignee, setAssignee] = useState('')
	const [priority, setPriority] = useState('medium')

	const data = useMemo(() => mockTickets, [])

	const toggle = (id) => setSelected((prev) => (prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id]))

	const run = () => {
		console.log('Bulk action', { action, selected, assignee, priority })
		alert(`Applied '${action}' to ${selected.length} tickets (mock).`)
		setSelected([])
	}

	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Bulk Operations</h2>
			<div className="mt-3 flex flex-wrap gap-2 items-center text-sm">
				<select value={action} onChange={(e) => setAction(e.target.value)} className="border border-gray-300 rounded-md px-2 py-1">
					<option value="close">Close tickets</option>
					<option value="reassign">Reassign</option>
					<option value="priority">Change priority</option>
				</select>
				{action === 'reassign' && (
					<select value={assignee} onChange={(e) => setAssignee(e.target.value)} className="border border-gray-300 rounded-md px-2 py-1">
						<option value="">Select technician</option>
						{mockTechnicians.map(t => <option key={t.id} value={t.id}>{t.name}</option>)}
					</select>
				)}
				{action === 'priority' && (
					<select value={priority} onChange={(e) => setPriority(e.target.value)} className="border border-gray-300 rounded-md px-2 py-1">
						<option value="low">low</option>
						<option value="medium">medium</option>
						<option value="high">high</option>
						<option value="critical">critical</option>
					</select>
				)}
				<button onClick={run} className="bg-blue-600 text-white px-3 py-1.5 rounded-md hover:bg-blue-700">Apply</button>
			</div>
			<div className="mt-3 overflow-x-auto">
				<table className="min-w-full text-sm">
					<thead>
						<tr className="text-left text-gray-500">
							<th className="py-2"><input type="checkbox" onChange={(e) => setSelected(e.target.checked ? data.map(d => d.id) : [])} checked={selected.length === data.length && data.length > 0} /></th>
							<th className="py-2">Ticket</th>
							<th className="py-2">Client</th>
							<th className="py-2">Priority</th>
							<th className="py-2">Status</th>
						</tr>
					</thead>
					<tbody className="divide-y">
						{data.map(t => (
							<tr key={t.id}>
								<td className="py-2"><input type="checkbox" checked={selected.includes(t.id)} onChange={() => toggle(t.id)} /></td>
								<td className="py-2 font-medium">{t.id} — {t.title}</td>
								<td>{t.client}</td>
								<td>{t.priority}</td>
								<td>{t.status}</td>
							</tr>
						))}
					</tbody>
				</table>
			</div>
		</section>
	)
}
