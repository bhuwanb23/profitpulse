export default function IntegrationTesting() {
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Integration Testing Tools</h2>
			<div className="mt-3 grid grid-cols-1 sm:grid-cols-2 gap-3 text-sm">
				<button className="px-3 py-2 rounded bg-gray-100 hover:bg-gray-200 text-left">Test SuperOps Connection</button>
				<button className="px-3 py-2 rounded bg-gray-100 hover:bg-gray-200 text-left">Test QuickBooks Auth</button>
				<button className="px-3 py-2 rounded bg-gray-100 hover:bg-gray-200 text-left">Send Zapier Test Event</button>
			</div>
		</section>
	)
}
