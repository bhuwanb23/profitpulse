import UserProfile from '../components/settings/UserProfile'
import RolesPermissions from '../components/settings/RolesPermissions'
import TeamManagement from '../components/settings/TeamManagement'
import AccessControl from '../components/settings/AccessControl'
import ActivityLogs from '../components/settings/ActivityLogs'
import SecuritySettings from '../components/settings/SecuritySettings'
import SuperOpsSetup from '../components/settings/integrations/SuperOpsSetup'
import QuickBooksSetup from '../components/settings/integrations/QuickBooksSetup'
import ZapierWebhook from '../components/settings/integrations/ZapierWebhook'
import APIKeyManagement from '../components/settings/integrations/APIKeyManagement'
import SyncStatus from '../components/settings/integrations/SyncStatus'
import IntegrationTesting from '../components/settings/integrations/IntegrationTesting'
import OrganizationSettings from '../components/settings/system/OrganizationSettings'
import NotificationPreferences from '../components/settings/system/NotificationPreferences'
import ThemeCustomization from '../components/settings/system/ThemeCustomization'
import DataExport from '../components/settings/system/DataExport'
import BackupConfig from '../components/settings/system/BackupConfig'
import SystemHealth from '../components/settings/system/SystemHealth'

export default function Settings() {
	return (
		<div className="space-y-6">
			<h1 className="text-2xl font-semibold">Settings</h1>

			<div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
				<UserProfile />
				<OrganizationSettings />
				<RolesPermissions />
				<TeamManagement />
				<AccessControl />
				<ActivityLogs />
				<SecuritySettings />
				<NotificationPreferences />
				<ThemeCustomization />
				<DataExport />
				<BackupConfig />
				<SystemHealth />
			</div>

			<div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
				<SuperOpsSetup />
				<QuickBooksSetup />
				<ZapierWebhook />
				<APIKeyManagement />
				<SyncStatus />
				<IntegrationTesting />
			</div>
		</div>
	)
}
