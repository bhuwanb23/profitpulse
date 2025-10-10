-- Sample data for SuperHack AI Platform
-- This file contains sample data for testing and development

-- Insert sample organization
INSERT INTO organizations (id, name, domain, subscription_plan) VALUES 
('550e8400-e29b-41d4-a716-446655440000', 'TechMSP Solutions', 'techmsp.com', 'pro');

-- Insert sample users
INSERT INTO users (id, email, password_hash, first_name, last_name, role) VALUES 
('550e8400-e29b-41d4-a716-446655440001', 'admin@techmsp.com', '$2b$10$example_hash', 'John', 'Admin', 'admin'),
('550e8400-e29b-41d4-a716-446655440002', 'finance@techmsp.com', '$2b$10$example_hash', 'Sarah', 'Finance', 'finance'),
('550e8400-e29b-41d4-a716-446655440003', 'ops@techmsp.com', '$2b$10$example_hash', 'Mike', 'Operations', 'ops');

-- Link users to organization
INSERT INTO organization_users (organization_id, user_id, role) VALUES 
('550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440001', 'owner'),
('550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440002', 'admin'),
('550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440003', 'member');

-- Insert sample clients
INSERT INTO clients (id, organization_id, name, email, phone, industry, contract_type, contract_value, start_date, end_date) VALUES 
('550e8400-e29b-41d4-a716-446655440010', '550e8400-e29b-41d4-a716-446655440000', 'Acme Corp', 'contact@acme.com', '+1-555-0101', 'Manufacturing', 'annual', 50000.00, '2024-01-01', '2024-12-31'),
('550e8400-e29b-41d4-a716-446655440011', '550e8400-e29b-41d4-a716-446655440000', 'TechStart Inc', 'hello@techstart.com', '+1-555-0102', 'Technology', 'monthly', 5000.00, '2024-03-01', NULL),
('550e8400-e29b-41d4-a716-446655440012', '550e8400-e29b-41d4-a716-446655440000', 'RetailMax', 'support@retailmax.com', '+1-555-0103', 'Retail', 'annual', 75000.00, '2024-01-15', '2024-12-15');

-- Insert sample services
INSERT INTO services (id, organization_id, name, description, category, base_price, billing_type) VALUES 
('550e8400-e29b-41d4-a716-446655440020', '550e8400-e29b-41d4-a716-446655440000', '24/7 Help Desk', 'Round-the-clock technical support', 'support', 150.00, 'per-user'),
('550e8400-e29b-41d4-a716-446655440021', '550e8400-e29b-41d4-a716-446655440000', 'Network Monitoring', 'Proactive network monitoring and maintenance', 'maintenance', 200.00, 'per-device'),
('550e8400-e29b-41d4-a716-446655440022', '550e8400-e29b-41d4-a716-446655440000', 'Cloud Migration', 'Cloud infrastructure migration services', 'consulting', 125.00, 'hourly'),
('550e8400-e29b-41d4-a716-446655440023', '550e8400-e29b-41d4-a716-446655440000', 'Security Assessment', 'Comprehensive security audit and recommendations', 'consulting', 200.00, 'hourly');

-- Link clients to services
INSERT INTO client_services (client_id, service_id, custom_price, quantity, billing_frequency, start_date, end_date) VALUES 
('550e8400-e29b-41d4-a716-446655440010', '550e8400-e29b-41d4-a716-446655440020', 140.00, 25, 'monthly', '2024-01-01', '2024-12-31'),
('550e8400-e29b-41d4-a716-446655440010', '550e8400-e29b-41d4-a716-446655440021', 180.00, 50, 'monthly', '2024-01-01', '2024-12-31'),
('550e8400-e29b-41d4-a716-446655440011', '550e8400-e29b-41d4-a716-446655440020', 150.00, 10, 'monthly', '2024-03-01', NULL),
('550e8400-e29b-41d4-a716-446655440012', '550e8400-e29b-41d4-a716-446655440020', 160.00, 40, 'monthly', '2024-01-15', '2024-12-15'),
('550e8400-e29b-41d4-a716-446655440012', '550e8400-e29b-41d4-a716-446655440023', 200.00, 1, 'annually', '2024-01-15', '2024-12-15');

-- Insert sample tickets
INSERT INTO tickets (id, organization_id, client_id, ticket_number, title, description, priority, status, category, assigned_to, time_spent, billable_hours, hourly_rate) VALUES 
('550e8400-e29b-41d4-a716-446655440030', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440010', 'TKT-001', 'Email server down', 'Exchange server is not responding', 'high', 'resolved', 'infrastructure', '550e8400-e29b-41d4-a716-446655440003', 2.5, 2.5, 125.00),
('550e8400-e29b-41d4-a716-446655440031', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440011', 'TKT-002', 'VPN connection issues', 'Users cannot connect to VPN', 'medium', 'in_progress', 'network', '550e8400-e29b-41d4-a716-446655440003', 1.0, 1.0, 125.00),
('550e8400-e29b-41d4-a716-446655440032', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440012', 'TKT-003', 'Software installation', 'Need to install new accounting software', 'low', 'open', 'software', NULL, 0, 0, 125.00);

-- Insert sample invoices
INSERT INTO invoices (id, organization_id, client_id, invoice_number, invoice_date, due_date, subtotal, tax_amount, total_amount, status) VALUES 
('550e8400-e29b-41d4-a716-446655440040', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440010', 'INV-2024-001', '2024-01-31', '2024-02-15', 8000.00, 800.00, 8800.00, 'paid'),
('550e8400-e29b-41d4-a716-446655440041', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440011', 'INV-2024-002', '2024-02-28', '2024-03-15', 1500.00, 150.00, 1650.00, 'sent'),
('550e8400-e29b-41d4-a716-446655440042', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440012', 'INV-2024-003', '2024-03-31', '2024-04-15', 6400.00, 640.00, 7040.00, 'overdue');

-- Insert sample invoice items
INSERT INTO invoice_items (invoice_id, description, quantity, unit_price, total_price, service_id, ticket_id) VALUES 
('550e8400-e29b-41d4-a716-446655440040', '24/7 Help Desk - 25 users', 1, 3500.00, 3500.00, '550e8400-e29b-41d4-a716-446655440020', NULL),
('550e8400-e29b-41d4-a716-446655440040', 'Network Monitoring - 50 devices', 1, 9000.00, 9000.00, '550e8400-e29b-41d4-a716-446655440021', NULL),
('550e8400-e29b-41d4-a716-446655440040', 'Emergency Support - Email Server', 1, 312.50, 312.50, NULL, '550e8400-e29b-41d4-a716-446655440030'),
('550e8400-e29b-41d4-a716-446655440041', '24/7 Help Desk - 10 users', 1, 1500.00, 1500.00, '550e8400-e29b-41d4-a716-446655440020', NULL),
('550e8400-e29b-41d4-a716-446655440042', '24/7 Help Desk - 40 users', 1, 6400.00, 6400.00, '550e8400-e29b-41d4-a716-446655440020', NULL);

-- Insert sample budgets
INSERT INTO budgets (id, organization_id, name, description, budget_type, total_amount, spent_amount, start_date, end_date) VALUES 
('550e8400-e29b-41d4-a716-446655440050', '550e8400-e29b-41d4-a716-446655440000', 'Q1 2024 Operations', 'Q1 operational budget', 'quarterly', 100000.00, 75000.00, '2024-01-01', '2024-03-31'),
('550e8400-e29b-41d4-a716-446655440051', '550e8400-e29b-41d4-a716-446655440000', 'Annual Equipment', 'Annual equipment and software budget', 'annual', 50000.00, 15000.00, '2024-01-01', '2024-12-31');

-- Insert sample budget categories
INSERT INTO budget_categories (budget_id, name, allocated_amount, spent_amount) VALUES 
('550e8400-e29b-41d4-a716-446655440050', 'Personnel', 60000.00, 45000.00),
('550e8400-e29b-41d4-a716-446655440050', 'Equipment', 25000.00, 18000.00),
('550e8400-e29b-41d4-a716-446655440050', 'Software Licenses', 15000.00, 12000.00),
('550e8400-e29b-41d4-a716-446655440051', 'Hardware', 30000.00, 8000.00),
('550e8400-e29b-41d4-a716-446655440051', 'Software', 20000.00, 7000.00);

-- Insert sample expenses
INSERT INTO expenses (organization_id, budget_id, budget_category_id, description, amount, expense_date, category, vendor, is_billable, client_id) VALUES 
('550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440050', '550e8400-e29b-41d4-a716-446655440050', 'Salaries - January', 15000.00, '2024-01-31', 'personnel', 'Payroll', false, NULL),
('550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440050', '550e8400-e29b-41d4-a716-446655440050', 'Salaries - February', 15000.00, '2024-02-29', 'personnel', 'Payroll', false, NULL),
('550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440050', '550e8400-e29b-41d4-a716-446655440050', 'Salaries - March', 15000.00, '2024-03-31', 'personnel', 'Payroll', false, NULL),
('550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440050', '550e8400-e29b-41d4-a716-446655440050', 'New Server Hardware', 12000.00, '2024-02-15', 'equipment', 'Dell Technologies', false, NULL),
('550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440050', '550e8400-e29b-41d4-a716-446655440050', 'Microsoft 365 Licenses', 3000.00, '2024-01-15', 'software', 'Microsoft', false, NULL),
('550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440050', '550e8400-e29b-41d4-a716-446655440050', 'Client-specific software', 2000.00, '2024-03-10', 'software', 'Software Vendor', true, '550e8400-e29b-41d4-a716-446655440010');

-- Insert sample AI analytics
INSERT INTO ai_analytics (organization_id, analysis_type, client_id, data, confidence_score, status) VALUES 
('550e8400-e29b-41d4-a716-446655440000', 'profitability', '550e8400-e29b-41d4-a716-446655440010', '{"profitability_score": 0.85, "revenue": 50000, "costs": 35000, "margin": 0.30}', 0.92, 'completed'),
('550e8400-e29b-41d4-a716-446655440000', 'revenue_leak', '550e8400-e29b-41d4-a716-446655440011', '{"leak_amount": 1500, "leak_sources": ["unbilled_hours", "underpriced_services"], "potential_recovery": 1200}', 0.88, 'completed'),
('550e8400-e29b-41d4-a716-446655440000', 'budget_optimization', NULL, '{"optimization_potential": 0.15, "savings_opportunities": ["equipment_consolidation", "license_optimization"], "estimated_savings": 7500}', 0.90, 'completed');

-- Insert sample AI recommendations
INSERT INTO ai_recommendations (organization_id, client_id, recommendation_type, title, description, impact_score, implementation_effort, estimated_savings, estimated_revenue_increase, status) VALUES 
('550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440010', 'pricing_adjustment', 'Increase Help Desk Pricing', 'Client shows high utilization but low margin. Consider 15% price increase.', 0.85, 'low', 0, 5250.00, 'pending'),
('550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440011', 'service_optimization', 'Add Network Monitoring Service', 'Client has no monitoring but high support tickets. Add monitoring service.', 0.75, 'medium', 0, 2400.00, 'pending'),
('550e8400-e29b-41d4-a716-446655440000', NULL, 'budget_reallocation', 'Optimize Software Licenses', 'Reduce unused licenses and consolidate tools to save $2,400 annually.', 0.80, 'low', 2400.00, 0, 'pending');

-- Insert sample integration settings
INSERT INTO integration_settings (organization_id, integration_type, settings, is_active, last_sync) VALUES 
('550e8400-e29b-41d4-a716-446655440000', 'superops', '{"api_key": "sk_test_...", "base_url": "https://api.superops.ai", "sync_frequency": "daily"}', true, '2024-03-15 10:30:00'),
('550e8400-e29b-41d4-a716-446655440000', 'quickbooks', '{"client_id": "qbo_...", "client_secret": "secret_...", "company_id": "123456789", "sync_frequency": "daily"}', true, '2024-03-15 09:15:00');
