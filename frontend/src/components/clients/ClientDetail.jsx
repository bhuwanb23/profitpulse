import { useMemo } from 'react'
import { useParams } from 'react-router-dom'
import { mockClients, mockServices, mockAssignments } from '../../services/mockClients'
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts'

function InfoItem({ label, value }) {
	return (
		<div>
			<div className="text-xs text-gray-500">{label}</div>
			<div className="text-sm font-medium">{value}</div>
		</div>
	)
}

export default function ClientDetail() {
	const { id } = useParams()
	const client = mockClients.find(c => c.id === id)
	const assignments = mockAssignments[id] || []

	const utilizationData = useMemo(() => (
		assignments.map(a => {
			const svc = mockServices.find(s => s.id === a.serviceId)
			return { service: svc?.name || a.serviceId, quantity: a.quantity }
		})
	), [assignments])

	if (!client) return <div className="text-sm text-gray-500">Client not found.</div>

	return (
		<div className="space-y-6">
			<div className="flex items-center justify-between">
				<h1 className="text-2xl font-semibold">{client.name}</h1>
				<span className="text-sm px-3 py-1 rounded bg-gray-100">{client.industry}</span>
			</div>

			{/* Top cards */}
			<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
				<div className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
					<div className="text-sm text-gray-500">Profitability</div>
					<div className="mt-2">
						<div className="w-full h-3 bg-gray-100 rounded-full">
							<div className="h-3 bg-emerald-500 rounded-full" style={{ width: `${client.profitability * 100}%` }} />
						</div>
						<div className="text-xs text-gray-500 mt-1">{Math.round(client.profitability * 100)}%</div>
					</div>
				</div>
				<div className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
					<div className="text-sm text-gray-500">MRR</div>
					<div className="mt-2 text-2xl font-semibold">${client.mrr.toLocaleString()}</div>
				</div>
				<div className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
					<div className="text-sm text-gray-500">Open Tickets</div>
					<div className="mt-2 text-2xl font-semibold">{client.ticketsOpen}</div>
				</div>
				<div className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
					<div className="text-sm text-gray-500">Contract Value</div>
					<div className="mt-2 text-2xl font-semibold">${client.contractValue.toLocaleString()}</div>
				</div>
			</div>

			{/* Contract and metrics */}
			<div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
				<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm lg:col-span-2">
					<h2 className="font-semibold">Service Utilization</h2>
					<div className="mt-4 h-72">
						<ResponsiveContainer width="100%" height="100%">
							<BarChart data={utilizationData} margin={{ top: 10, right: 16, bottom: 0, left: 0 }}>
								<CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
								<XAxis dataKey="service" stroke="#9ca3af" />
								<YAxis stroke="#9ca3af" />
								<Tooltip />
								<Bar dataKey="quantity" fill="#3b82f6" radius={[6,6,0,0]} />
							</BarChart>
						</ResponsiveContainer>
					</div>
				</section>

				<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
					<h2 className="font-semibold">Contract</h2>
					<div className="mt-4 grid grid-cols-2 gap-4 text-sm">
						<InfoItem label="Type" value={client.contract} />
						<InfoItem label="Value" value={`$${client.contractValue.toLocaleString()}`} />
						<InfoItem label="Start" value={client.startDate} />
						<InfoItem label="End" value={client.endDate || 'N/A'} />
					</div>
				</section>
			</div>

			{/* Performance */}
			<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
				<h2 className="font-semibold">Performance Metrics</h2>
				<div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
					<InfoItem label="Avg. Resolution Time" value="3.2h" />
					<InfoItem label="SLA Compliance" value="98%" />
					<InfoItem label="Monthly Tickets" value="14" />
					<InfoItem label="CSAT" value="4.6/5" />
				</div>
			</section>
		</div>
	)
}
