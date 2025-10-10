export default function BackupConfig() {
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Backup Configuration</h2>
			<div className="mt-3 text-sm space-y-2">
				<label className="block">
					<span className="text-sm text-gray-600">Frequency</span>
					<select className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2">
						<option>Daily</option>
						<option>Weekly</option>
						<option>Monthly</option>
					</select>
				</label>
				<label className="block">
					<span className="text-sm text-gray-600">Retention</span>
					<select className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2">
						<option>30 days</option>
						<option>90 days</option>
						<option>1 year</option>
					</select>
				</label>
				<button className="text-sm px-3 py-2 rounded bg-blue-600 text-white hover:bg-blue-700 w-max">Save</button>
			</div>
		</section>
	)
}
