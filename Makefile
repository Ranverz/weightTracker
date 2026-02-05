.PHONY: help setup up down build logs clean test lint format fmt check prod

help:
	@echo "Targets:"
	@echo "  make setup     - create .env from .env.example"
	@echo "  make up        - start dev stack (docker compose)"
	@echo "  make down      - stop dev stack"
	@echo "  make build     - rebuild images"
	@echo "  make logs      - tail logs"
	@echo "  make clean     - remove containers and volumes"
	@echo "  make test      - run backend tests"
	@echo "  make lint      - run ruff"
	@echo "  make format    - run black"
	@echo "  make check     - run lint + tests"
	@echo "  make prod      - start production stack"

up:
	docker compose up --build

down:
	docker compose down

build:
	docker compose build

logs:
	docker compose logs -f

clean:
	docker compose down -v

test:
	cd backend && pytest

lint:
	cd backend && ruff check .

format fmt:
	cd backend && black .

check: lint test

prod:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
setup:
	@test -f .env || cp .env.example .env
