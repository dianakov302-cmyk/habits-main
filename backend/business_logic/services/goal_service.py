from datetime import UTC, datetime
from typing import Any

from backend.repositories.goal_repository import GoalRepository
from backend.business_logic.services.interfaces import IGoalService

GOAL_RESOURCES: dict[str, dict] = {
    "focus_productivity": {
        "books": [
            {"title": "Deep Work", "author": "Cal Newport", "description": "Rules for focused success in a distracted world."},
            {"title": "Atomic Habits", "author": "James Clear", "description": "Tiny changes, remarkable results."},
            {"title": "The One Thing", "author": "Gary Keller", "description": "Extraordinary results through focus on the one thing that matters."},
        ],
        "videos": [
            {"title": "The Power of Deep Work", "type": "lecture", "description": "Cal Newport on eliminating distraction."},
            {"title": "Building Atomic Habits", "type": "summary", "description": "James Clear's habit loop explained."},
            {"title": "Pomodoro Technique Walkthrough", "type": "tutorial", "description": "How to implement 25/5 work-break cycles."},
            {"title": "Time-Blocking Masterclass", "type": "workshop", "description": "Full calendar control with time-blocking."},
            {"title": "Focus Music - Lo-Fi Study", "type": "playlist", "description": "Ambient music for sustained focus sessions."},
        ],
    },
    "build_discipline": {
        "books": [
            {"title": "Can't Hurt Me", "author": "David Goggins", "description": "Master your mind and defy the odds."},
            {"title": "Discipline Equals Freedom", "author": "Jocko Willink", "description": "Field manual for self-discipline."},
            {"title": "Atomic Habits", "author": "James Clear", "description": "Build systems that make discipline automatic."},
        ],
        "videos": [
            {"title": "Jocko Willink on Discipline", "type": "talk", "description": "The mindset of extreme ownership."},
            {"title": "David Goggins — Suffering is the Path", "type": "interview", "description": "Mental toughness through adversity."},
            {"title": "Morning Routine for Discipline", "type": "tutorial", "description": "How to build an unbreakable morning."},
            {"title": "Breaking Bad Habits Cold Turkey", "type": "lecture", "description": "Science of habit replacement."},
            {"title": "The 5 AM Club", "type": "summary", "description": "Robin Sharma's morning ritual framework."},
        ],
    },
    "physical_health": {
        "books": [
            {"title": "Why We Sleep", "author": "Matthew Walker", "description": "The science of sleep and its power over your life."},
            {"title": "Outlive", "author": "Peter Attia", "description": "The science and art of longevity."},
            {"title": "The Blue Zones", "author": "Dan Buettner", "description": "Lessons from the world's longest-lived people."},
        ],
        "videos": [
            {"title": "Andrew Huberman — Sleep Toolkit", "type": "podcast", "description": "Science-backed sleep optimization."},
            {"title": "Peter Attia on Zone 2 Training", "type": "interview", "description": "Longevity exercise protocol."},
            {"title": "How to Build a Workout Habit", "type": "tutorial", "description": "Behavioral design for consistent fitness."},
            {"title": "The Blue Zones — Lessons from Centenarians", "type": "documentary", "description": "What the world's healthiest people do."},
            {"title": "Nutrition Science Basics", "type": "lecture", "description": "Evidence-based nutrition fundamentals."},
        ],
    },
    "mental_balance": {
        "books": [
            {"title": "The Power of Now", "author": "Eckhart Tolle", "description": "A guide to spiritual enlightenment and present-moment awareness."},
            {"title": "Wherever You Go, There You Are", "author": "Jon Kabat-Zinn", "description": "Mindfulness meditation in everyday life."},
            {"title": "Lost Connections", "author": "Johann Hari", "description": "Uncovering the real causes of depression."},
        ],
        "videos": [
            {"title": "Jon Kabat-Zinn — Mindfulness for Beginners", "type": "lecture", "description": "Introduction to mindfulness practice."},
            {"title": "Sam Harris — Waking Up Meditation", "type": "app", "description": "Secular meditation and mindfulness."},
            {"title": "The Science of Stress", "type": "documentary", "description": "How stress affects the body and brain."},
            {"title": "Box Breathing Tutorial", "type": "tutorial", "description": "4-4-4-4 breathing for instant calm."},
            {"title": "Digital Minimalism", "type": "talk", "description": "Cal Newport on reclaiming attention."},
        ],
    },
    "personal_growth": {
        "books": [
            {"title": "Mindset", "author": "Carol Dweck", "description": "The new psychology of success through growth mindset."},
            {"title": "The War of Art", "author": "Steven Pressfield", "description": "Break through the blocks and win your inner creative battles."},
            {"title": "Man's Search for Meaning", "author": "Viktor Frankl", "description": "Finding purpose through suffering."},
        ],
        "videos": [
            {"title": "Carol Dweck — Growth Mindset", "type": "ted_talk", "description": "The power of believing you can improve."},
            {"title": "Steven Pressfield on Resistance", "type": "interview", "description": "The creative battle everyone faces."},
            {"title": "Ikigai — Finding Your Purpose", "type": "lecture", "description": "The Japanese concept of reason for being."},
            {"title": "Personal Values Clarification", "type": "workshop", "description": "Identify what matters most to you."},
            {"title": "The Hero's Journey Applied", "type": "lecture", "description": "Mythological structure of personal transformation."},
        ],
    },
    "social_motivation": {
        "books": [
            {"title": "Give and Take", "author": "Adam Grant", "description": "Why helping others drives our success."},
            {"title": "The Art of Belonging", "author": "Hugh Mackay", "description": "Why human connection is our deepest need."},
            {"title": "Tribe", "author": "Sebastian Junger", "description": "On homecoming and belonging."},
        ],
        "videos": [
            {"title": "Adam Grant — The Surprising Habits of Givers", "type": "ted_talk", "description": "How generosity creates success."},
            {"title": "Brené Brown — The Power of Vulnerability", "type": "ted_talk", "description": "Connection through authentic vulnerability."},
            {"title": "How to Make Real Friends", "type": "tutorial", "description": "Science of adult friendships."},
            {"title": "Community Building Masterclass", "type": "workshop", "description": "Creating genuine belonging."},
            {"title": "The Loneliness Epidemic", "type": "documentary", "description": "Understanding and solving modern isolation."},
        ],
    },
    "life_reset": {
        "books": [
            {"title": "The Mountain Is You", "author": "Brianna Wiest", "description": "Transforming self-sabotage into self-mastery."},
            {"title": "Tiny Habits", "author": "B.J. Fogg", "description": "The small changes that change everything."},
            {"title": "The Obstacle Is the Way", "author": "Ryan Holiday", "description": "The timeless art of turning trials into triumph."},
        ],
        "videos": [
            {"title": "Brianna Wiest — The Mountain Is You", "type": "talk", "description": "Self-sabotage and how to overcome it."},
            {"title": "Ryan Holiday — Stoicism Explained", "type": "lecture", "description": "Ancient philosophy for modern challenges."},
            {"title": "How to Start Over", "type": "tutorial", "description": "Practical steps for a life reset."},
            {"title": "The Science of Motivation", "type": "lecture", "description": "What actually drives sustained change."},
            {"title": "Identity-Based Change", "type": "talk", "description": "James Clear on becoming vs. achieving."},
        ],
    },
    "studying": {
        "books": [
            {"title": "Make It Stick", "author": "Brown, Roediger, McDaniel", "description": "The science of successful learning."},
            {"title": "Ultralearning", "author": "Scott Young", "description": "Master hard skills, outsmart the competition."},
            {"title": "A Mind for Numbers", "author": "Barbara Oakley", "description": "How to excel at math and science."},
        ],
        "videos": [
            {"title": "Active Recall vs. Passive Review", "type": "tutorial", "description": "The most effective study technique."},
            {"title": "Spaced Repetition Explained", "type": "lecture", "description": "How to remember almost anything forever."},
            {"title": "The Feynman Technique", "type": "tutorial", "description": "Learn anything by teaching it simply."},
            {"title": "Ultralearning Projects", "type": "case_study", "description": "Scott Young's rapid skill-acquisition examples."},
            {"title": "How to Study Effectively", "type": "workshop", "description": "Cognitive science applied to student learning."},
        ],
    },
    "find_people": {
        "books": [
            {"title": "How to Win Friends and Influence People", "author": "Dale Carnegie", "description": "The classic guide to human relationships."},
            {"title": "Attached", "author": "Amir Levine & Rachel Heller", "description": "Attachment theory applied to adult relationships."},
            {"title": "The Courage to Be Disliked", "author": "Kishimi & Koga", "description": "Adlerian psychology and freedom from others' opinions."},
        ],
        "videos": [
            {"title": "Attachment Styles Explained", "type": "lecture", "description": "Secure, anxious, avoidant — which are you?"},
            {"title": "How to Be a Better Listener", "type": "tutorial", "description": "The skill at the core of every relationship."},
            {"title": "Building Real Connections", "type": "workshop", "description": "Moving from small talk to meaningful conversation."},
            {"title": "Brené Brown — Belonging vs. Fitting In", "type": "talk", "description": "The difference between true belonging and performance."},
            {"title": "Social Anxiety Toolkit", "type": "tutorial", "description": "Evidence-based strategies for social confidence."},
        ],
    },
    "find_direction": {
        "books": [
            {"title": "Man's Search for Meaning", "author": "Viktor Frankl", "description": "Finding purpose through suffering and meaning-making."},
            {"title": "The Mountain Is You", "author": "Brianna Wiest", "description": "Finding your direction through self-mastery."},
            {"title": "Ikigai", "author": "Héctor García & Francesc Miralles", "description": "The Japanese secret to a long and happy life."},
        ],
        "videos": [
            {"title": "Viktor Frankl — Logotherapy Explained", "type": "lecture", "description": "The search for meaning as a human drive."},
            {"title": "Ikigai — Your Reason for Being", "type": "animation", "description": "Visual guide to finding your purpose."},
            {"title": "Simon Sinek — Find Your Why", "type": "ted_talk", "description": "How to discover your personal why."},
            {"title": "Identity and Direction Workshop", "type": "workshop", "description": "Exercises for clarifying who you are becoming."},
            {"title": "The North Star Exercise", "type": "tutorial", "description": "Define your guiding values and vision."},
        ],
    },
}

HABIT_RECOMMENDATIONS: dict[str, dict[str, list[dict]]] = {
    "focus_productivity": {
        "beginner": [
            {"name": "Pomodoro Session", "description": "25-minute focused work block with 5-min break."},
            {"name": "Phone-Free Morning", "description": "Keep phone away for the first 30 minutes after waking."},
            {"name": "Top 3 Daily Priorities", "description": "Write your 3 most important tasks before starting work."},
        ],
        "medium": [
            {"name": "Deep Work Block", "description": "90-minute distraction-free work session."},
            {"name": "Daily Time-Blocking", "description": "Schedule every hour of your workday on a calendar."},
            {"name": "Digital Sunset", "description": "No screens 1 hour before bed."},
            {"name": "Single-Tab Browser Rule", "description": "Only one browser tab open during work sessions."},
        ],
        "advanced": [
            {"name": "Morning Deep Work", "description": "90-min deep work session before checking any messages."},
            {"name": "Full Digital Minimalism", "description": "Phone on airplane mode until noon."},
            {"name": "Weekly Focus Review", "description": "Sunday planning session for the entire week ahead."},
            {"name": "Spaced Repetition Practice", "description": "Daily review of key concepts using flashcards."},
        ],
    },
    "build_discipline": {
        "beginner": [
            {"name": "Make Your Bed", "description": "First small win of the day — sets the tone for everything."},
            {"name": "No Phone Morning", "description": "Phone-free for the first 60 minutes after waking."},
            {"name": "Daily Reading", "description": "10 pages of a book every day, no exceptions."},
        ],
        "medium": [
            {"name": "Cold Shower", "description": "End every shower with 30-60 seconds of cold water."},
            {"name": "Structured Work Sessions", "description": "Time-blocked calendar with no unplanned breaks."},
            {"name": "No Snooze Rule", "description": "First alarm is final. Get up immediately."},
            {"name": "Daily Journaling", "description": "5-min evening reflection on what you did and learned."},
        ],
        "advanced": [
            {"name": "5am Wake-Up", "description": "Fixed 5am wake time regardless of sleep time."},
            {"name": "Workout Before Anything", "description": "Movement before any screen time or meals."},
            {"name": "Weekly Discipline Audit", "description": "Review every commitment and whether you kept it."},
            {"name": "Monthly Challenge", "description": "One hard challenge per month to expand your comfort zone."},
        ],
    },
    "physical_health": {
        "beginner": [
            {"name": "Water Tracking", "description": "Track 8 glasses of water per day."},
            {"name": "Daily Walk", "description": "15-minute walk after lunch, every day."},
            {"name": "Sleep Schedule", "description": "Same bedtime and wake time every day, including weekends."},
        ],
        "medium": [
            {"name": "Workout Days", "description": "3 structured workouts per week — non-negotiable."},
            {"name": "Step Goal", "description": "8,000 steps per day tracked consistently."},
            {"name": "Meal Timing", "description": "No eating within 2 hours of bedtime."},
            {"name": "Screen Curfew", "description": "Phone away 1 hour before sleep for better sleep quality."},
        ],
        "advanced": [
            {"name": "Zone 2 Cardio", "description": "3× 45-min low-intensity cardio sessions per week."},
            {"name": "Strength Training", "description": "4× structured resistance training per week."},
            {"name": "Sleep Optimization", "description": "Track sleep quality, optimize environment, hit 7-9hrs."},
            {"name": "Recovery Protocol", "description": "Weekly active recovery day with stretching and mobility."},
        ],
    },
    "mental_balance": {
        "beginner": [
            {"name": "Morning Meditation", "description": "5 minutes of silent sitting after waking."},
            {"name": "Gratitude Journal", "description": "Write 3 things you're grateful for each evening."},
            {"name": "Screen-Free Hour", "description": "One hour per day with all screens off."},
        ],
        "medium": [
            {"name": "Breathing Practice", "description": "Box breathing (4-4-4-4) for 10 minutes daily."},
            {"name": "Nature Walk", "description": "30-minute walk outside, phone in pocket, eyes open."},
            {"name": "Digital Detox Evening", "description": "No phone after 8pm, every weekday."},
            {"name": "Weekly Mood Check", "description": "Rate your energy and mood every Sunday."},
        ],
        "advanced": [
            {"name": "20-Min Meditation", "description": "Deep sit daily — body scan, breath, or open awareness."},
            {"name": "Journaling Practice", "description": "Morning pages: 3 unfiltered pages every morning."},
            {"name": "Full Rest Day Design", "description": "One day per week intentionally free of productivity goals."},
            {"name": "Therapy or Coaching", "description": "Regular session for external perspective and growth."},
        ],
    },
    "studying": {
        "beginner": [
            {"name": "Daily Study Block", "description": "1 Pomodoro (25 min) of focused studying per day."},
            {"name": "Flashcard Review", "description": "5-minute daily review of yesterday's notes as flashcards."},
            {"name": "Note Summarization", "description": "After each session, write a 3-sentence summary."},
        ],
        "medium": [
            {"name": "Active Recall Session", "description": "Study by testing yourself, not re-reading."},
            {"name": "Spaced Repetition", "description": "Use SR cards to review material at growing intervals."},
            {"name": "Teach-Back Method", "description": "Explain one concept out loud as if teaching someone."},
            {"name": "Weekly Study Review", "description": "Sunday review of everything covered in the past week."},
        ],
        "advanced": [
            {"name": "3-Hour Deep Study", "description": "Single-subject deep work session with full focus."},
            {"name": "Interleaved Practice", "description": "Mix topics during a session for stronger retention."},
            {"name": "Concept Mapping", "description": "Weekly visual map of how concepts connect."},
            {"name": "Mock Testing", "description": "Monthly exam simulation from memory, no notes."},
        ],
    },
    "find_people": {
        "beginner": [
            {"name": "Weekly Reach-Out", "description": "Message one person you care about every week."},
            {"name": "Genuine Compliment", "description": "Give one sincere, specific compliment per day."},
            {"name": "Community Check-In", "description": "Participate in one group or challenge per week."},
        ],
        "medium": [
            {"name": "Social Commitment", "description": "Plan one social event or activity per week in advance."},
            {"name": "Active Listening Practice", "description": "In every conversation, focus entirely on the other person."},
            {"name": "New Connection Goal", "description": "Meet one new person per week in a setting you enjoy."},
        ],
        "advanced": [
            {"name": "Host a Gathering", "description": "Organize a small get-together once per month."},
            {"name": "Mentorship", "description": "Find someone to mentor or be mentored by."},
            {"name": "Community Leadership", "description": "Take on a leadership role in an existing community."},
        ],
    },
    "find_direction": {
        "beginner": [
            {"name": "Daily Journaling", "description": "5 minutes of uncensored stream-of-consciousness writing."},
            {"name": "Values Reflection", "description": "Weekly: write one thing that felt deeply right or wrong."},
            {"name": "New Experience", "description": "Try one new activity, food, or place per week."},
        ],
        "medium": [
            {"name": "Ikigai Mapping", "description": "Monthly reflection on what you love, are good at, and the world needs."},
            {"name": "Identity Statement", "description": "Write and update a 3-sentence statement of who you're becoming."},
            {"name": "Curiosity Exploration", "description": "Spend 1 hour per week exploring a topic that fascinates you."},
        ],
        "advanced": [
            {"name": "Annual Vision Document", "description": "Write a detailed 1-year vision for your ideal life."},
            {"name": "Monthly Life Review", "description": "Rate every area of life and identify where to focus next."},
            {"name": "North Star Exercise", "description": "Define 3 guiding principles that will never compromise."},
        ],
    },
    "personal_growth": {
        "beginner": [
            {"name": "Daily Reading", "description": "10 pages of a personal development book per day."},
            {"name": "Reflection Journal", "description": "Evening reflection: what did you learn today?"},
            {"name": "Comfort Zone Step", "description": "One small action outside your comfort zone per week."},
        ],
        "medium": [
            {"name": "Weekly Learning Goal", "description": "Set and complete one learning objective per week."},
            {"name": "Feedback Seeking", "description": "Ask one trusted person for honest feedback monthly."},
            {"name": "Skill Practice", "description": "Deliberate practice on a chosen skill for 30 min/day."},
        ],
        "advanced": [
            {"name": "Deliberate Practice", "description": "90-min deep skill practice with immediate feedback."},
            {"name": "Monthly Challenge", "description": "One ambitious challenge per month at the edge of your ability."},
            {"name": "Mentorship", "description": "Regular sessions with a mentor in your area of growth."},
        ],
    },
    "social_motivation": {
        "beginner": [
            {"name": "Community Participation", "description": "Show up to one group activity or challenge per week."},
            {"name": "Support Someone", "description": "Offer genuine help or encouragement to one person per day."},
            {"name": "Share Progress", "description": "Post or share one update about your journey publicly per week."},
        ],
        "medium": [
            {"name": "Accountability Partner", "description": "Check in with a partner on your goals weekly."},
            {"name": "Group Challenge", "description": "Join and complete one group challenge per month."},
            {"name": "Vulnerability Practice", "description": "Share one real struggle with a trusted person weekly."},
        ],
        "advanced": [
            {"name": "Community Contribution", "description": "Create value for your community weekly — share what you know."},
            {"name": "Challenge Leadership", "description": "Lead or organize a community challenge."},
            {"name": "Deep Relationship Investment", "description": "Dedicate focused quality time to 3 key relationships weekly."},
        ],
    },
    "life_reset": {
        "beginner": [
            {"name": "Morning Routine", "description": "Simple 20-min morning: water, stretch, plan."},
            {"name": "One Thing Daily", "description": "Identify and do the one thing that matters most today."},
            {"name": "Evening Wind-Down", "description": "30-minute screen-free wind-down before bed."},
        ],
        "medium": [
            {"name": "Weekly Planning Session", "description": "Sunday 45-min review and planning for the week."},
            {"name": "Identity Habit Stack", "description": "3 habits that reinforce who you are becoming."},
            {"name": "Declutter Practice", "description": "Remove one thing (digital or physical) from your life per week."},
        ],
        "advanced": [
            {"name": "Full Reset Protocol", "description": "Monthly audit of relationships, commitments, and environment."},
            {"name": "Deep Work Priority", "description": "Most important work done first, every single day."},
            {"name": "Annual Life Architecture", "description": "Design your ideal year and reverse-engineer the habits."},
        ],
    },
}


class GoalService(IGoalService):
    GOAL_OPTIONS = [
        {
            "code": "focus_productivity",
            "title": "Focus & Productivity",
            "description": "Improve concentration and reduce distractions to get more done daily.",
            "schedule": "Daily work sessions",
        },
        {
            "code": "nutrition",
            "title": "Nutrition",
            "description": "Fuel your body with the right food for energy and health.",
            "schedule": "Every meal",
        },
        {
            "code": "self_discipline",
            "title": "Self-Discipline",
            "description": "Build a consistent routine for workouts, movement, and healthy sleep.",
            "schedule": "Daily",
        },
        {
            "code": "studying",
            "title": "Studying",
            "description": "Learn faster and more effectively.",
            "schedule": "Daily study blocks",
        },
        {
            "code": "find_people",
            "title": "Find your person / people",
            "description": "Connect with like-minded individuals on the same journey.",
            "schedule": "Weekly community check-in",
        },
        {
            "code": "find_direction",
            "title": "Find Identity / Direction",
            "description": "Discover your true purpose and path.",
            "schedule": "Daily reflection",
        },
        {
            "code": "health",
            "title": "Health",
            "description": "Prioritize your physical and mental well-being.",
            "schedule": "Daily",
        },
    ]

    def __init__(self, goal_repository: GoalRepository):
        self.goal_repository = goal_repository
        self._options_by_code = {
            option["code"]: option for option in self.GOAL_OPTIONS
        }

    def get_goal_options(self) -> dict[str, list[dict[str, str]]]:
        return {"status": "success", "data": self.GOAL_OPTIONS}

    def set_goal(self, email: str, goal_code: str) -> dict[str, str | dict]:
        goal_option = self._options_by_code.get(goal_code)
        if goal_option is None:
            return {"status": "error", "message": "Goal code is not supported."}

        goal_data = {
            "email": email,
            "goalCode": goal_option["code"],
            "goalTitle": goal_option["title"],
            "goalDescription": goal_option["description"],
            "schedule": goal_option["schedule"],
            "updatedAt": datetime.now(UTC).isoformat(),
        }
        try:
            self.goal_repository.upsert_goal(email, goal_data)
            return {
                "status": "success",
                "message": "Goal saved successfully.",
                "data": goal_data,
            }
        except Exception as e:
            return {"status": "error", "message": f"Failed to save goal: {str(e)}"}

    def get_user_goal(self, email: str) -> dict[str, str | dict]:
        try:
            goal = self.goal_repository.find_by_email(email)
            if goal is None:
                return {"status": "error", "message": "Goal not found."}

            goal["_id"] = str(goal["_id"])
            return {"status": "success", "data": goal}
        except Exception as e:
            return {"status": "error", "message": f"Failed to fetch goal: {str(e)}"}

    def get_goal_resources(self, goal_code: str) -> dict[str, Any]:
        resources = GOAL_RESOURCES.get(goal_code)
        if resources is None:
            return {"status": "error", "message": f"No resources found for goal: {goal_code}"}
        return {"status": "success", "data": resources}

    def get_habit_recommendations(self, goal_code: str, level: str = "beginner") -> dict[str, Any]:
        if level not in ("beginner", "medium", "advanced"):
            return {"status": "error", "message": "level must be: beginner, medium, or advanced"}
        goal_recs = HABIT_RECOMMENDATIONS.get(goal_code)
        if goal_recs is None:
            return {"status": "error", "message": f"No recommendations for goal: {goal_code}"}
        habits = goal_recs.get(level, goal_recs.get("beginner", []))
        return {"status": "success", "data": habits}
