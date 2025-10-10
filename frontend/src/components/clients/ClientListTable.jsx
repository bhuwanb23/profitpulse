import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { mockClients } from '../../services/mockClients'

export default function ClientListTable() {
	const [query, setQuery] = useState('')
	const [industry, setIndustry] = useState('all')
	const [contract, setContract] = useState('all')

	const industries = useMemo(() => ['all', ...Array.from(new Set(mockClients.map(c => c.industry)))], [])

	const filtered = useMemo(() => {
		return mockClients.filter(c => {
			const matchesQuery = c.name.toLowerCase().includes(query.toLowerCase())
			const matchesIndustry = industry === 'all' || c.industry === industry
			const matchesContract = contract === 'all' || c.contract.toLowerCase() === contract
			return matchesQuery && matchesIndustry && matchesContract
		})
	}, [query, industry, contract])

	return (
		<div className="bg-white rounded-xl border border-gray-200 p-4 shadow-sm">
			<div className="flex flex-wrap gap-2 mb-3 items-center">
				<input className="w-64 rounded-md border border-gray-300 px-3 py-2 text-sm" placeholder="Search clients…" value={query} onChange={(e) => setQuery(e.target.value)} />
				<select className="text-sm border border-gray-300 rounded-md px-2 py-1" value={industry} onChange={(e) => setIndustry(e.target.value)}>
					{industries.map(i => <option key={i} value={i}>{i.charAt(0).toUpperCase() + i.slice(1)}</option>)}
				</select>
				<select className="text-sm border border-gray-300 rounded-md px-2 py-1" value={contract} onChange={(e) => setContract(e.target.value)}>
					<option value="all">All contracts</option>
					<option value="monthly">Monthly</option>
					<option value="annual">Annual</option>
				</select>
			</div>
			<div className="overflow-x-auto">
				<table className="min-w-full text-sm">
					<thead>
						<tr className="text-left text-gray-500">
							<th className="py-2">Client</th>
							<th className="py-2">Industry</th>
							<th className="py-2">Contract</th>
							<th className="py-2">MRR</th>
							<th className="py-2">Profitability</th>
							<th className="py-2">Open Tickets</th>
							<th className="py-2"></th>
						</tr>
					</thead>
					<tbody className="divide-y">
						{filtered.map((c) => (
							<tr key={c.id}>
								<td className="py-3 font-medium">{c.name}</td>
								<td>{c.industry}</td>
								<td>{c.contract}</td>
								<td>${c.mrr.toLocaleString()}</td>
								<td>
									<div className="w-36 h-2 bg-gray-100 rounded-full">
										<div className="h-2 bg-green-500 rounded-full" style={{ width: `${c.profitability * 100}%` }} />
									</div>
								</td>
								<td>{c.ticketsOpen}</td>
								<td className="text-right">
									<Link to={`/clients/${c.id}`} className="text-blue-600 hover:underline">View</Link>
								</td>
							</tr>
						))}
					</tbody>
				</table>
			</div>
		</div>
	)
}
