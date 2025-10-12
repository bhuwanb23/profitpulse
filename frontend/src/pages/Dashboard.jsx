import { useMemo } from 'react'
// import RevenueLineChart from '../components/charts/RevenueLineChart'
// import QuickActions from '../components/dashboard/QuickActions'

const StatCard = ({ title, value, change, positive }) => (
	<div style={{ backgroundColor: 'white', borderRadius: '12px', border: '1px solid #e5e7eb', padding: '20px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)', marginBottom: '16px' }}>
		<div style={{ fontSize: '14px', color: '#6b7280', marginBottom: '8px' }}>{title}</div>
		<div style={{ display: 'flex', alignItems: 'flex-end', justifyContent: 'space-between' }}>
			<div style={{ fontSize: '24px', fontWeight: '600' }}>{value}</div>
			<div style={{ 
				fontSize: '12px', 
				padding: '4px 8px', 
				borderRadius: '6px', 
				backgroundColor: positive ? '#dcfce7' : '#fef2f2', 
				color: positive ? '#166534' : '#dc2626' 
			}}>
				{positive ? '▲' : '▼'} {change}
			</div>
		</div>
	</div>
)

export default function Dashboard() {
	console.log('Dashboard component is rendering!')
	console.log('Dashboard: Current URL =', window.location.href)
	
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
		<div style={{ padding: '20px', backgroundColor: '#f0f0f0' }}>
			{/* Test Message */}
			<div style={{ backgroundColor: '#d4edda', border: '1px solid #c3e6cb', color: '#155724', padding: '12px', borderRadius: '4px', marginBottom: '20px' }}>
				✅ Dashboard is working! You are logged in successfully.
			</div>
			
			{/* Title */}
			<div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
				<div>
					<h1 style={{ fontSize: '24px', fontWeight: '600', margin: '0 0 8px 0' }}>Dashboard</h1>
					<p style={{ color: '#666', fontSize: '14px', margin: '0' }}>Overview of key metrics and AI insights</p>
				</div>
				<button style={{ backgroundColor: '#2563eb', color: 'white', padding: '8px 16px', borderRadius: '6px', border: 'none', cursor: 'pointer' }}>+ New Report</button>
			</div>

			{/* Stats grid */}
			<div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '16px', marginBottom: '24px' }}>
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
					{/* <RevenueLineChart data={revenueData} /> */}
					<div className="mt-4 h-64 bg-gray-100 rounded flex items-center justify-center">
						<p className="text-gray-500">Revenue Chart Placeholder</p>
					</div>
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
			{/* <QuickActions /> */}
			<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
				<h2 className="font-semibold mb-3">Quick Actions</h2>
				<div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-3">
					<div className="flex items-start gap-3 rounded-xl border border-gray-200 bg-white p-4 shadow-sm hover:shadow transition">
						<div className="h-10 w-10 flex items-center justify-center rounded-lg bg-blue-50 text-blue-700 text-lg">🎫</div>
						<div className="text-left">
							<div className="font-medium text-sm">New Ticket</div>
							<div className="text-xs text-gray-500">Create a support ticket</div>
						</div>
					</div>
					<div className="flex items-start gap-3 rounded-xl border border-gray-200 bg-white p-4 shadow-sm hover:shadow transition">
						<div className="h-10 w-10 flex items-center justify-center rounded-lg bg-green-50 text-green-700 text-lg">👤</div>
						<div className="text-left">
							<div className="font-medium text-sm">Add Client</div>
							<div className="text-xs text-gray-500">Create a new client</div>
						</div>
					</div>
					<div className="flex items-start gap-3 rounded-xl border border-gray-200 bg-white p-4 shadow-sm hover:shadow transition">
						<div className="h-10 w-10 flex items-center justify-center rounded-lg bg-amber-50 text-amber-700 text-lg">💵</div>
						<div className="text-left">
							<div className="font-medium text-sm">Create Invoice</div>
							<div className="text-xs text-gray-500">Bill for services</div>
						</div>
					</div>
					<div className="flex items-start gap-3 rounded-xl border border-gray-200 bg-white p-4 shadow-sm hover:shadow transition">
						<div className="h-10 w-10 flex items-center justify-center rounded-lg bg-purple-50 text-purple-700 text-lg">⬆️</div>
						<div className="text-left">
							<div className="font-medium text-sm">Import CSV</div>
							<div className="text-xs text-gray-500">Upload data file</div>
						</div>
					</div>
				</div>
			</section>

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
