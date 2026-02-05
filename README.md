 # WeightTracker

Production‑style reference project for a Telegram Mini App + backend service.

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

## Notes
- This is an educational, “corporate‑style” codebase: clean structure, clear boundaries, readable code.
- If you want production‑grade auth, add Telegram `initData` verification on the backend.
