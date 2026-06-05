# Anaida Space — Use Case Specification

**Document version:** 1.0  
**Date:** 2026-05-27  
**Platform:** Anaida Space (FastAPI + MongoDB)  
**Author role:** Business Analyst

---

## Table of Contents

1. [System Purpose](#1-system-purpose)
2. [Actors](#2-actors)
3. [Use Case Catalog](#3-use-case-catalog)
4. [Detailed Use Cases](#4-detailed-use-cases)
   - [Authentication (UC-001–UC-007)](#authentication-uc-001uc-007)
   - [Identity (UC-010–UC-013)](#identity-uc-010uc-013)
   - [Habits (UC-020–UC-025)](#habits-uc-020uc-025)
   - [Daily Protocol (UC-030–UC-034)](#daily-protocol-uc-030uc-034)
   - [Deload Days (UC-040–UC-043)](#deload-days-uc-040uc-043)
   - [30-Day Programs (UC-050–UC-055)](#30-day-programs-uc-050uc-055)
   - [Weekly Reviews (UC-060–UC-063)](#weekly-reviews-uc-060uc-063)
   - [Goals (UC-070–UC-074)](#goals-uc-070uc-074)
   - [Community Groups (UC-080–UC-083)](#community-groups-uc-080uc-083)
   - [Challenges (UC-090–UC-098)](#challenges-uc-090uc-098)
   - [Rewards (UC-100–UC-104)](#rewards-uc-100uc-104)
   - [Chat (UC-110–UC-116)](#chat-uc-110uc-116)
   - [Productivity — Water (UC-120–UC-122)](#productivity--water-uc-120uc-122)
   - [Productivity — Planner (UC-123–UC-126)](#productivity--planner-uc-123uc-126)
   - [Productivity — Spaced Repetition (UC-127–UC-130)](#productivity--spaced-repetition-uc-127uc-130)
   - [Productivity — Brainstorm (UC-131–UC-132)](#productivity--brainstorm-uc-131uc-132)
5. [Appendix A: Endpoint-to-Use-Case Mapping](#appendix-a-endpoint-to-use-case-mapping)
6. [Appendix B: MongoDB Collection Reference](#appendix-b-mongodb-collection-reference)
7. [Appendix C: Known Implementation Gaps](#appendix-c-known-implementation-gaps)

---

## 1. System Purpose

### Problem Statement

Modern self-improvement apps overwhelm users with badges, point tallies, and gamification loops that generate short-term engagement but do not produce real behavioural change. Users burn out because the platform rewards activity volume over consistent, sustainable effort.

### Solution

Anaida Space is a premium, psychologically intelligent self-development platform that helps users build genuine, lasting discipline. It achieves this through:

- **Identity-first design** — Users track a real identity score (0–100) derived from measurable behavioural inputs: streaks, habit completion rates, protocol adherence, weekly reflections, and program completion. The score maps to six named levels (Lost → Explorer → Builder → Disciplined → Focused → Elite), creating a meaningful progression narrative without badges or point displays.
- **Three-tier daily protocol** — Each day has a Minimum task (1 pt), Target task (2 pts), and Bonus task (3 pts). The streak counts when the Minimum is done. There is no punishment for not completing Target or Bonus, removing the all-or-nothing failure pattern.
- **Adaptive 30-day programs** — Three phases (START 1–7, RHYTHM 8–21, REINFORCEMENT 22–30) with task content tailored to the user's chosen goal and declared difficulty level (beginner / medium / advanced).
- **Deliberate recovery** — After every 7-day streak, the system automatically creates a deload day. One recovery activity preserves the streak. Recovery is planned, not a failure.
- **Community accountability** — Groups, challenges with proof submission, a leaderboard, and direct messaging connect users pursuing shared goals.
- **Integrated productivity layer** — Water tracking, daily planner, spaced repetition flashcards, and brainstorm boards make Anaida Space the single workspace for the user's self-development routine.

### Target Users

| User Type | Description |
|-----------|-------------|
| New User | Someone starting their self-development journey; may arrive via the onboarding quiz before creating an account |
| Active User | Registered user tracking habits, daily protocols, and a 30-day program |
| Community Member | Registered user who joins groups, enters challenges, and messages other users |
| Challenge Moderator / Admin | A user who creates and moderates challenges (no separate role flag in the current system — any authenticated user can call admin endpoints) |

---

## 2. Actors

| Actor | Description | Authentication Required |
|-------|-------------|------------------------|
| **Anonymous User** | Unauthenticated visitor; can take the onboarding quiz, view public goal options, and register | None |
| **Authenticated User** | Registered user with a valid JWT Bearer token; full access to personal features | JWT Bearer token (30-day expiry, HS256) |
| **Google OAuth User** | User who authenticates via Google; account auto-created on first sign-in without a password | Google ID token |
| **Admin** | Any authenticated user calling challenge creation / moderation endpoints (no role gate in current implementation) | JWT Bearer token |
| **System** | Internal automated actor that creates deload days after 7-day streaks, resolves identity levels after recalculation, advances program phases, and triggers reward unlocks | Internal — no HTTP credential |

---

## 3. Use Case Catalog

| UC ID | Use Case Name | Primary Actor | Priority |
|-------|---------------|---------------|----------|
| UC-001 | Register Account | Anonymous User | Must |
| UC-002 | Log In | Anonymous User | Must |
| UC-003 | Log Out | Authenticated User | Should |
| UC-004 | View Profile | Authenticated User | Must |
| UC-005 | Update Profile | Authenticated User | Should |
| UC-006 | Take Assessment Quiz | Anonymous User | Must |
| UC-007 | Verify Session | Authenticated User | Must |
| UC-010 | View Identity Level | Authenticated User | Must |
| UC-011 | Recalculate Identity Score | System / Authenticated User | Must |
| UC-012 | Level Up Notification | System | Should |
| UC-013 | Score Breakdown | Authenticated User | Should |
| UC-020 | Create Habit | Authenticated User | Must |
| UC-021 | List Habits | Authenticated User | Must |
| UC-022 | Complete Habit | Authenticated User | Must |
| UC-023 | Delete Habit | Authenticated User | Should |
| UC-024 | Track Habit Streak | System | Must |
| UC-025 | View Completion History | Authenticated User | Could |
| UC-030 | View Today's Protocol | Authenticated User | Must |
| UC-031 | Create Daily Protocol | Authenticated User | Must |
| UC-032 | Complete Minimum Task | Authenticated User | Must |
| UC-033 | Complete Target Task | Authenticated User | Must |
| UC-034 | Complete Bonus Task | Authenticated User | Should |
| UC-040 | Check Deload Status | Authenticated User | Must |
| UC-041 | Complete Deload Activity | Authenticated User | Must |
| UC-042 | View Deload History | Authenticated User | Could |
| UC-043 | Automatic Deload After Streak | System | Must |
| UC-050 | Start Program | Authenticated User | Must |
| UC-051 | View Program Status | Authenticated User | Must |
| UC-052 | Complete Program Day | Authenticated User | Must |
| UC-053 | Progress Through Phases | System | Must |
| UC-054 | View Phase Content | Authenticated User | Should |
| UC-055 | Complete Program | System | Must |
| UC-060 | Submit Weekly Review | Authenticated User | Must |
| UC-061 | View Review History | Authenticated User | Should |
| UC-062 | View Latest Review | Authenticated User | Should |
| UC-063 | Review Affects Identity Score | System | Must |
| UC-070 | Browse Goal Options | Anonymous / Authenticated User | Must |
| UC-071 | Set Goal | Authenticated User | Must |
| UC-072 | View Current Goal | Authenticated User | Should |
| UC-073 | View Goal Resources | Authenticated User | Could |
| UC-074 | Get Goal Recommendations | Authenticated User | Should |
| UC-080 | Browse Groups | Authenticated User | Should |
| UC-081 | Create Group | Authenticated User | Should |
| UC-082 | Join Group | Authenticated User | Should |
| UC-083 | View Group Members | Authenticated User | Could |
| UC-090 | Browse Challenges | Authenticated User | Must |
| UC-091 | Create Challenge | Admin | Must |
| UC-092 | Register for Challenge | Authenticated User | Must |
| UC-093 | Submit Proof | Authenticated User | Must |
| UC-094 | View Leaderboard | Authenticated User | Should |
| UC-095 | Moderate Submission | Admin | Must |
| UC-096 | Update Challenge | Admin | Should |
| UC-097 | Delete Challenge | Admin | Should |
| UC-098 | View Submissions | Admin | Should |
| UC-100 | Browse Reward Catalog | Authenticated User | Should |
| UC-101 | View Unlocked Rewards | Authenticated User | Should |
| UC-102 | Check for New Rewards | System / Authenticated User | Must |
| UC-103 | Activate Reward | Authenticated User | Should |
| UC-104 | Reward Unlock Criteria | System | Must |
| UC-110 | View Conversations | Authenticated User | Should |
| UC-111 | Start Conversation | Authenticated User | Should |
| UC-112 | Send Message | Authenticated User | Should |
| UC-113 | Read Messages | Authenticated User | Should |
| UC-114 | Search Users | Authenticated User | Should |
| UC-115 | Group Conversation | Authenticated User | Could |
| UC-116 | AI Coach Conversation | Authenticated User | Should |
| UC-120 | Log Water Intake | Authenticated User | Could |
| UC-121 | View Water Log | Authenticated User | Could |
| UC-122 | Set Daily Water Goal | Authenticated User | Could |
| UC-123 | Add Planner Task | Authenticated User | Could |
| UC-124 | View Planner | Authenticated User | Could |
| UC-125 | Update Task | Authenticated User | Could |
| UC-126 | Delete Task | Authenticated User | Could |
| UC-127 | Create SR Card | Authenticated User | Could |
| UC-128 | Review SR Card | Authenticated User | Could |
| UC-129 | View SR Queue | Authenticated User | Could |
| UC-130 | SR Algorithm | System | Could |
| UC-131 | Create Brainstorm Session | Authenticated User | Could |
| UC-132 | Add Ideas to Session | Authenticated User | Could |

---

## 4. Detailed Use Cases

---

### Authentication (UC-001–UC-007)

---

#### UC-001: Register Account

**Actor(s):** Anonymous User  
**Endpoint:** `POST /users/register`

**Preconditions:**
- The user does not already have an account with the provided email address.
- `email` is 3–320 characters; `password` is non-empty; `name` is optional (1–200 characters if provided).

**Basic Flow:**
1. User submits `email`, `password`, and optional `name`.
2. System validates field lengths via Pydantic; rejects the request with HTTP 422 if constraints are violated.
3. System queries the `users` collection to determine whether the email already exists.
4. Email is not found; system hashes the password using bcrypt with a generated salt.
5. System inserts a new user document into `users` with `email`, hashed `password`, and `name`.
6. System returns `{ "status": "success", "message": "Registration successful. Welcome aboard!" }`.

**Alternative Flows:**

- **AF-001-A: Email already registered** — At step 3, the email is found. System returns `{ "status": "error", "message": "Email already registered. Please log in." }`. No document is created.
- **AF-001-B: Database error** — At step 5, the insert raises an exception. System returns `{ "status": "error", "message": "Registration failed: <detail>" }`.

**Postconditions:**
- A new user document exists in `users`. Password is stored as a bcrypt hash. The user is not automatically logged in.

**Business Rules:**
- Email length is 3–320 characters; no format (RFC 5322) validation is applied beyond length at the service level.
- Duplicate email check happens before hashing — no partial writes occur on collision.
- The `name` field defaults to an empty string if omitted.

---

#### UC-002: Log In

**Actor(s):** Anonymous User  
**Endpoint:** `POST /users/login`

**Preconditions:**
- A user account exists for the submitted email.
- `email` and `password` are non-empty.

**Basic Flow:**
1. User submits `email` and `password`.
2. System validates field lengths.
3. System queries `users` by email.
4. User found; system attempts bcrypt verification against the stored password hash.
5. Password is correct; system generates a JWT access token (HS256, 30-day expiry) with the user's email as the `sub` claim.
6. System returns `{ "status": "success", "access_token": "<token>", "token_type": "bearer", "email": "<email>", "message": "Login successful. Welcome back!" }`.

**Alternative Flows:**

- **AF-002-A: User not found** — At step 3, no document matches the email. System returns `{ "status": "error", "message": "Identity not found. Please sign up." }`.
- **AF-002-B: Legacy plain-text password migration** — At step 4, bcrypt raises an exception (stored password was never hashed). System falls back to plain-text comparison. If they match, system re-hashes the password with bcrypt, updates the user document, and proceeds to step 5.
- **AF-002-C: Wrong password** — Bcrypt returns False and plain-text fallback also fails. System returns `{ "status": "error", "message": "Wrong password. Please try again." }`.

**Postconditions:**
- Client holds a JWT Bearer token valid for 30 calendar days from issuance.
- If AF-002-B triggered, the stored password is now a bcrypt hash.

**Business Rules:**
- JWT secret is `anaida-secret-key-change-in-production` — must be replaced before any production deployment.
- All subsequent authenticated requests supply the token as `Authorization: Bearer <token>`.
- Token algorithm is HS256; the `sub` claim contains the user's email address.

---

#### UC-003: Log Out

**Actor(s):** Authenticated User  
**Endpoint:** `POST /users/logout`

**Preconditions:**
- Request body contains `email`.

**Basic Flow:**
1. User submits a logout request with their email.
2. System returns `{ "status": "success", "message": "Logout successful. See you next time!" }`.

**Alternative Flows:**
- None. The service always returns success regardless of whether the email exists in the database.

**Postconditions:**
- No server-side session state is changed. Token invalidation is the client's responsibility.

**Business Rules:**
- This is a stateless logout — no token blocklist exists. The JWT remains technically valid until its 30-day expiry unless the client discards it.

---

#### UC-004: View Profile

**Actor(s):** Authenticated User  
**Endpoint:** `GET /users/profile`

**Preconditions:**
- Request includes a valid `Authorization: Bearer <token>` header.

**Basic Flow:**
1. System resolves the authenticated user's email from the JWT via the `get_current_user` dependency.
2. System queries the `users` collection for the document matching that email.
3. System excludes the `_id` and `password` fields from the result.
4. Document found; system returns `{ "status": "success", "data": { <profile fields> } }`.

**Alternative Flows:**

- **AF-004-A: User document not found** — No document matches the token email (data inconsistency). System returns `{ "status": "error", "message": "User not found." }`.

**Postconditions:**
- Client receives all stored profile fields (email, name, and any additional fields added at registration or via OAuth) without the password or internal `_id`.

**Business Rules:**
- The `_id` and `password` fields are stripped at the repository layer before the response is constructed.

---

#### UC-005: Update Profile

**Actor(s):** Authenticated User  
**Endpoint:** `PUT /users/profile`

**Preconditions:**
- User is authenticated.
- Request body includes the current `email` and at least one of `new_email` or `new_password`.

**Basic Flow:**
1. System resolves the authenticated user's email from the JWT.
2. System validates that at least one update field (`new_email`, `new_password`) is non-null.
3. System constructs a `$set` update map from the provided fields.
4. System performs `update_one` on the `users` collection using the current email as the filter.
5. Document found and updated; system returns `{ "status": "success", "message": "Profile updated successfully." }`.

**Alternative Flows:**

- **AF-005-A: No update fields provided** — Both `new_email` and `new_password` are absent. System returns `{ "status": "error", "message": "No updates provided." }`.
- **AF-005-B: User not found** — `update_one` matches zero documents. System returns `{ "status": "error", "message": "User not found." }`.

**Postconditions:**
- The user document in `users` is updated with the new email or new password (or both).

**Business Rules:**
- Password updated via this endpoint is stored as plain text in the current implementation — bcrypt hashing is not applied here. This is a known gap.
- If `new_email` is changed, the existing JWT (which encodes the old email) will fail future profile lookups until the user re-authenticates to obtain a new token.

---

#### UC-006: Take Assessment Quiz

**Actor(s):** Anonymous User  
**Endpoint:** Quiz interaction is client-side; results are persisted via `POST /users/test-result`

**Preconditions:**
- User is on the publicly accessible frontend application (no login required).

**Basic Flow:**
1. User navigates to the assessment section of the frontend.
2. Frontend presents a multi-question quiz profiling the user's discipline level, goals, and blockers.
3. User answers each question; answers are accumulated as a list of strings in the client.
4. Client generates a `session_id` (minimum 8 characters) to identify the anonymous session.
5. Client optionally prompts for an email address to associate results with an account.
6. Client submits `session_id`, `answers`, `profile` dictionary, `roadmap` dictionary, and optional `email` to `POST /users/test-result`.
7. System persists the result: if `email` is provided, the data is stored within the matching `users` document; otherwise it is stored in the `quiz_results` collection as an anonymous session.
8. System returns `{ "status": "success", "message": "Test result saved.", "storage": "<location>" }`.

**Alternative Flows:**

- **AF-006-A: Database error** — Insertion fails. System returns `{ "status": "error", "message": "Failed to save test result: <detail>" }`.

**Postconditions:**
- Quiz session data (answers, profile, roadmap) is persisted, either linked to a user account or stored anonymously in `quiz_results`.

**Business Rules:**
- The `profile` and `roadmap` fields are freeform JSON dictionaries; no schema validation is applied beyond them being valid dicts.
- Anonymous quiz results can be linked to an account later using the `session_id`.
- This endpoint does not require authentication — anonymous users can save results before registering.

---

#### UC-007: Verify Session

**Actor(s):** Authenticated User  
**Endpoint:** `GET /users/me`

**Preconditions:**
- Request includes a valid `Authorization: Bearer <token>` header.

**Basic Flow:**
1. Client sends a request with the JWT in the Authorization header.
2. The `get_current_user` dependency extracts the Bearer credential.
3. System decodes and verifies the JWT using HS256 and the secret key, checking the expiry claim.
4. Token is valid and not expired; system extracts the email from the `sub` claim.
5. System returns `{ "email": "<email>", "authenticated": true }`.

**Alternative Flows:**

- **AF-007-A: No Authorization header** — At step 2, no credential is present. System returns HTTP 401: `{ "detail": "Not authenticated" }`.
- **AF-007-B: Invalid or expired token** — At step 3, JWT decoding fails or the `exp` claim is in the past. System returns HTTP 401: `{ "detail": "Invalid or expired token" }`.

**Postconditions:**
- Client confirms that their token is valid and receives the associated email for subsequent requests.

**Business Rules:**
- All protected endpoints across the entire platform share the same `get_current_user` dependency. A token rejected here will be rejected everywhere.
- The only unprotected endpoints (no JWT required) are: `GET /goals/options` and `POST /users/test-result`.

---

### Identity (UC-010–UC-013)

---

#### UC-010: View Identity Level

**Actor(s):** Authenticated User  
**Endpoint:** `GET /identity/profile`

**Preconditions:**
- User is authenticated.
- `email` is provided as a query parameter.

**Basic Flow:**
1. System queries the `user_identity` collection for a document matching the email.
2. Document found; system returns `{ "status": "success", "data": { score, level, next_level, progress_to_next, streak_score, habit_completion_score, protocol_score, weekly_review_score, program_score } }`.
3. If no document exists (first access), system automatically triggers a recalculation (UC-011) with all component scores defaulting to 0, persists the resulting document, and returns it.

**Alternative Flows:**

- **AF-010-A: First-time access** — No identity document exists. System falls through to `recalculate`, which inserts a new document with all scores at 0 and level "Lost". This new document is returned.

**Postconditions:**
- Client receives the current identity score (0–100), named level, next level name, progress percentage within the current level band, and all five component sub-scores.

**Business Rules — Identity Score Formula:**

| Component | Weight | Field |
|-----------|--------|-------|
| Streak score | 30% | `streak_score` |
| Habit completion score | 30% | `habit_completion_score` |
| Protocol score | 20% | `protocol_score` |
| Weekly review score | 10% | `weekly_review_score` |
| Program score | 10% | `program_score` |

`identity_score = streak*0.30 + habit*0.30 + protocol*0.20 + reviews*0.10 + program*0.10`

---

#### UC-011: Recalculate Identity Score

**Actor(s):** Authenticated User, System  
**Endpoint:** `POST /identity/recalculate`

**Preconditions:**
- Request body contains the user's `email`.
- The user's `user_identity` document exists (or will be created from defaults).

**Basic Flow:**
1. User or System submits a recalculation request with the user's email.
2. System reads the existing `user_identity` document; if none exists, all component scores default to 0.
3. System applies the weighted formula: `score = streak*0.30 + habit*0.30 + protocol*0.20 + reviews*0.10 + program*0.10`.
4. System clamps the result to the range 0.0–100.0.
5. System resolves the identity level from the computed score using the level threshold table.
6. System computes `progress_to_next` as the percentage through the current band (Elite users get 100%).
7. System upserts the full identity document into `user_identity`.
8. System returns `{ "status": "success", "data": { <recalculated fields> } }`.

**Postconditions:**
- The `user_identity` document reflects the latest computed score, level, and component breakdown.

**Business Rules:**
- Recalculate is idempotent — calling it multiple times without changing component scores produces the same result.
- Individual component scores are updated by other services via `update_component` before triggering recalculation.

---

#### UC-012: Level Up Notification

**Actor(s):** System (triggered by UC-011 when a recalculation crosses a level boundary)

**Preconditions:**
- A recalculation has been performed and the new level name differs from the previously stored level name.

**Basic Flow:**
1. During UC-011, system computes the new level name.
2. System compares the new level with the previously stored level in `user_identity`.
3. New level is higher than the old level; system records the transition in the identity document (the `level` field is updated to the new name).
4. The API response for UC-011 includes the new level, allowing the client to display a level-up notification.

**Alternative Flows:**

- **AF-012-A: Score decreases and level drops** — If a component score falls (e.g., streak resets), the level can decrease. The same comparison logic applies; the client receives the lower level in the response.

**Postconditions:**
- `user_identity.level` reflects the level corresponding to the current computed score.

**Business Rules — Level Thresholds:**

| Score Range | Level |
|-------------|-------|
| 0–19 | Lost |
| 20–39 | Explorer |
| 40–59 | Builder |
| 60–74 | Disciplined |
| 75–89 | Focused |
| 90–100 | Elite |

---

#### UC-013: Score Breakdown

**Actor(s):** Authenticated User  
**Endpoint:** `GET /identity/profile` (same endpoint as UC-010; breakdown is part of the response)

**Preconditions:**
- User is authenticated; `email` query parameter provided.

**Basic Flow:**
1. System retrieves the `user_identity` document (see UC-010).
2. System returns all five component sub-scores alongside the composite score and level.
3. Client uses the breakdown to understand which behaviours are contributing most to the identity score.

**Alternative Flows:**

- **AF-013-A: All components at zero** — New user with no activity. All sub-scores are 0; level is "Lost"; `progress_to_next` is 0%.

**Postconditions:**
- Client can display a breakdown chart or summary showing relative contribution of each component.

**Business Rules:**
- Component scores are stored as floats in [0.0, 100.0]. The five components sum with their respective weights to produce the composite score.
- The `protocol_score` component is updated externally (e.g., after daily protocol completions feed back into the identity system via `update_component`).

---

### Habits (UC-020–UC-025)

---

#### UC-020: Create Habit

**Actor(s):** Authenticated User  
**Endpoint:** `POST /habits/create`

**Preconditions:**
- `name` is 1–200 characters; `description` is 1–1000 characters.

**Basic Flow:**
1. User submits a habit creation request with `name` and `description`.
2. System validates field lengths via Pydantic; returns HTTP 422 if constraints are violated.
3. System inserts a new document `{ "name": name, "description": description }` into the `userHabits` collection.
4. System returns `{ "message": "Habit created", "id": "<inserted_id>" }`.

**Alternative Flows:**

- **AF-020-A: Validation failure** — Field lengths violated. FastAPI returns HTTP 422 with validation details.
- **AF-020-B: Database error** — System returns `{ "error": "Failed to create habit: <detail>" }`.

**Postconditions:**
- A new habit document exists in `userHabits` with the provided name and description.

**Business Rules:**
- The habit document does not initially include `current_streak` or `last_completed_at` fields. These are added the first time UC-022 is called for the habit.
- There is no duplicate-name guard — users can create multiple habits with the same name.

---

#### UC-021: List Habits

**Actor(s):** Authenticated User  
**Endpoint:** `GET /habits/`

**Preconditions:**
- User is authenticated.

**Basic Flow:**
1. System queries the `userHabits` collection for all documents.
2. System converts `_id` fields to strings for JSON serialisation.
3. System returns the full list of habit objects in the response body.

**Alternative Flows:**

- **AF-021-A: No habits exist** — Collection is empty. System returns an empty array `[]`.
- **AF-021-B: Database error** — Exception raised. System logs the error and returns `[]`.

**Postconditions:**
- Client receives all habit records in the `userHabits` collection.

**Business Rules:**
- The current implementation returns all habits from the collection without filtering by the requesting user's identity. User-scoped filtering would need to be added for full multi-user isolation.

---

#### UC-022: Complete Habit

**Actor(s):** Authenticated User  
**Endpoint:** `POST /habits/{id}/complete`

**Preconditions:**
- Request body contains `user_id` and `habit_id`, both non-empty strings.
- The habit identified by the path `id` parameter must exist in `userHabits`.

**Basic Flow:**
1. User submits a completion event with `user_id` and `habit_id`.
2. System validates the request body via the `HabitCompletionRequest` Pydantic model.
3. System records a completion log entry in the `progress` collection with `user_id`, `habit_id`, and a UTC timestamp.
4. System retrieves the habit's current streak state (`current_streak`, `last_completed_at`).
5. System applies streak logic (see UC-024) and updates the habit document.
6. System returns a completion confirmation.

**Alternative Flows:**

- **AF-022-A: Habit not found** — The `id` in the path does not match any document. System returns an error response.
- **AF-022-B: Already completed today** — `last_completed_at` equals today's date. Streak is unchanged; system returns the current streak value.

**Postconditions:**
- A new completion log entry exists in `progress`.
- The habit's `current_streak` and `last_completed_at` fields are updated per streak rules (UC-024).

---

#### UC-023: Delete Habit

**Actor(s):** Authenticated User  
**Endpoint:** `DELETE /habits/{id}`

**Preconditions:**
- `id` in the path is a valid MongoDB ObjectId string.

**Basic Flow:**
1. User sends a DELETE request with the habit's `id` in the path.
2. System converts the string `id` to a `bson.ObjectId`.
3. System calls `delete_one` on `userHabits` with the ObjectId filter.
4. One document is deleted; system returns `true` (HTTP 200 with the boolean).

**Alternative Flows:**

- **AF-023-A: Invalid ObjectId format** — `ObjectId(id)` raises `InvalidId`. System returns `false`.
- **AF-023-B: Habit not found** — `delete_one` deletes zero documents. System returns `false`.

**Postconditions:**
- The habit document is removed from `userHabits`.

**Business Rules:**
- Deleting a habit does not cascade-delete associated entries in the `progress` collection. Historical completion logs are retained independently.

---

#### UC-024: Track Habit Streak

**Actor(s):** System (triggered by UC-022)

**Preconditions:**
- A habit completion event has been recorded.
- The habit document may or may not yet have `last_completed_at` and `current_streak` fields.

**Basic Flow:**
1. System retrieves the habit document by ID.
2. System computes `today` and `yesterday` as date boundaries using the server clock.
3. If `last_completed_at` equals today: habit already completed today. `current_streak` is returned unchanged (no-op).
4. If `last_completed_at` equals yesterday: streak is unbroken. `new_streak = current_streak + 1`.
5. If `last_completed_at` is absent or older than yesterday: streak broken. `new_streak = 1`.
6. System updates `current_streak` and `last_completed_at` in the `userHabits` document.

**Postconditions:**
- `current_streak` and `last_completed_at` are updated in the habit document.

**Business Rules:**
- Only one completion is counted per day per habit for streak purposes. Subsequent completions on the same calendar day are no-ops.
- A missed day resets the streak to 1 on the next completion (not to 0).

---

#### UC-025: View Completion History

**Actor(s):** Authenticated User  
**Endpoint:** Service-level method; accessible via the `progress` collection query

**Preconditions:**
- `user_id` or `habit_id` is provided to scope the query.

**Basic Flow:**
1. System queries the `progress` collection for entries matching the provided filter.
2. System returns the list of completion log entries, each including `user_id`, `habit_id`, and completion timestamp.

**Alternative Flows:**

- **AF-025-A: No completions recorded** — System returns an empty list.

**Postconditions:**
- Client receives a chronological log of all habit completion events for the requested scope.

**Business Rules:**
- The `progress` collection is append-only. Completion entries are never modified or deleted, even if the parent habit is deleted (UC-023).

---

### Daily Protocol (UC-030–UC-034)

---

#### UC-030: View Today's Protocol

**Actor(s):** Authenticated User  
**Endpoint:** `GET /daily-protocols/today`

**Preconditions:**
- `email` is provided as a query parameter.

**Basic Flow:**
1. System determines today's date in ISO format (YYYY-MM-DD) from the server clock.
2. System queries `daily_protocols` for a document matching `email` and `date == today`.
3. Document found; system returns `{ "status": "success", "data": { <protocol document> } }`.
4. No document found; system returns `{ "status": "success", "data": null, "message": "No protocol for today. Create one via POST /daily-protocols/create" }`.

**Postconditions:**
- Client receives the full protocol document including all three task titles, their `completed` flags, `points_earned`, and the `streak_counts` boolean.

**Business Rules:**
- A null response for today's protocol is not an error — it means the user has not yet created their day. This is a normal state for new users and for days when the protocol has not been set up.

---

#### UC-031: Create Daily Protocol

**Actor(s):** Authenticated User  
**Endpoint:** `POST /daily-protocols/create`

**Preconditions:**
- No protocol document exists in `daily_protocols` for the given `email` and `date`.
- Request body: `email`, `date` (YYYY-MM-DD, exactly 10 characters), `minimum_task` (1–300 chars), `target_task` (1–300 chars), `bonus_task` (1–300 chars).

**Basic Flow:**
1. User submits the protocol creation request with email, date, and the three task strings.
2. System checks for an existing protocol document matching the email and date.
3. No existing protocol found; system constructs the document:
   - `minimum_task: { title: <text>, completed: false }`
   - `target_task: { title: <text>, completed: false }`
   - `bonus_task: { title: <text>, completed: false }`
   - `points_earned: 0`
   - `streak_counts: false`
4. System upserts the document into `daily_protocols`.
5. System reads back the newly created document and returns `{ "status": "success", "data": { <protocol> } }`.

**Alternative Flows:**

- **AF-031-A: Protocol already exists** — At step 2, an existing document is found for that email and date. System returns `{ "status": "error", "message": "Protocol already exists for this date." }`.

**Postconditions:**
- A new protocol document exists in `daily_protocols` for the specified email and date with all three tasks in an incomplete state.

**Business Rules:**
- Exactly one protocol is permitted per user per calendar date.
- All three task strings must be defined at creation time; individual tasks cannot be added or modified after creation.
- Points tiers: Minimum = 1 pt, Target = 2 pts, Bonus = 3 pts. Maximum daily protocol score = 6 pts.

---

#### UC-032: Complete Minimum Task

**Actor(s):** Authenticated User  
**Endpoint:** `POST /daily-protocols/complete-task` (with `task_type: "minimum"`)

**Preconditions:**
- A protocol document exists for the given `email` and `date`.
- The minimum task has not already been marked complete.

**Basic Flow:**
1. User submits `email`, `date`, and `task_type: "minimum"`.
2. System validates `task_type` is one of: `minimum`, `target`, `bonus`.
3. System retrieves the protocol document for the email and date.
4. System checks whether `minimum_task.completed` is already `true`; if so, returns "Task already completed."
5. System sets `minimum_task.completed = true`.
6. System recalculates `points_earned`: adds 1 point for the minimum task.
7. System sets `streak_counts = true` (completing the minimum task qualifies this day for the streak).
8. System upserts the updated protocol document.
9. System returns `{ "status": "success", "message": "minimum task completed. +1 point.", "data": <updated_protocol> }`.

**Alternative Flows:**

- **AF-032-A: Protocol not found** — No protocol exists for the date. System returns `{ "status": "error", "message": "Protocol not found for this date." }`.
- **AF-032-B: Task already completed** — Returns `{ "status": "success", "message": "Task already completed.", "data": <protocol> }` — not treated as an error.

**Postconditions:**
- `minimum_task.completed` is `true`.
- `points_earned` is incremented by 1 (or includes the 1 point in the total).
- `streak_counts` is `true`, qualifying this calendar day for streak continuity.

**Business Rules:**
- `streak_counts` becomes `true` exclusively when the minimum task is marked complete. Completing only target or only bonus does not qualify the day for the streak.
- There is no penalty mechanism for days where the minimum task is not completed.

---

#### UC-033: Complete Target Task

**Actor(s):** Authenticated User  
**Endpoint:** `POST /daily-protocols/complete-task` (with `task_type: "target"`)

**Preconditions:**
- A protocol document exists for the given `email` and `date`.
- The target task has not already been marked complete.

**Basic Flow:**
1. User submits `email`, `date`, and `task_type: "target"`.
2. System validates `task_type`.
3. System retrieves the protocol document.
4. System checks whether `target_task.completed` is already `true`.
5. System sets `target_task.completed = true`.
6. System recalculates `points_earned`: sums points for all completed tasks (target = 2 pts).
7. System does NOT change `streak_counts` — this is controlled only by the minimum task.
8. System upserts the updated document.
9. System returns `{ "status": "success", "message": "target task completed. +2 point(s).", "data": <updated_protocol> }`.

**Alternative Flows:**

- Same as UC-032 alternative flows, applied to `target_task`.

**Postconditions:**
- `target_task.completed` is `true`. `points_earned` reflects the cumulative sum of all completed tasks.

**Business Rules:**
- Tasks within a protocol are independent — completing the target does not require the minimum to have been done first. However, only the minimum triggers `streak_counts`.

---

#### UC-034: Complete Bonus Task

**Actor(s):** Authenticated User  
**Endpoint:** `POST /daily-protocols/complete-task` (with `task_type: "bonus"`)

**Preconditions:**
- A protocol document exists for the given `email` and `date`.
- The bonus task has not already been marked complete.

**Basic Flow:**
1. User submits `email`, `date`, and `task_type: "bonus"`.
2. System validates `task_type`.
3. System retrieves the protocol document.
4. System checks whether `bonus_task.completed` is already `true`.
5. System sets `bonus_task.completed = true`.
6. System recalculates `points_earned`: adds 3 pts for the bonus task to the running total.
7. System upserts the updated document.
8. System returns `{ "status": "success", "message": "bonus task completed. +3 point(s).", "data": <updated_protocol> }`.

**Alternative Flows:**

- Same as UC-032 alternative flows, applied to `bonus_task`.

**Postconditions:**
- `bonus_task.completed` is `true`. `points_earned` reflects the cumulative total, up to a maximum of 6 for the day.

**Business Rules:**
- Completing the bonus task does not affect `streak_counts`. It earns extra points but has no impact on the streak gate.
- Maximum daily protocol score is 6 pts (1 + 2 + 3).

---

### Deload Days (UC-040–UC-043)

---

#### UC-040: Check Deload Status

**Actor(s):** Authenticated User  
**Endpoint:** `GET /deload/status`

**Preconditions:**
- `email` is provided as a query parameter.

**Basic Flow:**
1. System queries `deload_days` for an active (not yet completed) deload record for the user.
2. No active deload found; system returns `{ "status": "success", "data": { "active": false } }`.
3. Active deload found; system returns `{ "status": "success", "data": { "active": true, "deload": <record>, "activity_options": [ <list of 5 recovery activities> ] } }`.

**Postconditions:**
- Client knows whether a deload day is active and, if so, receives the five available recovery activity options.

**Business Rules — Recovery Activity Options:**

| Code | Label |
|------|-------|
| `meditation` | Meditation |
| `walk` | Walk in Nature |
| `bath` | Relaxing Bath |
| `social_time` | Quality Social Time |
| `digital_detox` | Digital Detox |

---

#### UC-041: Complete Deload Activity

**Actor(s):** Authenticated User  
**Endpoint:** `POST /deload/complete`

**Preconditions:**
- An active (incomplete) deload day document exists in `deload_days` for the user.
- `activity` in the request body is one of: `meditation`, `walk`, `bath`, `social_time`, `digital_detox`.

**Basic Flow:**
1. User submits `email` and chosen `activity` code.
2. System validates the activity code against the allowed set.
3. System retrieves the active (incomplete) deload record.
4. System marks the deload as complete: sets `activity_chosen`, `completed: true`, `completed_at: <UTC timestamp>`, `points_earned: 1`.
5. System upserts the deload document.
6. System returns `{ "status": "success", "message": "Deload day complete. +1 point. Streak preserved.", "activity": "<Activity Label>" }`.

**Alternative Flows:**

- **AF-041-A: Invalid activity code** — `activity` not in the valid set. System returns `{ "status": "error", "message": "Invalid activity. Choose from: meditation, walk, bath, social_time, digital_detox" }`.
- **AF-041-B: No active deload** — `find_active` returns None. System returns `{ "status": "error", "message": "No active deload day found." }`.

**Postconditions:**
- The deload record is marked complete. The user's streak is preserved — completing the deload counts as the qualifying day.

**Business Rules:**
- Completing a deload earns exactly 1 point regardless of which activity is chosen.
- Only one activity may be selected per deload day; there is no multi-activity option.
- A deload day is not a streak break — it is a planned recovery event that maintains streak continuity.

---

#### UC-042: View Deload History

**Actor(s):** Authenticated User  
**Endpoint:** `GET /deload/history`

**Preconditions:**
- `email` is provided as a query parameter.

**Basic Flow:**
1. System queries `deload_days` for all documents matching the user's email.
2. System returns `{ "status": "success", "data": [ <list of all deload records> ] }`.

**Alternative Flows:**

- **AF-042-A: No deload records** — System returns an empty list in the `data` field.

**Postconditions:**
- Client receives all historical deload records, each showing the trigger streak, chosen activity, completion status, and timestamp.

---

#### UC-043: Automatic Deload After Streak

**Actor(s):** System (triggered by streak-tracking logic after each 7th consecutive streak day)

**Preconditions:**
- The user's cumulative streak has reached a multiple of 7 (7, 14, 21, …).
- No deload day document already exists for today's date and this user.

**Basic Flow:**
1. External streak or protocol completion logic detects the 7-day milestone.
2. System calls `DeloadService.create_deload_day(email, trigger_streak)`.
3. System checks for an existing deload document for today's date (idempotency guard).
4. No existing document found; system creates a new deload document: `{ email, date: today, trigger_streak, activity_chosen: null, completed: false, completed_at: null, points_earned: 0 }`.
5. System upserts into `deload_days` and returns the created document.

**Alternative Flows:**

- **AF-043-A: Deload already created for today** — At step 3, an existing document is found for today. System returns the existing document unchanged (idempotent behaviour).

**Postconditions:**
- A new deload day document exists in `deload_days` in an incomplete state, awaiting the user's activity choice.

**Business Rules:**
- Deload creation is idempotent — calling it multiple times for the same date produces no duplicates.
- The `trigger_streak` field records which streak length triggered the deload (e.g., 7, 14, 21) for historical reference.
- The deload must be completed by the user via UC-041; it is not auto-completed.

---

### 30-Day Programs (UC-050–UC-055)

---

#### UC-050: Start Program

**Actor(s):** Authenticated User  
**Endpoint:** `POST /programs/start`

**Preconditions:**
- No active program exists for the user. Only one program may be active at a time.
- `goal_code` is a non-empty string (1–100 characters).
- `level` is one of: `beginner`, `medium`, `advanced`. Defaults to `beginner`.

**Basic Flow:**
1. User submits `email`, `goal_code`, and optional `level`.
2. System validates the `level` value against the allowed set.
3. System queries `user_programs` for any active program document for this email.
4. No active program found; system creates the program document:
   - `email`, `goal_code`, `level`, `start_date` (today), `current_day: 1`, `current_phase: "START"`, `status: "active"`, `completed_days: []`, `total_days: 30`, `created_at`.
5. System inserts the document into `user_programs`.
6. System retrieves the Day 1 tasks for the given `goal_code`, `current_phase`, and `level`.
7. System returns `{ "status": "success", "message": "30-day program started. Day 1 begins now.", "data": { <program>, "today_tasks": [<task strings>] } }`.

**Alternative Flows:**

- **AF-050-A: Invalid level** — System returns `{ "status": "error", "message": "level must be: beginner, medium, or advanced" }`.
- **AF-050-B: Active program already exists** — System returns `{ "status": "error", "message": "You already have an active program. Complete or abandon it first." }`.

**Postconditions:**
- A new program document exists in `user_programs` at Day 1, Phase START, with an empty `completed_days` list.

**Business Rules:**
- Goal codes with defined phase task content: `focus_productivity`, `build_discipline`, `physical_health`, `studying`, `mental_balance`. All other codes fall back to a default generic task set.
- Programs are never deleted on completion — `status` changes to `"completed"`. Historical programs are retained in `user_programs`.

---

#### UC-051: View Program Status

**Actor(s):** Authenticated User  
**Endpoint:** `GET /programs/status`

**Preconditions:**
- `email` is provided as a query parameter.

**Basic Flow:**
1. System queries `user_programs` for the active program document.
2. Active program found; system retrieves today's task list for the current `goal_code`, `current_phase`, and `level`.
3. System returns `{ "status": "success", "data": { <program fields>, "today_tasks": [<task strings>] } }`.
4. No active program; system returns `{ "status": "success", "data": null, "message": "No active program." }`.

**Postconditions:**
- Client receives the full program state: current day (1–30), current phase name, list of completed day numbers, days remaining, and today's assigned task strings.

---

#### UC-052: Complete Program Day

**Actor(s):** Authenticated User  
**Endpoint:** `POST /programs/complete-day`

**Preconditions:**
- An active program exists for the user.
- `current_day` has not already been added to `completed_days`.

**Basic Flow:**
1. User submits `email`.
2. System retrieves the active program document.
3. System checks whether `current_day` is already in `completed_days`; if yes, returns "Day already completed."
4. System appends `current_day` to `completed_days`.
5. System computes `next_day = current_day + 1`.
6. If `next_day > 30`: program is complete — see UC-055.
7. System determines the phase for `next_day` via `_get_phase_for_day(next_day)`.
8. System upserts the program document with updated `current_day`, `current_phase`, and `completed_days`.
9. System retrieves task strings for the new `current_day`, `current_phase`, and `level`.
10. System returns `{ "status": "success", "message": "Day <N> complete. Day <N+1> unlocked.", "data": { current_day, current_phase, tomorrow_tasks, days_remaining } }`.

**Alternative Flows:**

- **AF-052-A: No active program** — System returns `{ "status": "error", "message": "No active program." }`.
- **AF-052-B: Day already completed** — System returns `{ "status": "success", "message": "Day already completed.", "data": <program> }`.

**Postconditions:**
- `completed_days` includes the completed day number. `current_day` advances by 1. `current_phase` may have changed if a phase boundary was crossed.

**Business Rules:**
- Each day must be completed sequentially. Days cannot be skipped.
- The phase transition is automatic and non-reversible — once the program advances to RHYTHM, it cannot go back to START.

---

#### UC-053: Progress Through Phases

**Actor(s):** System (triggered by UC-052 when a day completion crosses a phase boundary)

**Preconditions:**
- `complete_day` has been called and `next_day` crosses a phase boundary.

**Basic Flow:**
1. System calls `_get_phase_for_day(next_day)` to resolve the phase name.
2. If `next_day` is in [1–7]: phase is `"START"`.
3. If `next_day` is in [8–21]: phase is `"RHYTHM"`.
4. If `next_day` is in [22–30]: phase is `"REINFORCEMENT"`.
5. System updates `current_phase` in the program document.

**Phase Definitions:**

| Phase | Days | Focus | Intensity |
|-------|------|-------|-----------|
| START | 1–7 | Micro habits and low-resistance routines | Easy |
| RHYTHM | 8–21 | Stable targets, weekly review, consistency building | Medium |
| REINFORCEMENT | 22–30 | Deeper work, focus protection, final reflection | Hard |

**Postconditions:**
- `current_phase` in the program document reflects the phase for the new current day.

**Business Rules:**
- Task content becomes progressively more demanding across phases. For example, in `build_discipline / advanced`: START = "No phone until noon", RHYTHM = "3 discipline habits daily", REINFORCEMENT = "72-hr extreme discipline sprint".

---

#### UC-054: View Phase Content

**Actor(s):** Authenticated User  
**Endpoint:** `GET /programs/phases`

**Preconditions:**
- User is authenticated.

**Basic Flow:**
1. System returns the static phase definition list (no database query required).
2. Response: `{ "status": "success", "data": [ { name, days, focus, intensity, description } × 3 ] }`.

**Postconditions:**
- Client receives descriptions for all three phases: START, RHYTHM, and REINFORCEMENT — useful for onboarding and setting expectations before starting a program.

---

#### UC-055: Complete Program

**Actor(s):** System (triggered by UC-052 when Day 30 is completed)

**Preconditions:**
- `complete_day` has been called for the program's Day 30 (i.e., `next_day > 30`).

**Basic Flow:**
1. User completes Day 30 via UC-052; system detects `next_day > 30`.
2. System appends day 30 to `completed_days`.
3. System upserts the program document with `status: "completed"`, `current_day: 30`, and `completed_at: <UTC timestamp>`.
4. System returns `{ "status": "success", "message": "Program complete! 30-day journey finished.", "data": { "completed": true, "total_days_done": 30 } }`.

**Postconditions:**
- Program `status` is `"completed"` in `user_programs`. The user may now start a new program.

**Business Rules:**
- Program completion triggers eligibility for the `program_complete` reward (UC-102 / UC-104) — that reward requires `completed_programs >= 1`.
- Program completion feeds into the `program_score` identity component, raising the identity score on the next recalculation.

---

### Weekly Reviews (UC-060–UC-063)

---

#### UC-060: Submit Weekly Review

**Actor(s):** Authenticated User  
**Endpoint:** `POST /weekly-reviews/submit`

**Preconditions:**
- Request body: `email`, `what_worked` (1–2000 chars), `what_distracted` (1–2000 chars), `what_to_change` (1–2000 chars).

**Basic Flow:**
1. User submits the three reflection fields.
2. System determines the current ISO week number and year from the server clock.
3. System scans `what_distracted` and `what_to_change` for keyword signals to generate contextual suggestions (see UC-063).
4. System generates a reflection paragraph combining `what_worked` and `what_to_change` content.
5. System stores a new document in `weekly_reviews`: `email`, `week_number`, `year`, the three response fields, `suggestions` list, `reflection` string, `created_at`.
6. System returns `{ "status": "success", "message": "Review saved.", "data": { suggestions, reflection, week_number } }`.

**Alternative Flows:**

- **AF-060-A: No keyword matches in suggestion generation** — If none of the five keyword signals are detected, the system returns two generic fallback suggestions instead.

**Postconditions:**
- A new review document exists in `weekly_reviews`. The client receives AI-generated (keyword-matching) suggestions and a reflection paragraph immediately on submission.

**Business Rules:**
- Multiple reviews per week can be submitted — no unique-per-week constraint is enforced. Retrieval uses "latest" and "history" models.
- The `week_number` is the ISO week number of the submission date (not a configurable field).

---

#### UC-061: View Review History

**Actor(s):** Authenticated User  
**Endpoint:** `GET /weekly-reviews/history`

**Preconditions:**
- `email` is provided as a query parameter.

**Basic Flow:**
1. System queries `weekly_reviews` for all documents matching the email, ordered by `created_at` descending.
2. System returns `{ "status": "success", "data": [ <list of review documents> ] }`.

**Alternative Flows:**

- **AF-061-A: No reviews exist** — System returns an empty list in the `data` field.

**Postconditions:**
- Client receives a full history of all weekly review submissions in reverse chronological order.

---

#### UC-062: View Latest Review

**Actor(s):** Authenticated User  
**Endpoint:** `GET /weekly-reviews/latest`

**Preconditions:**
- At least one review exists for the user.
- `email` is provided as a query parameter.

**Basic Flow:**
1. System queries `weekly_reviews` for the single most recent document for the email.
2. Document found; system returns `{ "status": "success", "data": <review document> }`.

**Alternative Flows:**

- **AF-062-A: No reviews exist** — System returns `{ "status": "error", "message": "No reviews found." }`.

**Postconditions:**
- Client receives the most recently submitted review including the stored suggestions and reflection.

---

#### UC-063: Review Affects Identity Score

**Actor(s):** System (triggered when weekly review count contributes to `weekly_review_score` component)

**Preconditions:**
- A weekly review has been submitted via UC-060.

**Basic Flow:**
1. The `weekly_review_score` component in `user_identity` can be updated externally to reflect the user's accumulated review count.
2. System calls `IdentityService.update_component(email, "weekly_review_score", new_value)`.
3. System clamps the new value to [0.0, 100.0] and upserts the identity document.
4. System triggers a recalculation (UC-011) to update the composite identity score.

**Postconditions:**
- `weekly_review_score` is updated; composite identity score is recalculated.

**Business Rules:**
- The `frame_reflection` reward (UC-104) requires `weekly_reviews >= 5`. Reaching this threshold unlocks the Reflection Master avatar frame.
- The `weekly_review_score` component carries a 10% weight in the composite identity score.

**Keyword Suggestion Rules (applied during UC-060):**

| Keyword Signal (case-insensitive, in `what_distracted` + `what_to_change`) | Suggestion Generated |
|-----------------------------------------------------------------------------|---------------------|
| "phone", "social media", "scroll" | "Try a 1-hour digital sunset before bed — no phone, just wind-down." |
| "focus", "distract", "concentrat" | "Protect your first 90 minutes in the morning as sacred deep-work time." |
| "sleep", "tired", "energy" | "Anchor your sleep schedule — same bedtime and wake time every day." |
| "plan", "organize", "schedule" | "Use the daily planner to time-block your top 3 priorities each morning." |
| "exercise", "workout", "movement" | "Commit to movement before checking any messages — even a 15-min walk counts." |
| (no match) | Two generic fallback suggestions about consistency and minimum tasks |

---

### Goals (UC-070–UC-074)

---

#### UC-070: Browse Goal Options

**Actor(s):** Anonymous User, Authenticated User  
**Endpoint:** `GET /goals/options`

**Preconditions:**
- None. This endpoint does not require authentication.

**Basic Flow:**
1. System returns the static list of available goal options (no database query).
2. Each option includes `code`, `title`, `description`, and `schedule`.

**Available Goals:**

| Code | Title | Schedule |
|------|-------|----------|
| `focus_productivity` | Focus & Productivity | Daily work sessions |
| `nutrition` | Nutrition | Every meal |
| `self_discipline` | Self-Discipline | Daily |
| `studying` | Studying | Daily study blocks |
| `find_people` | Find your person / people | Weekly community check-in |
| `find_direction` | Find Identity / Direction | Daily reflection |
| `health` | Health | Daily |

**Postconditions:**
- Client receives all available goal options. This data is used to populate the goal selection UI on the onboarding screen.

---

#### UC-071: Set Goal

**Actor(s):** Authenticated User  
**Endpoint:** `POST /goals/set`

**Preconditions:**
- `email` is 3–320 characters.
- `goal_code` must match one of the codes listed in UC-070.

**Basic Flow:**
1. User submits `email` and `goal_code`.
2. System looks up the goal option by code in the static options dictionary.
3. Goal code found; system constructs the goal data document: `email`, `goalCode`, `goalTitle`, `goalDescription`, `schedule`, `updatedAt`.
4. System upserts the document in the `goals` collection (one record per user — existing goals are replaced).
5. System returns `{ "status": "success", "message": "Goal saved successfully.", "data": <goal_data> }`.

**Alternative Flows:**

- **AF-071-A: Unknown goal code** — `goal_code` not in the options dictionary. System returns `{ "status": "error", "message": "Goal code is not supported." }`.

**Postconditions:**
- The user has exactly one active goal in `goals`. Re-setting overwrites the previous goal without creating a history entry.

**Business Rules:**
- A user can change their goal at any time. The upsert pattern retains only the most recently set goal.
- The goal code drives program task selection (UC-050) and resource / recommendation retrieval (UC-073, UC-074).

---

#### UC-072: View Current Goal

**Actor(s):** Authenticated User  
**Endpoint:** `GET /goals/user`

**Preconditions:**
- `email` is provided as a query parameter.
- A goal has been set for the user.

**Basic Flow:**
1. System queries `goals` for the document matching the email.
2. Document found; system converts `_id` to a string and returns `{ "status": "success", "data": <goal document> }`.

**Alternative Flows:**

- **AF-072-A: No goal set** — System returns `{ "status": "error", "message": "Goal not found." }`.

**Postconditions:**
- Client receives the stored goal data including code, title, description, schedule, and when it was last updated.

---

#### UC-073: View Goal Resources

**Actor(s):** Authenticated User  
**Endpoint:** `GET /goals/resources`

**Preconditions:**
- `goal_code` query parameter must match a code that has defined resources.

**Basic Flow:**
1. User requests resources for a specific `goal_code`.
2. System looks up the `GOAL_RESOURCES` dictionary by code.
3. Resources found; system returns `{ "status": "success", "data": { "books": [...], "videos": [...] } }`.

**Alternative Flows:**

- **AF-073-A: No resources for goal code** — System returns `{ "status": "error", "message": "No resources found for goal: <goal_code>" }`.

**Postconditions:**
- Client receives a curated list of books (3 per goal) and videos (5 per goal), each with title, author/type, and a short description.

**Business Rules:**
- Resources are static, curated content — not dynamically fetched from external APIs.
- Goal codes with defined resources: `focus_productivity`, `build_discipline`, `physical_health`, `mental_balance`, `personal_growth`, `social_motivation`, `life_reset`, `studying`, `find_people`, `find_direction`.

---

#### UC-074: Get Goal Recommendations

**Actor(s):** Authenticated User  
**Endpoint:** `GET /goals/recommendations`

**Preconditions:**
- `goal_code` is provided as a query parameter.
- `level` is one of `beginner`, `medium`, `advanced` (defaults to `beginner`).

**Basic Flow:**
1. User requests habit recommendations for a `goal_code` at a difficulty `level`.
2. System validates the `level` value.
3. System looks up `HABIT_RECOMMENDATIONS[goal_code][level]`.
4. System returns `{ "status": "success", "data": [ { name, description } × 3–4 habits ] }`.

**Alternative Flows:**

- **AF-074-A: Invalid level** — System returns `{ "status": "error", "message": "level must be: beginner, medium, or advanced" }`.
- **AF-074-B: No recommendations for goal code** — System returns `{ "status": "error", "message": "No recommendations for goal: <goal_code>" }`.

**Postconditions:**
- Client receives 3–4 concrete, named habit recommendations tailored to the goal and difficulty level. Each includes a `name` (short label) and `description` (actionable instruction).

---

### Community Groups (UC-080–UC-083)

---

#### UC-080: Browse Groups

**Actor(s):** Authenticated User  
**Endpoint:** `GET /groups/`

**Preconditions:**
- User is authenticated.

**Basic Flow:**
1. System queries the `groups` collection for all documents.
2. System returns the full list, or an empty list if no groups exist.

**Postconditions:**
- Client receives all available group records for browsing.

---

#### UC-081: Create Group

**Actor(s):** Authenticated User  
**Endpoint:** `POST /groups/create`

**Preconditions:**
- `name` is 1–200 characters.

**Basic Flow:**
1. User submits a group creation request with `name`.
2. System inserts a new group document `{ "name": name }` into the `groups` collection.
3. System returns `{ "message": "Group created", "id": "<inserted_id>" }`.

**Alternative Flows:**

- **AF-081-A: Database error** — System returns `{ "error": "Failed to create group: <detail>" }`.

**Postconditions:**
- A new group document exists in `groups`.

**Business Rules:**
- There is no duplicate-name guard — groups with identical names can be created.
- The creator is not automatically added as a member or assigned an admin role in the group document.

---

#### UC-082: Join Group

**Actor(s):** Authenticated User  
**Endpoint:** `POST /groups/join`

**Preconditions:**
- `group_id` identifies an existing group document.
- `user_id` is the requesting user's identifier.

**Basic Flow:**
1. User submits `group_id` and `user_id`.
2. System calls `GroupService.join_group(group_id, user_id)`.
3. System verifies the group exists, then records the membership.
4. System returns `{ "message": "Joined group" }`.

**Alternative Flows:**

- **AF-082-A: Group not found** — `join_group` returns `false` or `None`. System raises HTTP 404: `{ "detail": "Group not found" }`.

**Postconditions:**
- The user is recorded as a member of the specified group.

---

#### UC-083: View Group Members

**Actor(s):** Authenticated User  
**Endpoint:** Membership data is stored in the `groups` collection document.

**Preconditions:**
- The group exists and the user is authenticated.

**Basic Flow:**
1. System retrieves the group document by `group_id`.
2. System returns the group's `members` array.

**Alternative Flows:**

- **AF-083-A: Group not found** — System returns an appropriate 404 error.

**Postconditions:**
- Client receives the list of member identifiers in the group.

**Business Rules:**
- Group posts exist in the data model (`posts` collection, `group_post.py` domain model) but no group post controller is mounted in the current `create_app()` implementation. Viewing and creating posts is a future feature.

---

### Challenges (UC-090–UC-098)

---

#### UC-090: Browse Challenges

**Actor(s):** Authenticated User  
**Endpoint:** `GET /challenges/`

**Preconditions:**
- User is authenticated.

**Basic Flow:**
1. System queries the `challenges` collection (via `PostRepository`) for all documents.
2. System converts `_id` fields to strings for JSON serialisation.
3. System returns the full list of challenge objects.

**Postconditions:**
- Client receives all challenge records. No `is_active` filtering is applied at the service layer — all challenges are returned.

---

#### UC-091: Create Challenge

**Actor(s):** Admin  
**Endpoint:** `POST /challenges/create`

**Preconditions:**
- `title` is 1–200 characters.

**Basic Flow:**
1. Admin submits a challenge creation request with `title`.
2. System inserts `{ "title": title }` into the challenges collection.
3. System returns `{ "message": "Challenge created", "id": "<inserted_id>" }`.

**Postconditions:**
- A new challenge document exists. All additional fields (description, dates, `is_active`, tasks) must be added via UC-096.

---

#### UC-092: Register for Challenge

**Actor(s):** Authenticated User  
**Endpoint:** `POST /challenges/{challenge_id}/register`

**Preconditions:**
- `challenge_id` is a valid MongoDB ObjectId string.
- `user_email` is provided in the request body.

**Basic Flow:**
1. User submits a registration request with their email.
2. System validates and converts the `challenge_id` ObjectId.
3. System applies `$addToSet` to the challenge's `participants` array, adding `user_email`.
4. Challenge found and updated; system returns `{ "status": "success", "message": "Registered for challenge." }`.

**Alternative Flows:**

- **AF-092-A: Invalid ObjectId** — System returns `{ "status": "error", "message": "Invalid challenge ID." }`.
- **AF-092-B: Challenge not found** — `update_one` matches zero documents. System returns `{ "status": "error", "message": "Challenge not found." }`.

**Postconditions:**
- The user's email is in the challenge's `participants` array. `$addToSet` ensures no duplicates — registering twice is idempotent.

---

#### UC-093: Submit Proof

**Actor(s):** Authenticated User  
**Endpoint:** `POST /challenges/{challenge_id}/submit`

**Preconditions:**
- `user_email` is provided.
- `day` is an integer between 1 and 30 (inclusive).
- `proof_url` is 1–2000 characters (a URL pointing to the proof image or media).

**Basic Flow:**
1. User submits `user_email`, `day`, and `proof_url` for a specific challenge.
2. System creates a submission document: `challenge_id`, `user_email`, `day`, `proof_url`, `status: "pending"`, `submitted_at: <UTC timestamp>`.
3. System inserts into `challenge_submissions`.
4. System returns `{ "status": "success", "message": "Proof submitted. Awaiting review.", "submission_id": "<id>" }`.

**Postconditions:**
- A new submission exists in `challenge_submissions` with `status: "pending"`. Visible to admins for moderation (UC-095, UC-098).

**Business Rules:**
- There is no duplicate-submission guard — a user can submit multiple proofs for the same day.
- Proof URL format is not validated beyond length; any string is accepted.

---

#### UC-094: View Leaderboard

**Actor(s):** Authenticated User  
**Endpoint:** `GET /challenges/{challenge_id}/leaderboard`

**Preconditions:**
- `challenge_id` is a valid identifier.

**Basic Flow:**
1. System retrieves all submissions for the challenge from `challenge_submissions`.
2. System filters to `status: "approved"` submissions and counts them per `user_email`.
3. System sorts participants by `completed_days` count descending.
4. System assigns rank numbers starting from 1.
5. System returns `{ "status": "success", "data": [ { email, completed_days, streak, rank } × N ] }`.

**Postconditions:**
- Client sees a ranked list of participants ordered by number of approved completed days.

**Business Rules:**
- Only approved submissions count toward the leaderboard — pending and rejected submissions are excluded.
- The `streak` field is computed as 0 for all users in the current implementation (streak calculation in the leaderboard is a placeholder).

---

#### UC-095: Moderate Submission

**Actor(s):** Admin  
**Endpoint:** `PUT /challenges/{challenge_id}/submissions/{submission_id}`

**Preconditions:**
- `submission_id` identifies an existing submission in `challenge_submissions`.
- `status` in the request body is either `"approved"` or `"rejected"`.

**Basic Flow:**
1. Admin submits a moderation decision.
2. System validates the `status` value against the allowed set.
3. System calls `update_status(submission_id, status)` which performs a `$set` on the submission document.
4. Submission found and updated; system returns `{ "status": "success", "message": "Submission approved." }` (or "rejected.").

**Alternative Flows:**

- **AF-095-A: Invalid status value** — System returns `{ "status": "error", "message": "status must be 'approved' or 'rejected'" }`.
- **AF-095-B: Submission not found** — System returns `{ "status": "error", "message": "Submission not found." }`.

**Postconditions:**
- Submission `status` is updated. Approved submissions immediately affect the leaderboard (UC-094).

---

#### UC-096: Update Challenge

**Actor(s):** Admin  
**Endpoint:** `PUT /challenges/{challenge_id}`

**Preconditions:**
- `challenge_id` is a valid ObjectId string.
- At least one of the allowed update fields is provided: `title`, `description`, `start_date`, `end_date`, `registration_deadline`, `is_active`.

**Basic Flow:**
1. Admin submits an update request.
2. System validates the ObjectId format.
3. System filters the update payload to allowed fields only.
4. System calls `update_one` with `$set`.
5. Challenge found and updated; system returns `{ "status": "success", "message": "Challenge updated." }`.

**Alternative Flows:**

- **AF-096-A: Invalid ObjectId** — `{ "status": "error", "message": "Invalid challenge ID." }`.
- **AF-096-B: No valid update fields** — `{ "status": "error", "message": "No valid fields to update." }`.
- **AF-096-C: Challenge not found** — `{ "status": "error", "message": "Challenge not found." }`.

**Postconditions:**
- The challenge document is updated with the provided fields.

---

#### UC-097: Delete Challenge

**Actor(s):** Admin  
**Endpoint:** `DELETE /challenges/{challenge_id}`

**Preconditions:**
- `challenge_id` is a valid ObjectId string.

**Basic Flow:**
1. Admin sends a DELETE request.
2. System validates and converts the ObjectId.
3. System calls `delete_one`; one document is removed.
4. System returns `{ "status": "success", "message": "Challenge deleted." }`.

**Alternative Flows:**

- Invalid ObjectId: `{ "status": "error", "message": "Invalid challenge ID." }`.
- Not found: `{ "status": "error", "message": "Challenge not found." }`.

**Postconditions:**
- The challenge document is removed. Participant registrations and proof submissions in `challenge_submissions` are not automatically cleaned up (orphaned records remain).

---

#### UC-098: View Submissions

**Actor(s):** Admin, Authenticated User  
**Endpoint:** `GET /challenges/{challenge_id}/submissions`

**Preconditions:**
- `challenge_id` is a valid identifier.

**Basic Flow:**
1. System retrieves all submission documents from `challenge_submissions` where `challenge_id` matches.
2. System returns the full list including pending, approved, and rejected submissions.

**Alternative Flows:**

- **AF-098-A: No submissions** — System returns an empty list.

**Postconditions:**
- Client receives all proof submissions for the challenge, including their current moderation status, for review or display.

---

### Rewards (UC-100–UC-104)

---

#### UC-100: Browse Reward Catalog

**Actor(s):** Authenticated User  
**Endpoint:** `GET /rewards/catalog`

**Preconditions:**
- User is authenticated.

**Basic Flow:**
1. System returns the static reward catalog (no database query required).
2. Response: `{ "status": "success", "data": [ <6 reward objects> ] }`.

**Reward Catalog:**

| Code | Title | Type | Trigger | Unlock Requirement |
|------|-------|------|---------|-------------------|
| `avatar_frame_7` | Silver Ring | avatar_frame | streak_7 | Streak ≥ 7 |
| `theme_midnight` | Midnight Theme | profile_theme | streak_14 | Streak ≥ 14 |
| `bg_elite` | Elite Background | background | streak_30 | Streak ≥ 30 |
| `focus_room` | Focus Room | focus_room | streak_60 | Streak ≥ 60 |
| `program_complete` | 30-Day Completion | badge | program_complete_1 | Programs completed ≥ 1 |
| `frame_reflection` | Reflection Master | avatar_frame | reviews_5 | Weekly reviews ≥ 5 |

**Postconditions:**
- Client receives the full catalog for display in the rewards UI.

---

#### UC-101: View Unlocked Rewards

**Actor(s):** Authenticated User  
**Endpoint:** `GET /rewards/user`

**Preconditions:**
- `email` query parameter provided.

**Basic Flow:**
1. System queries `user_rewards` for the user's reward document.
2. Document found; system returns `{ "status": "success", "data": <reward document> }`.
3. No document found; system returns a default: `{ "status": "success", "data": { "unlocked": [], "active_theme": "default" } }`.

**Postconditions:**
- Client receives the list of unlocked reward codes (with unlock timestamps) and currently active cosmetic settings (`active_theme`, `active_avatar_frame`, `active_background`, `active_focus_room`).

---

#### UC-102: Check for New Rewards

**Actor(s):** System, Authenticated User  
**Endpoint:** `POST /rewards/check-unlock`

**Preconditions:**
- Request body: `email`, `current_streak` (≥0 integer), `completed_programs` (≥0 integer), `weekly_reviews` (≥0 integer).

**Basic Flow:**
1. User or System submits current achievement metrics.
2. System retrieves the user's existing unlocked reward codes from `user_rewards`.
3. For each of the 6 rewards in the catalog not yet in the unlocked list, system evaluates:
   - Streak-based rewards: `current_streak >= required_streak`.
   - Program rewards: `completed_programs >= required_programs`.
   - Review rewards: `weekly_reviews >= required_reviews`.
4. For each newly qualifying reward, system calls `add_unlocked(email, code, timestamp)` to record it in `user_rewards`.
5. System returns `{ "status": "success", "newly_unlocked": [ { code, title } × N ], "message": "Unlocked N new reward(s)." }` (or "No new rewards unlocked.").

**Postconditions:**
- All newly qualifying rewards are added to the user's `unlocked` array. Already-unlocked rewards are never duplicated.

**Business Rules:**
- Reward unlocking is cumulative — unlocking `avatar_frame_7` (streak ≥ 7) does not prevent later unlocking `theme_midnight` (streak ≥ 14).
- The caller is responsible for passing accurate metrics; the endpoint does not independently re-derive them from other collections.

---

#### UC-103: Activate Reward

**Actor(s):** Authenticated User  
**Endpoint:** `POST /rewards/activate`

**Preconditions:**
- `reward_code` is a known catalog code.
- The reward is present in the user's `unlocked` list (i.e., it has been unlocked via UC-102).

**Basic Flow:**
1. User submits `email` and `reward_code`.
2. System validates the code against the catalog.
3. System checks that the reward is in the user's unlocked list.
4. System resolves the activation field from the reward type: `avatar_frame` → `active_avatar_frame`, `profile_theme` → `active_theme`, `background` → `active_background`, `focus_room` → `active_focus_room`.
5. System upserts the activation field in `user_rewards`.
6. System returns `{ "status": "success", "message": "<Reward Title> activated.", "activated": "<reward_code>" }`.

**Alternative Flows:**

- **AF-103-A: Unknown reward code** — `{ "status": "error", "message": "Unknown reward code." }`.
- **AF-103-B: Reward not yet unlocked** — `{ "status": "error", "message": "Reward not unlocked yet." }`.
- **AF-103-C: Badge type cannot be activated** — The `badge` type has no activation field. System returns `{ "status": "error", "message": "This reward type cannot be activated." }`.

**Postconditions:**
- The activation field is updated to the new reward code, replacing any previously active reward of the same type.

**Business Rules:**
- Only one reward per type can be active at a time. Activating a new avatar frame replaces the current one.
- Badges (e.g., `program_complete`) are awarded but cannot be "activated" — they are achievement records only.

---

#### UC-104: Reward Unlock Criteria

**Actor(s):** System (evaluated during UC-102)

**This use case documents the business rules governing reward unlock thresholds.**

**Unlock Conditions:**

| Reward Code | Metric Checked | Threshold |
|-------------|----------------|-----------|
| `avatar_frame_7` | `current_streak` | ≥ 7 days |
| `theme_midnight` | `current_streak` | ≥ 14 days |
| `bg_elite` | `current_streak` | ≥ 30 days |
| `focus_room` | `current_streak` | ≥ 60 days |
| `program_complete` | `completed_programs` | ≥ 1 |
| `frame_reflection` | `weekly_reviews` | ≥ 5 |

**Business Rules:**
- Rewards are purely cosmetic — no performance advantage is conferred.
- Once unlocked, a reward cannot be revoked (no unlock-reversal mechanism exists).
- The system design is premium-minimal: no badges are displayed as notifications, no points tallies are shown. Rewards are surfaced only when the user navigates to the Rewards section.

---

### Chat (UC-110–UC-116)

---

#### UC-110: View Conversations

**Actor(s):** Authenticated User  
**Endpoint:** `GET /chat/conversations`

**Preconditions:**
- `email` query parameter provided.

**Basic Flow:**
1. System queries `conversations` for all documents where the `participants` array contains the user's email.
2. System returns `{ "status": "success", "data": [ <list of conversation documents> ] }`.

**Postconditions:**
- Client receives all conversations the user participates in, including `last_message`, `last_message_at`, type, and participant list.

---

#### UC-111: Start Conversation

**Actor(s):** Authenticated User  
**Endpoint:** `POST /chat/conversations`

**Preconditions:**
- Request body: `sender_email` and `recipient_email`, both valid emails.
- They must be different addresses.
- `recipient_email` must correspond to an existing user account.

**Basic Flow:**
1. User submits `sender_email` and `recipient_email`.
2. System validates they are not the same address.
3. System looks up the recipient in `users` to confirm they exist.
4. System checks for an existing DM conversation between the two participants.
5. Existing conversation found; system returns it with message "Conversation already exists."
6. No existing conversation; system creates: `{ type: "dm", participants: [sender, recipient], last_message: null, last_message_at: <now>, challenge_id: null }`.
7. System inserts into `conversations` and returns `{ "status": "success", "data": <new conversation>, "message": "Conversation started." }`.

**Alternative Flows:**

- **AF-111-A: Self-messaging** — `sender_email == recipient_email`. System returns `{ "status": "error", "message": "Cannot start a conversation with yourself." }`.
- **AF-111-B: Recipient not found** — System returns `{ "status": "error", "message": "Recipient not found." }`.

**Postconditions:**
- A DM conversation document exists (or was confirmed to exist) in `conversations` between the two participants.

---

#### UC-112: Send Message

**Actor(s):** Authenticated User  
**Endpoint:** `POST /chat/conversations/{conversation_id}/messages`

**Preconditions:**
- `conversation_id` identifies an existing conversation.
- `sender_email` is a participant in the conversation.
- `content` is 1–4000 characters.

**Basic Flow:**
1. User submits `sender_email` and `content` for a specific conversation.
2. System retrieves the conversation document.
3. System verifies `sender_email` is in the `participants` array.
4. System creates a message document: `conversation_id`, `sender_email`, `content`, `sent_at: <UTC timestamp>`, `read_by: [sender_email]`.
5. System inserts into `messages`.
6. System updates the conversation's `last_message` and `last_message_at` fields.
7. System returns `{ "status": "success", "data": { <message with id> } }`.

**Alternative Flows:**

- **AF-112-A: Conversation not found** — `{ "status": "error", "message": "Conversation not found." }`.
- **AF-112-B: Sender not a participant** — `{ "status": "error", "message": "You are not a participant in this conversation." }`.

**Postconditions:**
- A new message document exists in `messages`. The conversation's `last_message` and `last_message_at` are updated.

**Business Rules:**
- The sender is automatically added to `read_by` on send. Read receipts for other participants are not automatically tracked at send time.

---

#### UC-113: Read Messages

**Actor(s):** Authenticated User  
**Endpoint:** `GET /chat/conversations/{conversation_id}/messages`

**Preconditions:**
- `conversation_id` identifies an existing conversation.

**Basic Flow:**
1. System queries `messages` for all documents where `conversation_id` matches, ordered chronologically by `sent_at`.
2. System returns `{ "status": "success", "data": [ <list of message documents> ] }`.

**Postconditions:**
- Client receives the full chronological message thread including sender email, content, send timestamp, and `read_by` array for each message.

---

#### UC-114: Search Users

**Actor(s):** Authenticated User  
**Endpoint:** `GET /chat/search-users`

**Preconditions:**
- `query` is at least 2 characters.

**Basic Flow:**
1. User submits a search query string.
2. System performs a case-insensitive regex search on the `email` and `name` fields in the `users` collection.
3. System returns up to 20 matching users with only `email` and `name` exposed (no password, no `_id`).
4. System returns `{ "status": "success", "data": [ { email, name } × up to 20 ] }`.

**Alternative Flows:**

- **AF-114-A: Query too short** — Fewer than 2 characters submitted. System returns `{ "status": "error", "message": "Query must be at least 2 characters." }`.

**Postconditions:**
- Client receives a list of matching users to select as a conversation recipient.

---

#### UC-115: Group Conversation

**Actor(s):** Authenticated User  
**Endpoint:** `POST /chat/conversations` (same endpoint as UC-111, with `type: "group"`)

**Preconditions:**
- Request includes multiple participant emails.

**Basic Flow:**
1. User creates a conversation with more than two participants.
2. System creates a conversation document with `type: "group"` and a `participants` array containing all provided emails.
3. System returns the new group conversation document.

**Postconditions:**
- A group conversation document exists in `conversations` with all listed participants.

**Business Rules:**
- Group conversations share the same `messages` collection and the same send / read mechanics as direct messages (UC-112, UC-113).

#### UC-116: AI Coach Conversation

**Actor(s):** Authenticated User  
**Endpoint:** `GET /chat/conversations/{conversation_id}/messages`, `POST /chat/conversations/{conversation_id}/messages`

**Preconditions:**
- The user is authenticated.
- The user has access to their automatically created coach thread.

**Basic Flow:**
1. User opens the AI Coach card in the Chat section.
2. System resolves the virtual `conversation_id = "coach"` thread for the authenticated user.
3. If the thread does not yet exist, the system creates a dedicated `type: "coach"` conversation and seeds it with a welcome message.
4. User sends a message to the coach thread.
5. System stores the user's message in `messages`.
6. System generates a short motivational coach reply in the same coaching tone and stores it as a second message in the same conversation.
7. System updates the conversation preview to the coach reply and returns success.

**Alternative Flows:**

- **AF-116-A: Coach thread not yet created** — On first access, the system creates the thread automatically with a welcome message from the AI coach.
- **AF-116-B: Conversation not found** — Existing chat errors still apply if the conversation id is invalid or inaccessible.

**Postconditions:**
- Every authenticated user has a persistent coaching thread that can be reopened at any time.
- The thread always speaks in a motivational, action-oriented tone focused on discipline, momentum, and practical next steps.

**Business Rules:**
- The AI coach is a system participant, not a separate user account.
- The coach thread uses the existing `conversations` and `messages` collections; no new collection is introduced.
- Responses must remain supportive, concise, and action-first rather than therapeutic or generic.

---

### Productivity — Water (UC-120–UC-122)

---

#### UC-120: Log Water Intake

**Actor(s):** Authenticated User  
**Endpoint:** `POST /productivity/water/log`

**Preconditions:**
- Request body: `email`, `date` (YYYY-MM-DD), `amount_ml` (50–2000 ml, default 250).

**Basic Flow:**
1. User submits a water intake event with email, date, and amount in millilitres.
2. System records the current UTC time in HH:MM format.
3. System creates an entry `{ time: <HH:MM>, amount_ml: <amount> }` and pushes it to the `logs` array in the `water_logs` document for the email + date combination (upsert).
4. System increments the `glasses` counter on the document.
5. System reads back the updated document.
6. System returns `{ "status": "success", "message": "+1 glass logged (<amount>ml).", "data": <updated log> }`.

**Postconditions:**
- A new intake entry is appended to the day's `water_logs` document. The `glasses` counter reflects the total number of log entries for the day.

**Business Rules:**
- Minimum log amount is 50 ml; maximum per entry is 2000 ml.
- Multiple logs per day are supported — each call adds one entry.
- "Glasses" counts log entries, not a conversion of ml to standard glass sizes.

---

#### UC-121: View Water Log

**Actor(s):** Authenticated User  
**Endpoint:** `GET /productivity/water`

**Preconditions:**
- `email` and `date` (YYYY-MM-DD) query parameters provided.

**Basic Flow:**
1. System queries `water_logs` for a document matching `email` and `date`.
2. Document found; system returns `{ "status": "success", "data": <log document> }`.
3. No document found; system returns a default structure: `{ email, date, glasses: 0, goal: 8, logs: [] }`.

**Postconditions:**
- Client receives the water log for the date including total glass count, daily goal, and the ordered list of individual intake entries.

---

#### UC-122: Set Daily Water Goal

**Actor(s):** Authenticated User  
**Endpoint:** `PUT /productivity/water/goal`

**Preconditions:**
- `goal_glasses` is an integer between 1 and 20 (inclusive).

**Basic Flow:**
1. User submits `email` and `goal_glasses`.
2. System upserts the `goal` field on today's `water_logs` document for the email.
3. System returns `{ "status": "success", "message": "Water goal set to <N> glasses/day." }`.

**Postconditions:**
- Today's water log document has the updated `goal` value. This value is displayed in the water tracking UI as the daily target.

---

### Productivity — Planner (UC-123–UC-126)

---

#### UC-123: Add Planner Task

**Actor(s):** Authenticated User  
**Endpoint:** `POST /productivity/planner`

**Preconditions:**
- `email`, `date` (YYYY-MM-DD), `title` (1–300 chars) are required.
- Optional: `description` (max 2000 chars, default `""`), `priority` (`high` / `medium` / `low`, default `medium`), `time_slot` (max 50 chars, default `""`).

**Basic Flow:**
1. User submits a task creation request.
2. System validates `priority` against the allowed set.
3. System creates the task document: all input fields plus `completed: false` and `created_at: <UTC timestamp>`.
4. System inserts into `planner_tasks` and returns `{ "status": "success", "data": { <task with id> } }`.

**Alternative Flows:**

- **AF-123-A: Invalid priority** — System returns `{ "status": "error", "message": "priority must be: high, medium, or low" }`.

**Postconditions:**
- A new planner task document exists in `planner_tasks` with `completed: false`.

---

#### UC-124: View Planner

**Actor(s):** Authenticated User  
**Endpoint:** `GET /productivity/planner`

**Preconditions:**
- `email` and `date` query parameters provided.

**Basic Flow:**
1. System queries `planner_tasks` for all documents matching `email` and `date`.
2. System returns `{ "status": "success", "data": [ <list of tasks> ] }`.

**Alternative Flows:**

- **AF-124-A: No tasks for date** — System returns an empty list in the `data` field.

**Postconditions:**
- Client receives all planner tasks for the requested date with their title, description, priority, time slot, and completion status.

---

#### UC-125: Update Task

**Actor(s):** Authenticated User  
**Endpoint:** `PUT /productivity/planner/{task_id}`

**Preconditions:**
- `task_id` in the path identifies an existing task.
- At least one of the allowed update fields is provided: `title`, `description`, `priority`, `time_slot`.

**Basic Flow:**
1. User submits an update request with the task ID and update fields.
2. System filters the payload to allowed fields only.
3. System calls `update_planner_task(task_id, updates)` which performs a `$set`.
4. Task found and updated; system returns `{ "status": "success", "message": "Task updated." }`.

**Alternative Flows:**

- **AF-125-A: No valid fields** — `{ "status": "error", "message": "No valid fields to update." }`.
- **AF-125-B: Task not found** — `{ "status": "error", "message": "Task not found." }`.

**Postconditions:**
- The planner task document is updated with the provided fields.

---

#### UC-126: Delete Task

**Actor(s):** Authenticated User  
**Endpoint:** `DELETE /productivity/planner/{task_id}`

**Preconditions:**
- `task_id` identifies an existing task.

**Basic Flow:**
1. System calls `delete_planner_task(task_id)`.
2. Task found and deleted; system returns `{ "status": "success", "message": "Task deleted." }`.

**Alternative Flows:**

- **AF-126-A: Task not found** — `{ "status": "error", "message": "Task not found." }`.

**Postconditions:**
- The task document is removed from `planner_tasks`.

**Business Rules:**
- There is no soft-delete mechanism. Deletion is permanent and immediate.

---

### Productivity — Spaced Repetition (UC-127–UC-130)

---

#### UC-127: Create SR Card

**Actor(s):** Authenticated User  
**Endpoint:** `POST /productivity/sr/cards`

**Preconditions:**
- `email`, `deck` (1–100 chars), `front` (1–1000 chars), `back` (1–1000 chars) are all required.

**Basic Flow:**
1. User submits a card creation request with email, deck name, front text, and back text.
2. System creates a card document with SM-2 initial values: `ease_factor: 2.5`, `interval_days: 1`, `repetitions: 0`, `next_review_date: today` (ISO date).
3. System inserts into `sr_cards`.
4. System returns `{ "status": "success", "data": { <card with id> } }`.

**Postconditions:**
- A new SR card is created and immediately due for review (`next_review_date` = today).

**Business Rules:**
- The `deck` field organises cards into named groups within a user's collection.
- SM-2 initial values follow the standard SuperMemo algorithm starting conditions: ease factor 2.5, interval 1 day, 0 repetitions.

---

#### UC-128: Review SR Card

**Actor(s):** Authenticated User  
**Endpoint:** `POST /productivity/sr/cards/{card_id}/review`

**Preconditions:**
- `card_id` identifies an existing card owned by the user.
- `ease` is an integer 1–4: 1 = Again, 2 = Hard, 3 = Good, 4 = Easy.

**Basic Flow:**
1. User submits a review with the `ease` rating.
2. System retrieves the card's current SM-2 state: `ease_factor`, `interval_days`, `repetitions`.
3. System applies the SM-2 algorithm:
   - If `ease < 3` (Again or Hard): `repetitions = 0`, `interval = 1` day.
   - If `ease >= 3` (Good or Easy): increment `repetitions`; interval = 1 day (rep 1) → 6 days (rep 2) → `interval * ease_factor` (rep 3+).
   - `new_ease_factor = max(1.3, ease_factor + 0.1 - (5 - ease) * (0.08 + (5 - ease) * 0.02))`.
4. System computes `next_review_date = today + new_interval` days (ISO date string).
5. System updates the card with new `ease_factor`, `interval_days`, `repetitions`, `next_review_date`.
6. System returns `{ "status": "success", "message": "Review saved. Next review in <N> day(s).", "next_review_date": "<date>" }`.

**Alternative Flows:**

- **AF-128-A: Card not found** — `{ "status": "error", "message": "Card not found." }`.

**Postconditions:**
- The card's SM-2 scheduling metadata is updated. The card will next appear in the review queue (`GET /productivity/sr/review`) on the computed `next_review_date`.

**Business Rules:**
- Ease factor has a floor of 1.3 to prevent interval collapse.
- Again (1) or Hard (2) resets the interval to 1 day — the card must be reviewed again tomorrow.
- Easy (4) on a mature card can produce very long intervals (weeks or months).

---

#### UC-129: View SR Queue

**Actor(s):** Authenticated User  
**Endpoint:** `GET /productivity/sr/review`

**Preconditions:**
- `email` query parameter provided.

**Basic Flow:**
1. System determines today's date in ISO format from the server clock.
2. System queries `sr_cards` for all cards belonging to the user where `next_review_date <= today`.
3. System returns `{ "status": "success", "data": [ <due cards> ], "count": <N> }`.

**Alternative Flows:**

- **AF-129-A: No cards due** — System returns an empty list with `count: 0`.

**Postconditions:**
- Client receives only the cards that are due today or overdue, ready for review.

---

#### UC-130: SR Algorithm

**Actor(s):** System (executed during UC-128)

**This use case documents the SM-2 algorithm implementation in detail.**

**Algorithm Steps:**

1. Input: `ease` (1–4), current `ease_factor` (float ≥ 1.3), current `interval_days` (int), current `repetitions` (int).
2. If `ease < 3`: `new_repetitions = 0`, `new_interval = 1`.
3. If `ease >= 3`:
   - `new_repetitions = repetitions + 1`
   - If `new_repetitions == 1`: `new_interval = 1`
   - If `new_repetitions == 2`: `new_interval = 6`
   - If `new_repetitions >= 3`: `new_interval = round(interval_days * ease_factor)`
4. `new_ease_factor = max(1.3, ease_factor + 0.1 - (5 - ease) * (0.08 + (5 - ease) * 0.02))`
5. `next_review_date = today + timedelta(days=new_interval)`

**Business Rules:**
- Ease factor floor is 1.3. This prevents the interval from shrinking to near-zero for difficult cards.
- The algorithm is the standard SuperMemo SM-2 (1987) formulation.

---

### Productivity — Brainstorm (UC-131–UC-132)

---

#### UC-131: Create Brainstorm Session

**Actor(s):** Authenticated User  
**Endpoint:** `POST /productivity/brainstorm`

**Preconditions:**
- `email` and `title` (1–200 chars) are required.
- `tags` (list of strings) is optional, defaults to an empty list.

**Basic Flow:**
1. User submits a session creation request with title and optional tags.
2. System creates the session document: `email`, `title`, `ideas: []`, `tags`, `created_at: <UTC timestamp>`, `updated_at: <UTC timestamp>`.
3. System inserts into `brainstorm_sessions`.
4. System returns `{ "status": "success", "data": { <session with id> } }`.

**Alternative Flows:**

- **AF-131-A: Database error** — System returns `{ "status": "error", "message": "Failed to create session: <detail>" }`.

**Postconditions:**
- A new, empty brainstorm session document exists in `brainstorm_sessions` with an empty `ideas` array.

**Business Rules:**
- There is no limit on the number of brainstorm sessions a user can create.
- Sessions are not scoped to a specific date — they persist indefinitely until explicitly deleted.

---

#### UC-132: Add Ideas to Session

**Actor(s):** Authenticated User  
**Endpoint:** `POST /productivity/brainstorm/{session_id}/ideas`

**Preconditions:**
- `session_id` identifies an existing brainstorm session owned by the user.
- `content` is 1–2000 characters.

**Basic Flow:**
1. User submits idea content for a specific session.
2. System retrieves the session document to verify it exists.
3. System creates an idea entry: `{ content: <text>, added_at: <UTC timestamp> }`.
4. System pushes the entry to the session's `ideas` array.
5. System updates the session's `updated_at` to the current UTC timestamp.
6. System returns `{ "status": "success", "message": "Idea added.", "data": <idea entry> }`.

**Alternative Flows:**

- **AF-132-A: Session not found** — System returns `{ "status": "error", "message": "Session not found." }`.

**Postconditions:**
- The new idea is appended to the session's `ideas` array. The session's `updated_at` timestamp is refreshed.

**Business Rules:**
- There is no limit on the number of ideas per session.
- Ideas cannot be individually deleted — only the entire session can be deleted (via `DELETE /productivity/brainstorm/{session_id}`).
- Ideas are stored inline in the session document's `ideas` array, not as separate documents.

---

## Appendix A: Endpoint-to-Use-Case Mapping

| Endpoint | Method | Use Case |
|----------|--------|----------|
| `/users/register` | POST | UC-001 |
| `/users/login` | POST | UC-002 |
| `/users/logout` | POST | UC-003 |
| `/users/profile` | GET | UC-004 |
| `/users/profile` | PUT | UC-005 |
| `/users/test-result` | POST | UC-006 |
| `/users/me` | GET | UC-007 |
| `/identity/profile` | GET | UC-010, UC-013 |
| `/identity/recalculate` | POST | UC-011 |
| `/habits/create` | POST | UC-020 |
| `/habits/` | GET | UC-021 |
| `/habits/{id}/complete` | POST | UC-022 |
| `/habits/{id}` | DELETE | UC-023 |
| `/daily-protocols/today` | GET | UC-030 |
| `/daily-protocols/create` | POST | UC-031 |
| `/daily-protocols/complete-task` (minimum) | POST | UC-032 |
| `/daily-protocols/complete-task` (target) | POST | UC-033 |
| `/daily-protocols/complete-task` (bonus) | POST | UC-034 |
| `/daily-protocols/history` | GET | UC-025 (progress history) |
| `/deload/status` | GET | UC-040 |
| `/deload/complete` | POST | UC-041 |
| `/deload/history` | GET | UC-042 |
| `/programs/start` | POST | UC-050 |
| `/programs/status` | GET | UC-051 |
| `/programs/complete-day` | POST | UC-052 |
| `/programs/phases` | GET | UC-054 |
| `/weekly-reviews/submit` | POST | UC-060 |
| `/weekly-reviews/history` | GET | UC-061 |
| `/weekly-reviews/latest` | GET | UC-062 |
| `/goals/options` | GET | UC-070 |
| `/goals/set` | POST | UC-071 |
| `/goals/user` | GET | UC-072 |
| `/goals/resources` | GET | UC-073 |
| `/goals/recommendations` | GET | UC-074 |
| `/groups/` | GET | UC-080 |
| `/groups/create` | POST | UC-081 |
| `/groups/join` | POST | UC-082 |
| `/challenges/` | GET | UC-090 |
| `/challenges/create` | POST | UC-091 |
| `/challenges/{id}/register` | POST | UC-092 |
| `/challenges/{id}/submit` | POST | UC-093 |
| `/challenges/{id}/leaderboard` | GET | UC-094 |
| `/challenges/{id}/submissions/{sid}` | PUT | UC-095 |
| `/challenges/{id}` | PUT | UC-096 |
| `/challenges/{id}` | DELETE | UC-097 |
| `/challenges/{id}/submissions` | GET | UC-098 |
| `/rewards/catalog` | GET | UC-100 |
| `/rewards/user` | GET | UC-101 |
| `/rewards/check-unlock` | POST | UC-102 |
| `/rewards/activate` | POST | UC-103 |
| `/chat/conversations` | GET | UC-110 |
| `/chat/conversations` | POST | UC-111, UC-115 |
| `/chat/conversations/{id}/messages` | POST | UC-112, UC-116 |
| `/chat/conversations/{id}/messages` | GET | UC-113, UC-116 |
| `/chat/search-users` | GET | UC-114 |
| `/productivity/water/log` | POST | UC-120 |
| `/productivity/water` | GET | UC-121 |
| `/productivity/water/goal` | PUT | UC-122 |
| `/productivity/planner` | POST | UC-123 |
| `/productivity/planner` | GET | UC-124 |
| `/productivity/planner/{id}` | PUT | UC-125 |
| `/productivity/planner/{id}` | DELETE | UC-126 |
| `/productivity/sr/cards` | POST | UC-127 |
| `/productivity/sr/cards/{id}/review` | POST | UC-128 |
| `/productivity/sr/review` | GET | UC-129 |
| `/productivity/brainstorm` | POST | UC-131 |
| `/productivity/brainstorm/{id}/ideas` | POST | UC-132 |

---

## Appendix B: MongoDB Collection Reference

| Collection | Primary Use Cases |
|------------|-------------------|
| `users` | UC-001, UC-002, UC-004, UC-005, UC-006 |
| `quiz_results` | UC-006 (anonymous sessions) |
| `userHabits` | UC-020, UC-021, UC-022, UC-023, UC-024 |
| `progress` | UC-022, UC-025 |
| `goals` | UC-071, UC-072 |
| `groups` | UC-080, UC-081, UC-082, UC-083 |
| `user_identity` | UC-010, UC-011, UC-012, UC-013 |
| `daily_protocols` | UC-030, UC-031, UC-032, UC-033, UC-034 |
| `deload_days` | UC-040, UC-041, UC-042, UC-043 |
| `user_programs` | UC-050, UC-051, UC-052, UC-053, UC-055 |
| `weekly_reviews` | UC-060, UC-061, UC-062 |
| `user_rewards` | UC-101, UC-102, UC-103 |
| `challenge_submissions` | UC-093, UC-094, UC-095, UC-098 |
| `messages` | UC-112, UC-113, UC-116 |
| `conversations` | UC-110, UC-111, UC-115, UC-116 |
| `water_logs` | UC-120, UC-121, UC-122 |
| `planner_tasks` | UC-123, UC-124, UC-125, UC-126 |
| `sr_cards` | UC-127, UC-128, UC-129, UC-130 |
| `brainstorm_sessions` | UC-131, UC-132 |

---

## Appendix C: Known Implementation Gaps

| Gap | Affected Use Cases | Detail |
|-----|--------------------|--------|
| Password update not hashed | UC-005 | `update_user_profile` stores `new_password` as plain text. Bcrypt is only applied on registration (UC-001) and the login migration path (UC-002). |
| JWT not revocable | UC-003 | Logout is stateless. Tokens remain valid until their 30-day expiry — no token blocklist exists. |
| Habits not user-scoped | UC-021 | `GET /habits/` returns all documents from `userHabits` without filtering by the requesting user's identity. |
| Group posts not exposed via API | UC-083 | The `group_post.py` domain model and `PostRepository` exist but no group post controller route is mounted in `create_app()`. |
| Challenge leaderboard streak always 0 | UC-094 | The `streak` field in leaderboard entries is hardcoded to 0 for all participants. |
| Reward check is caller-driven | UC-102 | The endpoint does not independently derive streak or review counts — the caller must supply accurate current metrics. |
| No role-based access control | UC-091–UC-098 | Admin-level operations (create/update/delete challenge, moderate submissions) are not protected by a role check. Any authenticated user can call them. |
| SM-2 card lookup uses linear scan | UC-128 | `review_sr_card` performs a linear scan over all user cards when looking up by ID, which is inefficient at scale. |
| No program abandonment endpoint | UC-050 | The error message for existing programs says "Complete or abandon it first," but no abandon/cancel endpoint is implemented. |

---

*End of document*
