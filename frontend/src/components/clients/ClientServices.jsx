import { useState } from 'react'
import { mockAssignments, mockServices } from '../../services/mockClients'

export default function ClientServices({ clientId = 'c1' }) {
	const [rows, setRows] = useState(
		(mockAssignments[clientId] || []).map(a => {
			const svc = mockServices.find(s => s.id === a.serviceId)
			return { ...a, name: svc?.name || a.serviceId, billing: svc?.billing || '-', serviceId: a.serviceId }
		})
	)

	const updateRow = (idx, patch) => {
		setRows(prev => prev.map((r, i) => (i === idx ? { ...r, ...patch } : r)))
	}

	const onSave = () => {
		// Mock save: here you would POST to API
		console.log('Saving assignments', rows)
		alert('Service assignments saved (mock).')
	}

	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<div className="flex items-center justify-between">
				<h2 className="font-semibold">Assigned Services</h2>
				<button onClick={onSave} className="text-xs px-3 py-1.5 rounded bg-blue-600 text-white hover:bg-blue-700">Save Changes</button>
			</div>
			<div className="mt-3 overflow-x-auto">
				<table className="min-w-full text-sm">
					<thead>
						<tr className="text-left text-gray-500">
							<th className="py-2">Service</th>
							<th className="py-2">Billing</th>
							<th className="py-2">Quantity</th>
							<th className="py-2">Frequency</th>
							<th className="py-2">Custom Price</th>
						</tr>
					</thead>
					<tbody className="divide-y">
						{rows.map((r, i) => (
							<tr key={`${r.serviceId}-${i}`}>
								<td className="py-2">{r.name}</td>
								<td>{r.billing}</td>
								<td>
									<input type="number" min={0} value={r.quantity}
										onChange={(e) => updateRow(i, { quantity: Number(e.target.value) })}
										className="w-20 rounded-md border border-gray-300 px-2 py-1 text-sm" />
								</td>
								<td>
									<select value={r.frequency}
										onChange={(e) => updateRow(i, { frequency: e.target.value })}
										className="rounded-md border border-gray-300 px-2 py-1 text-sm">
										<option value="monthly">Monthly</option>
										<option value="quarterly">Quarterly</option>
										<option value="annually">Annually</option>
									</select>
								</td>
								<td>
									<div className="flex items-center gap-2">
										<span className="text-gray-500">$</span>
										<input type="number" min={0} value={r.customPrice}
											onChange={(e) => updateRow(i, { customPrice: Number(e.target.value) })}
											className="w-24 rounded-md border border-gray-300 px-2 py-1 text-sm" />
									</div>
								</td>
							</tr>
						))}
					</tbody>
				</table>
			</div>
		</section>
	)
}
