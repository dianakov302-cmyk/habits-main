# Architecture

## Layer diagram

```
HTTP Request
    │
    ▼
Controller  (FastAPI router, input validation, HTTP concerns)
    │
    ▼
Service     (business logic, implements abstract Interface)
    │
    ▼
Repository  (MongoDB data access, thin wrapper)
    │
    ▼
MongoDB Collection
```

## Dependency injection

`backend/main.py` holds a `Container` class that lazily creates every repository
and service once and reuses it for the life of the process.

```python
class Container:
    def get_user_service(self) -> UserService:
        if self._user_service is None:
            self._user_repository = self._user_repository or UserRepository()
            self._user_service = UserService(self._user_repository)
        return self._user_service
```

Controllers receive a factory callable (`get_service`) and declare it as a FastAPI
`Depends()` so the framework calls it per-request (but the Container returns the
same cached instance every time).

```python
def create_router(get_service: Callable[[], IUserService]) -> APIRouter:
    @router.post("/login")
    def login(service: IUserService = Depends(get_service)):
        ...
```

## Adding a new feature (checklist)

1. **Repository** — `backend/repositories/<name>_repository.py`
   - `__init__` gets collection(s) via `get_collection("collection_name")`
   - Only thin data-access methods; no business logic

2. **Interface** — `backend/business_logic/services/interfaces/<name>_interface.py`
   - Abstract class extending ABC
   - Export from `__init__.py` in that package

3. **Service** — `backend/business_logic/services/<name>_service.py`
   - Implements interface; constructor receives repository
   - All business logic here

4. **Controller** — `backend/controllers/<name>_controller.py`
   - `create_router(get_service)` factory function
   - Request models from `backend/controllers/requests/requests.py`

5. **Wire up** — `backend/main.py`
   - Add `_xyz_repository` and `_xyz_service` to Container
   - Add `get_xyz_service()` method
   - `app.include_router(create_xyz_router(container.get_xyz_service))`

6. **Request models** — add to `backend/controllers/requests/requests.py` and re-export in `__init__.py`

## Module map

```
backend/
├── main.py                        ← FastAPI app + Container
├── repositories/
│   ├── database.py                ← MongoDB client singleton
│   ├── user_repository.py
│   ├── habit_repository.py
│   ├── progress_repository.py
│   ├── goal_repository.py
│   ├── groups_repository.py
│   ├── challenge_repository.py
│   ├── punchcards_repository.py
│   ├── identity_repository.py     ← NEW
│   ├── daily_protocol_repository.py ← NEW
│   ├── deload_repository.py       ← NEW
│   ├── program_repository.py      ← NEW
│   ├── weekly_review_repository.py ← NEW
│   ├── reward_repository.py       ← NEW
│   ├── chat_repository.py         ← NEW
│   └── productivity_repository.py ← NEW
├── business_logic/
│   └── services/
│       ├── interfaces/
│       │   ├── __init__.py
│       │   ├── user_imterface.py
│       │   ├── habit_interface.py
│       │   ├── progress_imterface.py
│       │   ├── goal_interface.py
│       │   ├── groups_imterface.py
│       │   ├── challenge_imterface.py
│       │   ├── identity_interface.py  ← NEW
│       │   ├── daily_protocol_interface.py ← NEW
│       │   ├── deload_interface.py    ← NEW
│       │   ├── program_interface.py   ← NEW
│       │   ├── weekly_review_interface.py ← NEW
│       │   ├── reward_interface.py    ← NEW
│       │   ├── chat_interface.py      ← NEW
│       │   └── productivity_interface.py ← NEW
│       ├── user_service.py
│       ├── habit_service.py
│       ├── progress_service.py
│       ├── goal_service.py            ← EXTENDED (books, videos, recommendations)
│       ├── groups_service.py
│       ├── challenge_service.py       ← EXTENDED (admin CRUD, leaderboard)
│       ├── punchcard_services.py
│       ├── streaks_services.py
│       ├── identity_service.py        ← NEW
│       ├── daily_protocol_service.py  ← NEW
│       ├── deload_service.py          ← NEW
│       ├── program_service.py         ← NEW
│       ├── weekly_review_service.py   ← NEW
│       ├── reward_service.py          ← NEW
│       ├── chat_service.py            ← NEW
│       └── productivity_service.py    ← NEW
└── controllers/
    ├── requests/
    │   ├── __init__.py
    │   └── requests.py               ← EXTENDED
    ├── user_controller.py
    ├── habit_controller.py
    ├── progress_controller.py
    ├── goal_controller.py             ← EXTENDED
    ├── groups_controller.py
    ├── challenges_controller.py       ← EXTENDED
    ├── identity_controller.py         ← NEW
    ├── daily_protocol_controller.py   ← NEW
    ├── deload_controller.py           ← NEW
    ├── program_controller.py          ← NEW
    ├── weekly_review_controller.py    ← NEW
    ├── reward_controller.py           ← NEW
    ├── chat_controller.py             ← NEW
    └── productivity_controller.py     ← NEW
```

## Data flow example — completing a daily protocol task

```
POST /protocol/complete-task
        │
        ▼
DailyProtocolController.complete_task()
  validates: DailyProtocolCompleteRequest (email, date, task_type)
        │
        ▼
DailyProtocolService.complete_task(email, date, task_type)
  - loads protocol from repository
  - marks task completed
  - calculates points (min=1, target=2, bonus=3)
  - checks if minimum done → sets streak_counts=True
  - calls IdentityService.recalculate(email) side-effect
        │
        ▼
DailyProtocolRepository.update_protocol(email, date, data)
  → MongoDB "daily_protocols" collection
```
