# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Run Commands

### Backend + Database (Docker)
```bash
docker compose --profile dev up --build    # Flask dev server with live reload + Postgres
docker compose --profile dev down
docker compose --profile prod up --build   # Gunicorn (2 workers) + Postgres
```

### Frontend (run separately from backend)
```bash
cd frontend && pnpm install && pnpm dev    # Dev server at http://localhost:3000
pnpm build                                 # Production build
pnpm preview                               # Preview production build
```

### Linting & Type Checking
```bash
cd frontend && pnpm run lint               # ESLint check
cd frontend && pnpm run lint --fix         # ESLint auto-fix
cd frontend && pnpm run typecheck          # Nuxt type checking
```

### Testing
```bash
# Route tests (requires running backend at localhost:8000)
BASE_URL=http://localhost:8000 pytest tests/backend_client -q

# Unit tests
pytest tests/unit
```
Test files must be named `test_*.py`. Route tests go in `tests/backend_client/`, unit tests in `tests/unit/`.

## Architecture

**Two-service system**: Flask API (`backend/`) + Nuxt 4 frontend (`frontend/`), orchestrated by Docker Compose with PostgreSQL 15.

### Backend (`backend/app/`)
- **App factory**: `create_app()` in `__init__.py` configures Flask, CORS, logging, and registers route blueprints.
- **Service layer pattern**: Routes (`routes/`) delegate to business logic in `services/`. Routes handle HTTP concerns; services handle DB logic.
- **Database**: SQLAlchemy 2.0 with `psycopg` driver. `db.py` manages engine creation, connection pooling (10+10 overflow), session context manager (`session_scope()`), and uses PostgreSQL advisory locks for safe concurrent table creation on startup.
- **Models**: `ShortURL` (short_id, original_url) and `NewsletterSubscriber` (email) in `models.py`. Tables auto-created on startup.
- **Short IDs**: 6-character uppercase hex, generated in `services/shortener.py`. Same URL always returns same short ID (idempotent).

### Frontend (`frontend/`)
- **Nuxt 4** with `@nuxt/ui` component library, `@nuxt/content` for CMS, TypeScript throughout.
- **Auth**: Better Auth (`server/lib/auth.ts`) with email OTP (via Resend) and Google OAuth. Client setup in `app/lib/auth-client.ts`.
- **Pages**: `index.vue` (URL shortener + QR code generator), `login.vue` (email OTP + Google OAuth two-step flow).
- **Layouts**: `default.vue` (header/footer) and `auth.vue` (centered card).
- **Runtime config**: `backendBaseUrl` and `mainUrl` from environment variables.

### Deployment & Infrastructure
- Railway handles CD for both services. GitHub Actions handle CI (backend Docker build + pytest, frontend lint + typecheck + build).
- Cloudflare Worker proxies `exq.io/<id>` to the API; DNS managed by Cloudflare.
- `SHORT_HOST` env var controls the host in generated short-link URLs.

## Key Environment Variables

**Backend**: `DATABASE_URL`, `SECRET_KEY`, `SHORT_HOST`, `SESSION_COOKIE_SAMESITE`, `SESSION_COOKIE_SECURE`, `DB_POOL_MAX`, `DB_CONNECT_RETRIES`

**Frontend/Auth**: `FRONTEND_BASE_URL`, `BACKEND_BASE_URL`, `DATABASE_URL`, `BETTER_AUTH_URL`, `BETTER_AUTH_TRUSTED_ORIGINS`, `RESEND_API_KEY`, `RESEND_FROM`, `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GTM_ID`

**IMPORTANT — Adding new frontend env vars**: Railway injects env vars at build time via Docker build args. Every new frontend env var **must** be added in three places:
1. `frontend/.env.example` — placeholder for local dev
2. `frontend/nuxt.config.ts` — `runtimeConfig` (public or private)
3. `frontend/Dockerfile` — as an `ARG`+`ENV` pair in the `build` stage (before `RUN pnpm run build`), following the existing pattern:
   ```dockerfile
   ARG MY_NEW_VAR
   ENV MY_NEW_VAR=$MY_NEW_VAR
   ```
   Without this, the env var will be undefined during the Nuxt build on Railway.

## Coding Conventions
- 2-space indentation everywhere (backend and frontend)
- Python: snake_case for modules and functions
- Frontend: Nuxt defaults + ESLint config in `frontend/eslint.config.mjs` (Stylistic rules: no comma dangle, 1tbs brace style)
- Commit messages: short, lowercase fragments (e.g., "swagger dev only", "linter fix")
