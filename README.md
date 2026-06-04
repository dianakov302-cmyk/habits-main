# Anaida Space

**Anaida Space** is an adaptive self-development platform. It creates personalized discipline systems through behavioral testing, structured habits, recovery cycles, and social accountability.

> Design philosophy: Apple × Notion × behavioral psychology. Premium minimalism, psychologically intelligent UX, dark-first.

---

## Quick start

### 1. Prerequisites

- Python 3.11 or newer
- pip
- A MongoDB Atlas cluster (or local MongoDB)

### 2. Clone & enter the project

```
git clone <repo-url>
cd habits-main
```

### 3. Create a virtual environment

```
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies

```
pip install -r backend/requirements.txt
```

### 5. Configure environment

```
cp .env.example .env
```

Open `.env` and set your MongoDB connection string:

```
MONGODB_URI=mongodb+srv://<user>:<password>@<cluster>.mongodb.net/
MONGODB_DB_NAME=habitplatform
MONGODB_TIMEOUT_MS=5000
```

If you skip this step the app falls back to `mongodb://localhost:27017/`.
Set `MONGODB_URI` for Atlas or any remote MongoDB instance.

### 6. Run the application

```
# Backend (port 8080) + static frontend (port 3000) together:
python dev.py

# Backend only:
python -m uvicorn backend.main:app --reload --port 8080

# Custom ports:
python dev.py --backend-port 9090 --frontend-port 4000
```

### 7. Open in browser

| URL | What |
|-----|------|
| `http://127.0.0.1:3000` | Frontend (landing + dashboard) |
| `http://127.0.0.1:8080/app` | Frontend served via backend |
| `http://127.0.0.1:8080/docs` | Swagger API docs |
| `http://127.0.0.1:8080/health` | Health check |

### 8. Run tests

**Unit tests** (no server needed):
```
pip install pytest
python -m pytest tests/ -v
```

**UI tests** (requires dev server running on port 3000):
```
pip install pytest-playwright
playwright install chromium
python dev.py &          # start server first
python -m pytest tests/test_ui.py -v
python -m pytest tests/test_ui.py -v --headed   # with visible browser
```

---

## Project structure

```
habits-main/
├── backend/                  # FastAPI application
│   ├── main.py               # App factory + DI Container
│   ├── requirements.txt      # Python dependencies
│   ├── controllers/          # HTTP routes + request validation
│   ├── business_logic/       # Services + interfaces (business logic)
│   ├── repositories/         # MongoDB data access
│   └── domain/models/        # Pydantic schemas
├── frontend/
│   └── site/                 # Static files served at /static
│       ├── index.html        # Landing page
│       ├── dashboard.html    # Main app dashboard (all features)
│       ├── registration.html # Sign up / login
│       └── css/ js/          # Styles and modules
├── tests/                    # Unit tests (81 tests, all passing)
├── docs/                     # Architecture, API reference, feature specs
├── dev.py                    # Dev runner (starts both servers)
├── .env.example              # Environment template
├── pytest.ini                # Test config
└── CLAUDE.md                 # AI assistant guide (architecture + conventions)
```

---

## Features

### Core platform
- **Identity Progression** — Six levels (Lost → Explorer → Builder → Disciplined → Focused → Elite) based on consistency score
- **Daily Protocol** — Minimum / Target / Bonus daily tasks (1 / 2 / 3 points). Streaks only count when Minimum is done
- **Deload System** — Recovery day after every 7-day streak. Choose one activity to keep streak alive
- **30-Day Adaptive Program** — Three phases (START / RHYTHM / REINFORCEMENT) per goal and level

### Goals & habits
- **10 Goal Paths** — Focus, Discipline, Health, Mental Balance, Personal Growth, Social, Life Reset, Studying, Find People, Find Direction
- **Habit Recommendations** — Curated habits per goal + level (beginner / medium / advanced)
- **Books & Resources** — 3 books + 5 videos per goal

### Tracking
- **Habit Tracker** — Create, complete, streak-track habits
- **Progress Log** — Completion history
- **Weekly Review** — What worked / what distracted / what to change → auto-generated suggestions
- **Pomodoro Timer** — Focus/break sessions

### Productivity
- **Water Tracker** — Daily intake log with glass-by-glass tracking
- **Daily Planner** — Time-slotted tasks with priorities
- **Spaced Repetition** — SM-2 algorithm flashcards with due-card queue
- **Brainstorm Board** — Capture ideas in named sessions

### Community
- **Groups & Challenges** — Join groups, weekly challenges with daily proof submission, admin moderation, leaderboard
- **Chat** — Direct messages + challenge group chats, user search

### Progression
- **Rewards** — Cosmetic unlocks at streak milestones (7 / 14 / 30 / 60 days) — avatar frames, themes, backgrounds

---

## API reference

Full reference: [`docs/API.md`](docs/API.md)

Base URL: `http://127.0.0.1:8080`
Interactive docs: `http://127.0.0.1:8080/docs`

---

## Architecture

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the full layer diagram and pattern guide.

Every feature follows: `Controller → Service → Repository → MongoDB`

---

## Troubleshooting

**`ModuleNotFoundError: No module named 'backend'`**
Run all commands from the project root (`habits-main/`), not from inside `backend/`.

**`pymongo.errors.ServerSelectionTimeoutError`**
Your MongoDB URI is wrong or your IP is not whitelisted in Atlas.

**`StaticFiles directory does not exist`**
The `frontend/site/` directory must exist before starting the server.
