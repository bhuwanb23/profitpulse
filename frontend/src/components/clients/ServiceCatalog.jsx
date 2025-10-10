import { useMemo, useState } from 'react'
import { mockServices } from '../../services/mockClients'

export default function ServiceCatalog() {
	const [q, setQ] = useState('')
	const [cat, setCat] = useState('all')
	const cats = useMemo(() => ['all', ...Array.from(new Set(mockServices.map(s => s.category)))], [])
	const list = useMemo(() => (
		mockServices.filter(s => (q ? s.name.toLowerCase().includes(q.toLowerCase()) : true) && (cat === 'all' || s.category === cat))
	), [q, cat])

	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Service Catalog</h2>
			<div className="mt-3 flex flex-wrap gap-2 items-center">
				<input className="w-64 rounded-md border border-gray-300 px-3 py-2 text-sm" placeholder="Search services…" value={q} onChange={(e) => setQ(e.target.value)} />
				<select className="text-sm border border-gray-300 rounded-md px-2 py-1" value={cat} onChange={(e) => setCat(e.target.value)}>
					{cats.map(c => <option key={c} value={c}>{c}</option>)}
				</select>
			</div>
			<div className="mt-4 grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
				{list.map(s => (
					<div key={s.id} className="border border-gray-200 rounded-lg p-4">
						<div className="font-medium">{s.name}</div>
						<div className="text-xs text-gray-500">{s.category} • {s.billing}</div>
						<div className="mt-2 text-sm"><span className="text-gray-500">Base:</span> ${s.basePrice}</div>
						<button className="mt-3 text-xs px-3 py-1.5 rounded bg-blue-600 text-white hover:bg-blue-700">Add to client</button>
					</div>
				))}
			</div>
		</section>
	)
}
