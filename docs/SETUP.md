# Setup Guide

## Prerequisites

- Python 3.11 or higher
- pip
- MongoDB Atlas account (or local MongoDB)
- Git

## Local installation

```bash
# 1. Clone and enter project
git clone <repo-url>
cd habits-main

# 2. Create virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 3. Install dependencies
pip install -r backend/requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your MongoDB URI
```

## Environment file

```env
MONGODB_URI=mongodb+srv://<user>:<pass>@<cluster>.mongodb.net/
MONGODB_DB_NAME=habitplatform
MONGODB_TIMEOUT_MS=5000
```

If `.env` is absent, the app falls back to `mongodb://localhost:27017/`.
For Atlas or any remote database, always set `MONGODB_URI`.

## Running the application

```bash
# Both backend (8080) and frontend (3000)
python dev.py

# Custom ports
python dev.py --backend-port 9090 --frontend-port 4000

# Backend only
uvicorn backend.main:app --reload --port 8080

# From project root (Windows PowerShell)
python -m uvicorn backend.main:app --reload --port 8080
```

## Verifying the setup

```bash
# Health check
curl http://127.0.0.1:8080/health
# Expected: {"status":"ok","database":"connected"}

# API docs
# Open in browser: http://127.0.0.1:8080/docs
```

## Running tests

```bash
# All tests
python -m pytest tests/ -v

# Specific file
python -m pytest tests/test_user_registration.py -v

# With coverage (install pytest-cov first)
pip install pytest-cov
python -m pytest tests/ --cov=backend --cov-report=term-missing
```

## Project structure quick reference

```
habits-main/
├── backend/          # FastAPI application
│   ├── main.py       # Entry point, Container, app factory
│   ├── requirements.txt
│   ├── controllers/  # HTTP layer (routes, request validation)
│   ├── business_logic/services/  # Business logic
│   ├── repositories/ # MongoDB data access
│   └── domain/models/ # Pydantic schemas
├── frontend/
│   └── site/         # Static files served at /static
├── tests/            # Unit tests
├── dev.py            # Dev runner (backend + frontend)
├── .env.example      # Environment template
├── pytest.ini        # Test configuration
├── CLAUDE.md         # AI assistant guide
└── docs/             # This documentation
```

## Common issues

**`ModuleNotFoundError: No module named 'backend'`**
Run from the project root (`habits-main/`), not from inside `backend/`.

**`pymongo.errors.ServerSelectionTimeoutError`**
Check your `MONGODB_URI` in `.env`. Ensure your IP is whitelisted in MongoDB Atlas.

**`StaticFiles directory does not exist`**
The `frontend/site/` directory must exist. It's served at `/static`.

**Tests fail with import errors**
Ensure you're running `python -m pytest` (not just `pytest`) from the project root.
