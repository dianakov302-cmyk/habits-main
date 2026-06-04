"""
Seed script - populates the local MongoDB with demo data so the dashboard
has something to show on first run.

Usage:
    python seed.py               # insert demo data (skips if already exists)
    python seed.py --reset       # drop all app collections first, then seed

What it creates:
  - 1 demo user        (email: demo@anaida.space  password: demo1234)
  - identity profile   (Builder level, score 42)
  - today's daily protocol (3 tasks, all pending)
  - an active 30-day program (Focus goal, day 3)
  - a completed weekly review
  - water log for today (3 glasses)
  - 3 planner tasks for today
  - 2 spaced-repetition cards (both due today)
  - 1 brainstorm session with 2 ideas
  - 1 reward unlocked
  - 1 DM conversation with 2 messages
"""

import os
import sys
from datetime import date, datetime, timezone
from pathlib import Path

from pymongo import MongoClient

# Load .env manually so the script works when invoked directly (outside the
# app server) without needing python-dotenv installed as a hard dependency.
_env_file = Path(__file__).resolve().parent / ".env"
if _env_file.exists():
    with _env_file.open() as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _key, _, _val = _line.partition("=")
                os.environ.setdefault(_key.strip(), _val.strip())

# Config — falls back to localhost if MONGODB_URI is not set in .env
MONGO_URI     = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/")
DB_NAME       = os.environ.get("MONGODB_DB_NAME", "habitplatform")
DEMO_EMAIL    = "demo@anaida.space"
DEMO_PASSWORD = "demo1234"
TODAY         = date.today().isoformat()
NOW           = datetime.now(timezone.utc).isoformat()
RESET         = "--reset" in sys.argv

# Connect
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
try:
    client.admin.command("ping")
    print("Connected to MongoDB")
except Exception as e:
    print(f"Cannot reach MongoDB: {e}")
    sys.exit(1)

db = client[DB_NAME]

COLLECTIONS = [
    "users", "quiz_results", "userHabits", "progress", "goals", "groups",
    "posts", "punch_cards", "user_identity", "daily_protocols", "deload_days",
    "user_programs", "weekly_reviews", "user_rewards", "challenge_submissions",
    "messages", "conversations", "water_logs", "planner_tasks", "sr_cards",
    "brainstorm_sessions",
]

if RESET:
    for col in COLLECTIONS:
        db[col].drop()
    print("All collections dropped (reset mode)")


def exists(collection, query):
    return db[collection].find_one(query) is not None


# 1. User
if not exists("users", {"email": DEMO_EMAIL}):
    db["users"].insert_one({
        "email":      DEMO_EMAIL,
        "password":   DEMO_PASSWORD,
        "name":       "Demo User",
        "created_at": NOW,
        "goal":       "focus_productivity",
        "quiz_done":  True,
    })
    print("  [OK] Demo user created")
else:
    print("  [--] Demo user already exists")

# 2. Identity profile
if not exists("user_identity", {"email": DEMO_EMAIL}):
    db["user_identity"].insert_one({
        "email":            DEMO_EMAIL,
        "level":            "Builder",
        "score":            42,
        "message":          "You're building real momentum.",
        "next_level":       "Disciplined",
        "current_streak":   3,
        "today_points":     0,
        "habit_completion": 0.6,
        "updated_at":       NOW,
    })
    print("  [OK] Identity profile created")
else:
    print("  [--] Identity profile already exists")

# 3. Daily protocol
if not exists("daily_protocols", {"email": DEMO_EMAIL, "date": TODAY}):
    db["daily_protocols"].insert_one({
        "email":         DEMO_EMAIL,
        "date":          TODAY,
        "minimum_task":  {"title": "Meditate 5 minutes", "completed": False},
        "target_task":   {"title": "Complete one Pomodoro session", "completed": False},
        "bonus_task":    {"title": "Cold shower after workout", "completed": False},
        "points_earned": 0,
        "streak_counts": False,
        "created_at":    NOW,
    })
    print("  [OK] Today's protocol created")
else:
    print("  [--] Today's protocol already exists")

# 4. 30-day program
if not exists("user_programs", {"email": DEMO_EMAIL, "status": "active"}):
    db["user_programs"].insert_one({
        "email":         DEMO_EMAIL,
        "status":        "active",
        "goal_code":     "focus_productivity",
        "level":         "beginner",
        "current_day":   3,
        "current_phase": "START",
        "start_date":    TODAY,
        "created_at":    NOW,
        "updated_at":    NOW,
    })
    print("  [OK] Active 30-day program created")
else:
    print("  [--] Active program already exists")

# 5. Weekly review
if not exists("weekly_reviews", {"email": DEMO_EMAIL}):
    db["weekly_reviews"].insert_one({
        "email":           DEMO_EMAIL,
        "date":            TODAY,
        "what_worked":     "Morning meditation kept me grounded this week.",
        "what_distracted": "Social media in the evenings derailed my reading habit.",
        "what_to_change":  "Put the phone in another room after 9pm.",
        "reflection":      "You showed up consistently on 5 of 7 days - that's real progress.",
        "suggestions": [
            "Try a phone-free hour before bed",
            "Stack reading with an existing habit",
            "Track distraction triggers in your journal",
        ],
        "created_at": NOW,
    })
    print("  [OK] Weekly review created")
else:
    print("  [--] Weekly review already exists")

# 6. Water log
if not exists("water_logs", {"email": DEMO_EMAIL, "date": TODAY}):
    db["water_logs"].insert_one({
        "email":   DEMO_EMAIL,
        "date":    TODAY,
        "glasses": 3,
        "goal":    8,
        "logs": [
            {"time": "08:00", "amount_ml": 250},
            {"time": "10:00", "amount_ml": 250},
            {"time": "12:00", "amount_ml": 250},
        ],
    })
    print("  [OK] Water log created (3 glasses)")
else:
    print("  [--] Water log already exists")

# 7. Planner tasks
if not exists("planner_tasks", {"email": DEMO_EMAIL, "date": TODAY}):
    db["planner_tasks"].insert_many([
        {
            "email": DEMO_EMAIL, "date": TODAY,
            "title": "Review project goals", "priority": "high",
            "time_slot": "09:00-09:30", "completed": False,
            "description": "", "created_at": NOW,
        },
        {
            "email": DEMO_EMAIL, "date": TODAY,
            "title": "Deep work block", "priority": "high",
            "time_slot": "10:00-12:00", "completed": False,
            "description": "", "created_at": NOW,
        },
        {
            "email": DEMO_EMAIL, "date": TODAY,
            "title": "Read 20 pages", "priority": "low",
            "time_slot": "20:00-20:30", "completed": False,
            "description": "", "created_at": NOW,
        },
    ])
    print("  [OK] Planner tasks created")
else:
    print("  [--] Planner tasks already exist")

# 8. Spaced repetition cards
if not exists("sr_cards", {"email": DEMO_EMAIL}):
    db["sr_cards"].insert_many([
        {
            "email": DEMO_EMAIL, "deck": "Habits",
            "front": "What is the Two-Minute Rule?",
            "back":  "If a task takes less than 2 minutes, do it immediately.",
            "ease_factor": 2.5, "interval_days": 1, "repetitions": 0,
            "next_review_date": TODAY, "created_at": NOW,
        },
        {
            "email": DEMO_EMAIL, "deck": "Habits",
            "front": "What is habit stacking?",
            "back":  "Linking a new habit to an existing one: After I [CURRENT], I will [NEW].",
            "ease_factor": 2.5, "interval_days": 1, "repetitions": 0,
            "next_review_date": TODAY, "created_at": NOW,
        },
    ])
    print("  [OK] SR cards created (2 due today)")
else:
    print("  [--] SR cards already exist")

# 9. Brainstorm session
if not exists("brainstorm_sessions", {"email": DEMO_EMAIL}):
    db["brainstorm_sessions"].insert_one({
        "email": DEMO_EMAIL,
        "title": "Morning routine ideas",
        "tags":  ["habits", "morning"],
        "ideas": [
            {"content": "Start with 2 minutes of stretching before checking phone",
             "added_at": NOW},
            {"content": "Prepare gym bag the night before to remove friction",
             "added_at": NOW},
        ],
        "created_at": NOW,
        "updated_at": NOW,
    })
    print("  [OK] Brainstorm session created")
else:
    print("  [--] Brainstorm session already exists")

# 10. Rewards
if not exists("user_rewards", {"email": DEMO_EMAIL}):
    db["user_rewards"].insert_one({
        "email":             DEMO_EMAIL,
        "unlocked_rewards":  ["first_week_frame"],
        "active_theme":      None,
        "active_frame":      "first_week_frame",
        "active_background": None,
        "updated_at":        NOW,
    })
    print("  [OK] User rewards created")
else:
    print("  [--] User rewards already exist")

# 11. Demo conversation + messages
if not exists("conversations", {"participants": DEMO_EMAIL}):
    from bson import ObjectId
    conv_id = ObjectId()
    db["conversations"].insert_one({
        "_id":          conv_id,
        "type":         "dm",
        "participants": [DEMO_EMAIL, "alex@anaida.space"],
        "last_message": "Hey, how's the program going?",
        "created_at":   NOW,
        "updated_at":   NOW,
    })
    db["messages"].insert_many([
        {
            "conversation_id": str(conv_id),
            "sender_email":    "alex@anaida.space",
            "content":         "Hey, how's the program going?",
            "created_at":      NOW,
        },
        {
            "conversation_id": str(conv_id),
            "sender_email":    DEMO_EMAIL,
            "content":         "Day 3 - feeling good! The morning protocol really helps.",
            "created_at":      NOW,
        },
    ])
    print("  [OK] Demo conversation + messages created")
else:
    print("  [--] Conversation already exists")

# Done
print()
print("=" * 48)
print("  Seed complete!")
print(f"  Login:    {DEMO_EMAIL}")
print(f"  Password: {DEMO_PASSWORD}")
print("  URL:      http://127.0.0.1:3000/dashboard.html")
print("=" * 48)
