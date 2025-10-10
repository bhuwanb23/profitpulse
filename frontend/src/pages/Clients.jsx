export default function Clients() {
	return (
		<div className="space-y-6">
			<div className="flex items-center justify-between">
				<h1 className="text-2xl font-semibold">Clients</h1>
				<div className="flex gap-2">
					<input className="w-64 rounded-md border border-gray-300 px-3 py-2 text-sm" placeholder="Search clients..." />
					<button className="bg-blue-600 text-white text-sm px-3 py-2 rounded-md hover:bg-blue-700">+ New Client</button>
				</div>
			</div>

			<div className="bg-white rounded-xl border border-gray-200 p-4 shadow-sm">
				<div className="flex flex-wrap gap-2 mb-3">
					<select className="text-sm border border-gray-300 rounded-md px-2 py-1"><option>All Industries</option></select>
					<select className="text-sm border border-gray-300 rounded-md px-2 py-1"><option>All Contracts</option></select>
					<select className="text-sm border border-gray-300 rounded-md px-2 py-1"><option>Sort by</option></select>
				</div>
				<div className="overflow-x-auto">
					<table className="min-w-full text-sm">
						<thead>
							<tr className="text-left text-gray-500">
								<th className="py-2">Name</th>
								<th className="py-2">Industry</th>
								<th className="py-2">Contract</th>
								<th className="py-2">Revenue</th>
								<th className="py-2">Profitability</th>
								<th className="py-2"></th>
							</tr>
						</thead>
						<tbody className="divide-y">
							{[
								{ name: 'Acme Corp', industry: 'Manufacturing', contract: 'Annual', revenue: '$50,000', profitability: '0.85' },
								{ name: 'TechStart Inc', industry: 'Technology', contract: 'Monthly', revenue: '$5,000', profitability: '0.78' },
							].map((c) => (
								<tr key={c.name}>
									<td className="py-3 font-medium">{c.name}</td>
									<td>{c.industry}</td>
									<td>{c.contract}</td>
									<td>{c.revenue}</td>
									<td>
										<div className="w-36 h-2 bg-gray-100 rounded-full">
											<div className="h-2 bg-green-500 rounded-full" style={{ width: `${parseFloat(c.profitability) * 100}%` }} />
										</div>
									</td>
									<td className="text-right">
										<button className="text-blue-600 hover:underline">View</button>
									</td>
								</tr>
							))}
						</tbody>
					</table>
				</div>
			</div>
		</div>
	)
}
