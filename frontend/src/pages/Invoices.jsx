export default function Invoices() {
	return (
		<div className="space-y-6">
			<div className="flex items-center justify-between">
				<h1 className="text-2xl font-semibold">Invoices</h1>
				<button className="bg-blue-600 text-white text-sm px-3 py-2 rounded-md hover:bg-blue-700">+ New Invoice</button>
			</div>
			
			{/* Invoice List Placeholder */}
			<div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
				<h2 className="text-lg font-semibold mb-4">Invoice Management</h2>
				<div className="space-y-3">
					<div className="flex items-center justify-between p-3 border border-gray-200 rounded-lg">
						<div>
							<h3 className="font-medium">INV-001</h3>
							<p className="text-sm text-gray-500">Acme Corporation • $2,500</p>
						</div>
						<span className="px-2 py-1 bg-green-100 text-green-700 text-xs rounded">Paid</span>
					</div>
					<div className="flex items-center justify-between p-3 border border-gray-200 rounded-lg">
						<div>
							<h3 className="font-medium">INV-002</h3>
							<p className="text-sm text-gray-500">TechStart Inc • $1,800</p>
						</div>
						<span className="px-2 py-1 bg-yellow-100 text-yellow-700 text-xs rounded">Pending</span>
					</div>
					<div className="flex items-center justify-between p-3 border border-gray-200 rounded-lg">
						<div>
							<h3 className="font-medium">INV-003</h3>
							<p className="text-sm text-gray-500">Global Solutions • $3,200</p>
						</div>
						<span className="px-2 py-1 bg-red-100 text-red-700 text-xs rounded">Overdue</span>
					</div>
				</div>
			</div>
		</div>
	)
}
