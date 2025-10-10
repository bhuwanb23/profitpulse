import { useMemo } from 'react'
import { mockInvoices } from '../../../services/mockFinancial'

export default function OutstandingPayments() {
	const rows = useMemo(() => (
		mockInvoices.filter(i => i.status === 'sent' || i.status === 'overdue')
	), [])
	const totalOutstanding = rows.reduce((s, r) => s + r.total, 0)
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Outstanding Payments</h2>
			<div className="mt-3 overflow-x-auto">
				<table className="min-w-full text-sm">
					<thead>
						<tr className="text-left text-gray-500">
							<th className="py-2">Invoice</th>
							<th className="py-2">Client</th>
							<th className="py-2">Due</th>
							<th className="py-2 text-right">Amount Due</th>
						</tr>
					</thead>
					<tbody className="divide-y">
						{rows.map(r => (
							<tr key={r.id}>
								<td className="py-2 font-medium">{r.id}</td>
								<td>{r.client}</td>
								<td>{r.due}</td>
								<td className="text-right">${r.total.toLocaleString()}</td>
							</tr>
						))}
					</tbody>
					<tfoot>
						<tr>
							<td colSpan={3} className="py-2 font-medium">Total Outstanding</td>
							<td className="text-right font-medium">${totalOutstanding.toLocaleString()}</td>
						</tr>
					</tfoot>
				</table>
			</div>
		</section>
	)
}
