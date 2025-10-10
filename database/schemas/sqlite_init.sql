-- SuperHack SQLite Database Schema
-- Development and testing database

-- Enable foreign key constraints
PRAGMA foreign_keys = ON;

-- Users and Authentication
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    role TEXT DEFAULT 'user', -- admin, finance, ops, user
    is_active INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- MSP Organizations
CREATE TABLE organizations (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    domain TEXT,
    subscription_plan TEXT DEFAULT 'basic', -- basic, pro, enterprise
    is_active INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Organization Users (Many-to-Many)
CREATE TABLE organization_users (
    id TEXT PRIMARY KEY,
    organization_id TEXT REFERENCES organizations(id) ON DELETE CASCADE,
    user_id TEXT REFERENCES users(id) ON DELETE CASCADE,
    role TEXT DEFAULT 'member', -- owner, admin, member
    joined_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(organization_id, user_id)
);

-- Clients (MSP Clients)
CREATE TABLE clients (
    id TEXT PRIMARY KEY,
    organization_id TEXT REFERENCES organizations(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    address TEXT,
    industry TEXT,
    contract_type TEXT, -- monthly, annual, project
    contract_value REAL,
    start_date DATE,
    end_date DATE,
    is_active INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Services (IT Services offered)
CREATE TABLE services (
    id TEXT PRIMARY KEY,
    organization_id TEXT REFERENCES organizations(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    category TEXT, -- support, maintenance, consulting, etc.
    base_price REAL,
    billing_type TEXT, -- hourly, monthly, per-user, per-device
    is_active INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Client Services (Many-to-Many with pricing)
CREATE TABLE client_services (
    id TEXT PRIMARY KEY,
    client_id TEXT REFERENCES clients(id) ON DELETE CASCADE,
    service_id TEXT REFERENCES services(id) ON DELETE CASCADE,
    custom_price REAL,
    quantity INTEGER DEFAULT 1,
    billing_frequency TEXT, -- monthly, quarterly, annually
    start_date DATE,
    end_date DATE,
    is_active INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tickets (Support Tickets)
CREATE TABLE tickets (
    id TEXT PRIMARY KEY,
    organization_id TEXT REFERENCES organizations(id) ON DELETE CASCADE,
    client_id TEXT REFERENCES clients(id) ON DELETE CASCADE,
    ticket_number TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    priority TEXT DEFAULT 'medium', -- low, medium, high, critical
    status TEXT DEFAULT 'open', -- open, in_progress, resolved, closed
    category TEXT,
    assigned_to TEXT REFERENCES users(id),
    time_spent REAL DEFAULT 0, -- in hours
    billable_hours REAL DEFAULT 0,
    hourly_rate REAL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    resolved_at DATETIME
);

-- Invoices
CREATE TABLE invoices (
    id TEXT PRIMARY KEY,
    organization_id TEXT REFERENCES organizations(id) ON DELETE CASCADE,
    client_id TEXT REFERENCES clients(id) ON DELETE CASCADE,
    invoice_number TEXT UNIQUE NOT NULL,
    invoice_date DATE NOT NULL,
    due_date DATE,
    subtotal REAL NOT NULL,
    tax_amount REAL DEFAULT 0,
    total_amount REAL NOT NULL,
    status TEXT DEFAULT 'draft', -- draft, sent, paid, overdue
    payment_date DATE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Invoice Items
CREATE TABLE invoice_items (
    id TEXT PRIMARY KEY,
    invoice_id TEXT REFERENCES invoices(id) ON DELETE CASCADE,
    description TEXT NOT NULL,
    quantity REAL DEFAULT 1,
    unit_price REAL NOT NULL,
    total_price REAL NOT NULL,
    service_id TEXT REFERENCES services(id),
    ticket_id TEXT REFERENCES tickets(id),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Budgets
CREATE TABLE budgets (
    id TEXT PRIMARY KEY,
    organization_id TEXT REFERENCES organizations(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    budget_type TEXT, -- monthly, quarterly, annual, project
    total_amount REAL NOT NULL,
    spent_amount REAL DEFAULT 0,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    is_active INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Budget Categories
CREATE TABLE budget_categories (
    id TEXT PRIMARY KEY,
    budget_id TEXT REFERENCES budgets(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    allocated_amount REAL NOT NULL,
    spent_amount REAL DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Expenses
CREATE TABLE expenses (
    id TEXT PRIMARY KEY,
    organization_id TEXT REFERENCES organizations(id) ON DELETE CASCADE,
    budget_id TEXT REFERENCES budgets(id),
    budget_category_id TEXT REFERENCES budget_categories(id),
    description TEXT NOT NULL,
    amount REAL NOT NULL,
    expense_date DATE NOT NULL,
    category TEXT,
    vendor TEXT,
    is_billable INTEGER DEFAULT 0,
    client_id TEXT REFERENCES clients(id),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- AI Analytics Results
CREATE TABLE ai_analytics (
    id TEXT PRIMARY KEY,
    organization_id TEXT REFERENCES organizations(id) ON DELETE CASCADE,
    analysis_type TEXT NOT NULL, -- profitability, revenue_leak, budget_optimization
    client_id TEXT REFERENCES clients(id),
    data TEXT NOT NULL, -- JSON data
    confidence_score REAL, -- 0.00 to 1.00
    status TEXT DEFAULT 'pending', -- pending, completed, failed
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- AI Recommendations
CREATE TABLE ai_recommendations (
    id TEXT PRIMARY KEY,
    organization_id TEXT REFERENCES organizations(id) ON DELETE CASCADE,
    client_id TEXT REFERENCES clients(id),
    recommendation_type TEXT NOT NULL, -- pricing_adjustment, service_optimization, budget_reallocation
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    impact_score REAL, -- 0.00 to 1.00
    implementation_effort TEXT, -- low, medium, high
    estimated_savings REAL,
    estimated_revenue_increase REAL,
    status TEXT DEFAULT 'pending', -- pending, accepted, rejected, implemented
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Integration Settings
CREATE TABLE integration_settings (
    id TEXT PRIMARY KEY,
    organization_id TEXT REFERENCES organizations(id) ON DELETE CASCADE,
    integration_type TEXT NOT NULL, -- superops, quickbooks, zapier
    settings TEXT NOT NULL, -- JSON settings
    is_active INTEGER DEFAULT 1,
    last_sync DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Audit Log
CREATE TABLE audit_log (
    id TEXT PRIMARY KEY,
    organization_id TEXT REFERENCES organizations(id) ON DELETE CASCADE,
    user_id TEXT REFERENCES users(id),
    action TEXT NOT NULL,
    table_name TEXT,
    record_id TEXT,
    old_values TEXT, -- JSON
    new_values TEXT, -- JSON
    ip_address TEXT,
    user_agent TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_tickets_client_id ON tickets(client_id);
CREATE INDEX idx_tickets_organization_id ON tickets(organization_id);
CREATE INDEX idx_tickets_status ON tickets(status);
CREATE INDEX idx_invoices_client_id ON invoices(client_id);
CREATE INDEX idx_invoices_organization_id ON invoices(organization_id);
CREATE INDEX idx_invoices_status ON invoices(status);
CREATE INDEX idx_expenses_organization_id ON expenses(organization_id);
CREATE INDEX idx_expenses_budget_id ON expenses(budget_id);
CREATE INDEX idx_ai_analytics_organization_id ON ai_analytics(organization_id);
CREATE INDEX idx_ai_analytics_type ON ai_analytics(analysis_type);
CREATE INDEX idx_ai_recommendations_organization_id ON ai_recommendations(organization_id);
CREATE INDEX idx_ai_recommendations_status ON ai_recommendations(status);
