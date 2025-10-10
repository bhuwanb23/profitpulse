import { useMemo, useState } from 'react'
import { mockInvoices } from '../../../services/mockFinancial'

export default function BulkInvoiceOperations() {
	const data = useMemo(() => mockInvoices, [])
	const [selected, setSelected] = useState([])
	const [action, setAction] = useState('status')
	const [status, setStatus] = useState('sent')
	const [paidAt, setPaidAt] = useState('')

	const toggle = (id) => setSelected((prev) => (prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id]))

	const run = () => {
		console.log('Bulk invoice action', { action, selected, status, paidAt })
		alert(`Applied '${action}' to ${selected.length} invoices (mock).`)
		setSelected([])
	}

	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Bulk Invoice Operations</h2>
			<div className="mt-3 flex flex-wrap gap-2 items-center text-sm">
				<select value={action} onChange={(e) => setAction(e.target.value)} className="border border-gray-300 rounded-md px-2 py-1">
					<option value="status">Change status</option>
					<option value="paidAt">Set paid date</option>
					<option value="export">Export CSV</option>
				</select>
				{action === 'status' && (
					<select value={status} onChange={(e) => setStatus(e.target.value)} className="border border-gray-300 rounded-md px-2 py-1">
						<option value="draft">draft</option>
						<option value="sent">sent</option>
						<option value="paid">paid</option>
						<option value="overdue">overdue</option>
					</select>
				)}
				{action === 'paidAt' && (
					<input value={paidAt} onChange={(e) => setPaidAt(e.target.value)} className="border border-gray-300 rounded-md px-2 py-1" placeholder="YYYY-MM-DD" />
				)}
				<button onClick={run} className="bg-blue-600 text-white px-3 py-1.5 rounded-md hover:bg-blue-700">Apply</button>
			</div>
			<div className="mt-3 overflow-x-auto">
				<table className="min-w-full text-sm">
					<thead>
						<tr className="text-left text-gray-500">
							<th className="py-2"><input type="checkbox" onChange={(e) => setSelected(e.target.checked ? data.map(d => d.id) : [])} checked={selected.length === data.length && data.length > 0} /></th>
							<th className="py-2">Invoice</th>
							<th className="py-2">Client</th>
							<th className="py-2">Date</th>
							<th className="py-2">Total</th>
							<th className="py-2">Status</th>
						</tr>
					</thead>
					<tbody className="divide-y">
						{data.map(i => (
							<tr key={i.id}>
								<td className="py-2"><input type="checkbox" checked={selected.includes(i.id)} onChange={() => toggle(i.id)} /></td>
								<td className="py-2 font-medium">{i.id}</td>
								<td>{i.client}</td>
								<td>{i.date}</td>
								<td>${i.total.toLocaleString()}</td>
								<td>{i.status}</td>
							</tr>
						))}
					</tbody>
				</table>
			</div>
		</section>
	)
}
