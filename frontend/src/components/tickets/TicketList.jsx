import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { mockTickets, mockTicketCategories } from '../../services/mockTickets'

const statuses = ['all', 'open', 'in_progress', 'resolved', 'closed']
const priorities = ['all', 'low', 'medium', 'high', 'critical']

export default function TicketList() {
	const [q, setQ] = useState('')
	const [status, setStatus] = useState('all')
	const [priority, setPriority] = useState('all')
	const [category, setCategory] = useState('all')

	const filtered = useMemo(() => {
		return mockTickets.filter(t => {
			const mq = q ? (t.title.toLowerCase().includes(q.toLowerCase()) || t.id.toLowerCase().includes(q.toLowerCase()) || t.client.toLowerCase().includes(q.toLowerCase())) : true
			const ms = status === 'all' || t.status === status
			const mp = priority === 'all' || t.priority === priority
			const mc = category === 'all' || t.category === category
			return mq && ms && mp && mc
		})
	}, [q, status, priority, category])

	return (
		<div className="bg-white rounded-xl border border-gray-200 p-4 shadow-sm">
			<div className="flex flex-wrap gap-2 mb-3 items-center">
				<input className="w-72 rounded-md border border-gray-300 px-3 py-2 text-sm" placeholder="Search by title, ID, client…" value={q} onChange={(e) => setQ(e.target.value)} />
				<select className="text-sm border border-gray-300 rounded-md px-2 py-1" value={status} onChange={(e) => setStatus(e.target.value)}>
					{statuses.map(s => <option key={s} value={s}>{s}</option>)}
				</select>
				<select className="text-sm border border-gray-300 rounded-md px-2 py-1" value={priority} onChange={(e) => setPriority(e.target.value)}>
					{priorities.map(p => <option key={p} value={p}>{p}</option>)}
				</select>
				<select className="text-sm border border-gray-300 rounded-md px-2 py-1" value={category} onChange={(e) => setCategory(e.target.value)}>
					<option value="all">all</option>
					{mockTicketCategories.map(c => <option key={c} value={c}>{c}</option>)}
				</select>
			</div>
			<div className="overflow-x-auto">
				<table className="min-w-full text-sm">
					<thead>
						<tr className="text-left text-gray-500">
							<th className="py-2">Ticket</th>
							<th className="py-2">Client</th>
							<th className="py-2">Priority</th>
							<th className="py-2">Status</th>
							<th className="py-2">Category</th>
							<th className="py-2">Created</th>
							<th className="py-2 text-right"></th>
						</tr>
					</thead>
					<tbody className="divide-y">
						{filtered.map(t => (
							<tr key={t.id}>
								<td className="py-2 font-medium">{t.id} — {t.title}</td>
								<td>{t.client}</td>
								<td><span className="text-xs px-2 py-1 rounded bg-gray-100">{t.priority}</span></td>
								<td><span className="text-xs px-2 py-1 rounded bg-gray-100">{t.status}</span></td>
								<td>{t.category}</td>
								<td>{t.createdAt}</td>
								<td className="text-right"><Link to={`/tickets/${t.id}`} className="text-blue-600 hover:underline">View</Link></td>
							</tr>
						))}
					</tbody>
				</table>
			</div>
		</div>
	)
}
