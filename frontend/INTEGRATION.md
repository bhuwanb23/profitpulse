# Frontend ↔ Backend Integration Plan

This document enumerates all tasks and sub‑tasks required to fully integrate the React frontend with the Node.js backend (and indirectly the AI/ML service via backend). Use this as the single source of truth for implementation and verification.

---

## 1) Environment & Configuration

- [ ] Configure API base URL
  - [ ] Ensure `VITE_API_URL` is set (defaults to `http://localhost:3000/api`)
  - [ ] Document environment setup in README and `.env.example`
  - [ ] Add build-time validation for missing `VITE_API_URL`
- [ ] HTTP client setup
  - [ ] Centralize axios instance in `src/services/api.js`
  - [ ] Request interceptor: inject `Authorization: Bearer <JWT>`
  - [ ] Response interceptor: handle 401 (logout/refresh), 429 (retry/backoff), network errors
  - [ ] Add X-Request-ID passthrough if provided by backend
- [ ] Global error mapping
  - [ ] Normalize backend error schema to UI‐friendly messages
  - [ ] Standardize empty/partial data handling
  - [ ] Provide default fallbacks for non‑critical widgets

---

## 2) Authentication & Access Control

- [ ] Auth flows
  - [ ] Login → POST `/api/auth/login`
  - [ ] Register → POST `/api/auth/register`
  - [ ] Logout → POST `/api/auth/logout` (or client-only clear)
  - [ ] Get profile → GET `/api/users/me`
- [ ] Token lifecycle
  - [ ] Persist JWT securely (localStorage minimal, consider memory + refresh strategy)
  - [ ] Optional: implement refresh flow if backend supports it
  - [ ] Clear state on 401/invalid token
- [ ] Route protection
  - [ ] Protect app routes with `ProtectedRoute`
  - [ ] Hide/disable UI for unauthorized roles (RBAC in UI aligned with backend claims)

---

## 3) AI/ML Insights & Predictions (via Backend)

- [ ] Replace mock data with live API
  - [ ] AI Insights page: GET
    - [ ] `/api/ai/insights/profitability-genome`
    - [ ] `/api/ai/analytics/revenue-leaks`
    - [ ] `/api/ai/analytics/profitability-scores`
    - [ ] `/api/ai/analytics/recommendations`
  - [ ] Predictive analytics: GET
    - [ ] `/api/ai/predictions/revenue`
    - [ ] `/api/ai/predictions/churn`
    - [ ] `/api/ai/predictions/demand`
    - [ ] `/api/ai/predictions/budget`
    - [ ] `/api/ai/predictions/market`
    - [ ] `/api/ai/predictions/growth`
  - [ ] Model actions (POST)
    - [ ] `/api/ai/profitability` (request body mapping from UI)
    - [ ] `/api/ai/churn`
    - [ ] `/api/ai/revenue-leaks`
    - [ ] `/api/ai/pricing`
    - [ ] `/api/ai/budget`
    - [ ] `/api/ai/demand`
    - [ ] `/api/ai/anomalies`
- [ ] UI data mapping
  - [ ] Define mapping UI ↔ backend response for each widget
  - [ ] Support confidence, explanations, and fallback flags (if returned)
  - [ ] Show “Simulated/Fallback” badge if backend indicates fallback used
- [ ] Error/empty/loading states
  - [ ] Granular skeletons per card/chart
  - [ ] Distinguish soft errors (partial data) vs hard errors (block UI section)
  - [ ] Retry affordance for transient errors

---

## 4) Dashboard & Analytics

- [ ] Dashboard KPIs & charts
  - [ ] Replace mock with `/api/analytics/*` endpoints where applicable
  - [ ] Ensure tooltips/legends use backend units/scales
- [ ] Billing analytics
  - [ ] Wire to `/api/analytics/revenue-trends`, `/api/analytics/payment-status`, `/api/analytics/outstanding-payments`, `/api/analytics/billing-efficiency`, `/api/analytics/revenue-forecasting`, `/api/analytics/payment-methods`
  - [ ] Add pagination/sorting/filtering via query params
- [ ] Predictive charts
  - [ ] Integrate churn & demand data from backend predictions to charts
  - [ ] Align date/time axes and formatting

---

## 5) Clients & Services

- [ ] Clients
  - [ ] List: GET `/api/clients`
  - [ ] Detail: GET `/api/clients/:id`
  - [ ] Analytics: GET `/api/clients/:id/analytics`
  - [ ] Profitability: GET `/api/clients/:id/profitability`
- [ ] Services
  - [ ] Catalog/list: GET `/api/services`
  - [ ] Assign/Unassign: POST `/api/services/:id/assign`
  - [ ] Pricing updates: PUT `/api/services/:id/pricing`
- [ ] Forms & validation
  - [ ] Client create/update (align with backend validators)
  - [ ] Graceful error messages on validation failures

---

## 6) Tickets & Operations

- [ ] Tickets
  - [ ] List/filters: GET `/api/tickets`
  - [ ] CRUD: POST/PUT/DELETE `/api/tickets`
  - [ ] Status/time logs: PUT `/api/tickets/:id/status`, POST `/api/tickets/:id/time`
- [ ] Ticket analytics
  - [ ] Volume, resolution, categories, technician performance, SLA, satisfaction → `/api/tickets/analytics/*`
- [ ] Operations
  - [ ] Bulk ops/templates/routing/SLA monitor per routes in `routes/ticketOperations.js`
  - [ ] Error feedback + optimistic UI where safe (idempotent ops)

---

## 7) Invoices & Financials

- [ ] Invoices
  - [ ] List/detail: GET `/api/invoices`, `/api/invoices/:id`
  - [ ] Create/update/delete: POST/PUT/DELETE
  - [ ] Send/payment ops: `/api/invoices/:id/send`, `/api/invoices/:id/payment`
  - [ ] Bulk ops: `/api/invoices/bulk`
- [ ] Budgets
  - [ ] CRUD: `/api/budgets` + nested categories `/api/budgets/:id/categories`
  - [ ] Analytics/alerts: `/api/budgets/:id/alerts`, `/api/budgets/:id/expenses`
- [ ] Formatting
  - [ ] Currency/percent locale formatting centralized utility
  - [ ] Large lists virtualization if needed

---

## 8) Notifications & Reports

- [ ] Notifications
  - [ ] List/mark read: `/api/notifications`, `/api/notifications/:id/read`
  - [ ] Preferences & email settings: `/api/notifications/preferences`, `/api/notifications/email-settings`
  - [ ] Alerts feed on dashboard
- [ ] Reports
  - [ ] Templates/list: `/api/reports/templates`
  - [ ] Generate/export/schedule: `/api/reports/generate`, `/api/reports/:id/export`, `/api/reports/schedule`
  - [ ] Scheduled list/cancel: `/api/reports/scheduled`, `/api/reports/scheduled/:id`

---

## 9) Integrations Settings (Admin)

- [ ] SuperOps
  - [ ] Connect/status/sync/settings per `/api/integrations/superops/*`
  - [ ] Health checks & test buttons
- [ ] QuickBooks
  - [ ] Connect/status/sync/export/settings per `/api/integrations/quickbooks/*`
  - [ ] OAuth flow guidance in UI
- [ ] Zapier
  - [ ] Webhook config & test per `/api/integrations/zapier/*`

---

## 10) Data Access Patterns

- [ ] Fetch layer
  - [ ] Simple fetch hooks or React Query/SWR for caching + revalidation
  - [ ] Cache invalidation on mutations
  - [ ] Background refresh for dashboard
- [ ] Query params integration
  - [ ] Pagination/sort/filter synchronized to URL
  - [ ] Server-side validation feedback surfaced in UI

---

## 11) Error Handling & Resilience

- [ ] Error boundary coverage for pages/sections
- [ ] Standard network/retry policy (exponential backoff on idempotent GETs)
- [ ] Timeouts & cancellation (AbortController) for chart-heavy pages
- [ ] Empty state designs for all lists/charts

---

## 12) Security & Compliance

- [ ] Token storage & leak prevention (sanitize logs, avoid PII in console)
- [ ] Input sanitization for form fields (client‐side)
- [ ] Respect roles/permissions in UI (hide or disable prohibited actions)

---

## 13) Observability & Telemetry

- [ ] Correlation IDs
  - [ ] Propagate request IDs (if backend returns `X-Request-ID`)
  - [ ] Log critical user actions with request IDs
- [ ] Client metrics
  - [ ] Measure first load/TTI on key pages
  - [ ] Log API timing for large charts (debug only in dev)

---

## 14) Performance

- [ ] Code‑split heavy routes (analytics/reports)
- [ ] Virtualize long lists (invoices/tickets/clients when necessary)
- [ ] Memoize heavy chart data transforms

---

## 15) Realtime (Optional, Phase 2)

- [ ] WebSocket channel for
  - [ ] Live AI batch job status
  - [ ] Notifications/alerts stream
  - [ ] Health indicators

---

## 16) Testing

- [ ] Integration tests (frontend hitting backend dev server)
  - [ ] Auth happy/edge paths
  - [ ] Critical AI pages render with live data
  - [ ] Forms: validation, error handling, success states
- [ ] Visual checks for charts/cards under diverse datasets

---

## 17) Documentation

- [ ] API contracts matrix (UI field ↔ backend field ↔ AI meaning if applicable)
- [ ] Error codes & messages reference
- [ ] Local runbook: start backend, AI/ML, and frontend

---

## 18) Rollout & Feature Flags

- [ ] Gated release of AI features per route/section
- [ ] Progressive exposure (non‑AI features always on)

---

## Acceptance Criteria (Go/No‑Go)

- [ ] All listed pages load data from backend without mocks
- [ ] Error/empty/loading states verified for each section
- [ ] AI endpoints return and render without breaking UI; fallback state visible when applicable
- [ ] Authenticated routes blocked when unauthenticated; RBAC respected
- [ ] Basic integration tests pass locally


