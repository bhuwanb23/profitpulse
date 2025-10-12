export default function Clients() {
	return (
		<div className="space-y-6">
			<div className="flex items-center justify-between">
				<h1 className="text-2xl font-semibold">Clients</h1>
				<div className="flex gap-2">
					<button className="bg-blue-600 text-white text-sm px-3 py-2 rounded-md hover:bg-blue-700">+ New Client</button>
				</div>
			</div>
			
			{/* Client List Placeholder */}
			<div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
				<h2 className="text-lg font-semibold mb-4">Client Management</h2>
				<div className="space-y-3">
					<div className="flex items-center justify-between p-3 border border-gray-200 rounded-lg">
						<div>
							<h3 className="font-medium">Acme Corporation</h3>
							<p className="text-sm text-gray-500">contact@acme.com</p>
						</div>
						<span className="px-2 py-1 bg-green-100 text-green-700 text-xs rounded">Active</span>
					</div>
					<div className="flex items-center justify-between p-3 border border-gray-200 rounded-lg">
						<div>
							<h3 className="font-medium">TechStart Inc</h3>
							<p className="text-sm text-gray-500">info@techstart.com</p>
						</div>
						<span className="px-2 py-1 bg-green-100 text-green-700 text-xs rounded">Active</span>
					</div>
					<div className="flex items-center justify-between p-3 border border-gray-200 rounded-lg">
						<div>
							<h3 className="font-medium">Global Solutions</h3>
							<p className="text-sm text-gray-500">support@global.com</p>
						</div>
						<span className="px-2 py-1 bg-yellow-100 text-yellow-700 text-xs rounded">Pending</span>
					</div>
				</div>
			</div>
		</div>
	)
}

