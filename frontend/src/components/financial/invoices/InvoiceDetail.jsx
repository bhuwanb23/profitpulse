import { useMemo, useState } from 'react'
import { useParams } from 'react-router-dom'
import { mockInvoices, mockInvoiceItems } from '../../../services/mockFinancial'

export default function InvoiceDetail() {
	const { id } = useParams()
	const invoice = useMemo(() => mockInvoices.find(i => i.id === id), [id])
	const items = mockInvoiceItems[id] || []
	const [status, setStatus] = useState(invoice?.status || 'draft')
	const [paidAt, setPaidAt] = useState(invoice?.paidAt || '')
	const [method, setMethod] = useState(invoice?.method || 'card')

	if (!invoice) return <div className="text-sm text-gray-500">Invoice not found.</div>

	const subtotal = items.reduce((s, it) => s + it.qty * it.price, 0)
	const tax = Math.round(subtotal * 0.1 * 100) / 100
	const total = subtotal + tax

	const save = () => {
		console.log('Saving invoice meta', { status, paidAt, method })
		alert('Invoice updated (mock).')
	}

	return (
		<div className="space-y-6">
			<div className="flex items-center justify-between">
				<div>
					<h1 className="text-2xl font-semibold">{invoice.id}</h1>
					<p className="text-sm text-gray-500">{invoice.client} • {invoice.date}</p>
				</div>
				<button onClick={save} className="bg-blue-600 text-white text-sm px-3 py-2 rounded-md hover:bg-blue-700">Save</button>
			</div>

			<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
				<h2 className="font-semibold">Status & Payment</h2>
				<div className="mt-4 grid grid-cols-1 md:grid-cols-4 gap-4 text-sm">
					<div>
						<label className="block text-gray-600 text-xs">Status</label>
						<select value={status} onChange={(e) => setStatus(e.target.value)} className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 text-sm">
							<option value="draft">draft</option>
							<option value="sent">sent</option>
							<option value="paid">paid</option>
							<option value="overdue">overdue</option>
						</select>
					</div>
					<div>
						<label className="block text-gray-600 text-xs">Payment Method</label>
						<select value={method} onChange={(e) => setMethod(e.target.value)} className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 text-sm">
							<option value="card">card</option>
							<option value="bank">bank</option>
							<option value="cash">cash</option>
						</select>
					</div>
					<div>
						<label className="block text-gray-600 text-xs">Paid At</label>
						<input value={paidAt || ''} onChange={(e) => setPaidAt(e.target.value)} className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 text-sm" placeholder="YYYY-MM-DD" />
					</div>
				</div>
			</section>

			<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
				<h2 className="font-semibold">Items</h2>
				<div className="mt-3 overflow-x-auto">
					<table className="min-w-full text-sm">
						<thead>
							<tr className="text-left text-gray-500">
								<th className="py-2">Description</th>
								<th className="py-2">Qty</th>
								<th className="py-2">Unit Price</th>
								<th className="py-2">Amount</th>
							</tr>
						</thead>
						<tbody className="divide-y">
							{items.map((it, i) => (
								<tr key={i}>
									<td className="py-2">{it.desc}</td>
									<td>{it.qty}</td>
									<td>${it.price.toLocaleString()}</td>
									<td>${(it.qty * it.price).toLocaleString()}</td>
								</tr>
							))}
						</tbody>
						<tfoot>
							<tr>
								<td colSpan={3} className="py-2 text-right">Subtotal</td>
								<td className="font-medium">${subtotal.toLocaleString()}</td>
							</tr>
							<tr>
								<td colSpan={3} className="py-2 text-right">Tax (10%)</td>
								<td className="font-medium">${tax.toLocaleString()}</td>
							</tr>
							<tr>
								<td colSpan={3} className="py-2 text-right">Total</td>
								<td className="font-semibold">${total.toLocaleString()}</td>
							</tr>
						</tfoot>
					</table>
				</div>
			</section>
		</div>
	)
}
