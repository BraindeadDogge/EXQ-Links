# Repository Guidelines

## Project Structure & Module Organization
- `backend/`: Flask API. Core code lives in `backend/app/` with `routes/`, `services/`, `models.py`, and `db.py`.
- `frontend/`: Nuxt 4 app (`app/`, `server/`, `content/`, `public/`) with its own README and tooling.
- `tests/`: pytest checks. Route tests in `tests/backend_client/`, unit tests in `tests/unit/`.
- Root: `docker-compose.yml` orchestrates backend + PostgreSQL; `README.md` describes the system.

## Build, Test, and Development Commands
- `docker compose --profile dev up --build`: run API + DB with Flask live reload.
- `docker compose --profile dev down`: stop dev stack.
- `docker compose --profile prod up --build`: run Gunicorn production profile locally.
- Frontend: `pnpm install`, `pnpm dev`, `pnpm build`, `pnpm preview`.
- Linting: `pnpm run lint` (check) and `pnpm run lint --fix` (auto-fix).
- Tests: `pytest tests/unit` and `BASE_URL=http://localhost:8000 pytest tests/backend_client`.

## Coding Style & Naming Conventions
- Indentation: 2 spaces in both backend and frontend (see `frontend/.editorconfig` and `backend/app/*`).
- Python: keep snake_case modules/functions (e.g., `shortener.py`, `get_or_create_short_id`).
- Frontend/TypeScript: follow Nuxt defaults and ESLint config in `frontend/eslint.config.mjs`.
- Keep Markdown readable; trailing whitespace is allowed in `*.md` per editorconfig.

## Testing Guidelines
- Framework: pytest (see `tests/README.md`).
- API route tests require a running backend; set `BASE_URL` to your local API.
- Name new tests `test_*.py` and place route checks under `tests/backend_client/`.

## Commit & Pull Request Guidelines
- Commit messages in history are short, lowercase fragments (e.g., “swagger dev only”, “linter fix”).
- PRs should include: a concise summary, commands run, and screenshots for UI changes.

## Configuration Tips
- Backend uses `DATABASE_URL` for Postgres and `SHORT_HOST` to control generated short-link hosts.
- Local defaults: API at `http://localhost:8000/ping`, frontend at `http://localhost:3000`.
