export default function ReportScheduler() {
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Scheduled Reports</h2>
			<div className="mt-3 grid grid-cols-1 sm:grid-cols-3 gap-3 text-sm">
				<label className="block">
					<span className="text-gray-600">Frequency</span>
					<select className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2">
						<option>Daily</option>
						<option>Weekly</option>
						<option>Monthly</option>
					</select>
				</label>
				<label className="block">
					<span className="text-gray-600">Recipients</span>
					<input className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2" placeholder="email1@example.com, email2@example.com" />
				</label>
				<div className="flex items-end">
					<button className="w-full px-3 py-2 rounded bg-blue-600 text-white hover:bg-blue-700">Schedule</button>
				</div>
			</div>
		</section>
	)
}
