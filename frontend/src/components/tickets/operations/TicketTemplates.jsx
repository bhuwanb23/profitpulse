const templates = [
	{ id: 'tmp1', name: 'Onboarding - New User', title: 'New user onboarding', category: 'software', priority: 'medium', description: 'Create account, assign licenses, setup email' },
	{ id: 'tmp2', name: 'Incident - Security', title: 'Security incident investigation', category: 'security', priority: 'high', description: 'Investigate and mitigate security incident' },
	{ id: 'tmp3', name: 'Maintenance - Server', title: 'Server maintenance window', category: 'infrastructure', priority: 'low', description: 'Apply updates and reboot during maintenance window' },
]

export default function TicketTemplates() {
	const quickCreate = (t) => {
		console.log('Create from template', t)
		alert(`Ticket created from template '${t.name}' (mock).`)
	}
	return (
		<section className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
			<h2 className="font-semibold">Ticket Templates</h2>
			<div className="mt-4 grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
				{templates.map(t => (
					<div key={t.id} className="border border-gray-200 rounded-lg p-4">
						<div className="font-medium">{t.name}</div>
						<div className="text-xs text-gray-500">{t.category} • {t.priority}</div>
						<p className="mt-2 text-sm text-gray-700 min-h-[48px]">{t.description}</p>
						<button onClick={() => quickCreate(t)} className="mt-3 text-xs px-3 py-1.5 rounded bg-blue-600 text-white hover:bg-blue-700">Create</button>
					</div>
				))}
			</div>
		</section>
	)
}
