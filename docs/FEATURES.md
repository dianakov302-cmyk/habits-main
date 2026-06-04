# Feature Specifications

## 1. Identity Progression System

Users evolve through six identity levels based on behavioral consistency.

### Levels

| Level | Score Range | Description |
|-------|-------------|-------------|
| Lost | 0–19 | Starting point, no consistent behavior |
| Explorer | 20–39 | Beginning to explore habits |
| Builder | 40–59 | Actively building routines |
| Disciplined | 60–74 | Consistent and structured |
| Focused | 75–89 | Deep work and clarity |
| Elite | 90–100 | Mastery level consistency |

### Score calculation

```
identity_score = (
    streak_component   * 0.30 +
    habit_completion   * 0.30 +
    protocol_points    * 0.20 +
    weekly_reviews     * 0.10 +
    program_progress   * 0.10
)
```

- `streak_component`: min(current_streak / 30, 1) * 100
- `habit_completion`: (completed_habits_last_7_days / total_habits / 7) * 100
- `protocol_points`: min(total_points_last_30_days / 60, 1) * 100
- `weekly_reviews`: min(reviews_last_30_days / 4, 1) * 100
- `program_progress`: (completed_program_days / 30) * 100 if active program

### UI display

> "You are 63% closer to becoming **Disciplined**."
> Current level: Builder → Next: Disciplined

---

## 2. Daily Protocol System

Every day is structured into three tiers.

### Tiers

| Tier | Points | Meaning |
|------|--------|---------|
| Minimum | 1 | Mandatory baseline task |
| Target | 2 | Standard productive day |
| Bonus | 3 | Extra challenge / above-and-beyond |

### Rules

- Each tier completed independently (minimum doesn't need target to be done first)
- Maximum 3 points per day (one of each tier, but only highest completed counts)
- Actually: points stack — completing all three = 1+2+3 = 6 pts (or just award the tier's value)
- **No punishment** for missing minimum — score stays at 0, no streak penalty logic
- Streaks only increment when **minimum** is marked complete
- Points are cumulative and feed into identity score

### Daily protocol creation

Created automatically when user first accesses the day, or manually via `POST /protocol/create`.
Tasks come from the user's active 30-day program phase, or from free-form creation.

---

## 3. Deload System

Burnout prevention built into the streak system.

### Trigger

After every 7-day streak (multiples of 7: day 7, 14, 21, …), the system:
1. Creates a recovery day entry
2. Prompts the user to choose ONE activity

### Recovery activities

| Activity | Code |
|----------|------|
| Meditation | `meditation` |
| Walk | `walk` |
| Bath / self-care | `bath` |
| Social time | `social_time` |
| Digital detox | `digital_detox` |

### Completion

- Completing the chosen activity: +1 point, streak preserved
- Skipping: 0 points, streak still preserved (deload days don't break streaks)

### Goal

Prevent the "all-or-nothing" collapse. Deload days are intentional recovery, not failure.

---

## 4. 30-Day Adaptive Program

A structured program with three phases that adapts to the user's goal and level.

### Phases

| Phase | Days | Focus | Intensity |
|-------|------|-------|-----------|
| START | 1–7 | Micro habits, low resistance | Easy |
| RHYTHM | 8–21 | Stable targets, weekly reviews | Medium |
| REINFORCEMENT | 22–30 | Harder tasks, deep work | Hard |

### Levels

- **Beginner**: 1 habit/day, short focus blocks (25 min), light tasks
- **Medium**: 2 habits/day, standard Pomodoro (50 min), moderate tasks
- **Advanced**: 3+ habits/day, deep work sessions (90 min), challenging tasks

### Program creation

User selects goal + level → program generated with day-by-day tasks per phase.
Each day maps to the active phase's task set for the chosen goal.

---

## 5. Goal-Based Personalized Plans

Ten goals with full resource packs.

### Goals

| Code | Title |
|------|-------|
| `focus_productivity` | Focus & Productivity |
| `build_discipline` | Build Discipline |
| `physical_health` | Physical Health |
| `mental_balance` | Mental Balance |
| `personal_growth` | Personal Growth |
| `social_motivation` | Social Motivation |
| `life_reset` | Life Reset |
| `studying` | Studying |
| `find_people` | Find Your People |
| `find_direction` | Find Identity / Direction |

### Resource pack per goal

Each goal includes:
- 3 recommended books (title + author + description)
- 5 recommended videos/resources (title + type + description)
- Habit recommendations by level (beginner/medium/advanced)
- Program phase tasks

---

## 6. Habit Recommendation Engine

Users don't create habits from scratch — the system suggests based on context.

### Recommendation factors

1. Selected goal code
2. Quiz/test result profile
3. User level (beginner/medium/advanced)
4. Motivation type (intrinsic/extrinsic/social/achievement)

### Example recommendations by goal

**Focus & Productivity**
- Pomodoro Technique (25/5 work-break cycles)
- Deep Work Sessions (90-min distraction-free blocks)
- Spaced Repetition (review material at increasing intervals)
- Morning Planning (15-min daily planning ritual)
- Digital Sunset (no screens 1hr before bed)

**Build Discipline**
- No Phone Morning (first 60 min phone-free)
- Structured Reading (30 min daily)
- Structured Work Sessions (time-blocked calendar)
- Cold Shower (morning cold exposure)
- Journaling (nightly reflection)

**Physical Health**
- Water Tracking (8 glasses/day)
- Sleep Schedule (fixed sleep/wake time)
- Workout Days (3–5x/week movement)
- Step Goal (8,000 steps daily)
- Screen Curfew (phones away 1hr before sleep)

**Mental Balance**
- Morning Meditation (10 min)
- Gratitude Journal (3 things daily)
- Breathing Exercises (box breathing)
- Nature Walk (15 min outside)
- Digital Detox Hour (1hr/day screen-free)

**Studying**
- Pomodoro Study Blocks
- Spaced Repetition Reviews
- Active Recall Practice
- Note Summarization
- Weekly Review Session

**Find Your People**
- Weekly Reach-Out (message one person/week)
- Community Check-In (group challenge participation)
- Social Commitment (plan one social event/week)
- Compliment Practice (one genuine compliment/day)

**Find Identity / Direction**
- Daily Journaling (stream-of-consciousness)
- Values Clarification (weekly exercise)
- Ikigai Reflection (monthly)
- New Experience (try one new thing/week)

---

## 7. Weekly Review System

Structured reflection every 7 days.

### Review prompts

1. What worked well this week?
2. What distracted or derailed you?
3. What will you change next week?

### Generated output

- Progress score (habit completion %, points earned)
- AI-style suggestions based on answers
- Motivational reflection paragraph
- Streak status

---

## 8. Reward & Customization System

Premium cosmetic progression. Nothing childish.

### Unlockables

| Trigger | Reward | Code |
|---------|--------|------|
| 7-day streak | Avatar frame (silver ring) | `avatar_frame_7` |
| 14-day streak | Profile theme (midnight) | `theme_midnight` |
| 30-day streak | Animated elite background | `bg_elite` |
| 60-day streak | Focus room customization | `focus_room` |
| Complete 30-day program | Program completion badge | `program_complete` |
| 5 weekly reviews | Reflection master frame | `frame_reflection` |

### Design principle

All rewards are cosmetic UI elements. No points counters, no XP bars, no confetti.
Everything feels like unlocking a new Notion theme — quiet, tasteful, earned.

---

## 9. Challenge System (Extended)

### Registration rules

- Weekly challenges: registration open until Sunday 23:59
- Challenge starts Monday 00:00
- Users joining after deadline see "next week's challenge"

### Submission flow

1. User completes daily task
2. Uploads proof (photo URL or text description)
3. Submission status: `pending` → `approved` / `rejected`
4. Admin moderates via dashboard endpoint

### Leaderboard metrics

1. **Consistency**: days completed / total days * 100
2. **Points**: total points earned
3. **Streak**: current consecutive days

### Admin capabilities

- Create challenge (title, description, tasks per day, dates)
- Edit challenge details
- Delete challenge
- Approve/reject submissions

---

## 10. Chat System

Telegram-inspired minimal design.

### Conversation types

- **Direct Messages**: 1:1 between users
- **Challenge Chats**: Group conversation per challenge (all participants)

### Features

- Search users by username/email
- Message users from challenge pages ("Message" button on leaderboard)
- Real-time feel (polling-based, not WebSocket for simplicity)
- Read receipts (array of emails who read)

---

## 11. Productivity Tools

### Water Tracker

- Log glasses of water (default unit: 250ml)
- Daily goal configurable (default: 8 glasses)
- Visual progress toward goal
- Date-based history

### Daily Planner

- Create tasks for a specific date
- Fields: title, description, priority (high/medium/low), time slot, completed
- Mark tasks complete
- No recurring tasks (handled by daily protocol instead)

### Spaced Repetition (SM-2 algorithm)

- Create flash cards (front/back) in decks
- Review cards → rate ease (1=again, 2=hard, 3=good, 4=easy)
- System calculates next review date using SM-2
- "Due today" queue shown on dashboard

### Brainstorm

- Create named sessions/boards
- Add ideas freely (timestamped)
- Tag sessions
- No structure imposed — pure capture tool

---

## 12. Books & Resources

### Focus & Productivity
**Books:**
- *Deep Work* — Cal Newport
- *Atomic Habits* — James Clear
- *The One Thing* — Gary Keller

**Videos/Resources:**
- "The Power of Deep Work" lecture
- "Building Atomic Habits" summary
- Pomodoro technique walkthrough
- Time-blocking masterclass
- Focus music / lo-fi playlists

### Build Discipline / Self-Discipline
**Books:**
- *Can't Hurt Me* — David Goggins
- *Discipline Equals Freedom* — Jocko Willink
- *Atomic Habits* — James Clear

### Studying
**Books:**
- *Make It Stick* — Brown, Roediger, McDaniel
- *Ultralearning* — Scott Young
- *A Mind for Numbers* — Barbara Oakley

### Find Your People
**Books:**
- *How to Win Friends and Influence People* — Dale Carnegie
- *Attached* — Amir Levine
- *The Courage to Be Disliked* — Kishimi & Koga

### Find Identity / Direction
**Books:**
- *Man's Search for Meaning* — Viktor Frankl
- *The Mountain Is You* — Brianna Wiest
- *Ikigai* — Héctor García

### Physical Health
**Books:**
- *Why We Sleep* — Matthew Walker
- *Outlive* — Peter Attia
- *The Blue Zones* — Dan Buettner

### Mental Balance
**Books:**
- *The Power of Now* — Eckhart Tolle
- *Wherever You Go, There You Are* — Jon Kabat-Zinn
- *Lost Connections* — Johann Hari

### Personal Growth
**Books:**
- *Mindset* — Carol Dweck
- *The War of Art* — Steven Pressfield
- *Man's Search for Meaning* — Viktor Frankl

### Social Motivation
**Books:**
- *Give and Take* — Adam Grant
- *The Art of Belonging* — Hugh Mackay
- *Tribe* — Sebastian Junger

### Life Reset
**Books:**
- *The Mountain Is You* — Brianna Wiest
- *Tiny Habits* — B.J. Fogg
- *The Obstacle Is the Way* — Ryan Holiday
