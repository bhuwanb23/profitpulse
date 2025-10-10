export default function Invoices() {
	return (
		<div className="space-y-6">
			<div className="flex items-center justify-between">
				<h1 className="text-2xl font-semibold">Invoices</h1>
				<div className="flex gap-2">
					<select className="text-sm border border-gray-300 rounded-md px-2 py-1"><option>All Statuses</option></select>
					<select className="text-sm border border-gray-300 rounded-md px-2 py-1"><option>All Periods</option></select>
					<button className="bg-blue-600 text-white text-sm px-3 py-2 rounded-md hover:bg-blue-700">+ Create Invoice</button>
				</div>
			</div>

			<div className="bg-white rounded-xl border border-gray-200 p-4 shadow-sm">
				<div className="overflow-x-auto">
					<table className="min-w-full text-sm">
						<thead>
							<tr className="text-left text-gray-500">
								<th className="py-2">Invoice</th>
								<th className="py-2">Client</th>
								<th className="py-2">Date</th>
								<th className="py-2">Total</th>
								<th className="py-2">Status</th>
								<th className="py-2"></th>
							</tr>
						</thead>
						<tbody className="divide-y">
							{[
								{ no: 'INV-2024-001', client: 'Acme Corp', date: '2024-01-31', total: '$8,800', status: 'Paid' },
								{ no: 'INV-2024-002', client: 'TechStart Inc', date: '2024-02-28', total: '$1,650', status: 'Sent' },
								{ no: 'INV-2024-003', client: 'RetailMax', date: '2024-03-31', total: '$7,040', status: 'Overdue' },
							].map((i) => (
								<tr key={i.no}>
									<td className="py-3 font-medium">{i.no}</td>
									<td>{i.client}</td>
									<td>{i.date}</td>
									<td>{i.total}</td>
									<td>
										<span className={`text-xs px-2 py-1 rounded ${i.status === 'Paid' ? 'bg-green-50 text-green-700' : i.status === 'Overdue' ? 'bg-red-50 text-red-700' : 'bg-gray-100'}`}>{i.status}</span>
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
