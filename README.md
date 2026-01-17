# Link Shortener V1

## Description

Link Shortener now consists of a Flask + PostgreSQL API paired with a modern Nuxt 4 frontend. The API generates six‑character uppercase hex IDs and stores mappings in Postgres for durability across restarts. A Nuxt UI on `frontend/` provides a clean interface where users paste long URLs and immediately receive a short link and QR code. The API can be deployed separately behind a `api.exq.io` subdomain with a `SHORT_HOST` environment variable controlling the host printed in responses, while the frontend runs at `exq.io`. Both services are continuously deployed to Railway, and Cloudflare manages DNS and proxies short‑link hits on `exq.io/<id>` to the API via a Worker. Docker/Compose workflows are provided, and GitHub Actions handle CI while Railway handles CD.

## Setup

_Visit `http://localhost:8000/ping` (API) and `http://localhost:3000` (frontend) to verify the services are up. In production the API lives at `https://api.exq.io` and the frontend at `https://exq.io`._

### Production Environment — Gunicorn Server (multiple workers)

```bash
docker compose --profile prod up --build
# later
docker compose --profile prod down
```

### Development Environment — Live Reload (Flask)

```bash
docker compose --profile dev up --build
# later
docker compose --profile dev down
```

### Frontend

Frontend is intended to be booted up separately. Check its README for more info.

---

The backend now uses SQLAlchemy with the `psycopg` driver. `DATABASE_URL` can be provided as `postgresql://...` or `postgresql+psycopg://...`; if you omit `+psycopg`, it will be added automatically.

## Requirements
  - Docker and Docker Compose orchestrating both backend and database containers (PostgreSQL 15).
  - GitHub Actions powers the CI workflows stored in .github/workflows, while CD is handled entirely by Railway even though no extra deployment code exists in the repo.
  - Node.js 18+ and pnpm for the Nuxt 4 frontend.
  - A Cloudflare account to manage DNS and the Worker that proxies exq.io/\<id\> to the API.

## Features
  - Feature 1: Instant URL Shortening: GET /shorten?url=... returns a six‑character uppercase hex ID; the same long URL always returns the same ID.
  - Feature 2: Built‑in Nuxt 4 Frontend: The index route on the frontend lets you paste a link, get a short URL and see a dowloadable QR code.
  - Feature 3: API and Frontend on Railway: The backend and frontend run on separate Railway services (api.exq.io and exq.io).
  - Feature 4: Cloudflare Integration: DNS is managed by Cloudflare, and a Worker proxies requests like https://exq.io/\<id\> to the API while the API responds with a 301 redirect to the original long URL. Custom domains and SSL certificates are handled by Cloudflare.

## API
  - `GET /ping` returns a simple health payload.
  - `GET /shorten?url=` shortens a URL and returns `original_url`, `short_id`, and a `short_url`.
  - `POST /newsletter/subscribe` accepts `{"email": "you@example.com"}`, returns `201` when a new record is created and `200` if the address was already subscribed.
  - `POST /auth/register` accepts `{"email": "you@example.com", "password": "..."}` and creates a user session.
  - `POST /auth/login` accepts `{"email": "you@example.com", "password": "...", "remember": true}` and returns the current user.
  - `POST /auth/logout` clears the current session.
  - `GET /auth/me` returns the current user when logged in.
  - `GET /<short_id>` redirects to the original URL for that short id.
  - `GET /debug/log-stores` dumps the most recent 100 stored URLs.

## Git

The main branch holds the latest stable version of the application.

## Success Criteria
  - Criteria 1: The Compose stack builds successfully, the backend and frontend route checks remain green, /ping stays healthy, /shorten persists/reuses mappings in PostgreSQL, the Nuxt frontend displays and shortens links correctly, CI checks remain green, Railway deploys both services, and the Cloudflare Worker proxies short links properly.
