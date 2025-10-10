import { Routes, Route } from 'react-router-dom'
import InvoiceList from '../components/financial/invoices/InvoiceList'
import InvoiceDetail from '../components/financial/invoices/InvoiceDetail'
import CreateInvoice from '../components/financial/invoices/CreateInvoice'
import BulkInvoiceOperations from '../components/financial/invoices/BulkInvoiceOperations'

export default function Invoices() {
	return (
		<div className="space-y-6">
			<div className="flex items-center justify-between">
				<h1 className="text-2xl font-semibold">Invoices</h1>
			</div>
			<CreateInvoice />
			<BulkInvoiceOperations />
			<Routes>
				<Route index element={<InvoiceList />} />
				<Route path=":id" element={<InvoiceDetail />} />
			</Routes>
		</div>
	)
}
