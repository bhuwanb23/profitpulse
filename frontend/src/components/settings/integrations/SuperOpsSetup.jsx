export default function SuperOpsSetup() {
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">SuperOps Integration</h2>
			<div className="mt-4 grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm">
				<div>
					<label className="text-sm text-gray-600">API Key</label>
					<input className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2" placeholder="sk_..." />
				</div>
				<div>
					<label className="text-sm text-gray-600">Account Domain</label>
					<input className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2" placeholder="example.superops.ai" />
				</div>
			</div>
			<button className="mt-3 text-sm px-3 py-2 rounded bg-blue-600 text-white hover:bg-blue-700 w-max">Connect</button>
		</section>
	)
}
