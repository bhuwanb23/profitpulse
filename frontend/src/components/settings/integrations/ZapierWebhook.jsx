export default function ZapierWebhook() {
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Zapier Webhook</h2>
			<div className="mt-3 text-sm">
				<label className="text-sm text-gray-600">Webhook URL</label>
				<input className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2" placeholder="https://hooks.zapier.com/..." />
				<button className="mt-3 text-sm px-3 py-2 rounded bg-blue-600 text-white hover:bg-blue-700 w-max">Save</button>
			</div>
		</section>
	)
}
