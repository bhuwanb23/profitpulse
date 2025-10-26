"""
Data Transformers
Transform API responses from SuperOps and QuickBooks to unified internal format
"""

import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class InternalTicket:
    """Internal ticket data structure"""
    id: str
    display_id: str
    subject: str
    description: Optional[str]
    status: str
    priority: str
    created_at: datetime
    updated_at: datetime
    first_response_time: Optional[datetime]
    resolution_time: Optional[datetime]
    sla_violated: bool
    technician_id: Optional[str]
    technician_name: Optional[str]
    requester_id: Optional[str]
    requester_name: Optional[str]
    client_id: Optional[str]
    client_name: Optional[str]
    service_type: Optional[str]
    category: Optional[str]
    subcategory: Optional[str]
    estimated_hours: Optional[float]
    actual_hours: Optional[float]
    billing_rate: Optional[float]
    total_cost: Optional[float]
    tags: List[str]
    custom_fields: Dict[str, Any]


@dataclass
class InternalClient:
    """Internal client data structure"""
    id: str
    name: str
    email: Optional[str]
    phone: Optional[str]
    address: Dict[str, str]
    industry: Optional[str]
    company_size: Optional[str]
    contract_type: Optional[str]
    contract_value: Optional[float]
    contract_start_date: Optional[datetime]
    contract_end_date: Optional[datetime]
    billing_frequency: Optional[str]
    payment_terms: Optional[str]
    primary_contact: Optional[str]
    secondary_contact: Optional[str]
    service_level: Optional[str]
    tags: List[str]
    custom_fields: Dict[str, Any]
    created_date: Optional[datetime]
    last_activity: Optional[datetime]


@dataclass
class InternalTechnician:
    """Internal technician data structure"""
    id: str
    name: str
    email: Optional[str]
    phone: Optional[str]
    role: Optional[str]
    department: Optional[str]
    skills: List[str]
    certifications: List[str]
    hourly_rate: Optional[float]
    availability: Optional[str]
    workload: Optional[float]
    performance_score: Optional[float]
    tickets_resolved: Optional[int]
    avg_resolution_time: Optional[float]
    customer_satisfaction: Optional[float]
    created_date: Optional[datetime]
    last_active: Optional[datetime]


@dataclass
class InternalInvoice:
    """Internal invoice data structure"""
    id: str
    invoice_number: str
    customer_id: str
    customer_name: str
    date: datetime
    due_date: Optional[datetime]
    amount: float
    tax_amount: Optional[float]
    total_amount: float
    balance_due: float
    status: str
    payment_terms: Optional[str]
    line_items: List[Dict[str, Any]]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


@dataclass
class InternalPayment:
    """Internal payment data structure"""
    id: str
    payment_number: str
    invoice_id: Optional[str]
    customer_id: str
    customer_name: str
    date: datetime
    amount: float
    payment_method: Optional[str]
    reference: Optional[str]
    status: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


@dataclass
class InternalExpense:
    """Internal expense data structure"""
    id: str
    expense_number: str
    vendor_id: Optional[str]
    vendor_name: Optional[str]
    date: datetime
    amount: float
    tax_amount: Optional[float]
    total_amount: float
    category: Optional[str]
    description: Optional[str]
    payment_method: Optional[str]
    status: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class DataTransformer:
    """Transform API responses to unified internal format"""
    
    @staticmethod
    def transform_superops_tickets(raw_data: List[Dict[str, Any]]) -> List[InternalTicket]:
        """Transform SuperOps ticket data to internal format"""
        try:
            transformed_tickets = []
            
            for ticket_data in raw_data:
                # Parse datetime fields
                created_at = DataTransformer._parse_datetime(ticket_data.get("createdTime"))
                updated_at = DataTransformer._parse_datetime(ticket_data.get("updatedTime"))
                first_response_time = DataTransformer._parse_datetime(ticket_data.get("firstResponseTime"))
                resolution_time = DataTransformer._parse_datetime(ticket_data.get("resolutionTime"))
                
                # Parse worklog time spent
                worklog_timespent = ticket_data.get("worklogTimespent", "0")
                actual_hours = None
                if worklog_timespent and worklog_timespent != "0":
                    try:
                        actual_hours = float(worklog_timespent) / 60.0  # Convert minutes to hours
                    except (ValueError, TypeError):
                        actual_hours = None
                
                # Determine SLA violation
                sla_violated = (
                    ticket_data.get("firstResponseViolated", False) or 
                    ticket_data.get("resolutionViolated", False)
                )
                
                # Extract technician info
                technician = ticket_data.get("technician", {})
                technician_id = technician.get("userId") if technician else None
                technician_name = technician.get("name") if technician else None
                
                # Extract requester info
                requester = ticket_data.get("requester", {})
                requester_id = requester.get("userId") if requester else None
                requester_name = requester.get("name") if requester else None
                
                # Extract site/client info
                site = ticket_data.get("site", {})
                client_id = site.get("id") if site else None
                client_name = site.get("name") if site else None
                
                # Extract custom fields
                custom_fields = {}
                raw_custom_fields = ticket_data.get("customFields", [])
                if isinstance(raw_custom_fields, list):
                    for field in raw_custom_fields:
                        if isinstance(field, dict) and "fieldName" in field and "fieldValue" in field:
                            custom_fields[field["fieldName"]] = field["fieldValue"]
                
                ticket = InternalTicket(
                    id=ticket_data.get("ticketId", ""),
                    display_id=ticket_data.get("displayId", ""),
                    subject=ticket_data.get("subject", ""),
                    description=None,  # Not available in GraphQL response
                    status=ticket_data.get("status", ""),
                    priority=ticket_data.get("priority", ""),
                    created_at=created_at,
                    updated_at=updated_at,
                    first_response_time=first_response_time,
                    resolution_time=resolution_time,
                    sla_violated=sla_violated,
                    technician_id=technician_id,
                    technician_name=technician_name,
                    requester_id=requester_id,
                    requester_name=requester_name,
                    client_id=client_id,
                    client_name=client_name,
                    service_type=None,  # Not available in GraphQL response
                    category=None,  # Not available in GraphQL response
                    subcategory=None,  # Not available in GraphQL response
                    estimated_hours=None,  # Not available in GraphQL response
                    actual_hours=actual_hours,
                    billing_rate=None,  # Not available in GraphQL response
                    total_cost=None,  # Not available in GraphQL response
                    tags=ticket_data.get("tags", []),
                    custom_fields=custom_fields
                )
                
                transformed_tickets.append(ticket)
            
            logger.info(f"Transformed {len(transformed_tickets)} SuperOps tickets")
            return transformed_tickets
            
        except Exception as e:
            logger.error(f"Failed to transform SuperOps tickets: {e}")
            return []
    
    @staticmethod
    def transform_superops_clients(raw_data: List[Dict[str, Any]]) -> List[InternalClient]:
        """Transform SuperOps client/site data to internal format"""
        try:
            transformed_clients = []
            
            for client_data in raw_data:
                # Parse datetime fields
                created_date = DataTransformer._parse_datetime(client_data.get("createdDate"))
                last_activity = DataTransformer._parse_datetime(client_data.get("lastActivity"))
                contract_start_date = DataTransformer._parse_datetime(client_data.get("contractStartDate"))
                contract_end_date = DataTransformer._parse_datetime(client_data.get("contractEndDate"))
                
                # Extract address
                address = {}
                raw_address = client_data.get("address", {})
                if isinstance(raw_address, dict):
                    address = {
                        "street": raw_address.get("line1", ""),
                        "city": raw_address.get("city", ""),
                        "state": raw_address.get("stateCode", ""),
                        "zip": raw_address.get("zipCode", ""),
                        "country": raw_address.get("countryCode", "")
                    }
                
                # Extract custom fields
                custom_fields = {}
                raw_custom_fields = client_data.get("customFields", [])
                if isinstance(raw_custom_fields, list):
                    for field in raw_custom_fields:
                        if isinstance(field, dict) and "fieldName" in field and "fieldValue" in field:
                            custom_fields[field["fieldName"]] = field["fieldValue"]
                
                client = InternalClient(
                    id=client_data.get("id", ""),
                    name=client_data.get("name", ""),
                    email=client_data.get("email"),
                    phone=client_data.get("contactNumber"),
                    address=address,
                    industry=client_data.get("industry"),
                    company_size=client_data.get("companySize"),
                    contract_type=client_data.get("contractType"),
                    contract_value=client_data.get("contractValue"),
                    contract_start_date=contract_start_date,
                    contract_end_date=contract_end_date,
                    billing_frequency=client_data.get("billingFrequency"),
                    payment_terms=client_data.get("paymentTerms"),
                    primary_contact=client_data.get("primaryContact"),
                    secondary_contact=client_data.get("secondaryContact"),
                    service_level=client_data.get("serviceLevel"),
                    tags=client_data.get("tags", []),
                    custom_fields=custom_fields,
                    created_date=created_date,
                    last_activity=last_activity
                )
                
                transformed_clients.append(client)
            
            logger.info(f"Transformed {len(transformed_clients)} SuperOps clients")
            return transformed_clients
            
        except Exception as e:
            logger.error(f"Failed to transform SuperOps clients: {e}")
            return []
    
    @staticmethod
    def transform_superops_technicians(raw_data: List[Dict[str, Any]]) -> List[InternalTechnician]:
        """Transform SuperOps technician data to internal format"""
        try:
            transformed_technicians = []
            
            for tech_data in raw_data:
                # Parse datetime fields
                created_date = DataTransformer._parse_datetime(tech_data.get("createdDate"))
                last_active = DataTransformer._parse_datetime(tech_data.get("lastActive"))
                
                # Extract department info
                department = None
                raw_department = tech_data.get("department", {})
                if isinstance(raw_department, dict):
                    department = raw_department.get("name")
                
                technician = InternalTechnician(
                    id=tech_data.get("userId", ""),
                    name=tech_data.get("name", ""),
                    email=tech_data.get("email"),
                    phone=tech_data.get("phone"),
                    role=None,  # Not available in GraphQL response
                    department=department,
                    skills=tech_data.get("skills", []),
                    certifications=tech_data.get("certifications", []),
                    hourly_rate=tech_data.get("hourlyRate"),
                    availability=tech_data.get("availability"),
                    workload=None,  # Not available in GraphQL response
                    performance_score=tech_data.get("performanceScore"),
                    tickets_resolved=tech_data.get("ticketsResolved"),
                    avg_resolution_time=tech_data.get("avgResolutionTime"),
                    customer_satisfaction=tech_data.get("customerSatisfaction"),
                    created_date=created_date,
                    last_active=last_active
                )
                
                transformed_technicians.append(technician)
            
            logger.info(f"Transformed {len(transformed_technicians)} SuperOps technicians")
            return transformed_technicians
            
        except Exception as e:
            logger.error(f"Failed to transform SuperOps technicians: {e}")
            return []
    
    @staticmethod
    def transform_quickbooks_invoices(raw_data: List[Dict[str, Any]]) -> List[InternalInvoice]:
        """Transform QuickBooks invoice data to internal format"""
        try:
            transformed_invoices = []
            
            for invoice_data in raw_data:
                # Parse datetime fields
                date = DataTransformer._parse_datetime(invoice_data.get("TxnDate"))
                due_date = DataTransformer._parse_datetime(invoice_data.get("DueDate"))
                created_at = DataTransformer._parse_datetime(invoice_data.get("MetaData", {}).get("CreateTime"))
                updated_at = DataTransformer._parse_datetime(invoice_data.get("MetaData", {}).get("LastUpdatedTime"))
                
                # Extract customer info
                customer_ref = invoice_data.get("CustomerRef", {})
                customer_id = customer_ref.get("value", "") if isinstance(customer_ref, dict) else ""
                customer_name = customer_ref.get("name", "") if isinstance(customer_ref, dict) else ""
                
                # Extract line items
                line_items = []
                raw_line_items = invoice_data.get("Line", [])
                if isinstance(raw_line_items, list):
                    for line in raw_line_items:
                        if isinstance(line, dict):
                            line_items.append({
                                "description": line.get("Description", ""),
                                "quantity": line.get("Qty", 1),
                                "rate": line.get("Rate", 0),
                                "amount": line.get("Amount", 0)
                            })
                
                # Determine status
                status = "Draft"
                if invoice_data.get("Balance", 0) == 0:
                    status = "Paid"
                elif invoice_data.get("Balance", 0) > 0:
                    status = "Unpaid"
                
                invoice = InternalInvoice(
                    id=invoice_data.get("Id", ""),
                    invoice_number=invoice_data.get("DocNumber", ""),
                    customer_id=customer_id,
                    customer_name=customer_name,
                    date=date,
                    due_date=due_date,
                    amount=invoice_data.get("TotalAmt", 0),
                    tax_amount=invoice_data.get("TaxAmt"),
                    total_amount=invoice_data.get("TotalAmt", 0),
                    balance_due=invoice_data.get("Balance", 0),
                    status=status,
                    payment_terms=invoice_data.get("PaymentTerms"),
                    line_items=line_items,
                    created_at=created_at,
                    updated_at=updated_at
                )
                
                transformed_invoices.append(invoice)
            
            logger.info(f"Transformed {len(transformed_invoices)} QuickBooks invoices")
            return transformed_invoices
            
        except Exception as e:
            logger.error(f"Failed to transform QuickBooks invoices: {e}")
            return []
    
    @staticmethod
    def transform_quickbooks_payments(raw_data: List[Dict[str, Any]]) -> List[InternalPayment]:
        """Transform QuickBooks payment data to internal format"""
        try:
            transformed_payments = []
            
            for payment_data in raw_data:
                # Parse datetime fields
                date = DataTransformer._parse_datetime(payment_data.get("TxnDate"))
                created_at = DataTransformer._parse_datetime(payment_data.get("MetaData", {}).get("CreateTime"))
                updated_at = DataTransformer._parse_datetime(payment_data.get("MetaData", {}).get("LastUpdatedTime"))
                
                # Extract customer info
                customer_ref = payment_data.get("CustomerRef", {})
                customer_id = customer_ref.get("value", "") if isinstance(customer_ref, dict) else ""
                customer_name = customer_ref.get("name", "") if isinstance(customer_ref, dict) else ""
                
                payment = InternalPayment(
                    id=payment_data.get("Id", ""),
                    payment_number=payment_data.get("PaymentRefNum", ""),
                    invoice_id=None,  # Not directly available in payment data
                    customer_id=customer_id,
                    customer_name=customer_name,
                    date=date,
                    amount=payment_data.get("TotalAmt", 0),
                    payment_method=payment_data.get("PaymentMethod"),
                    reference=payment_data.get("Reference"),
                    status=payment_data.get("Status", ""),
                    created_at=created_at,
                    updated_at=updated_at
                )
                
                transformed_payments.append(payment)
            
            logger.info(f"Transformed {len(transformed_payments)} QuickBooks payments")
            return transformed_payments
            
        except Exception as e:
            logger.error(f"Failed to transform QuickBooks payments: {e}")
            return []
    
    @staticmethod
    def transform_quickbooks_expenses(raw_data: List[Dict[str, Any]]) -> List[InternalExpense]:
        """Transform QuickBooks expense data to internal format"""
        try:
            transformed_expenses = []
            
            for expense_data in raw_data:
                # Parse datetime fields
                date = DataTransformer._parse_datetime(expense_data.get("TxnDate"))
                created_at = DataTransformer._parse_datetime(expense_data.get("MetaData", {}).get("CreateTime"))
                updated_at = DataTransformer._parse_datetime(expense_data.get("MetaData", {}).get("LastUpdatedTime"))
                
                # Extract vendor info
                vendor_ref = expense_data.get("VendorRef", {})
                vendor_id = vendor_ref.get("value") if isinstance(vendor_ref, dict) else None
                vendor_name = vendor_ref.get("name") if isinstance(vendor_ref, dict) else None
                
                expense = InternalExpense(
                    id=expense_data.get("Id", ""),
                    expense_number=expense_data.get("DocNumber", ""),
                    vendor_id=vendor_id,
                    vendor_name=vendor_name,
                    date=date,
                    amount=expense_data.get("TotalAmt", 0),
                    tax_amount=expense_data.get("TaxAmt"),
                    total_amount=expense_data.get("TotalAmt", 0),
                    category=expense_data.get("Category"),
                    description=expense_data.get("Description"),
                    payment_method=expense_data.get("PaymentMethod"),
                    status=expense_data.get("Status", ""),
                    created_at=created_at,
                    updated_at=updated_at
                )
                
                transformed_expenses.append(expense)
            
            logger.info(f"Transformed {len(transformed_expenses)} QuickBooks expenses")
            return transformed_expenses
            
        except Exception as e:
            logger.error(f"Failed to transform QuickBooks expenses: {e}")
            return []
    
    @staticmethod
    def transform_quickbooks_customers(raw_data: List[Dict[str, Any]]) -> List[InternalClient]:
        """Transform QuickBooks customer data to internal format"""
        try:
            transformed_customers = []
            
            for customer_data in raw_data:
                # Parse datetime fields
                created_at = DataTransformer._parse_datetime(customer_data.get("MetaData", {}).get("CreateTime"))
                updated_at = DataTransformer._parse_datetime(customer_data.get("MetaData", {}).get("LastUpdatedTime"))
                
                # Extract address
                address = {}
                raw_address = customer_data.get("BillAddr", {})
                if isinstance(raw_address, dict):
                    address = {
                        "street": raw_address.get("Line1", ""),
                        "city": raw_address.get("City", ""),
                        "state": raw_address.get("CountrySubDivisionCode", ""),
                        "zip": raw_address.get("PostalCode", ""),
                        "country": raw_address.get("Country", "")
                    }
                
                # Extract email
                email = None
                raw_email = customer_data.get("PrimaryEmailAddr", {})
                if isinstance(raw_email, dict):
                    email = raw_email.get("Address")
                
                # Extract phone
                phone = None
                raw_phone = customer_data.get("PrimaryPhone", {})
                if isinstance(raw_phone, dict):
                    phone = raw_phone.get("FreeFormNumber")
                
                customer = InternalClient(
                    id=customer_data.get("Id", ""),
                    name=customer_data.get("DisplayName", ""),
                    email=email,
                    phone=phone,
                    address=address,
                    industry=None,  # Not available in QuickBooks customer data
                    company_size=None,  # Not available in QuickBooks customer data
                    contract_type=None,  # Not available in QuickBooks customer data
                    contract_value=None,  # Not available in QuickBooks customer data
                    contract_start_date=None,  # Not available in QuickBooks customer data
                    contract_end_date=None,  # Not available in QuickBooks customer data
                    billing_frequency=None,  # Not available in QuickBooks customer data
                    payment_terms=customer_data.get("PaymentTerms"),
                    primary_contact=None,  # Not available in QuickBooks customer data
                    secondary_contact=None,  # Not available in QuickBooks customer data
                    service_level=None,  # Not available in QuickBooks customer data
                    tags=[],  # Not available in QuickBooks customer data
                    custom_fields={},  # Not available in QuickBooks customer data
                    created_date=created_at,
                    last_activity=updated_at
                )
                
                transformed_customers.append(customer)
            
            logger.info(f"Transformed {len(transformed_customers)} QuickBooks customers")
            return transformed_customers
            
        except Exception as e:
            logger.error(f"Failed to transform QuickBooks customers: {e}")
            return []
    
    @staticmethod
    def _parse_datetime(date_string: Optional[str]) -> Optional[datetime]:
        """Parse datetime string to datetime object"""
        if not date_string:
            return None
        
        try:
            # Try ISO format first
            if "T" in date_string:
                return datetime.fromisoformat(date_string.replace("Z", "+00:00"))
            
            # Try date only format
            return datetime.strptime(date_string, "%Y-%m-%d")
            
        except (ValueError, TypeError) as e:
            logger.warning(f"Failed to parse datetime '{date_string}': {e}")
            return None
    
    @staticmethod
    def calculate_metrics(transformed_data: Dict[str, List[Any]]) -> Dict[str, Any]:
        """Calculate metrics from transformed data"""
        try:
            metrics = {}
            
            # Ticket metrics
            tickets = transformed_data.get("tickets", [])
            if tickets:
                metrics["ticket_metrics"] = {
                    "total_tickets": len(tickets),
                    "open_tickets": len([t for t in tickets if t.status in ["Open", "In Progress", "Pending"]]),
                    "resolved_tickets": len([t for t in tickets if t.status in ["Resolved", "Closed"]]),
                    "sla_violations": len([t for t in tickets if t.sla_violated]),
                    "avg_resolution_time": DataTransformer._calculate_avg_resolution_time(tickets),
                    "tickets_by_priority": DataTransformer._group_by_priority(tickets)
                }
            
            # Financial metrics
            invoices = transformed_data.get("invoices", [])
            payments = transformed_data.get("payments", [])
            expenses = transformed_data.get("expenses", [])
            
            if invoices:
                metrics["financial_metrics"] = {
                    "total_revenue": sum(inv.total_amount for inv in invoices),
                    "outstanding_balance": sum(inv.balance_due for inv in invoices),
                    "total_invoices": len(invoices),
                    "paid_invoices": len([inv for inv in invoices if inv.status == "Paid"]),
                    "unpaid_invoices": len([inv for inv in invoices if inv.status == "Unpaid"])
                }
            
            if payments:
                metrics["payment_metrics"] = {
                    "total_payments": len(payments),
                    "total_payment_amount": sum(pay.amount for pay in payments),
                    "payments_by_method": DataTransformer._group_by_payment_method(payments)
                }
            
            if expenses:
                metrics["expense_metrics"] = {
                    "total_expenses": len(expenses),
                    "total_expense_amount": sum(exp.total_amount for exp in expenses),
                    "expenses_by_category": DataTransformer._group_by_category(expenses)
                }
            
            logger.info("Calculated metrics from transformed data")
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to calculate metrics: {e}")
            return {}
    
    @staticmethod
    def _calculate_avg_resolution_time(tickets: List[InternalTicket]) -> Optional[float]:
        """Calculate average resolution time in hours"""
        resolved_tickets = [t for t in tickets if t.resolution_time and t.created_at]
        if not resolved_tickets:
            return None
        
        total_time = 0
        for ticket in resolved_tickets:
            time_diff = ticket.resolution_time - ticket.created_at
            total_time += time_diff.total_seconds() / 3600  # Convert to hours
        
        return total_time / len(resolved_tickets)
    
    @staticmethod
    def _group_by_priority(tickets: List[InternalTicket]) -> Dict[str, int]:
        """Group tickets by priority"""
        priority_counts = {}
        for ticket in tickets:
            priority = ticket.priority or "Unknown"
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        return priority_counts
    
    @staticmethod
    def _group_by_payment_method(payments: List[InternalPayment]) -> Dict[str, int]:
        """Group payments by method"""
        method_counts = {}
        for payment in payments:
            method = payment.payment_method or "Unknown"
            method_counts[method] = method_counts.get(method, 0) + 1
        return method_counts
    
    @staticmethod
    def _group_by_category(expenses: List[InternalExpense]) -> Dict[str, float]:
        """Group expenses by category with amounts"""
        category_amounts = {}
        for expense in expenses:
            category = expense.category or "Unknown"
            category_amounts[category] = category_amounts.get(category, 0) + expense.total_amount
        return category_amounts
