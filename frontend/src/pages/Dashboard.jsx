import { useMemo } from 'react'
import RevenueLineChart from '../components/charts/RevenueLineChart'
import QuickActions from '../components/dashboard/QuickActions'

const StatCard = ({ title, value, change, positive }) => (
	<div className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
		<div className="text-sm text-gray-500">{title}</div>
		<div className="mt-2 flex items-end justify-between">
			<div className="text-2xl font-semibold">{value}</div>
			<div className={`text-xs px-2 py-1 rounded-md ${positive ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'}`}>
				{positive ? '▲' : '▼'} {change}
			</div>
		</div>
	</div>
)

export default function Dashboard() {
	const stats = useMemo(() => ([
		{ title: 'Total Revenue', value: '$88,400', change: '12.4%', positive: true },
		{ title: 'Active Clients', value: '42', change: '3.8%', positive: true },
		{ title: 'Open Tickets', value: '17', change: '5.1%', positive: false },
		{ title: 'Profitability', value: '31.2%', change: '1.2%', positive: true },
	]), [])

	const revenueData = useMemo(() => (
		[
			{ label: 'Jan', value: 6400 },
			{ label: 'Feb', value: 7200 },
			{ label: 'Mar', value: 8800 },
			{ label: 'Apr', value: 7600 },
			{ label: 'May', value: 9100 },
			{ label: 'Jun', value: 9800 },
			{ label: 'Jul', value: 10400 },
			{ label: 'Aug', value: 9900 },
			{ label: 'Sep', value: 11200 },
			{ label: 'Oct', value: 12400 },
			{ label: 'Nov', value: 11800 },
			{ label: 'Dec', value: 13100 },
		]
	), [])

	return (
		<div className="space-y-6">
			{/* Title */}
			<div className="flex items-center justify-between">
				<div>
					<h1 className="text-2xl font-semibold">Dashboard</h1>
					<p className="text-gray-500 text-sm">Overview of key metrics and AI insights</p>
				</div>
				<button className="inline-flex items-center gap-2 bg-blue-600 text-white text-sm px-4 py-2 rounded-md hover:bg-blue-700">+ New Report</button>
			</div>

			{/* Stats grid */}
			<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
				{stats.map((s) => (
					<StatCard key={s.title} {...s} />
				))}
			</div>

			{/* Content grid */}
			<div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
				{/* Revenue Trend */}
				<section className="lg:col-span-2 bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
					<div className="flex items-center justify-between">
						<h2 className="font-semibold">Revenue Trend</h2>
						<select className="text-sm border border-gray-300 rounded-md px-2 py-1">
							<option>Last 12 months</option>
							<option>Last 6 months</option>
							<option>Last 30 days</option>
						</select>
					</div>
					<RevenueLineChart data={revenueData} />
				</section>

				{/* AI Recommendations */}
				<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
					<h2 className="font-semibold">AI Recommendations</h2>
					<ul className="mt-3 space-y-3">
						{[
							{ title: 'Increase Help Desk Pricing', impact: 'High', score: 0.85 },
							{ title: 'Add Network Monitoring', impact: 'Medium', score: 0.75 },
							{ title: 'Optimize Software Licenses', impact: 'Low', score: 0.70 },
						].map((rec) => (
							<li key={rec.title} className="flex items-center justify-between p-3 border border-gray-200 rounded-lg hover:bg-gray-50">
								<div>
									<p className="font-medium text-sm">{rec.title}</p>
									<p className="text-xs text-gray-500">Impact: {rec.impact}</p>
								</div>
								<div className="text-xs text-gray-600">Confidence {(rec.score * 100).toFixed(0)}%</div>
							</li>
						))}
					</ul>
				</section>
			</div>

			{/* Quick Actions */}
			<QuickActions />

			{/* Secondary grid */}
			<div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
				<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
					<h2 className="font-semibold">Client Profitability</h2>
					<div className="mt-4 grid grid-cols-4 gap-2">
						{Array.from({ length: 24 }).map((_, i) => (
							<div key={i} className={`aspect-square rounded ${i % 5 === 0 ? 'bg-green-500/70' : i % 3 === 0 ? 'bg-yellow-400/70' : 'bg-red-400/70'}`}></div>
						))}
					</div>
				</section>

				<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
					<h2 className="font-semibold">Recent Tickets</h2>
					<ul className="mt-3 divide-y">
						{[
							{ id: 'TKT-001', title: 'Email server down', status: 'Resolved' },
							{ id: 'TKT-002', title: 'VPN issues', status: 'In Progress' },
							{ id: 'TKT-003', title: 'Software install', status: 'Open' },
						].map((t) => (
							<li key={t.id} className="py-3 flex items-center justify-between">
								<div>
									<p className="font-medium text-sm">{t.title}</p>
									<p className="text-xs text-gray-500">{t.id}</p>
								</div>
								<span className="text-xs px-2 py-1 rounded bg-gray-100">{t.status}</span>
							</li>
						))}
					</ul>
				</section>
			</div>
		</div>
	)
}
