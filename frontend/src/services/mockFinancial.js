export const mockInvoices = [
	{ 
		id: 'INV-2024-001', 
		client: 'Acme Corp', 
		clientId: 'client-1',
		date: '2024-01-31', 
		due: '2024-02-15', 
		subtotal: 8000, 
		tax: 800, 
		total: 8800, 
		status: 'paid', 
		method: 'credit_card', 
		paidAt: '2024-02-12',
		currency: 'USD',
		notes: 'Monthly IT support services',
		tags: ['recurring', 'support'],
		priority: 'normal',
		createdBy: 'John Smith',
		lastModified: '2024-02-12T10:30:00Z',
		paymentTerms: 'Net 15',
		discount: 0,
		discountType: 'percentage'
	},
	{ 
		id: 'INV-2024-002', 
		client: 'TechStart Inc', 
		clientId: 'client-2',
		date: '2024-02-28', 
		due: '2024-03-15', 
		subtotal: 1500, 
		tax: 150, 
		total: 1650, 
		status: 'sent', 
		method: 'bank_transfer', 
		paidAt: null,
		currency: 'USD',
		notes: 'Setup and configuration services',
		tags: ['one-time', 'setup'],
		priority: 'normal',
		createdBy: 'Sarah Johnson',
		lastModified: '2024-02-28T14:20:00Z',
		paymentTerms: 'Net 15',
		discount: 0,
		discountType: 'percentage'
	},
	{ 
		id: 'INV-2024-003', 
		client: 'RetailMax', 
		clientId: 'client-3',
		date: '2024-03-31', 
		due: '2024-04-15', 
		subtotal: 6400, 
		tax: 640, 
		total: 7040, 
		status: 'overdue', 
		method: 'credit_card', 
		paidAt: null,
		currency: 'USD',
		notes: 'Enterprise support package',
		tags: ['recurring', 'enterprise'],
		priority: 'high',
		createdBy: 'Mike Davis',
		lastModified: '2024-03-31T16:45:00Z',
		paymentTerms: 'Net 15',
		discount: 5,
		discountType: 'percentage'
	},
	{ 
		id: 'INV-2024-004', 
		client: 'HealthCare Plus', 
		clientId: 'client-4',
		date: '2024-03-31', 
		due: '2024-04-15', 
		subtotal: 4650, 
		tax: 465, 
		total: 5115, 
		status: 'sent', 
		method: 'bank_transfer', 
		paidAt: null,
		currency: 'USD',
		notes: 'HIPAA compliant IT services',
		tags: ['recurring', 'healthcare'],
		priority: 'high',
		createdBy: 'Lisa Chen',
		lastModified: '2024-03-31T11:15:00Z',
		paymentTerms: 'Net 15',
		discount: 0,
		discountType: 'percentage'
	},
	{ 
		id: 'INV-2024-005', 
		client: 'FinanceFirst', 
		clientId: 'client-5',
		date: '2024-03-31', 
		due: '2024-04-15', 
		subtotal: 3400, 
		tax: 340, 
		total: 3740, 
		status: 'paid', 
		method: 'credit_card', 
		paidAt: '2024-04-12',
		currency: 'USD',
		notes: 'Financial compliance monitoring',
		tags: ['recurring', 'compliance'],
		priority: 'normal',
		createdBy: 'David Wilson',
		lastModified: '2024-04-12T09:20:00Z',
		paymentTerms: 'Net 15',
		discount: 10,
		discountType: 'percentage'
	},
	{ 
		id: 'INV-2024-006', 
		client: 'StartupHub', 
		clientId: 'client-6',
		date: '2024-04-15', 
		due: '2024-04-30', 
		subtotal: 2200, 
		tax: 220, 
		total: 2420, 
		status: 'draft', 
		method: 'bank_transfer', 
		paidAt: null,
		currency: 'USD',
		notes: 'Cloud migration services',
		tags: ['one-time', 'migration'],
		priority: 'normal',
		createdBy: 'Emma Thompson',
		lastModified: '2024-04-15T13:30:00Z',
		paymentTerms: 'Net 15',
		discount: 0,
		discountType: 'percentage'
	},
	{ 
		id: 'INV-2024-007', 
		client: 'GlobalTech', 
		clientId: 'client-7',
		date: '2024-04-20', 
		due: '2024-05-05', 
		subtotal: 12500, 
		tax: 1250, 
		total: 13750, 
		status: 'sent', 
		method: 'wire_transfer', 
		paidAt: null,
		currency: 'USD',
		notes: 'Enterprise security audit',
		tags: ['one-time', 'security', 'audit'],
		priority: 'high',
		createdBy: 'Alex Rodriguez',
		lastModified: '2024-04-20T10:15:00Z',
		paymentTerms: 'Net 15',
		discount: 2.5,
		discountType: 'percentage'
	},
	{ 
		id: 'INV-2024-008', 
		client: 'EduTech Solutions', 
		clientId: 'client-8',
		date: '2024-04-25', 
		due: '2024-05-10', 
		subtotal: 5800, 
		tax: 580, 
		total: 6380, 
		status: 'paid', 
		method: 'credit_card', 
		paidAt: '2024-05-08',
		currency: 'USD',
		notes: 'Educational platform support',
		tags: ['recurring', 'education'],
		priority: 'normal',
		createdBy: 'Rachel Green',
		lastModified: '2024-05-08T15:45:00Z',
		paymentTerms: 'Net 15',
		discount: 0,
		discountType: 'percentage'
	}
]

export const mockInvoiceItems = {
	'INV-2024-001': [ 
		{ desc: 'Help Desk - 25 users', qty: 1, price: 3500, category: 'Support' }, 
		{ desc: 'Monitoring - 50 devices', qty: 1, price: 4000, category: 'Monitoring' }, 
		{ desc: 'Emergency Support', qty: 2, price: 250, category: 'Support' } 
	],
	'INV-2024-002': [ 
		{ desc: 'Help Desk - 10 users', qty: 1, price: 1500, category: 'Support' } 
	],
	'INV-2024-003': [ 
		{ desc: 'Help Desk - 40 users', qty: 1, price: 5500, category: 'Support' },
		{ desc: 'Premium Support Package', qty: 1, price: 900, category: 'Support' }
	],
	'INV-2024-004': [ 
		{ desc: 'HIPAA Compliant Help Desk - 30 users', qty: 1, price: 4000, category: 'Support' },
		{ desc: 'Security Monitoring', qty: 1, price: 650, category: 'Security' }
	],
	'INV-2024-005': [ 
		{ desc: 'Financial Services Help Desk - 20 users', qty: 1, price: 2800, category: 'Support' },
		{ desc: 'Compliance Monitoring', qty: 1, price: 600, category: 'Compliance' }
	],
	'INV-2024-006': [ 
		{ desc: 'Cloud Migration Assessment', qty: 1, price: 1200, category: 'Consulting' },
		{ desc: 'Migration Implementation', qty: 1, price: 1000, category: 'Implementation' }
	],
	'INV-2024-007': [ 
		{ desc: 'Security Audit - Enterprise', qty: 1, price: 8000, category: 'Security' },
		{ desc: 'Vulnerability Assessment', qty: 1, price: 3000, category: 'Security' },
		{ desc: 'Compliance Report', qty: 1, price: 1500, category: 'Compliance' }
	],
	'INV-2024-008': [ 
		{ desc: 'Educational Platform Support - 50 users', qty: 1, price: 4500, category: 'Support' },
		{ desc: 'Training Sessions', qty: 4, price: 325, category: 'Training' }
	]
}

export const mockInvoiceCategories = [
	{ id: 'support', name: 'Support Services', color: 'blue', icon: '🛠️' },
	{ id: 'monitoring', name: 'Monitoring', color: 'green', icon: '📊' },
	{ id: 'security', name: 'Security', color: 'red', icon: '🔒' },
	{ id: 'compliance', name: 'Compliance', color: 'purple', icon: '✅' },
	{ id: 'consulting', name: 'Consulting', color: 'orange', icon: '💡' },
	{ id: 'implementation', name: 'Implementation', color: 'indigo', icon: '⚙️' },
	{ id: 'training', name: 'Training', color: 'yellow', icon: '📚' }
]

export const mockPaymentMethods = [
	{ id: 'credit_card', name: 'Credit Card', icon: '💳' },
	{ id: 'bank_transfer', name: 'Bank Transfer', icon: '🏦' },
	{ id: 'wire_transfer', name: 'Wire Transfer', icon: '💸' },
	{ id: 'check', name: 'Check', icon: '📄' },
	{ id: 'cash', name: 'Cash', icon: '💵' }
]

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
