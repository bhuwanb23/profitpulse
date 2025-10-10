import { useMemo } from 'react'

export default function ExpenseTracking() {
	const rows = useMemo(() => (
		[
			{ date: '2024-01-15', category: 'Software', vendor: 'Microsoft', amount: 3000 },
			{ date: '2024-02-15', category: 'Equipment', vendor: 'Dell', amount: 12000 },
			{ date: '2024-03-10', category: 'Software', vendor: 'Vendor', amount: 2000 },
		]
	), [])
	const total = rows.reduce((s, r) => s + r.amount, 0)
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Expense Tracking</h2>
			<div className="mt-3 overflow-x-auto">
				<table className="min-w-full text-sm">
					<thead>
						<tr className="text-left text-gray-500">
							<th className="py-2">Date</th>
							<th className="py-2">Category</th>
							<th className="py-2">Vendor</th>
							<th className="py-2 text-right">Amount</th>
						</tr>
					</thead>
					<tbody className="divide-y">
						{rows.map((r, i) => (
							<tr key={i}>
								<td className="py-2">{r.date}</td>
								<td>{r.category}</td>
								<td>{r.vendor}</td>
								<td className="text-right">${r.amount.toLocaleString()}</td>
							</tr>
						))}
					</tbody>
					<tfoot>
						<tr>
							<td colSpan={3} className="py-2 font-medium">Total</td>
							<td className="text-right font-medium">${total.toLocaleString()}</td>
						</tr>
					</tfoot>
				</table>
			</div>
		</section>
	)
}
