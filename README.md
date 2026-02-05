# WeightTracker

Production‑style reference project for a Telegram Mini App + backend service.

## Tech Stack
- **Backend:** Python 3.11, Flask, psycopg (PostgreSQL)
- **Bot:** aiogram 3
- **DB:** PostgreSQL 15
- **Frontend:** Jinja templates, Chart.js, Telegram WebApp SDK
- **Infra:** Docker, Docker Compose, Nginx
- **Tooling:** Ruff, Black, Pytest, MyPy

**What’s inside**
- **backend/** — Flask web app (Mini App UI, data storage, stats)
- **bot/** — Telegram bot (launches the Mini App)
- **docker-compose.yml** — local development stack

---

## Quick start (Docker)
```bash
docker compose up --build
```

Backend is on:
- http://localhost:8000/miniapp

---

## перенос на другой ПК/сервер (полная копия)
```bash
git clone https://github.com/Ranverz/weightTracker.git
cd weightTracker
cp .env.example .env
```

Дальше открой `.env` и заполни реальные значения:
- `BOT_TOKEN`
- `WEBAPP_URL` (публичный URL, например ngrok)
- `DATABASE_URL`

Запуск:
```bash
docker compose up --build
```

## Environment variables
Create `.env` based on `.env.example` and set:

**Global**
- `DATABASE_URL` — Postgres connection string

**Bot**
- `BOT_TOKEN` — Telegram bot token
- `WEBAPP_URL` — public URL to your Mini App (ngrok, etc.)

---

## Project structure (backend)
```
backend/
  app/
    routes/        # HTTP routes / controllers
    services/      # business logic
    repositories/  # DB access
    schemas.py     # pydantic validation
    db.py          # connection helpers
    errors.py      # error handlers
    config.py      # app config
    static/        # JS/CSS
    templates/     # HTML templates
```

---

## Tests
```bash
cd backend
pytest
```

## Lint / format (optional)
```bash
cd backend
pip install -r requirements-dev.txt
ruff check .
black .
```

---

## Run without Docker (local)
```bash
# 1) create venv
python3.12 -m venv .venv
source .venv/bin/activate

# 2) export env vars
set -a
source .env
set +a

# 3) install deps
pip install -r backend/requirements.txt
pip install -r bot/requirements.txt

# 4) run backend
python -m backend.app.wsgi

# 5) run bot (separate terminal)
python -m bot.app.main
```

---

## Connect DB with DBeaver
If you use Docker:
- Host: `localhost`
- Port: `5432`
- Database: `weightdb`
- User: `postgres`
- Password: `postgres`

JDBC URL:
```
jdbc:postgresql://localhost:5432/weightdb
```

---

## Deploy on a server (Docker)
1) **Prepare server**
- Install Docker + Docker Compose
- Open ports: `80`, `443` (for HTTPS), and `22` (SSH)

2) **Clone and configure**
```bash
git clone https://github.com/Ranverz/weightTracker.git
cd weightTracker
cp .env.example .env
```
Edit `.env`:
- `BOT_TOKEN` — bot token
- `WEBAPP_URL` — your HTTPS domain (e.g. `https://app.example.com`)
- `DATABASE_URL` — keep default or use a managed DB

3) **Set Telegram domain**
In BotFather:
- `/setdomain` → choose your bot → set your HTTPS domain

4) **Run**
```bash
docker compose up -d --build
```

5) **Reverse proxy + HTTPS**
Use the provided `deploy/nginx.conf` and the production compose file:
```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

Then:
- Replace `your-domain.com` in `deploy/nginx.conf`
- Ensure SSL certs exist in `/etc/letsencrypt`

Telegram Mini Apps require **HTTPS** in production.

---

## Healthchecks & restarts
Production stack uses:
- `restart: unless-stopped`
- `/health` endpoint for backend
- `pg_isready` healthcheck for DB

## Notes
- This is an educational, “corporate‑style” codebase: clean structure, clear boundaries, readable code.
- If you want production‑grade auth, add Telegram `initData` verification on the backend.
