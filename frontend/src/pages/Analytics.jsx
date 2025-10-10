export default function Analytics() {
	return (
		<div className="space-y-6">
			<div className="flex items-center justify-between">
				<h1 className="text-2xl font-semibold">Analytics</h1>
				<div className="flex gap-2">
					<select className="text-sm border border-gray-300 rounded-md px-2 py-1"><option>Last 12 months</option></select>
					<button className="bg-blue-600 text-white text-sm px-3 py-2 rounded-md hover:bg-blue-700">Export</button>
				</div>
			</div>

			<div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
				<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
					<h2 className="font-semibold">Revenue Analytics</h2>
					<div className="mt-4 h-64 grid place-items-center text-gray-400 text-sm bg-[repeating-linear-gradient(0deg,#f9fafb, #f9fafb_12px, #f3f4f6_12px, #f3f4f6_24px)] rounded-lg">Chart placeholder</div>
				</section>
				<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
					<h2 className="font-semibold">Profitability Analysis</h2>
					<div className="mt-4 h-64 grid place-items-center text-gray-400 text-sm bg-[repeating-linear-gradient(0deg,#f9fafb, #f9fafb_12px, #f3f4f6_12px, #f3f4f6_24px)] rounded-lg">Chart placeholder</div>
				</section>
				<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm lg:col-span-2">
					<h2 className="font-semibold">Budget Utilization</h2>
					<div className="mt-4 h-64 grid place-items-center text-gray-400 text-sm bg-[repeating-linear-gradient(0deg,#f9fafb, #f9fafb_12px, #f3f4f6_12px, #f3f4f6_24px)] rounded-lg">Chart placeholder</div>
				</section>
			</div>
		</div>
	)
}
