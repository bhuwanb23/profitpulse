import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { mockInvoices } from '../../../services/mockFinancial'

const statuses = ['all', 'draft', 'sent', 'paid', 'overdue']

export default function InvoiceList() {
	const [q, setQ] = useState('')
	const [status, setStatus] = useState('all')
	const [method, setMethod] = useState('all')

	const clients = useMemo(() => ['all', ...Array.from(new Set(mockInvoices.map(i => i.client)))], [])
	const [client, setClient] = useState('all')

	const filtered = useMemo(() => (
		mockInvoices.filter(i => {
			const mq = q ? (i.id.toLowerCase().includes(q.toLowerCase()) || i.client.toLowerCase().includes(q.toLowerCase())) : true
			const ms = status === 'all' || i.status === status
			const mm = method === 'all' || i.method === method
			const mc = client === 'all' || i.client === client
			return mq && ms && mm && mc
		})
	), [q, status, method, client])

	return (
		<div className="bg-white rounded-xl border border-gray-200 p-4 shadow-sm">
			<div className="flex flex-wrap gap-2 mb-3 items-center">
				<input className="w-72 rounded-md border border-gray-300 px-3 py-2 text-sm" placeholder="Search by invoice or client…" value={q} onChange={(e) => setQ(e.target.value)} />
				<select className="text-sm border border-gray-300 rounded-md px-2 py-1" value={status} onChange={(e) => setStatus(e.target.value)}>
					{statuses.map(s => <option key={s} value={s}>{s}</option>)}
				</select>
				<select className="text-sm border border-gray-300 rounded-md px-2 py-1" value={client} onChange={(e) => setClient(e.target.value)}>
					{clients.map(c => <option key={c} value={c}>{c}</option>)}
				</select>
				<select className="text-sm border border-gray-300 rounded-md px-2 py-1" value={method} onChange={(e) => setMethod(e.target.value)}>
					<option value="all">all methods</option>
					<option value="card">card</option>
					<option value="bank">bank</option>
				</select>
			</div>
			<div className="overflow-x-auto">
				<table className="min-w-full text-sm">
					<thead>
						<tr className="text-left text-gray-500">
							<th className="py-2">Invoice</th>
							<th className="py-2">Client</th>
							<th className="py-2">Date</th>
							<th className="py-2">Total</th>
							<th className="py-2">Status</th>
							<th className="py-2 text-right"></th>
						</tr>
					</thead>
					<tbody className="divide-y">
						{filtered.map(i => (
							<tr key={i.id}>
								<td className="py-2 font-medium">{i.id}</td>
								<td>{i.client}</td>
								<td>{i.date}</td>
								<td>${i.total.toLocaleString()}</td>
								<td><span className={`text-xs px-2 py-1 rounded ${i.status === 'paid' ? 'bg-green-50 text-green-700' : i.status === 'overdue' ? 'bg-red-50 text-red-700' : 'bg-gray-100'}`}>{i.status}</span></td>
								<td className="text-right"><Link to={`/invoices/${i.id}`} className="text-blue-600 hover:underline">View</Link></td>
							</tr>
						))}
					</tbody>
				</table>
			</div>
		</div>
	)
}
