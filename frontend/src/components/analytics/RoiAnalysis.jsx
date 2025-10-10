import { useMemo } from 'react'

export default function RoiAnalysis() {
	const metrics = useMemo(() => ({ investment: 25000, returns: 37000 }), [])
	const roi = Math.round(((metrics.returns - metrics.investment) / metrics.investment) * 100)

	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">ROI Analysis</h2>
			<div className="mt-4">
				<div className="flex items-center justify-between text-sm">
					<span className="text-gray-600">ROI</span>
					<span className="font-medium">{roi}%</span>
				</div>
				<div className="mt-2 h-3 w-full bg-gray-100 rounded-full">
					<div className="h-3 bg-emerald-500 rounded-full" style={{ width: `${Math.min(Math.max(roi, 0), 100)}%` }} />
				</div>
				<div className="mt-4 grid grid-cols-2 gap-4 text-sm">
					<div className="p-3 border border-gray-200 rounded-lg">
						<div className="text-gray-500">Investment</div>
						<div className="font-medium">${metrics.investment.toLocaleString()}</div>
					</div>
					<div className="p-3 border border-gray-200 rounded-lg">
						<div className="text-gray-500">Returns</div>
						<div className="font-medium">${metrics.returns.toLocaleString()}</div>
					</div>
				</div>
			</div>
		</section>
	)
}
