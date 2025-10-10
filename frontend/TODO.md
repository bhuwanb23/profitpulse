# SuperHack Frontend TODO

This is the working checklist for the React + Tailwind frontend. Tailwind will be set up by you; components already use Tailwind utility classes.

## Phase 1 — Foundation (Current)
- [x] Add React Router and base routes (dashboard, clients, tickets, invoices, analytics, settings)
- [x] Implement professional base layout (`header`, `sidebar`, `Outlet`)
- [x] Create starter pages with placeholders and Tailwind styles
- [ ] Install dependencies in frontend: `npm i react-router-dom`
- [ ] Verify Tailwind setup and global styles

## Phase 2 — Dashboard
- [ ] Replace chart placeholders with Recharts
- [ ] Metrics API wiring (revenue, clients, tickets, profitability)
- [ ] AI recommendations widget (list + accept/reject actions)

## Phase 3 — Clients
- [ ] Client list (search, filters, sort, pagination)
- [ ] Client detail page (overview, services, invoices, analytics tabs)
- [ ] Profitability bar and trends per client

## Phase 4 — Tickets
- [ ] Ticket list (status/priority filters, SLA indicators)
- [ ] Ticket detail page (activity, time entries)
- [ ] New ticket form with validation

## Phase 5 — Invoices
- [ ] Invoices table (status filters, date range)
- [ ] Invoice details with items
- [ ] Create invoice form

## Phase 6 — Analytics
- [ ] Revenue trends (line chart)
- [ ] Profitability analysis (bar/heatmap)
- [ ] Budget utilization (stacked bars)

## Phase 7 — Settings
- [ ] Profile form (name/email, save)
- [ ] Organization settings (plan, name)
- [ ] Integrations (SuperOps, QuickBooks placeholders)

## Shared Infrastructure
- [ ] API client with base URL (Axios) and interceptors
- [ ] Error boundary, global toasts, loading skeletons
- [ ] Helpers: currency/date/percent formatters
- [ ] Environment variables (`VITE_API_URL`)

## Quality
- [ ] Add ESLint/Prettier config
- [ ] Add Vitest + React Testing Library scaffolding
- [ ] Smoke tests for pages and layout

Notes:
- Data is mocked for now; wire to backend/SQLite later.
- Keep components accessible (labels, focus states, contrast).
