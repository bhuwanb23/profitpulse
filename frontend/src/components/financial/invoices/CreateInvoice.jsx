import { useState } from 'react'

export default function CreateInvoice() {
	const [header, setHeader] = useState({ client: '', date: '', due: '' })
	const [items, setItems] = useState([{ desc: '', qty: 1, price: 0 }])
	const [errors, setErrors] = useState({})

	const subtotal = items.reduce((s, it) => s + (Number(it.qty) || 0) * (Number(it.price) || 0), 0)
	const tax = Math.round(subtotal * 0.1 * 100) / 100
	const total = subtotal + tax

	const validate = () => {
		const e = {}
		if (!header.client) e.client = 'Client is required'
		if (!header.date) e.date = 'Date is required'
		if (!header.due) e.due = 'Due date is required'
		if (items.length === 0 || items.some(it => !it.desc)) e.items = 'At least one item with description'
		setErrors(e)
		return Object.keys(e).length === 0
	}

	const addItem = () => setItems(prev => [...prev, { desc: '', qty: 1, price: 0 }])
	const removeItem = (idx) => setItems(prev => prev.filter((_, i) => i !== idx))
	const updateItem = (idx, patch) => setItems(prev => prev.map((it, i) => (i === idx ? { ...it, ...patch } : it)))

	const submit = (e) => {
		e.preventDefault()
		if (!validate()) return
		console.log('Create invoice (mock)', { header, items, subtotal, tax, total })
		alert('Invoice created (mock).')
		setHeader({ client: '', date: '', due: '' })
		setItems([{ desc: '', qty: 1, price: 0 }])
	}

	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Create Invoice</h2>
			<form onSubmit={submit} className="mt-4 space-y-4 text-sm">
				<div className="grid grid-cols-1 md:grid-cols-3 gap-4">
					<div>
						<label className="block text-gray-600 text-xs">Client</label>
						<input value={header.client} onChange={(e) => setHeader(prev => ({ ...prev, client: e.target.value }))} className={`mt-1 w-full rounded-md border px-3 py-2 ${errors.client ? 'border-red-400' : 'border-gray-300'}`} placeholder="Client name" />
						{errors.client && <p className="text-xs text-red-600 mt-1">{errors.client}</p>}
					</div>
					<div>
						<label className="block text-gray-600 text-xs">Date</label>
						<input value={header.date} onChange={(e) => setHeader(prev => ({ ...prev, date: e.target.value }))} className={`mt-1 w-full rounded-md border px-3 py-2 ${errors.date ? 'border-red-400' : 'border-gray-300'}`} placeholder="YYYY-MM-DD" />
						{errors.date && <p className="text-xs text-red-600 mt-1">{errors.date}</p>}
					</div>
					<div>
						<label className="block text-gray-600 text-xs">Due</label>
						<input value={header.due} onChange={(e) => setHeader(prev => ({ ...prev, due: e.target.value }))} className={`mt-1 w-full rounded-md border px-3 py-2 ${errors.due ? 'border-red-400' : 'border-gray-300'}`} placeholder="YYYY-MM-DD" />
						{errors.due && <p className="text-xs text-red-600 mt-1">{errors.due}</p>}
					</div>
				</div>

				<div className="overflow-x-auto">
					<table className="min-w-full text-sm">
						<thead>
							<tr className="text-left text-gray-500">
								<th className="py-2">Description</th>
								<th className="py-2">Qty</th>
								<th className="py-2">Unit Price</th>
								<th className="py-2 text-right">Amount</th>
								<th className="py-2"></th>
							</tr>
						</thead>
						<tbody className="divide-y">
							{items.map((it, i) => (
								<tr key={i}>
									<td className="py-2"><input value={it.desc} onChange={(e) => updateItem(i, { desc: e.target.value })} className="w-full rounded-md border border-gray-300 px-3 py-2" placeholder="Service or item" /></td>
									<td><input type="number" min={0} value={it.qty} onChange={(e) => updateItem(i, { qty: Number(e.target.value) })} className="w-20 rounded-md border border-gray-300 px-2 py-1" /></td>
									<td><input type="number" min={0} value={it.price} onChange={(e) => updateItem(i, { price: Number(e.target.value) })} className="w-28 rounded-md border border-gray-300 px-2 py-1" /></td>
									<td className="text-right">${((Number(it.qty)||0) * (Number(it.price)||0)).toLocaleString()}</td>
									<td className="text-right"><button type="button" onClick={() => removeItem(i)} className="text-xs px-2 py-1 rounded bg-gray-100 hover:bg-gray-200">Remove</button></td>
								</tr>
							))}
						</tbody>
						<tfoot>
							<tr>
								<td colSpan={5} className="py-2"><button type="button" onClick={addItem} className="text-xs px-3 py-1.5 rounded bg-blue-600 text-white hover:bg-blue-700">Add Item</button></td>
							</tr>
							<tr>
								<td colSpan={3} className="py-2 text-right">Subtotal</td>
								<td className="text-right font-medium">${subtotal.toLocaleString()}</td>
								<td></td>
							</tr>
							<tr>
								<td colSpan={3} className="py-2 text-right">Tax (10%)</td>
								<td className="text-right font-medium">${tax.toLocaleString()}</td>
								<td></td>
							</tr>
							<tr>
								<td colSpan={3} className="py-2 text-right">Total</td>
								<td className="text-right font-semibold">${total.toLocaleString()}</td>
								<td></td>
							</tr>
						</tfoot>
					</table>
				</div>
				{errors.items && <p className="text-xs text-red-600">{errors.items}</p>}
				<div>
					<button type="submit" className="mt-4 bg-blue-600 text-white text-sm px-4 py-2 rounded-md hover:bg-blue-700">Create Invoice</button>
				</div>
			</form>
		</section>
	)
}
