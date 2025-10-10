export const mockClients = [
	{ id: 'c1', name: 'Acme Corp', industry: 'Manufacturing', contract: 'Annual', contractValue: 50000, startDate: '2024-01-01', endDate: '2024-12-31', profitability: 0.85, mrr: 4200, ticketsOpen: 2 },
	{ id: 'c2', name: 'TechStart Inc', industry: 'Technology', contract: 'Monthly', contractValue: 5000, startDate: '2024-03-01', endDate: null, profitability: 0.78, mrr: 5000, ticketsOpen: 3 },
	{ id: 'c3', name: 'RetailMax', industry: 'Retail', contract: 'Annual', contractValue: 75000, startDate: '2024-01-15', endDate: '2024-12-15', profitability: 0.62, mrr: 6250, ticketsOpen: 4 },
	{ id: 'c4', name: 'HealthCare Plus', industry: 'Healthcare', contract: 'Annual', contractValue: 60000, startDate: '2024-02-01', endDate: '2025-01-31', profitability: 0.80, mrr: 5000, ticketsOpen: 1 },
	{ id: 'c5', name: 'FinanceFirst', industry: 'Finance', contract: 'Monthly', contractValue: 8000, startDate: '2024-01-01', endDate: null, profitability: 0.74, mrr: 8000, ticketsOpen: 2 },
]

export const mockServices = [
	{ id: 's1', name: '24/7 Help Desk', category: 'support', basePrice: 150, billing: 'per-user' },
	{ id: 's2', name: 'Network Monitoring', category: 'maintenance', basePrice: 200, billing: 'per-device' },
	{ id: 's3', name: 'Cloud Migration', category: 'consulting', basePrice: 125, billing: 'hourly' },
	{ id: 's4', name: 'Security Assessment', category: 'consulting', basePrice: 200, billing: 'hourly' },
	{ id: 's5', name: 'Backup & Recovery', category: 'maintenance', basePrice: 50, billing: 'per-device' },
]

export const mockAssignments = {
	c1: [ { serviceId: 's1', customPrice: 140, quantity: 25, frequency: 'monthly' }, { serviceId: 's2', customPrice: 180, quantity: 50, frequency: 'monthly' } ],
	c2: [ { serviceId: 's1', customPrice: 150, quantity: 10, frequency: 'monthly' } ],
	c3: [ { serviceId: 's1', customPrice: 160, quantity: 40, frequency: 'monthly' }, { serviceId: 's4', customPrice: 200, quantity: 1, frequency: 'annually' } ],
	c4: [ { serviceId: 's1', customPrice: 155, quantity: 30, frequency: 'monthly' }, { serviceId: 's2', customPrice: 190, quantity: 60, frequency: 'monthly' } ],
	c5: [ { serviceId: 's1', customPrice: 170, quantity: 20, frequency: 'monthly' }, { serviceId: 's3', customPrice: 130, quantity: 1, frequency: 'hourly' } ],
}
