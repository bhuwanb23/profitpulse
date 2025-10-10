export default function ProfitabilityGenome() {
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Profitability Genome</h2>
			<div className="mt-3 grid grid-cols-3 gap-2 text-[10px]">
				<div className="h-16 bg-emerald-100 rounded flex items-center justify-center">Labor</div>
				<div className="h-16 bg-blue-100 rounded flex items-center justify-center">Services</div>
				<div className="h-16 bg-amber-100 rounded flex items-center justify-center">Pricing</div>
				<div className="h-16 bg-rose-100 rounded flex items-center justify-center">Tickets</div>
				<div className="h-16 bg-indigo-100 rounded flex items-center justify-center">Projects</div>
				<div className="h-16 bg-cyan-100 rounded flex items-center justify-center">SaaS</div>
			</div>
		</section>
	)
}
