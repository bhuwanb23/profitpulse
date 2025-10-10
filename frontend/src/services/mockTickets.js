export const mockTechnicians = [
	{ id: 'u1', name: 'John Admin' },
	{ id: 'u2', name: 'Sarah Finance' },
	{ id: 'u3', name: 'Mike Ops' },
]

export const mockTicketCategories = ['infrastructure', 'network', 'software', 'security', 'database']

export const mockTickets = [
	{ id: 'TKT-001', title: 'Email server down', priority: 'high', status: 'resolved', category: 'infrastructure', client: 'Acme Corp', createdAt: '2024-01-15', assignedTo: 'u3', timeSpent: 2.5, description: 'Exchange server is not responding' },
	{ id: 'TKT-002', title: 'VPN connection issues', priority: 'medium', status: 'in_progress', category: 'network', client: 'TechStart Inc', createdAt: '2024-02-10', assignedTo: 'u3', timeSpent: 1.0, description: 'Users cannot connect to VPN' },
	{ id: 'TKT-003', title: 'Software installation', priority: 'low', status: 'open', category: 'software', client: 'RetailMax', createdAt: '2024-03-05', assignedTo: null, timeSpent: 0.0, description: 'Need to install new accounting software' },
	{ id: 'TKT-004', title: 'Security patch required', priority: 'high', status: 'resolved', category: 'security', client: 'HealthCare Plus', createdAt: '2024-03-12', assignedTo: 'u3', timeSpent: 1.5, description: 'Critical security update needed' },
	{ id: 'TKT-005', title: 'Database optimization', priority: 'medium', status: 'in_progress', category: 'database', client: 'FinanceFirst', createdAt: '2024-03-20', assignedTo: 'u3', timeSpent: 3.0, description: 'Database performance issues' },
]

export const mockTimeEntries = {
	'TKT-001': [ { at: '2024-01-15 10:00', technician: 'u3', hours: 2.5, note: 'Diagnosed and restarted services' } ],
	'TKT-002': [ { at: '2024-02-10 12:00', technician: 'u3', hours: 1.0, note: 'Fixed firewall rule' } ],
	'TKT-003': [],
	'TKT-004': [ { at: '2024-03-12 09:30', technician: 'u3', hours: 1.5, note: 'Applied patch, verified' } ],
	'TKT-005': [ { at: '2024-03-20 11:00', technician: 'u3', hours: 2.0, note: 'Index tuning' }, { at: '2024-03-21 14:00', technician: 'u3', hours: 1.0, note: 'Monitoring' } ],
}
