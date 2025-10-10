export default function MarketInsights() {
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Market Insights</h2>
			<div className="mt-3 grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
				<div className="p-3 border rounded-lg">
					<h3 className="text-sm font-medium">Market Analysis</h3>
					<ul className="mt-2 text-gray-700 space-y-1">
						<li>SMB security services CAGR: 13-15%</li>
						<li>Cloud backup adoption: +9% YoY</li>
						<li>Managed detection demand: rising Q/Q</li>
					</ul>
				</div>
				<div className="p-3 border rounded-lg">
					<h3 className="text-sm font-medium">Competitive Intelligence</h3>
					<ul className="mt-2 text-gray-700 space-y-1">
						<li>Competitor A: bundles MDR + NDR at aggressive pricing</li>
						<li>Competitor B: focuses on vCISO add‑ons</li>
						<li>Competitor C: heavy automation reducing ticket MTTR</li>
					</ul>
				</div>
			</div>
		</section>
	)
}
