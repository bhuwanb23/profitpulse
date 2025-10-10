import ServiceCatalog from '../components/clients/ServiceCatalog'
import ClientServices from '../components/clients/ClientServices'
import { useParams } from 'react-router-dom'

export default function ClientServicesPage() {
	const { id } = useParams()
	const clientId = id || 'c1'
	return (
		<div className="space-y-6">
			<div className="flex items-center justify-between">
				<h1 className="text-2xl font-semibold">Client Services</h1>
			</div>
			<div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
				<ServiceCatalog />
				<ClientServices clientId={clientId} />
			</div>
		</div>
	)
}
