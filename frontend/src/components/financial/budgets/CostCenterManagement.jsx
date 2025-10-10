import { useState } from 'react'
import { mockCostCenters } from '../../../services/mockFinancial'

export default function CostCenterManagement() {
	const [rows, setRows] = useState(mockCostCenters)
	const [name, setName] = useState('')
	const add = (e) => {
		e.preventDefault()
		if (!name) return
		setRows(prev => [...prev, { id: `CC-${Date.now()}`, name }])
		setName('')
	}
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Cost Centers</h2>
			<form onSubmit={add} className="mt-3 flex gap-2">
				<input value={name} onChange={(e) => setName(e.target.value)} className="rounded-md border border-gray-300 px-3 py-2 text-sm" placeholder="New cost center name" />
				<button type="submit" className="text-sm px-3 py-2 rounded bg-blue-600 text-white hover:bg-blue-700">Add</button>
			</form>
			<ul className="mt-4 divide-y">
				{rows.map(r => (
					<li key={r.id} className="py-2 text-sm flex items-center justify-between">
						<span>{r.name}</span>
					</li>
				))}
			</ul>
		</section>
	)
}
