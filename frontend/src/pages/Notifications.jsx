import { useMemo } from 'react'
import { KPICard } from '../components/clients/KPICard'
import { Button } from '../components/ui/Button'
import { 
	ExclamationTriangleIcon,
	CheckIcon,
	ClockIcon,
	UsersIcon,
	CalendarIcon,
	RefreshIcon,
	DocumentTextIcon,
	ChartBarIcon,
	TrendingUpIcon,
	TrendingDownIcon,
	XMarkIcon
} from '../components/ui/Icons'

import RealTimeNotifications from '../components/notifications/RealTimeNotifications'
import EmailAlertSettings from '../components/notifications/EmailAlertSettings'
import DashboardAlerts from '../components/notifications/DashboardAlerts'
import ThresholdMonitoring from '../components/notifications/ThresholdMonitoring'
import AlertHistory from '../components/notifications/AlertHistory'
import NotificationPreferences from '../components/notifications/NotificationPreferences'

export default function Notifications() {
	// Notifications analytics data
	const notificationsData = useMemo(() => {
		return {
			totalNotifications: 1247,
			unreadNotifications: 23,
			criticalAlerts: 5,
			avgResponseTime: 4.2,
			activeSubscribers: 156,
			deliveryRate: 98.7,
			recentNotifications: [
				{ title: 'Budget Threshold Exceeded', type: 'Critical', time: '2 minutes ago', category: 'Budget' },
				{ title: 'New Client Registration', type: 'Info', time: '15 minutes ago', category: 'Client' },
				{ title: 'System Maintenance Scheduled', type: 'Warning', time: '1 hour ago', category: 'System' },
				{ title: 'Invoice Payment Received', type: 'Success', time: '2 hours ago', category: 'Financial' },
				{ title: 'Ticket SLA Breach Alert', type: 'Critical', time: '3 hours ago', category: 'Support' }
			],
			notificationsByType: [
				{ type: 'Critical', count: 15, color: '#ef4444' },
				{ type: 'Warning', count: 42, color: '#f59e0b' },
				{ type: 'Info', count: 89, color: '#3b82f6' },
				{ type: 'Success', count: 67, color: '#10b981' }
			]
		}
	}, [])

	const getTypeColor = (type) => {
		const colors = {
			'Critical': 'bg-red-100 text-red-800',
			'Warning': 'bg-yellow-100 text-yellow-800',
			'Info': 'bg-blue-100 text-blue-800',
			'Success': 'bg-green-100 text-green-800'
		}
		return colors[type] || 'bg-gray-100 text-gray-800'
	}

	return (
		<div className="space-y-6">
			{/* Header */}
			<div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
				<div>
					<h1 className="text-3xl font-bold bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
						🔔 Notifications & Alerts
					</h1>
					<p className="text-gray-600 mt-1">Manage notifications, alerts, and communication preferences</p>
				</div>
				
				<div className="flex flex-wrap gap-3">
					<Button variant="outline" size="sm" className="flex items-center gap-2">
						<DocumentTextIcon className="h-4 w-4" />
						Export Logs
					</Button>
					<Button variant="outline" size="sm" className="flex items-center gap-2">
						<CalendarIcon className="h-4 w-4" />
						Schedule Report
					</Button>
					<Button variant="primary" size="sm" className="flex items-center gap-2 bg-gradient-to-r from-indigo-600 to-purple-600">
						<RefreshIcon className="h-4 w-4" />
						Refresh All
					</Button>
				</div>
			</div>

			{/* KPI Cards */}
			<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
				<KPICard
					title="Total Notifications"
					value={notificationsData.totalNotifications}
					change={15.3}
					changeType="positive"
					format="number"
					icon={DocumentTextIcon}
					iconColor="indigo"
				/>
				<KPICard
					title="Unread"
					value={notificationsData.unreadNotifications}
					change={-12.8}
					changeType="positive"
					format="number"
					icon={ExclamationTriangleIcon}
					iconColor="orange"
				/>
				<KPICard
					title="Critical Alerts"
					value={notificationsData.criticalAlerts}
					change={-25.4}
					changeType="positive"
					format="number"
					icon={ExclamationTriangleIcon}
					iconColor="red"
				/>
				<KPICard
					title="Avg Response Time"
					value={notificationsData.avgResponseTime}
					change={-8.7}
					changeType="positive"
					format="decimal"
					icon={ClockIcon}
					iconColor="blue"
					suffix="min"
				/>
				<KPICard
					title="Active Subscribers"
					value={notificationsData.activeSubscribers}
					change={7.2}
					changeType="positive"
					format="number"
					icon={UsersIcon}
					iconColor="green"
				/>
				<KPICard
					title="Delivery Rate"
					value={notificationsData.deliveryRate}
					change={2.1}
					changeType="positive"
					format="decimal"
					icon={CheckIcon}
					iconColor="emerald"
					suffix="%"
				/>
			</div>

			{/* Main Content Grid */}
			<div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
				{/* Left Column - Real-time & Alerts */}
				<div className="xl:col-span-2 space-y-6">
					{/* Enhanced Real-time Notifications */}
					<div className="bg-gradient-to-br from-indigo-50 to-white rounded-xl border border-gray-200 p-6 shadow-sm">
						<div className="flex items-center justify-between mb-4">
							<h2 className="text-lg font-semibold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
								🔴 Live Notifications
							</h2>
							<div className="flex items-center gap-2">
								<div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
								<span className="text-xs text-gray-500">Live</span>
							</div>
						</div>
						
						<div className="space-y-3 max-h-80 overflow-y-auto">
							{notificationsData.recentNotifications.map((notification, index) => (
								<div key={index} className="flex items-center justify-between p-4 bg-white rounded-lg border border-gray-200 hover:border-indigo-300 transition-all hover:shadow-sm">
									<div className="flex items-center gap-3">
										<div className="flex-shrink-0">
											<div className={`w-8 h-8 rounded-full flex items-center justify-center ${
												notification.type === 'Critical' ? 'bg-red-100' :
												notification.type === 'Warning' ? 'bg-yellow-100' :
												notification.type === 'Success' ? 'bg-green-100' : 'bg-blue-100'
											}`}>
												<ExclamationTriangleIcon className={`h-4 w-4 ${
													notification.type === 'Critical' ? 'text-red-600' :
													notification.type === 'Warning' ? 'text-yellow-600' :
													notification.type === 'Success' ? 'text-green-600' : 'text-blue-600'
												}`} />
											</div>
										</div>
										<div className="flex-1">
											<p className="font-medium text-gray-900 text-sm">{notification.title}</p>
											<p className="text-xs text-gray-500">{notification.category} • {notification.time}</p>
										</div>
									</div>
									<div className="flex items-center gap-2">
										<span className={`px-2 py-1 rounded-full text-xs font-medium ${getTypeColor(notification.type)}`}>
											{notification.type}
										</span>
										<button className="text-gray-400 hover:text-gray-600 transition-colors">
											<XMarkIcon className="h-4 w-4" />
										</button>
									</div>
								</div>
							))}
						</div>
					</div>

					{/* Enhanced Dashboard Alerts */}
					<div className="bg-gradient-to-br from-orange-50 to-white rounded-xl border border-gray-200 p-6 shadow-sm">
						<h2 className="text-lg font-semibold bg-gradient-to-r from-orange-600 to-red-600 bg-clip-text text-transparent mb-4">
							⚠️ System Alerts
						</h2>
						
						<div className="grid grid-cols-1 md:grid-cols-2 gap-4">
							{[
								{ title: 'High CPU Usage', value: '87%', status: 'critical', trend: 'up' },
								{ title: 'Memory Usage', value: '64%', status: 'warning', trend: 'stable' },
								{ title: 'Disk Space', value: '23%', status: 'normal', trend: 'down' },
								{ title: 'Network Latency', value: '45ms', status: 'normal', trend: 'stable' }
							].map((alert, index) => (
								<div key={index} className="bg-white rounded-lg border border-gray-200 p-4">
									<div className="flex items-center justify-between mb-2">
										<span className="text-sm font-medium text-gray-700">{alert.title}</span>
										<span className={`px-2 py-1 rounded-full text-xs font-medium ${
											alert.status === 'critical' ? 'bg-red-100 text-red-800' :
											alert.status === 'warning' ? 'bg-yellow-100 text-yellow-800' : 'bg-green-100 text-green-800'
										}`}>
											{alert.status}
										</span>
									</div>
									<div className="flex items-center justify-between">
										<span className="text-lg font-bold text-gray-900">{alert.value}</span>
										<div className="flex items-center gap-1">
											{alert.trend === 'up' && <TrendingUpIcon className="h-4 w-4 text-red-500" />}
											{alert.trend === 'down' && <TrendingDownIcon className="h-4 w-4 text-green-500" />}
											{alert.trend === 'stable' && <div className="w-4 h-0.5 bg-gray-400 rounded"></div>}
										</div>
									</div>
								</div>
							))}
						</div>
					</div>

					{/* Enhanced Threshold Monitoring */}
					<div className="bg-gradient-to-br from-purple-50 to-white rounded-xl border border-gray-200 p-6 shadow-sm">
						<h2 className="text-lg font-semibold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent mb-4">
							📊 Threshold Monitoring
						</h2>
						
						<div className="space-y-4">
							{[
								{ name: 'Revenue Target', current: 87, threshold: 90, unit: '%' },
								{ name: 'Response Time', current: 2.3, threshold: 3.0, unit: 's' },
								{ name: 'Error Rate', current: 0.8, threshold: 1.0, unit: '%' },
								{ name: 'User Satisfaction', current: 94, threshold: 85, unit: '%' }
							].map((metric, index) => (
								<div key={index} className="bg-white rounded-lg border border-gray-200 p-4">
									<div className="flex items-center justify-between mb-2">
										<span className="text-sm font-medium text-gray-700">{metric.name}</span>
										<span className="text-xs text-gray-500">Target: {metric.threshold}{metric.unit}</span>
									</div>
									<div className="w-full bg-gray-200 rounded-full h-2 mb-2">
										<div 
											className={`h-2 rounded-full transition-all duration-300 ${
												metric.current >= metric.threshold ? 'bg-green-500' : 'bg-yellow-500'
											}`}
											style={{ width: `${Math.min((metric.current / metric.threshold) * 100, 100)}%` }}
										></div>
									</div>
									<div className="flex justify-between text-xs text-gray-500">
										<span>Current: {metric.current}{metric.unit}</span>
										<span className={metric.current >= metric.threshold ? 'text-green-600' : 'text-yellow-600'}>
											{metric.current >= metric.threshold ? '✓ On Target' : '⚠ Below Target'}
										</span>
									</div>
								</div>
							))}
						</div>
					</div>
				</div>

				{/* Right Column - Settings & History */}
				<div className="space-y-6">
					{/* Enhanced Alert History */}
					<div className="bg-gradient-to-br from-blue-50 to-white rounded-xl border border-gray-200 p-6 shadow-sm">
						<h2 className="text-lg font-semibold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent mb-4">
							📋 Alert History
						</h2>
						
						<div className="space-y-3 max-h-64 overflow-y-auto">
							{[
								{ time: '2 hours ago', message: 'Budget threshold exceeded', type: 'Critical' },
								{ time: '4 hours ago', message: 'New user registration', type: 'Info' },
								{ time: '6 hours ago', message: 'System maintenance completed', type: 'Success' },
								{ time: '8 hours ago', message: 'High memory usage detected', type: 'Warning' },
								{ time: '1 day ago', message: 'Backup completed successfully', type: 'Success' }
							].map((item, index) => (
								<div key={index} className="flex items-start gap-3 p-3 bg-white rounded-lg border border-gray-200">
									<div className={`w-2 h-2 rounded-full mt-2 flex-shrink-0 ${
										item.type === 'Critical' ? 'bg-red-500' :
										item.type === 'Warning' ? 'bg-yellow-500' :
										item.type === 'Success' ? 'bg-green-500' : 'bg-blue-500'
									}`}></div>
									<div className="flex-1">
										<p className="text-sm text-gray-900">{item.message}</p>
										<p className="text-xs text-gray-500">{item.time}</p>
									</div>
								</div>
							))}
						</div>
					</div>

					{/* Enhanced Email Alert Settings */}
					<div className="bg-gradient-to-br from-green-50 to-white rounded-xl border border-gray-200 p-6 shadow-sm">
						<h2 className="text-lg font-semibold bg-gradient-to-r from-green-600 to-teal-600 bg-clip-text text-transparent mb-4">
							📧 Email Settings
						</h2>
						
						<div className="space-y-4">
							{[
								{ label: 'Critical Alerts', enabled: true },
								{ label: 'System Updates', enabled: true },
								{ label: 'Weekly Reports', enabled: false },
								{ label: 'Marketing Updates', enabled: false }
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

					{/* Enhanced Notification Preferences */}
					<div className="bg-gradient-to-br from-rose-50 to-white rounded-xl border border-gray-200 p-6 shadow-sm">
						<h2 className="text-lg font-semibold bg-gradient-to-r from-rose-600 to-pink-600 bg-clip-text text-transparent mb-4">
							⚙️ Preferences
						</h2>
						
						<div className="space-y-4">
							<div className="bg-white rounded-lg border border-gray-200 p-4">
								<label className="text-sm font-medium text-gray-700 mb-2 block">Notification Frequency</label>
								<select className="w-full p-2 border border-gray-300 rounded-lg text-sm">
									<option>Immediate</option>
									<option>Every 15 minutes</option>
									<option>Hourly</option>
									<option>Daily</option>
								</select>
							</div>
							
							<div className="bg-white rounded-lg border border-gray-200 p-4">
								<label className="text-sm font-medium text-gray-700 mb-2 block">Quiet Hours</label>
								<div className="grid grid-cols-2 gap-2">
									<input type="time" className="p-2 border border-gray-300 rounded-lg text-sm" defaultValue="22:00" />
									<input type="time" className="p-2 border border-gray-300 rounded-lg text-sm" defaultValue="08:00" />
								</div>
							</div>
							
							<button className="w-full bg-gradient-to-r from-rose-600 to-pink-600 text-white py-2 px-4 rounded-lg text-sm font-medium hover:from-rose-700 hover:to-pink-700 transition-all">
								Save Preferences
							</button>
						</div>
					</div>
				</div>
			</div>
		</div>
	)
}
