export default function ThresholdMonitoring() {
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Threshold Monitoring</h2>
			<div className="mt-3 grid grid-cols-1 sm:grid-cols-3 gap-3 text-sm">
				<label className="block">
					<span className="text-gray-600">SLA Breach %</span>
					<input className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2" defaultValue="5" />
				</label>
				<label className="block">
					<span className="text-gray-600">Outstanding Payments ($)</span>
					<input className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2" defaultValue="10000" />
				</label>
				<label className="block">
					<span className="text-gray-600">Backlog Tickets</span>
					<input className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2" defaultValue="50" />
				</label>
			</div>
			<button className="mt-3 text-sm px-3 py-2 rounded bg-blue-600 text-white hover:bg-blue-700 w-max">Save</button>
		</section>
	)
}
