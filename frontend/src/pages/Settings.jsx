import { useMemo, useState } from 'react'
import { KPICard } from '../components/clients/KPICard'
import { Button } from '../components/ui/Button'
import { 
	UsersIcon,
	CheckIcon,
	ExclamationTriangleIcon,
	CurrencyDollarIcon,
	DocumentTextIcon,
	CalendarIcon,
	RefreshIcon,
	TrendingUpIcon
} from '../components/ui/Icons'

export default function Settings() {
	const [activeTab, setActiveTab] = useState('general')

	// Settings data
	const settingsData = useMemo(() => {
		return {
			totalUsers: 12,
			activeUsers: 11,
			securityScore: 94.5,
			integrations: 8,
			storageUsed: 67.3,
			apiCalls: 15420,
			users: [
				{ name: 'John Smith', email: 'john@techwave.com', role: 'Admin', status: 'Active', lastLogin: '2 hours ago' },
				{ name: 'Sarah Johnson', email: 'sarah@techwave.com', role: 'Manager', status: 'Active', lastLogin: '1 day ago' },
				{ name: 'Mike Davis', email: 'mike@techwave.com', role: 'User', status: 'Inactive', lastLogin: '5 days ago' },
				{ name: 'Lisa Wilson', email: 'lisa@techwave.com', role: 'User', status: 'Active', lastLogin: '3 hours ago' }
			],
			integrationsData: [
				{ name: 'SuperOps', status: 'Connected', type: 'PSA', lastSync: '5 minutes ago' },
				{ name: 'QuickBooks', status: 'Connected', type: 'Accounting', lastSync: '1 hour ago' },
				{ name: 'Office 365', status: 'Connected', type: 'Productivity', lastSync: '30 minutes ago' },
				{ name: 'Slack', status: 'Pending', type: 'Communication', lastSync: 'Never' },
				{ name: 'Zapier', status: 'Error', type: 'Automation', lastSync: '2 days ago' }
			],
			securitySettings: [
				{ name: 'Two-Factor Authentication', status: 'Enabled', description: 'Required for all admin users' },
				{ name: 'Password Policy', status: 'Strong', description: 'Minimum 12 characters with complexity' },
				{ name: 'Session Timeout', status: 'Enabled', description: 'Auto logout after 30 minutes' },
				{ name: 'IP Whitelist', status: 'Disabled', description: 'Allow access from any IP' },
				{ name: 'Audit Logging', status: 'Enabled', description: 'All actions are logged' }
			]
		}
	}, [])

	const getStatusColor = (status) => {
		const colors = {
			'Active': 'bg-green-100 text-green-800',
			'Connected': 'bg-green-100 text-green-800',
			'Enabled': 'bg-green-100 text-green-800',
			'Strong': 'bg-green-100 text-green-800',
			'Inactive': 'bg-gray-100 text-gray-800',
			'Pending': 'bg-yellow-100 text-yellow-800',
			'Disabled': 'bg-gray-100 text-gray-800',
			'Error': 'bg-red-100 text-red-800'
		}
		return colors[status] || 'bg-gray-100 text-gray-800'
	}

	const getRoleColor = (role) => {
		const colors = {
			'Admin': 'bg-purple-100 text-purple-800',
			'Manager': 'bg-blue-100 text-blue-800',
			'User': 'bg-gray-100 text-gray-800'
		}
		return colors[role] || 'bg-gray-100 text-gray-800'
	}

	return (
		<div className="space-y-6">
			{/* Header */}
			<div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
				<div>
					<h1 className="text-3xl font-bold bg-gradient-to-r from-slate-600 via-gray-700 to-zinc-700 bg-clip-text text-transparent">
						⚙️ Settings & Configuration
					</h1>
					<p className="text-gray-600 mt-1">Manage system settings, users, security, and integrations</p>
				</div>
				
				<div className="flex flex-wrap gap-3">
					<Button variant="outline" size="sm" className="flex items-center gap-2">
						<DocumentTextIcon className="h-4 w-4" />
						Export Config
					</Button>
					<Button variant="outline" size="sm" className="flex items-center gap-2">
						<CalendarIcon className="h-4 w-4" />
						Backup Settings
					</Button>
					<Button variant="primary" size="sm" className="flex items-center gap-2 bg-gradient-to-r from-slate-600 to-gray-700">
						<RefreshIcon className="h-4 w-4" />
						Sync All
					</Button>
				</div>
			</div>

			{/* KPI Cards */}
			<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
				<KPICard
					title="Total Users"
					value={settingsData.totalUsers}
					change={8.3}
					changeType="positive"
					format="number"
					icon={UsersIcon}
					iconColor="blue"
				/>
				<KPICard
					title="Active Users"
					value={settingsData.activeUsers}
					change={5.2}
					changeType="positive"
					format="number"
					icon={CheckIcon}
					iconColor="green"
				/>
				<KPICard
					title="Security Score"
					value={settingsData.securityScore}
					change={2.1}
					changeType="positive"
					format="decimal"
					icon={ExclamationTriangleIcon}
					iconColor="purple"
					suffix="%"
				/>
				<KPICard
					title="Integrations"
					value={settingsData.integrations}
					change={12.5}
					changeType="positive"
					format="number"
					icon={TrendingUpIcon}
					iconColor="orange"
				/>
				<KPICard
					title="Storage Used"
					value={settingsData.storageUsed}
					change={3.7}
					changeType="neutral"
					format="decimal"
					icon={DocumentTextIcon}
					iconColor="teal"
					suffix="%"
				/>
				<KPICard
					title="API Calls"
					value={settingsData.apiCalls}
					change={15.8}
					changeType="positive"
					format="number"
					icon={CurrencyDollarIcon}
					iconColor="indigo"
				/>
			</div>

			{/* System Overview Cards */}
			<div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
				{/* System Status */}
				<div className="bg-gradient-to-br from-green-50 to-white rounded-xl border border-gray-200 p-6 shadow-sm">
					<h2 className="text-lg font-semibold bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent mb-4">
						🟢 System Status
					</h2>
					<div className="space-y-4">
						{[
							{ label: 'Server Status', value: 'Online', status: 'success' },
							{ label: 'Database', value: 'Connected', status: 'success' },
							{ label: 'API Health', value: 'Healthy', status: 'success' },
							{ label: 'Last Backup', value: '2 hours ago', status: 'info' }
						].map((item, index) => (
							<div key={index} className="flex items-center justify-between p-3 bg-white rounded-lg border border-gray-200">
								<span className="text-sm font-medium text-gray-700">{item.label}</span>
								<span className={`px-2 py-1 rounded-full text-xs font-medium ${
									item.status === 'success' ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800'
								}`}>
									{item.value}
								</span>
							</div>
						))}
					</div>
				</div>

				{/* Quick Actions */}
				<div className="bg-gradient-to-br from-blue-50 to-white rounded-xl border border-gray-200 p-6 shadow-sm">
					<h2 className="text-lg font-semibold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent mb-4">
						⚡ Quick Actions
					</h2>
					<div className="space-y-3">
						{[
							{ label: 'Create Backup', icon: '💾', color: 'blue' },
							{ label: 'Add New User', icon: '👤', color: 'green' },
							{ label: 'System Maintenance', icon: '🔧', color: 'orange' },
							{ label: 'Export Logs', icon: '📄', color: 'purple' }
						].map((action, index) => (
							<button key={index} className={`w-full flex items-center gap-3 p-3 bg-white rounded-lg border border-gray-200 hover:border-${action.color}-300 transition-all hover:shadow-sm`}>
								<span className="text-lg">{action.icon}</span>
								<span className="text-sm font-medium text-gray-700">{action.label}</span>
							</button>
						))}
					</div>
				</div>

				{/* Recent Activity */}
				<div className="bg-gradient-to-br from-purple-50 to-white rounded-xl border border-gray-200 p-6 shadow-sm">
					<h2 className="text-lg font-semibold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent mb-4">
						📊 Recent Activity
					</h2>
					<div className="space-y-3 max-h-64 overflow-y-auto">
						{[
							{ action: 'User login', user: 'John Smith', time: '5 minutes ago' },
							{ action: 'Settings updated', user: 'Admin', time: '1 hour ago' },
							{ action: 'Backup completed', user: 'System', time: '2 hours ago' },
							{ action: 'New integration', user: 'Sarah Johnson', time: '3 hours ago' },
							{ action: 'Security scan', user: 'System', time: '6 hours ago' }
						].map((activity, index) => (
							<div key={index} className="flex items-start gap-3 p-3 bg-white rounded-lg border border-gray-200">
								<div className="w-2 h-2 bg-purple-500 rounded-full mt-2 flex-shrink-0"></div>
								<div className="flex-1">
									<p className="text-sm text-gray-900">{activity.action}</p>
									<p className="text-xs text-gray-500">{activity.user} • {activity.time}</p>
								</div>
							</div>
						))}
					</div>
				</div>
			</div>

			{/* Tab Navigation */}
			<div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
				<div className="flex flex-wrap gap-2 mb-6">
					{[
						{ id: 'general', label: 'General', icon: '⚙️' },
						{ id: 'users', label: 'User Management', icon: '👥' },
						{ id: 'security', label: 'Security', icon: '🔒' },
						{ id: 'integrations', label: 'Integrations', icon: '🔗' }
					].map((tab) => (
						<button
							key={tab.id}
							onClick={() => setActiveTab(tab.id)}
							className={`px-4 py-2 rounded-lg font-medium transition-all flex items-center gap-2 ${
								activeTab === tab.id
									? 'bg-gradient-to-r from-slate-600 to-gray-700 text-white shadow-sm'
									: 'bg-gray-100 hover:bg-gray-200 text-gray-700'
							}`}
						>
							<span>{tab.icon}</span>
							{tab.label}
						</button>
					))}
				</div>

				{/* Tab Content */}
				{activeTab === 'general' && (
					<div className="space-y-6">
						<div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
							{/* Organization Settings */}
							<div className="bg-gradient-to-br from-blue-50 to-white rounded-lg border border-gray-200 p-6">
								<h3 className="text-lg font-semibold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent mb-4">
									🏢 Organization
								</h3>
								<div className="space-y-4">
									<div className="bg-white rounded-lg border border-gray-200 p-4">
										<label className="text-sm font-medium text-gray-700 mb-2 block">Company Name</label>
										<input type="text" className="w-full p-2 border border-gray-300 rounded-lg text-sm" defaultValue="TechWave MSP" />
									</div>
									<div className="bg-white rounded-lg border border-gray-200 p-4">
										<label className="text-sm font-medium text-gray-700 mb-2 block">Plan</label>
										<select className="w-full p-2 border border-gray-300 rounded-lg text-sm">
											<option>Enterprise</option>
											<option>Professional</option>
											<option>Basic</option>
										</select>
									</div>
									<div className="bg-white rounded-lg border border-gray-200 p-4">
										<label className="text-sm font-medium text-gray-700 mb-2 block">Time Zone</label>
										<select className="w-full p-2 border border-gray-300 rounded-lg text-sm">
											<option>UTC-05:00 (Eastern Time)</option>
											<option>UTC-08:00 (Pacific Time)</option>
											<option>UTC+00:00 (GMT)</option>
										</select>
									</div>
								</div>
							</div>

							{/* System Preferences */}
							<div className="bg-gradient-to-br from-green-50 to-white rounded-lg border border-gray-200 p-6">
								<h3 className="text-lg font-semibold bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent mb-4">
									🎛️ System Preferences
								</h3>
								<div className="space-y-4">
									{[
										{ label: 'Email Notifications', enabled: true },
										{ label: 'Auto Backup', enabled: true },
										{ label: 'Debug Mode', enabled: false },
										{ label: 'Maintenance Mode', enabled: false }
									].map((setting, index) => (
										<div key={index} className="flex items-center justify-between p-3 bg-white rounded-lg border border-gray-200">
											<span className="text-sm font-medium text-gray-700">{setting.label}</span>
											<div className={`w-10 h-6 rounded-full transition-colors ${
												setting.enabled ? 'bg-green-500' : 'bg-gray-300'
											} relative cursor-pointer`}>
												<div className={`w-4 h-4 bg-white rounded-full absolute top-1 transition-transform ${
													setting.enabled ? 'translate-x-5' : 'translate-x-1'
												}`}></div>
											</div>
										</div>
									))}
								</div>
							</div>
						</div>
					</div>
				)}

				{activeTab === 'users' && (
					<div className="space-y-4">
						<div className="flex items-center justify-between">
							<h3 className="text-lg font-semibold text-gray-900">User Management</h3>
							<button className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:from-blue-700 hover:to-indigo-700 transition-all">
								Add User
							</button>
						</div>
						<div className="space-y-3">
							{settingsData.users.map((user, index) => (
								<div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg border border-gray-200">
									<div className="flex items-center gap-4">
										<div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white font-semibold text-sm">
											{user.name.split(' ').map(n => n[0]).join('')}
										</div>
										<div>
											<p className="font-medium text-gray-900">{user.name}</p>
											<p className="text-sm text-gray-500">{user.email}</p>
											<p className="text-xs text-gray-400">Last login: {user.lastLogin}</p>
										</div>
									</div>
									<div className="flex items-center gap-2">
										<span className={`px-2 py-1 rounded-full text-xs font-medium ${getRoleColor(user.role)}`}>
											{user.role}
										</span>
										<span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(user.status)}`}>
											{user.status}
										</span>
										<button className="text-gray-400 hover:text-gray-600 transition-colors">
											<DocumentTextIcon className="h-4 w-4" />
										</button>
									</div>
								</div>
							))}
						</div>
					</div>
				)}

				{activeTab === 'security' && (
					<div className="space-y-4">
						<h3 className="text-lg font-semibold text-gray-900">Security Settings</h3>
						<div className="space-y-3">
							{settingsData.securitySettings.map((setting, index) => (
								<div key={index} className="p-4 bg-gray-50 rounded-lg border border-gray-200">
									<div className="flex items-center justify-between mb-2">
										<span className="font-medium text-gray-900">{setting.name}</span>
										<span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(setting.status)}`}>
											{setting.status}
										</span>
									</div>
									<p className="text-sm text-gray-500">{setting.description}</p>
								</div>
							))}
						</div>
					</div>
				)}

				{activeTab === 'integrations' && (
					<div className="space-y-4">
						<div className="flex items-center justify-between">
							<h3 className="text-lg font-semibold text-gray-900">Integrations</h3>
							<button className="bg-gradient-to-r from-green-600 to-emerald-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:from-green-700 hover:to-emerald-700 transition-all">
								Add Integration
							</button>
						</div>
						<div className="grid grid-cols-1 md:grid-cols-2 gap-4">
							{settingsData.integrationsData.map((integration, index) => (
								<div key={index} className="p-4 bg-gray-50 rounded-lg border border-gray-200">
									<div className="flex items-center justify-between mb-2">
										<div>
											<span className="font-medium text-gray-900">{integration.name}</span>
											<p className="text-xs text-gray-500">{integration.type}</p>
										</div>
										<span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(integration.status)}`}>
											{integration.status}
										</span>
									</div>
									<p className="text-sm text-gray-500">Last sync: {integration.lastSync}</p>
								</div>
							))}
						</div>
					</div>
				)}
			</div>
		</div>
	)
}
