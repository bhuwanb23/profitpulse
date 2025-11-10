# SuperHack Frontend (React + Vite)

## Environment Setup

- Node 18+
- pnpm/npm/yarn
- Backend running at `http://localhost:3000`

### Environment Variables

- `VITE_API_URL` (required in production)
  - Default (dev): `http://localhost:3000/api`
  - Example: `VITE_API_URL=http://localhost:3000/api`
  - In production builds, the build fails if `VITE_API_URL` is missing.

Create `.env` (or use OS env):
```
VITE_API_URL=http://localhost:3000/api
```

## Development

```
npm install
npm run dev
```

## Build

```
npm run build
```
The build validates that `VITE_API_URL` is present.

## HTTP Client

- Centralized axios instance: `src/services/api.js`
  - Injects `Authorization: Bearer <JWT>` when present
  - Adds `X-Correlation-ID` per request
  - Logs `X-Request-ID` in dev responses
  - Retries transient failures (429/network) with backoff
  - Normalizes errors to a consistent shape

