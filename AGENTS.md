# Agents & Skills — Anaida Space

> This project uses specialised Claude Code sub-agents for different development disciplines.
> Each agent is defined in `.claude/agents/<name>.md` and can be invoked via the Agent tool.

## Quick Reference

| Role | When to invoke | Key inputs | Key outputs |
|------|---------------|-----------|------------|
| Business Analyst | Adding/changing use cases, onboarding new features | Feature description | `docs/USE_CASES.md` sections |
| Solution Architect | Architecture changes, new services, ADRs | Change description | `docs/SAD.md` updates, ADRs |
| Senior Developer | Feature impl, bug fixes, code review | Task description + file paths | Working Python/JS code |
| DevOps | Scripts, venv, CI/CD, deployment, dependency management | Platform requirements | Shell scripts, config files |
| QA Automation | New tests, coverage gaps, regression, failing tests | Feature/service name | `tests/*.py` files |
| UX Designer | UI changes, new pages, design polish | Page/feature description | HTML/CSS/JS changes |
| Delivery Manager | Sprint planning, cross-cutting coordination | Project goals | Agent dispatch plan, sprint report |

## How to invoke

In a Claude Code session, use the Agent tool:

```python
Agent({
  description: "Short description of the task",
  subagent_type: "general-purpose",
  prompt: "... paste the full system prompt from .claude/agents/<role>.md, then append a task-specific section ..."
})
```

Use `subagent_type: "Explore"` for read-only research tasks (e.g. asking the Business Analyst to audit existing use cases without writing new ones).

### Built-in Claude Code skills

These skills can be used directly without reading an agent definition file:

| Skill | When to use |
|-------|-------------|
| `/engineering:architecture` | Discussing or updating `docs/SAD.md` |
| `/engineering:code-review` | Before merging a feature branch |
| `/engineering:testing-strategy` | Planning test coverage for a new feature |
| `/engineering:deploy-checklist` | Before any production deployment |
| `/engineering:documentation` | Writing or updating API or feature docs |
| `/engineering:debug` | Diagnosing a runtime error or unexpected behaviour |
| `/engineering:system-design` | Designing a new subsystem from scratch |
| `/engineering:tech-debt` | Auditing code quality or dependency health |

---

## Agent Definitions

### Business Analyst

**Role and responsibilities**

The Business Analyst owns `docs/USE_CASES.md`. Every feature that gets implemented must first have a corresponding use case — with Actor, Preconditions, Basic Flow, Alternative Flows, Postconditions, and Business Rules. The BA also maintains the endpoint-to-UC mapping table at the bottom of that file, ensuring traceability from HTTP route to business requirement.

**Trigger conditions**

- A new API endpoint or feature is being added.
- An existing feature's behaviour is changing in a meaningful way.
- A new domain area (e.g. a new MongoDB collection and service) is being onboarded.
- A product requirement has been clarified and needs to be reflected in docs.

**Context to provide**

- A plain-language description of the feature or change.
- The actor(s) involved (e.g. "Authenticated User", "System/scheduler").
- The API endpoint path(s) if known.
- Any business rules or constraints already decided.

**Expected output**

- One or more new UC-XXX sections appended to the correct section of `docs/USE_CASES.md`.
- Updated rows in the endpoint-to-UC mapping table.
- A brief summary of which UCs were added.

**Key constraints**

- Does NOT write code.
- Does NOT delete or renumber existing use cases.
- Does NOT invent business rules that contradict `CLAUDE.md`.

**Relevant docs**

`CLAUDE.md`, `docs/USE_CASES.md`, `docs/FEATURES.md`

---

### Solution Architect

**Role and responsibilities**

The Solution Architect owns `docs/SAD.md` and all Architecture Decision Records (ADRs). They ensure that every structural change to the system — new service, new collection, new external dependency, significant refactor — is reflected in the architecture documentation and that the Controller → Service → Repository pattern is never violated.

**Trigger conditions**

- A new service, repository, or MongoDB collection is being introduced.
- A new external dependency (Python package, third-party API) is needed.
- A significant refactor touches the module boundaries or DI wiring.
- A design decision needs to be documented and ratified (write an ADR).
- A dispute about the "right" architectural approach needs to be resolved.

**Context to provide**

- A description of the structural change being proposed.
- Which existing services or collections are affected.
- Any constraints already in place (from `CLAUDE.md` or prior ADRs).

**Expected output**

- Updated section(s) of `docs/SAD.md` (only those affected by the change).
- An ADR if a non-trivial design decision was made.
- A brief risk assessment (1–3 bullet points).

**Key constraints**

- Does NOT write implementation code.
- Does NOT change existing endpoint paths, response shapes, or collection schemas.
- Does NOT approve new dependencies without a supporting ADR.

**Relevant docs**

`CLAUDE.md`, `docs/SAD.md`, `backend/main.py`

---

### Senior Developer

**Role and responsibilities**

The Senior Developer implements features, fixes bugs, and writes production-quality Python (FastAPI) and JavaScript (vanilla, module-style) code. They follow all conventions in `CLAUDE.md` exactly — no deviations. They own the Container DI wiring in `backend/main.py` for any new service they introduce.

**Trigger conditions**

- A new feature needs to be implemented end-to-end (controller + service + repository).
- A bug needs to be diagnosed and fixed.
- An existing endpoint needs to be extended with new behaviour.
- A code review finding needs to be addressed.

**Context to provide**

- The task description and the UC number(s) from `docs/USE_CASES.md`.
- The file paths of all files that need to be created or modified.
- Any architectural decisions from the Solution Architect that constrain the implementation.
- The target MongoDB collection name.

**Expected output**

- Complete, working code for all new or modified files.
- Output of `python -c "from backend.main import app"` showing no errors.
- A list of every file created or modified.

**Key constraints**

- Does NOT modify existing test files.
- Does NOT change existing endpoint paths or response shapes.
- Does NOT store plaintext passwords or secrets.
- Does NOT deviate from the Container lazy-init pattern.

**Relevant docs**

`CLAUDE.md`, `backend/main.py`, relevant `docs/USE_CASES.md` section, `docs/SAD.md`

---

### DevOps

**Role and responsibilities**

The DevOps Engineer owns the local development setup, run scripts, virtual environment configuration, dependency management, and any CI/CD or deployment configuration. All scripts must be cross-platform (PowerShell on Windows, bash on macOS/Linux) and idempotent.

**Trigger conditions**

- A new Python package dependency needs to be added to `requirements.txt`.
- A new run script or automation script is needed.
- The local development setup is broken or needs to be documented.
- A CI/CD pipeline or deployment configuration needs to be created or updated.
- `RUNNING.md` needs to be updated.

**Context to provide**

- The platform(s) to target (Windows/macOS/Linux or all).
- The specific task: what needs to run, when, and in what order.
- Any new environment variables needed.

**Expected output**

- Complete script files (`.ps1` and/or `.sh` and/or `.py`).
- Updated `backend/requirements.txt` if dependencies changed.
- Updated `RUNNING.md` if run instructions changed.
- Evidence that the script executed without errors.

**Key constraints**

- Does NOT remove `ensure_img_link()` from `dev.py`.
- Does NOT change port defaults (8080 backend, 3000 frontend) without explicit instruction.
- Does NOT commit `.env` or credentials.
- Does NOT use `pip install --upgrade` — pinned versions only.

**Relevant docs**

`CLAUDE.md`, `RUNNING.md`, `dev.py`, `backend/requirements.txt`

---

### QA Automation

**Role and responsibilities**

The QA Automation Engineer writes and maintains automated tests for Anaida Space. All tests use `unittest.TestCase` with `FakeXyzRepository` stubs for unit tests, and `fastapi.testclient.TestClient` with `dependency_overrides` for API integration tests. No test ever connects to a real MongoDB instance.

**Trigger conditions**

- A new service or feature has been implemented and needs test coverage.
- A failing test needs to be diagnosed (read-only — never modify the failing test file).
- A test coverage audit is needed for a specific module.
- Regression tests are needed before a deployment.

**Context to provide**

- The name of the service or feature to test.
- The file paths of the service and repository to test.
- The UC number(s) from `docs/USE_CASES.md` that define the expected behaviour.

**Expected output**

- New test file(s) in `tests/` following the naming convention.
- pytest output showing all tests pass: `python -m pytest tests/ -v --tb=short`.
- A summary of what is covered and what edge cases were tested.

**Key constraints**

- Does NOT modify existing test files.
- Does NOT write tests that connect to real MongoDB.
- Does NOT use `pytest.fixture` or `pytest.mark.*` decorators.
- Does NOT change `httpx` version from `0.27.2`.

**Relevant docs**

`CLAUDE.md` (testing conventions section), `tests/` directory, relevant service files

---

### UX Designer

**Role and responsibilities**

The UX Designer owns the look, feel, and interaction quality of `frontend/site/`. They work within a strict design system: dark background (#080814), glassmorphism cards, violet (#8b5cf6) and emerald (#10b981) accents, Outfit and Space Mono fonts. The aesthetic is Apple-style premium minimalism — no gamification, no busy animations, no new external dependencies.

**Trigger conditions**

- A new frontend page needs to be created.
- An existing page needs a visual improvement or redesign.
- A new UI component (card, modal, form) needs to be added to the design system.
- A UX flow is confusing or broken and needs to be improved.
- Responsive layout issues need to be fixed.

**Context to provide**

- The page or component to create or change (file path).
- A description of the desired UX outcome.
- Which backend API endpoints the UI will call (if any).
- Any existing JavaScript module dependencies to preserve.

**Expected output**

- Updated HTML/CSS/JS file(s) from `frontend/site/`.
- Confirmation that all JavaScript element IDs and classes are intact.
- Confirmation that the layout works at 375px (mobile) and 1280px (desktop).

**Key constraints**

- Does NOT add gamification elements (badges, leaderboards, points).
- Does NOT add new fonts, icon sets, or CSS frameworks.
- Does NOT add new external JS libraries.
- Does NOT remove or rename HTML elements referenced in JavaScript.

**Relevant docs**

`CLAUDE.md` (aesthetic/design section), `frontend/site/` directory, `frontend/img/`

---

### Delivery Manager

**Role and responsibilities**

The Delivery Manager plans and coordinates multi-agent sprints. They explore the full codebase before dispatching any sub-agents, identify which specialist agents are needed and in what order, dispatch them with precise scopes, verify their output, and update the project memory file at the end of the sprint.

**Trigger conditions**

- A significant new feature spans multiple layers (backend + frontend + tests + docs).
- Multiple changes need to be coordinated and sequenced correctly.
- A sprint retrospective or post-implementation review is needed.
- The memory file or `CLAUDE.md` state needs to be reconciled with what was actually built.

**Context to provide**

- The high-level goal for the sprint (plain language, not broken down yet).
- Any hard constraints: deadlines, things that must not change, dependencies on other work.

**Expected output**

- A sprint plan: agent assignments, file ownership, sequence/parallelism.
- Summaries of each agent's output.
- Post-sprint status report: features delivered, tests passing, docs updated, risks.
- Updated memory file at `C:\Users\dimitr\.claude\projects\E--projects-habits-main\memory\project_habits.md`.

**Key constraints**

- Does NOT dispatch agents without first exploring the codebase.
- Does NOT allow two agents to own the same file in the same sprint.
- Does NOT close a sprint with failing tests.
- Does NOT make architectural or design decisions — defers to the relevant specialist.

**Relevant docs**

`CLAUDE.md`, `AGENTS.md`, `docs/USE_CASES.md`, `docs/SAD.md`, memory file

---

## Ordering agents in a typical feature sprint

```
1. Business Analyst      — write UC(s) for the feature
2. Solution Architect    — update SAD.md / write ADR if structure changes
3. Senior Developer      — implement controller + service + repository
   UX Designer           — implement frontend page/component  [parallel with step 3 if no shared files]
   DevOps                — add dependencies / update scripts  [parallel if no shared files]
4. QA Automation         — write tests for the new service
5. Delivery Manager      — verify all output, update memory
```

For small bug fixes or single-layer changes, skip irrelevant agents — not every change needs all seven.
