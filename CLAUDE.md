# Anaida Space — Claude Code Guide

> For multi-agent workflows (BA, SA, DevOps, QA, UI/UX, Senior Dev), see **[AGENTS.md](AGENTS.md)**.

## Project overview

**Anaida Space** is a FastAPI + MongoDB adaptive self-development platform. Users build discipline through personalized habit systems, identity progression, 30-day programs, community challenges, and productivity tools. The aesthetic is Apple-style premium minimalism — no gamification, psychologically intelligent UX.

## Tech stack

- **Backend**: FastAPI 0.104.1, Python 3.11+
- **Database**: MongoDB (pymongo sync)
- **Auth**: Email/password with bcrypt + JWT (python-jose). Token stored as `anaida_token` in localStorage. `Authorization: Bearer` on all API requests.
- **Frontend**: Static HTML/CSS/JS served from `frontend/site/`
- **Tests**: `unittest` (not pytest) — run with `python -m pytest tests/ -v`

## Architecture pattern

Every feature follows this strict layered pattern — do not deviate:

```
Controller  →  Service (implements Interface)  →  Repository  →  MongoDB
```

### Container (DI) — `backend/main.py`

All services are registered in the `Container` class. Add new services here:
```python
def get_xyz_service(self):
    if self._xyz_service is None:
        self._xyz_repository = self._xyz_repository or XyzRepository()
        self._xyz_service = XyzService(self._xyz_repository)
    return self._xyz_service
```

Then wire the router in `create_app()`:
```python
app.include_router(create_xyz_router(container.get_xyz_service))
```

### Auth pattern

`backend/auth.py` provides:
- `create_access_token(email)` — issues a 30-day JWT
- `get_current_user` — FastAPI `Depends()`; raises 401 if missing/invalid
- `JWT_SECRET_KEY` reads from env var (`.env`)

Every protected controller imports and uses `get_current_user`:
```python
from backend.auth import get_current_user
@router.get("/something")
def handler(current_user: str = Depends(get_current_user), ...):
    ...
```

Public endpoints (no auth required): `GET /groups/`, `GET /challenges/`, `GET /goals/options`.

### Interface convention

All interfaces live in `backend/business_logic/services/interfaces/`.
Filename typo in originals: `*_imterface.py` — new files use `*_interface.py`.
The `__init__.py` there re-exports all interfaces.

### Request DTOs

All Pydantic request models live in `backend/controllers/requests/requests.py`.
The `__init__.py` in that package re-exports everything — update both when adding models.

## Running locally

```bash
# Windows (PowerShell)
.\setup.ps1      # first time: creates venv, installs deps, copies .env
.\run.ps1        # start backend + frontend

# macOS / Linux
bash setup.sh
bash run.sh
```

See **[RUNNING.md](RUNNING.md)** for full instructions including demo data seeding.

URLs:
- Frontend: `http://127.0.0.1:3000`
- API: `http://127.0.0.1:8080`
- Swagger: `http://127.0.0.1:8080/docs`
- Health: `http://127.0.0.1:8080/health`

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MONGODB_URI` | `mongodb://localhost:27017/` | MongoDB Atlas SRV or local URI |
| `MONGODB_DB_NAME` | `habitplatform` | Database name |
| `MONGODB_TIMEOUT_MS` | `5000` | Connection timeout |
| `JWT_SECRET_KEY` | dev fallback | Change before any deployment |

## MongoDB collections

| Collection | Owner | Description |
|------------|-------|-------------|
| `users` | UserRepository | Accounts, auth, quiz data |
| `quiz_results` | UserRepository | Anonymous quiz sessions |
| `userHabits` | HabitRepository | Habit definitions |
| `progress` | ProgressRepository | Habit completion logs |
| `goals` | GoalRepository | User goal assignments |
| `groups` | GroupRepository | Community groups |
| `posts` | PostRepository | Group posts / challenge posts |
| `user_identity` | IdentityRepository | Identity level & scores |
| `daily_protocols` | DailyProtocolRepository | Min/Target/Bonus day tasks |
| `deload_days` | DeloadRepository | Recovery days after 7-day streaks |
| `user_programs` | ProgramRepository | 30-day adaptive programs |
| `weekly_reviews` | WeeklyReviewRepository | Weekly reflection entries |
| `user_rewards` | RewardRepository | Unlocked cosmetic rewards |
| `challenge_submissions` | ChallengeSubmissionRepository | Proof uploads for challenges |
| `messages` | ChatRepository | Chat messages |
| `conversations` | ChatRepository | Chat threads (DM + group) |
| `water_logs` | ProductivityRepository | Daily water intake |
| `planner_tasks` | ProductivityRepository | Daily planner items |
| `sr_cards` | ProductivityRepository | Spaced repetition cards |
| `brainstorm_sessions` | ProductivityRepository | Brainstorm idea boards |

## Key design decisions

- **Identity progression**: Score 0-100 from streak + habit completion rate + weekly reviews + completed programs. Maps to: Lost / Explorer / Builder / Disciplined / Focused / Elite.
- **Daily protocol**: Each day has Minimum (1pt), Target (2pt), Bonus (3pt). No punishment for missing minimum. Streaks only count when minimum is done.
- **Deload**: After every 7-day streak, system creates a recovery day. One activity keeps streak alive.
- **30-day program**: Three phases — START (1–7), RHYTHM (8–21), REINFORCEMENT (22–30). Phase content adapts to goal + level.
- **Rewards**: Purely cosmetic (avatar frame, profile theme, elite background). Premium/minimal — no badges or points displays.

## What NOT to change

- Existing endpoint paths, request/response shapes, or collection schemas
- `UserService`, `HabitService`, `ProgressService`, `GoalService`, `GroupService`, `ChallengeService`
- `UserRepository`, `HabitRepository`, `ProgressRepository`, `GoalRepository`, `GroupRepository`, `PostRepository`
- Test files (extend, never modify existing tests)
- Container lazy-init pattern — keep the exact same style

## Testing conventions

Tests use `unittest.TestCase` with fake/stub repositories (no mocks of MongoDB).
Pattern: `FakeXyzRepository` class → inject into service → assert on service output.
Never test repositories against a real database in unit tests.
Run: `python -m pytest tests/ -v`

## Documents

| Document | Purpose |
|----------|---------|
| [AGENTS.md](AGENTS.md) | All agent roles, prompts, and how to invoke each specialist |
| [RUNNING.md](RUNNING.md) | Setup, run, seed instructions for Windows + macOS |
| [docs/SAD.md](docs/SAD.md) | Software Architecture Document (Views and Beyond) |
| [docs/USE_CASES.md](docs/USE_CASES.md) | 132 use cases across 16 feature areas |
| [docs/API.md](docs/API.md) | API endpoint reference |
| [docs/FEATURES.md](docs/FEATURES.md) | Feature descriptions |
