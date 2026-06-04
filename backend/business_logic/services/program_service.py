from datetime import datetime, timezone
from typing import Any

from backend.repositories.program_repository import ProgramRepository
from backend.business_logic.services.interfaces import IProgramService

PHASES = [
    {
        "name": "START",
        "days": "1–7",
        "focus": "Micro habits and low-resistance routines",
        "intensity": "Easy",
        "description": (
            "Establish the foundation. Small wins build momentum. "
            "Keep friction as low as possible — the goal is to show up, not to excel."
        ),
    },
    {
        "name": "RHYTHM",
        "days": "8–21",
        "focus": "Stable targets, weekly review, consistency tracking",
        "intensity": "Medium",
        "description": (
            "Your baseline is set. Now build a rhythm. "
            "Weekly reviews begin here. Consistency becomes the metric."
        ),
    },
    {
        "name": "REINFORCEMENT",
        "days": "22–30",
        "focus": "Deeper work sessions, focus protection, final reflection",
        "intensity": "Hard",
        "description": (
            "Raise the bar. The habits are familiar — now go deeper. "
            "Protect your focus, do harder work, reflect on your transformation."
        ),
    },
]

PHASE_DAY_MAP = {"START": range(1, 8), "RHYTHM": range(8, 22), "REINFORCEMENT": range(22, 31)}

LEVEL_MULTIPLIERS = {"beginner": 1, "medium": 2, "advanced": 3}

GOAL_PHASE_TASKS: dict[str, dict[str, dict[str, list[str]]]] = {
    "focus_productivity": {
        "START": {
            "beginner": ["25-min Pomodoro session", "Phone-free morning (15 min)", "Write 3 daily priorities"],
            "medium": ["2× Pomodoro blocks", "Phone-free morning (30 min)", "Time-block calendar"],
            "advanced": ["90-min deep work session", "Phone-free morning (60 min)", "Full daily time-block"],
        },
        "RHYTHM": {
            "beginner": ["Daily Pomodoro + review", "No-distraction work hour", "Weekly focus reflection"],
            "medium": ["3× Pomodoro + weekly review", "2-hr distraction-free block", "Weekly focus reflection"],
            "advanced": ["2× 90-min deep work", "Full digital minimalism day", "Weekly focus reflection"],
        },
        "REINFORCEMENT": {
            "beginner": ["3-hr focused work day", "Distraction audit", "Final reflection journal"],
            "medium": ["4-hr deep work day", "Digital detox evening", "Final reflection journal"],
            "advanced": ["6-hr peak focus day", "Full digital detox day", "Final reflection journal"],
        },
    },
    "build_discipline": {
        "START": {
            "beginner": ["No phone for first 30 min", "Read 10 pages", "Make your bed"],
            "medium": ["No phone for first 60 min", "Read 20 pages", "Cold shower"],
            "advanced": ["No phone until noon", "Read 30 pages", "Cold shower + workout"],
        },
        "RHYTHM": {
            "beginner": ["Daily discipline habit stack", "Weekly commitment review", "Evening routine"],
            "medium": ["2 discipline habits daily", "Weekly commitment review", "Structured evening routine"],
            "advanced": ["3 discipline habits daily", "Weekly commitment review", "Full morning + evening routine"],
        },
        "REINFORCEMENT": {
            "beginner": ["Hard mode day (no comfort crutches)", "Discipline reflection", "30-day review"],
            "medium": ["2-day discipline challenge", "Discipline reflection", "30-day review"],
            "advanced": ["72-hr extreme discipline sprint", "Discipline reflection", "30-day review"],
        },
    },
    "physical_health": {
        "START": {
            "beginner": ["8 glasses of water", "10-min walk", "Sleep by midnight"],
            "medium": ["8 glasses + 20-min workout", "7,000 steps", "Sleep by 11pm"],
            "advanced": ["8 glasses + 45-min workout", "10,000 steps", "Sleep by 10:30pm"],
        },
        "RHYTHM": {
            "beginner": ["Daily water + movement", "Weekly workout plan", "Sleep schedule check"],
            "medium": ["3× workout/week", "Weekly workout plan", "Sleep tracking"],
            "advanced": ["5× workout/week", "Weekly workout plan", "Sleep + recovery tracking"],
        },
        "REINFORCEMENT": {
            "beginner": ["Active every day this week", "Body scan reflection", "Final health review"],
            "medium": ["5-day fitness streak", "Body scan reflection", "Final health review"],
            "advanced": ["7-day fitness streak", "Body scan reflection", "Final health review"],
        },
    },
    "studying": {
        "START": {
            "beginner": ["1 Pomodoro study block", "Review yesterday's notes", "Write 1 flashcard"],
            "medium": ["2 Pomodoro study blocks", "Active recall session", "5 flashcards"],
            "advanced": ["3 Pomodoro study blocks", "Full active recall", "10 flashcards"],
        },
        "RHYTHM": {
            "beginner": ["Daily study + flashcard review", "Weekly learning reflection", "Summarize key concepts"],
            "medium": ["2-hr study + spaced repetition", "Weekly learning reflection", "Teach back 1 concept"],
            "advanced": ["3-hr deep study + SR review", "Weekly learning reflection", "Full concept map"],
        },
        "REINFORCEMENT": {
            "beginner": ["Mock test / recall session", "Learning style reflection", "30-day study review"],
            "medium": ["2-hr exam simulation", "Learning style reflection", "30-day study review"],
            "advanced": ["Full exam simulation day", "Learning style reflection", "30-day study review"],
        },
    },
    "mental_balance": {
        "START": {
            "beginner": ["5-min morning meditation", "3 gratitude notes", "1 screen-free hour"],
            "medium": ["10-min meditation", "Gratitude journal", "Digital detox evening"],
            "advanced": ["20-min meditation", "Morning + evening gratitude", "Half-day screen-free"],
        },
        "RHYTHM": {
            "beginner": ["Daily meditation + gratitude", "Weekly mood check", "Nature walk"],
            "medium": ["Daily meditation + journaling", "Weekly mood check", "1-hr nature immersion"],
            "advanced": ["Daily sit + journaling + walk", "Weekly mood + energy check", "Full rest day design"],
        },
        "REINFORCEMENT": {
            "beginner": ["Mindfulness deep dive day", "Balance reflection", "30-day mental review"],
            "medium": ["Intentional rest day", "Balance reflection", "30-day mental review"],
            "advanced": ["Full digital detox day", "Balance reflection", "30-day mental review"],
        },
    },
}

# Fallback tasks for goals not listed above
DEFAULT_TASKS: dict[str, dict[str, list[str]]] = {
    "START": {
        "beginner": ["Complete your minimum habit today", "Reflect for 5 minutes"],
        "medium": ["Complete 2 habits today", "10-min reflection"],
        "advanced": ["Complete all habits today", "Full reflection journal"],
    },
    "RHYTHM": {
        "beginner": ["Maintain daily habit", "Weekly review"],
        "medium": ["2 habits + weekly review", "Weekly review"],
        "advanced": ["All habits + deep review", "Weekly review"],
    },
    "REINFORCEMENT": {
        "beginner": ["Push one level beyond minimum", "Final reflection"],
        "medium": ["Exceed your target", "Final reflection"],
        "advanced": ["Peak performance day", "Final reflection"],
    },
}


def _get_phase_for_day(day: int) -> str:
    if day <= 7:
        return "START"
    if day <= 21:
        return "RHYTHM"
    return "REINFORCEMENT"


def _get_tasks_for_day(goal_code: str, phase: str, level: str) -> list[str]:
    goal_map = GOAL_PHASE_TASKS.get(goal_code, {})
    phase_map = goal_map.get(phase, DEFAULT_TASKS.get(phase, {}))
    return phase_map.get(level, phase_map.get("beginner", ["Complete your habit today"]))


class ProgramService(IProgramService):
    def __init__(self, program_repository: ProgramRepository):
        self.program_repository = program_repository

    def start_program(self, email: str, goal_code: str, level: str) -> dict[str, Any]:
        try:
            if level not in LEVEL_MULTIPLIERS:
                return {
                    "status": "error",
                    "message": "level must be: beginner, medium, or advanced",
                }
            active = self.program_repository.find_active(email)
            if active:
                return {
                    "status": "error",
                    "message": "You already have an active program. Complete or abandon it first.",
                }
            now = datetime.now(timezone.utc).isoformat()
            today = now[:10]
            data = {
                "email": email,
                "goal_code": goal_code,
                "level": level,
                "start_date": today,
                "current_day": 1,
                "current_phase": "START",
                "status": "active",
                "completed_days": [],
                "total_days": 30,
                "created_at": now,
            }
            self.program_repository.insert(data)
            data.pop("_id", None)
            today_tasks = _get_tasks_for_day(goal_code, "START", level)
            return {
                "status": "success",
                "message": "30-day program started. Day 1 begins now.",
                "data": {**data, "today_tasks": today_tasks},
            }
        except Exception as e:
            return {"status": "error", "message": f"Failed to start program: {str(e)}"}

    def get_status(self, email: str) -> dict[str, Any]:
        try:
            program = self.program_repository.find_active(email)
            if program is None:
                return {"status": "success", "data": None, "message": "No active program."}
            today_tasks = _get_tasks_for_day(
                program["goal_code"], program["current_phase"], program["level"]
            )
            return {
                "status": "success",
                "data": {**program, "today_tasks": today_tasks},
            }
        except Exception as e:
            return {"status": "error", "message": f"Failed to get program status: {str(e)}"}

    def complete_day(self, email: str) -> dict[str, Any]:
        try:
            program = self.program_repository.find_active(email)
            if program is None:
                return {"status": "error", "message": "No active program."}

            current_day = program["current_day"]
            completed_days = program.get("completed_days", [])

            if current_day in completed_days:
                return {"status": "success", "message": "Day already completed.", "data": program}

            completed_days.append(current_day)
            next_day = current_day + 1

            if next_day > 30:
                self.program_repository.upsert_active(
                    email,
                    {
                        "status": "completed",
                        "completed_days": completed_days,
                        "current_day": 30,
                        "completed_at": datetime.now(timezone.utc).isoformat(),
                    },
                )
                return {
                    "status": "success",
                    "message": "Program complete! 30-day journey finished.",
                    "data": {"completed": True, "total_days_done": 30},
                }

            next_phase = _get_phase_for_day(next_day)
            self.program_repository.upsert_active(
                email,
                {
                    "current_day": next_day,
                    "current_phase": next_phase,
                    "completed_days": completed_days,
                },
            )
            next_tasks = _get_tasks_for_day(program["goal_code"], next_phase, program["level"])
            return {
                "status": "success",
                "message": f"Day {current_day} complete. Day {next_day} unlocked.",
                "data": {
                    "current_day": next_day,
                    "current_phase": next_phase,
                    "tomorrow_tasks": next_tasks,
                    "days_remaining": 30 - next_day + 1,
                },
            }
        except Exception as e:
            return {"status": "error", "message": f"Failed to complete day: {str(e)}"}

    def get_phases(self) -> dict[str, Any]:
        return {"status": "success", "data": PHASES}
