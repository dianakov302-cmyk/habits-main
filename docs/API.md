# API Reference

Base URL: `http://127.0.0.1:8080`
Interactive docs: `/docs` (Swagger UI), `/redoc` (ReDoc)

---

## Users `/users`

| Method | Path | Description |
|--------|------|-------------|
| POST | `/users/login` | Email + password login |
| POST | `/users/register` | Register new account |
| POST | `/users/logout` | Logout (stateless) |
| POST | `/users/test-result` | Save quiz/personality results |
| GET | `/users/profile?email=` | Fetch profile (no password) |
| PUT | `/users/profile` | Update email or password |

---

## Habits `/habits`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/habits/` | All habits |
| GET | `/habits/{id}` | Single habit |
| POST | `/habits/create` | Create habit |
| DELETE | `/habits/{id}` | Delete habit |
| POST | `/habits/{id}/complete` | Mark habit complete (updates streak) |

---

## Progress `/progress`

| Method | Path | Description |
|--------|------|-------------|
| POST | `/progress/complete` | Log habit completion |
| GET | `/progress/{user_id}` | Get user progress history |

---

## Goals `/goals`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/goals/options` | Available goal templates |
| POST | `/goals/set` | Assign goal to user |
| GET | `/goals/user?email=` | User's current goal |
| GET | `/goals/resources?goal_code=` | Books + videos for a goal |
| GET | `/goals/recommendations?goal_code=&level=` | Recommended habits for goal + level |

---

## Groups `/groups`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/groups/` | List all groups |
| POST | `/groups/create` | Create group |
| POST | `/groups/join` | Join group |

---

## Challenges `/challenges`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/challenges/` | List challenges |
| POST | `/challenges/create` | Create challenge (admin) |
| PUT | `/challenges/{id}` | Edit challenge (admin) |
| DELETE | `/challenges/{id}` | Delete challenge (admin) |
| POST | `/challenges/{id}/register` | Register for challenge |
| GET | `/challenges/{id}/leaderboard` | Challenge leaderboard |
| POST | `/challenges/{id}/submit` | Submit daily proof |
| GET | `/challenges/{id}/submissions` | List submissions (admin) |
| PUT | `/challenges/{id}/submissions/{sub_id}` | Moderate submission (admin) |

---

## Identity `/identity`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/identity/profile?email=` | Identity level + progress score |
| POST | `/identity/recalculate` | Recalculate identity score |

---

## Daily Protocol `/protocol`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/protocol/today?email=` | Today's protocol |
| POST | `/protocol/create` | Create today's protocol |
| POST | `/protocol/complete-task` | Mark minimum/target/bonus done |
| GET | `/protocol/history?email=&days=` | Protocol history |

---

## Deload `/deload`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/deload/status?email=` | Check if deload day active |
| POST | `/deload/complete` | Complete deload activity |
| GET | `/deload/history?email=` | Past deload days |

---

## 30-Day Program `/program`

| Method | Path | Description |
|--------|------|-------------|
| POST | `/program/start` | Start a 30-day program |
| GET | `/program/status?email=` | Current program + phase |
| POST | `/program/complete-day` | Mark today's program day done |
| GET | `/program/phases` | Phase descriptions |

---

## Weekly Review `/reviews`

| Method | Path | Description |
|--------|------|-------------|
| POST | `/reviews/submit` | Submit weekly review |
| GET | `/reviews/history?email=` | All past reviews |
| GET | `/reviews/latest?email=` | Most recent review |

---

## Rewards `/rewards`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/rewards/catalog` | All available rewards |
| GET | `/rewards/user?email=` | User's unlocked rewards |
| POST | `/rewards/check-unlock` | Check & unlock eligible rewards |
| POST | `/rewards/activate` | Activate a reward (theme/frame) |

---

## Chat `/chat`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/chat/conversations?email=` | User's conversations |
| POST | `/chat/conversations` | Start new conversation |
| GET | `/chat/conversations/{id}/messages` | Messages in conversation |
| POST | `/chat/conversations/{id}/messages` | Send message |
| GET | `/chat/search-users?query=` | Search users by username |

---

## Productivity `/productivity`

### Water Tracker
| Method | Path | Description |
|--------|------|-------------|
| GET | `/productivity/water?email=&date=` | Today's water log |
| POST | `/productivity/water/log` | Log a glass of water |
| PUT | `/productivity/water/goal` | Update daily water goal |

### Planner
| Method | Path | Description |
|--------|------|-------------|
| GET | `/productivity/planner?email=&date=` | Day's tasks |
| POST | `/productivity/planner` | Create planner task |
| PUT | `/productivity/planner/{id}` | Update task |
| DELETE | `/productivity/planner/{id}` | Delete task |
| POST | `/productivity/planner/{id}/complete` | Mark task done |

### Spaced Repetition
| Method | Path | Description |
|--------|------|-------------|
| GET | `/productivity/sr/cards?email=` | All cards |
| GET | `/productivity/sr/review?email=` | Cards due for review |
| POST | `/productivity/sr/cards` | Create card |
| POST | `/productivity/sr/cards/{id}/review` | Submit review result |
| DELETE | `/productivity/sr/cards/{id}` | Delete card |

### Brainstorm
| Method | Path | Description |
|--------|------|-------------|
| GET | `/productivity/brainstorm?email=` | All brainstorm sessions |
| POST | `/productivity/brainstorm` | Create session |
| POST | `/productivity/brainstorm/{id}/ideas` | Add idea to session |
| DELETE | `/productivity/brainstorm/{id}` | Delete session |

---

## System

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | API info |
| GET | `/health` | Health check (DB connectivity) |
| GET | `/app` | Serve frontend index.html |
