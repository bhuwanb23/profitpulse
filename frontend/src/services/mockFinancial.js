export const mockInvoices = [
	{ id: 'INV-2024-001', client: 'Acme Corp', date: '2024-01-31', due: '2024-02-15', subtotal: 8000, tax: 800, total: 8800, status: 'paid', method: 'card', paidAt: '2024-02-12' },
	{ id: 'INV-2024-002', client: 'TechStart Inc', date: '2024-02-28', due: '2024-03-15', subtotal: 1500, tax: 150, total: 1650, status: 'sent', method: 'bank', paidAt: null },
	{ id: 'INV-2024-003', client: 'RetailMax', date: '2024-03-31', due: '2024-04-15', subtotal: 6400, tax: 640, total: 7040, status: 'overdue', method: 'card', paidAt: null },
	{ id: 'INV-2024-004', client: 'HealthCare Plus', date: '2024-03-31', due: '2024-04-15', subtotal: 4650, tax: 465, total: 5115, status: 'sent', method: 'bank', paidAt: null },
	{ id: 'INV-2024-005', client: 'FinanceFirst', date: '2024-03-31', due: '2024-04-15', subtotal: 3400, tax: 340, total: 3740, status: 'paid', method: 'card', paidAt: '2024-04-12' },
]

export const mockInvoiceItems = {
	'INV-2024-001': [ { desc: 'Help Desk - 25 users', qty: 1, price: 3500 }, { desc: 'Monitoring - 50 devices', qty: 1, price: 9000 }, { desc: 'Emergency Support', qty: 1, price: 312.5 } ],
	'INV-2024-002': [ { desc: 'Help Desk - 10 users', qty: 1, price: 1500 } ],
	'INV-2024-003': [ { desc: 'Help Desk - 40 users', qty: 1, price: 6400 } ],
	'INV-2024-004': [ { desc: 'Help Desk - 30 users', qty: 1, price: 4650 } ],
	'INV-2024-005': [ { desc: 'Help Desk - 20 users', qty: 1, price: 3400 } ],
}

export const mockBudgets = [
	{ id: 'BUD-2024-Q1', name: 'Q1 2024 Operations', type: 'quarterly', total: 100000, spent: 75000, start: '2024-01-01', end: '2024-03-31' },
	{ id: 'BUD-2024-ANN', name: 'Annual Equipment', type: 'annual', total: 50000, spent: 15000, start: '2024-01-01', end: '2024-12-31' },
]

export const mockBudgetCategories = {
	'BUD-2024-Q1': [ { name: 'Personnel', alloc: 60000, spent: 45000 }, { name: 'Equipment', alloc: 25000, spent: 18000 }, { name: 'Software', alloc: 15000, spent: 12000 } ],
	'BUD-2024-ANN': [ { name: 'Hardware', alloc: 30000, spent: 8000 }, { name: 'Software', alloc: 20000, spent: 7000 } ],
}

export const mockExpenses = [
	{ id: 'EXP-001', budget: 'BUD-2024-Q1', category: 'Personnel', date: '2024-01-31', amount: 15000, vendor: 'Payroll' },
	{ id: 'EXP-002', budget: 'BUD-2024-Q1', category: 'Equipment', date: '2024-02-15', amount: 12000, vendor: 'Dell' },
	{ id: 'EXP-003', budget: 'BUD-2024-Q1', category: 'Software', date: '2024-01-15', amount: 3000, vendor: 'Microsoft' },
	{ id: 'EXP-004', budget: 'BUD-2024-ANN', category: 'Hardware', date: '2024-02-10', amount: 8000, vendor: 'Dell' },
]

export const mockCostCenters = [
	{ id: 'CC-OPS', name: 'Operations' },
	{ id: 'CC-SUP', name: 'Support' },
	{ id: 'CC-ENG', name: 'Engineering' },
]
