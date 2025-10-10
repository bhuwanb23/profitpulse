export default function ComparativeAnalysis() {
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Comparative Analysis</h2>
			<div className="mt-3 grid grid-cols-2 gap-3 text-sm">
				<div className="p-3 border rounded">
					<div className="text-gray-500">This Month</div>
					<div className="mt-1">Revenue: $124k</div>
					<div>Tickets: 482</div>
					<div>Profitability: 17.2%</div>
				</div>
				<div className="p-3 border rounded">
					<div className="text-gray-500">Last Month</div>
					<div className="mt-1">Revenue: $116k</div>
					<div>Tickets: 505</div>
					<div>Profitability: 15.8%</div>
				</div>
			</div>
		</section>
	)
}
