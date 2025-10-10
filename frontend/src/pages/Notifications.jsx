import RealTimeNotifications from '../components/notifications/RealTimeNotifications'
import EmailAlertSettings from '../components/notifications/EmailAlertSettings'
import DashboardAlerts from '../components/notifications/DashboardAlerts'
import ThresholdMonitoring from '../components/notifications/ThresholdMonitoring'
import AlertHistory from '../components/notifications/AlertHistory'
import NotificationPreferences from '../components/notifications/NotificationPreferences'

export default function Notifications() {
	return (
		<div className="space-y-6">
			<div className="flex items-center justify-between">
				<h1 className="text-2xl font-semibold">Notifications & Alerts</h1>
				<button className="bg-blue-600 text-white text-sm px-3 py-2 rounded-md hover:bg-blue-700">Refresh</button>
			</div>
			<div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
				<RealTimeNotifications />
				<DashboardAlerts />
				<ThresholdMonitoring />
				<AlertHistory />
				<EmailAlertSettings />
				<NotificationPreferences />
			</div>
		</div>
	)
}
