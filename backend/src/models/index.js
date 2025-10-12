const { sequelize } = require('../config/database');

// Import all models
const User = require('./User');
const Organization = require('./Organization');
const Client = require('./Client');
const Service = require('./Service');
const Ticket = require('./Ticket');
const Invoice = require('./Invoice');
const Budget = require('./Budget');
const Expense = require('./Expense');
const AIAnalytics = require('./AIAnalytics');
const AIRecommendation = require('./AIRecommendation');
const Report = require('./Report');
const ReportTemplate = require('./ReportTemplate');
const ScheduledReport = require('./ScheduledReport');

// Initialize models
const models = {
  User,
  Organization,
  Client,
  Service,
  Ticket,
  Invoice,
  Budget,
  Expense,
  AIAnalytics,
  AIRecommendation,
  Report,
  ReportTemplate,
  ScheduledReport
};

// Define associations
// Organization associations
Organization.hasMany(User, { foreignKey: 'organization_id', as: 'users' });
Organization.hasMany(Client, { foreignKey: 'organization_id', as: 'clients' });
Organization.hasMany(Service, { foreignKey: 'organization_id', as: 'services' });
Organization.hasMany(Ticket, { foreignKey: 'organization_id', as: 'tickets' });
Organization.hasMany(Invoice, { foreignKey: 'organization_id', as: 'invoices' });
Organization.hasMany(Budget, { foreignKey: 'organization_id', as: 'budgets' });
Organization.hasMany(Expense, { foreignKey: 'organization_id', as: 'expenses' });
Organization.hasMany(AIAnalytics, { foreignKey: 'organization_id', as: 'aiAnalytics' });
Organization.hasMany(AIRecommendation, { foreignKey: 'organization_id', as: 'aiRecommendations' });
Organization.hasMany(Report, { foreignKey: 'organization_id', as: 'reports' });
Organization.hasMany(ReportTemplate, { foreignKey: 'organization_id', as: 'reportTemplates' });
Organization.hasMany(ScheduledReport, { foreignKey: 'organization_id', as: 'scheduledReports' });

// User associations
User.belongsTo(Organization, { foreignKey: 'organization_id', as: 'organization' });
User.hasMany(Ticket, { foreignKey: 'assigned_to', as: 'assignedTickets' });
User.hasMany(Ticket, { foreignKey: 'created_by', as: 'createdTickets' });
User.hasMany(Invoice, { foreignKey: 'created_by', as: 'createdInvoices' });
User.hasMany(Budget, { foreignKey: 'created_by', as: 'createdBudgets' });
User.hasMany(Report, { foreignKey: 'created_by', as: 'createdReports' });
User.hasMany(ReportTemplate, { foreignKey: 'created_by', as: 'createdReportTemplates' });
User.hasMany(ScheduledReport, { foreignKey: 'created_by', as: 'createdScheduledReports' });

// Client associations
Client.belongsTo(Organization, { foreignKey: 'organization_id', as: 'organization' });
Client.hasMany(Service, { foreignKey: 'client_id', as: 'services' });
Client.hasMany(Ticket, { foreignKey: 'client_id', as: 'tickets' });
Client.hasMany(Invoice, { foreignKey: 'client_id', as: 'invoices' });
Client.hasMany(Expense, { foreignKey: 'client_id', as: 'expenses' });
Client.hasMany(AIAnalytics, { foreignKey: 'client_id', as: 'aiAnalytics' });
Client.hasMany(AIRecommendation, { foreignKey: 'client_id', as: 'aiRecommendations' });

// Service associations
Service.belongsTo(Organization, { foreignKey: 'organization_id', as: 'organization' });
Service.belongsTo(Client, { foreignKey: 'client_id', as: 'client' });
Service.hasMany(Ticket, { foreignKey: 'service_id', as: 'tickets' });

// Ticket associations
Ticket.belongsTo(Organization, { foreignKey: 'organization_id', as: 'organization' });
Ticket.belongsTo(Client, { foreignKey: 'client_id', as: 'client' });
Ticket.belongsTo(Service, { foreignKey: 'service_id', as: 'service' });
Ticket.belongsTo(User, { foreignKey: 'assigned_to', as: 'assignedUser' });
Ticket.belongsTo(User, { foreignKey: 'created_by', as: 'createdByUser' });

// Invoice associations
Invoice.belongsTo(Organization, { foreignKey: 'organization_id', as: 'organization' });
Invoice.belongsTo(Client, { foreignKey: 'client_id', as: 'client' });
Invoice.belongsTo(User, { foreignKey: 'created_by', as: 'createdByUser' });

// Budget associations
Budget.belongsTo(Organization, { foreignKey: 'organization_id', as: 'organization' });
Budget.belongsTo(User, { foreignKey: 'created_by', as: 'createdByUser' });
Budget.hasMany(Expense, { foreignKey: 'budget_id', as: 'expenses' });

// Expense associations
Expense.belongsTo(Organization, { foreignKey: 'organization_id', as: 'organization' });
Expense.belongsTo(Budget, { foreignKey: 'budget_id', as: 'budget' });
Expense.belongsTo(Client, { foreignKey: 'client_id', as: 'client' });

// AI Analytics associations
AIAnalytics.belongsTo(Organization, { foreignKey: 'organization_id', as: 'organization' });
AIAnalytics.belongsTo(Client, { foreignKey: 'client_id', as: 'client' });

// AI Recommendation associations
AIRecommendation.belongsTo(Organization, { foreignKey: 'organization_id', as: 'organization' });
AIRecommendation.belongsTo(Client, { foreignKey: 'client_id', as: 'client' });

// Report associations
Report.belongsTo(Organization, { foreignKey: 'organization_id', as: 'organization' });
Report.belongsTo(ReportTemplate, { foreignKey: 'template_id', as: 'template' });
Report.belongsTo(User, { foreignKey: 'created_by', as: 'createdByUser' });

// Report Template associations
ReportTemplate.belongsTo(Organization, { foreignKey: 'organization_id', as: 'organization' });
ReportTemplate.belongsTo(User, { foreignKey: 'created_by', as: 'createdByUser' });

// Scheduled Report associations
ScheduledReport.belongsTo(Organization, { foreignKey: 'organization_id', as: 'organization' });
ScheduledReport.belongsTo(Report, { foreignKey: 'report_id', as: 'report' });
ScheduledReport.belongsTo(ReportTemplate, { foreignKey: 'template_id', as: 'template' });
ScheduledReport.belongsTo(User, { foreignKey: 'created_by', as: 'createdByUser' });

// Export models and sequelize instance
module.exports = {
  sequelize,
  ...models
};
