# Running Anaida Space

This guide covers the script-based setup and run flow for both Windows and macOS/Linux.

---

## Prerequisites

- **Python 3.11+** — [python.org](https://www.python.org/downloads/)
- **MongoDB** — Atlas cluster (free tier works) or local MongoDB 6+

---

## Setup

Run once after cloning. Safe to re-run (idempotent).

**macOS / Linux**
```bash
bash setup.sh
```

**Windows (PowerShell)**
```powershell
.\setup.ps1
```

What it does:
1. Creates a `.venv/` virtual environment in the project root
2. Installs all Python dependencies from `backend/requirements.txt`
3. Copies `.env.example` → `.env` (only if `.env` does not already exist)

After setup, open `.env` and set your MongoDB connection string:

```
MONGODB_URI=mongodb+srv://<user>:<password>@<cluster>.mongodb.net/
```

---

## Run

**macOS / Linux**
```bash
bash run.sh
```

**Windows (PowerShell)**
```powershell
.\run.ps1
```

Starts both servers:

| Server | URL |
|--------|-----|
| FastAPI backend | `http://127.0.0.1:8080` |
| Static frontend | `http://127.0.0.1:3000` |
| Swagger docs | `http://127.0.0.1:8080/docs` |
| Frontend via backend | `http://127.0.0.1:8080/app` |

Pass port flags through to `dev.py`:
```bash
bash run.sh --backend-port 9090 --frontend-port 4000
```

Press `Ctrl+C` to stop both processes.

---

## Seed demo data

Populates MongoDB with a demo user and sample records so the dashboard has something to show on first run. Skips records that already exist (safe to re-run).

**macOS / Linux**
```bash
bash prefill.sh
```

**Windows (PowerShell)**
```powershell
.\prefill.ps1
```

After seeding, log in with:

| Field | Value |
|-------|-------|
| Email | `demo@anaida.space` |
| Password | `demo1234` |

To wipe all collections and re-seed from scratch:
```bash
.venv/bin/python seed.py --reset   # macOS/Linux
.\.venv\Scripts\python.exe seed.py --reset  # Windows
```

---

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MONGODB_URI` | *(required)* | MongoDB Atlas SRV or local URI |
| `MONGODB_DB_NAME` | `habitplatform` | Database name |
| `MONGODB_TIMEOUT_MS` | `5000` | Connection timeout in milliseconds |

---

## Notes

- All scripts must be run from the **project root** (`habits-main/`).
- On macOS/Linux, the `.sh` scripts do not need `chmod +x` — invoke them with `bash script.sh`.
- `dev.py` automatically creates a `frontend/site/img/` junction/symlink pointing to `frontend/img/` on first run, making images accessible from the static server without moving files.
- The `.venv/` directory and `.env` file are excluded from version control via `.gitignore`.
