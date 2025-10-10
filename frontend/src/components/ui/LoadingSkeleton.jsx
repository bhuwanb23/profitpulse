export function CardSkeleton() {
	return (
		<div className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm animate-pulse">
			<div className="h-3 w-28 bg-gray-200 rounded" />
			<div className="mt-3 h-6 w-20 bg-gray-200 rounded" />
		</div>
	)
}

export function SectionSkeleton({ rows = 6 }) {
	return (
		<div className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm animate-pulse">
			<div className="h-4 w-40 bg-gray-200 rounded" />
			<div className="mt-4 space-y-2">
				{Array.from({ length: rows }).map((_, i) => (
					<div key={i} className="h-3 w-full bg-gray-100 rounded" />
				))}
			</div>
		</div>
	)
}
