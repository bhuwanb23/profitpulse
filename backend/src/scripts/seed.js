const bcrypt = require('bcryptjs');
const { 
  User, 
  Organization, 
  Client, 
  Service, 
  Ticket, 
  Invoice, 
  Budget, 
  Expense, 
  AIAnalytics, 
  AIRecommendation 
} = require('../models');

async function seedDatabase() {
  try {
    console.log('🔄 Starting database seeding...');
    
    // Create sample organization
    const organization = await Organization.create({
      name: 'TechWave MSP',
      domain: 'techwave-msp.com',
      subscription_plan: 'enterprise',
      is_active: true
    });
    console.log('✅ Organization created:', organization.name);
    
    // Create admin user
    const adminPassword = await bcrypt.hash('admin123', 12);
    const adminUser = await User.create({
      email: 'admin@techwave.com',
      password_hash: adminPassword,
      first_name: 'Admin',
      last_name: 'User',
      role: 'admin',
      organization_id: organization.id,
      is_active: true
    });
    console.log('✅ Admin user created:', adminUser.email);
    
    // Create sample clients
    const clients = await Promise.all([
      Client.create({
        organization_id: organization.id,
        name: 'Acme Corporation',
        email: 'contact@acme.com',
        phone: '+1-555-0101',
        address: '123 Business St, City, State 12345',
        industry: 'Technology',
        contract_type: 'monthly',
        contract_value: 5000.00,
        start_date: '2024-01-01',
        end_date: '2024-12-31',
        is_active: true
      }),
      Client.create({
        organization_id: organization.id,
        name: 'Global Solutions Inc',
        email: 'it@globalsolutions.com',
        phone: '+1-555-0102',
        address: '456 Enterprise Ave, City, State 12345',
        industry: 'Manufacturing',
        contract_type: 'annual',
        contract_value: 12000.00,
        start_date: '2024-01-01',
        end_date: '2024-12-31',
        is_active: true
      }),
      Client.create({
        organization_id: organization.id,
        name: 'StartupXYZ',
        email: 'founder@startupxyz.com',
        phone: '+1-555-0103',
        address: '789 Innovation Dr, City, State 12345',
        industry: 'Finance',
        contract_type: 'project',
        contract_value: 2500.00,
        start_date: '2024-06-01',
        end_date: '2024-08-31',
        is_active: true
      })
    ]);
    console.log('✅ Sample clients created:', clients.length);
    
    // Create sample services
    const services = await Promise.all([
      Service.create({
        organization_id: organization.id,
        name: '24/7 Technical Support',
        description: 'Round-the-clock technical support for all IT issues',
        category: 'support',
        base_price: 150.00,
        billing_type: 'monthly',
        is_active: true
      }),
      Service.create({
        organization_id: organization.id,
        name: 'Network Monitoring',
        description: 'Continuous monitoring of network infrastructure',
        category: 'monitoring',
        base_price: 200.00,
        billing_type: 'monthly',
        is_active: true
      }),
      Service.create({
        organization_id: organization.id,
        name: 'Security Assessment',
        description: 'Comprehensive security audit and recommendations',
        category: 'security',
        base_price: 500.00,
        billing_type: 'hourly',
        is_active: true
      })
    ]);
    console.log('✅ Sample services created:', services.length);
    
    // Create sample tickets
    const tickets = await Promise.all([
      Ticket.create({
        organization_id: organization.id,
        client_id: clients[0].id,
        ticket_number: 'TKT-2024-001',
        title: 'Email server down',
        description: 'Users cannot send or receive emails',
        priority: 'high',
        status: 'resolved',
        category: 'email',
        assigned_to: adminUser.id,
        time_spent: 2.5,
        billable_hours: 2.5,
        hourly_rate: 150.00,
        resolved_at: new Date()
      }),
      Ticket.create({
        organization_id: organization.id,
        client_id: clients[1].id,
        ticket_number: 'TKT-2024-002',
        title: 'Network connectivity issues',
        description: 'Intermittent network drops in office',
        priority: 'medium',
        status: 'in_progress',
        category: 'network',
        assigned_to: adminUser.id,
        time_spent: 1.0,
        billable_hours: 1.0,
        hourly_rate: 150.00
      })
    ]);
    console.log('✅ Sample tickets created:', tickets.length);
    
    // Create sample invoices
    const invoices = await Promise.all([
      Invoice.create({
        organization_id: organization.id,
        client_id: clients[0].id,
        invoice_number: 'INV-2024-001',
        invoice_date: '2024-01-01',
        due_date: '2024-01-31',
        subtotal: 5000.00,
        tax_amount: 500.00,
        total_amount: 5500.00,
        status: 'paid',
        payment_date: '2024-01-15'
      }),
      Invoice.create({
        organization_id: organization.id,
        client_id: clients[1].id,
        invoice_number: 'INV-2024-002',
        invoice_date: '2024-01-01',
        due_date: '2024-01-31',
        subtotal: 12000.00,
        tax_amount: 1200.00,
        total_amount: 13200.00,
        status: 'sent'
      })
    ]);
    console.log('✅ Sample invoices created:', invoices.length);
    
    // Create sample budget
    const budget = await Budget.create({
      organization_id: organization.id,
      name: 'Q1 2024 Operations Budget',
      description: 'First quarter operational expenses',
      budget_type: 'quarterly',
      total_amount: 50000.00,
      spent_amount: 12500.00,
      start_date: '2024-01-01',
      end_date: '2024-03-31',
      is_active: true
    });
    console.log('✅ Sample budget created:', budget.name);
    
    // Create sample expenses
    const expenses = await Promise.all([
      Expense.create({
        organization_id: organization.id,
        budget_id: budget.id,
        description: 'Software licenses renewal',
        amount: 5000.00,
        expense_date: '2024-01-15',
        category: 'software',
        vendor: 'Microsoft',
        is_billable: false
      }),
      Expense.create({
        organization_id: organization.id,
        budget_id: budget.id,
        description: 'Hardware maintenance',
        amount: 2500.00,
        expense_date: '2024-01-20',
        category: 'hardware',
        vendor: 'Dell',
        is_billable: true,
        client_id: clients[0].id
      })
    ]);
    console.log('✅ Sample expenses created:', expenses.length);
    
    // Create sample AI analytics
    const aiAnalytics = await AIAnalytics.create({
      organization_id: organization.id,
      client_id: clients[0].id,
      analysis_type: 'profitability',
      data: JSON.stringify({
        profit_margin: 0.25,
        revenue_growth: 0.15,
        cost_efficiency: 0.85,
        recommendations: ['Increase service pricing by 10%', 'Optimize resource allocation']
      }),
      confidence_score: 0.87,
      status: 'completed'
    });
    console.log('✅ Sample AI analytics created');
    
    // Create sample AI recommendations
    const aiRecommendations = await Promise.all([
      AIRecommendation.create({
        organization_id: organization.id,
        client_id: clients[0].id,
        recommendation_type: 'pricing_adjustment',
        title: 'Increase Acme Corp Service Pricing',
        description: 'Based on profitability analysis, recommend 15% price increase for premium services',
        impact_score: 0.85,
        implementation_effort: 'medium',
        estimated_savings: 0,
        estimated_revenue_increase: 750.00,
        status: 'pending'
      }),
      AIRecommendation.create({
        organization_id: organization.id,
        client_id: clients[1].id,
        recommendation_type: 'service_optimization',
        title: 'Optimize Global Solutions Support',
        description: 'Implement automated monitoring to reduce manual support tickets by 30%',
        impact_score: 0.72,
        implementation_effort: 'high',
        estimated_savings: 2000.00,
        estimated_revenue_increase: 0,
        status: 'pending'
      })
    ]);
    console.log('✅ Sample AI recommendations created:', aiRecommendations.length);
    
    console.log('🎉 Database seeding completed successfully!');
    console.log('📊 Created:');
    console.log('  - 1 Organization');
    console.log('  - 1 Admin User');
    console.log('  - 3 Clients');
    console.log('  - 3 Services');
    console.log('  - 2 Tickets');
    console.log('  - 2 Invoices');
    console.log('  - 1 Budget');
    console.log('  - 2 Expenses');
    console.log('  - 1 AI Analytics');
    console.log('  - 2 AI Recommendations');
    
    process.exit(0);
  } catch (error) {
    console.error('❌ Seeding failed:', error);
    process.exit(1);
  }
}

seedDatabase();
