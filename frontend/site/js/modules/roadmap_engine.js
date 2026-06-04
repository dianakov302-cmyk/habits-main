const STORAGE_KEYS = {
  selectedGoal: 'anaida_user_goal',
  quizAnswers: 'anaida_quiz_answers',
  profile: 'anaida_user_profile',
  roadmap: 'anaida_user_roadmap',
};

const GOAL_LABELS = {
  focus: 'Focus & Productivity',
  nutrition: 'Nutrition',
  discipline: 'Self-Discipline',
  studying: 'Studying',
  person: 'Find your people',
  direction: 'Identity & Direction',
  health: 'Health',
};

const BASE_STEPS_BY_GOAL = {
  focus: [
    { title: 'Design a focused workspace', description: 'Remove visual noise and define one deep-work zone.', action: 'Set up desk, notifications off, one clear task list.', duration: 'Day 1-2' },
    { title: 'Run deep-work blocks', description: 'Train your attention in short, repeatable sessions.', action: 'Use 2x25-minute sessions daily for one week.', duration: 'Week 1' },
    { title: 'Track distractions', description: 'Measure where your focus breaks to improve fast.', action: 'Log top 3 distractions after each session.', duration: 'Week 1-2' },
    { title: 'Scale intensity', description: 'Increase session length once consistency is stable.', action: 'Move from 25 to 40-minute blocks.', duration: 'Week 3+' },
  ],
  nutrition: [
    { title: 'Audit your current eating pattern', description: 'Understand your baseline before changing behavior.', action: 'Track 3 days of meals and mood.', duration: 'Day 1-3' },
    { title: 'Build your default meal template', description: 'Create simple repeatable meals with protein and fiber.', action: 'Pick 2 breakfasts and 2 lunches for rotation.', duration: 'Week 1' },
    { title: 'Stabilize energy', description: 'Reduce sugar crashes and improve clarity.', action: 'Anchor meals at regular times; add hydration target.', duration: 'Week 2' },
    { title: 'Optimize and sustain', description: 'Refine portions and weekly prep flow.', action: 'Weekly grocery + prep routine every Sunday.', duration: 'Week 3+' },
  ],
  discipline: [
    { title: 'Define identity rule', description: 'Attach your goal to who you want to become.', action: 'Write one line: "I am the kind of person who..."', duration: 'Day 1' },
    { title: 'Create non-negotiable minimum', description: 'Make progress possible even on low-energy days.', action: 'Choose a 2-minute fallback habit.', duration: 'Week 1' },
    { title: 'Stack habits on existing routine', description: 'Use current anchors to reduce friction.', action: 'Attach new habit after wake-up or after dinner.', duration: 'Week 2' },
    { title: 'Review and tighten system', description: 'Iterate based on misses, not mood.', action: 'Weekly review: wins, misses, one system fix.', duration: 'Week 3+' },
  ],
  studying: [
    { title: 'Set learning outcome', description: 'Define what mastery looks like in 30 days.', action: 'Create one measurable target and syllabus list.', duration: 'Day 1' },
    { title: 'Use active recall', description: 'Switch from passive reading to retrieval practice.', action: 'Daily quiz yourself for 20 minutes.', duration: 'Week 1' },
    { title: 'Implement spaced repetition', description: 'Improve retention with smart review timing.', action: 'Review on day 1, 3, 7, 14.', duration: 'Week 2' },
    { title: 'Practice exam mode', description: 'Train under realistic pressure and constraints.', action: '1 timed session every 3 days.', duration: 'Week 3+' },
  ],
  person: [
    { title: 'Define your people profile', description: 'Clarify values and energy you seek in relationships.', action: 'List 5 values and 3 red flags.', duration: 'Day 1' },
    { title: 'Join aligned spaces', description: 'Increase chance of meaningful connection.', action: 'Join 2 communities tied to your interests.', duration: 'Week 1' },
    { title: 'Start intentional conversations', description: 'Move from passive presence to active connection.', action: 'Initiate 3 short conversations weekly.', duration: 'Week 2' },
    { title: 'Nurture promising bonds', description: 'Consistency turns contacts into real relationships.', action: 'Schedule one follow-up weekly.', duration: 'Week 3+' },
  ],
  direction: [
    { title: 'Map your strengths', description: 'Find patterns in what gives you energy.', action: 'Write 10 peak moments and common themes.', duration: 'Day 1-2' },
    { title: 'Run mini experiments', description: 'Test possible paths before committing.', action: 'Try 2 short projects in different areas.', duration: 'Week 1-2' },
    { title: 'Collect feedback loop', description: 'Use outside perspective to reduce blind spots.', action: 'Ask 3 people where they see your edge.', duration: 'Week 2' },
    { title: 'Choose next 90-day direction', description: 'Commit to one path long enough to gain clarity.', action: 'Set a 90-day focus theme and milestone.', duration: 'Week 3+' },
  ],
  health: [
    { title: 'Set health baseline', description: 'Track sleep, movement, and stress patterns.', action: 'Log 7 days of sleep and activity.', duration: 'Week 1' },
    { title: 'Anchor movement habit', description: 'Prioritize consistency over intensity.', action: '20 minutes movement, 5 days/week.', duration: 'Week 1-2' },
    { title: 'Upgrade recovery', description: 'Recovery drives long-term performance.', action: 'Create wind-down routine; fixed sleep window.', duration: 'Week 2' },
    { title: 'Build sustainable rhythm', description: 'Integrate training, nutrition, and rest.', action: 'Weekly planning for workouts and meals.', duration: 'Week 3+' },
  ],
};

const ARCHETYPE_ENHANCERS = {
  A: {
    title: 'Powerhouse',
    tone: 'High drive profile. Channel intensity into structure.',
    programTitle: '30-Day Powerhouse Program',
    programDescription: 'A 30-day system for ambitious users who need structure, deep work, and burnout protection.',
    books: [
      {
        title: 'Atomic Habits',
        author: 'James Clear',
        week: 1,
        reason: 'Build small systems that make discipline easier.'
      },
      {
        title: 'Deep Work',
        author: 'Cal Newport',
        week: 2,
        reason: 'Train focus and remove distraction.'
      },
      {
        title: 'Grit',
        author: 'Angela Duckworth',
        week: 2,
        reason: 'Strengthen long-term perseverance.'
      },
      {
        title: 'Essentialism',
        author: 'Greg McKeown',
        week: 3,
        reason: 'Choose fewer but more important actions.'
      },
      {
        title: 'Discipline Is Destiny',
        author: 'Ryan Holiday',
        week: 4,
        reason: 'Turn discipline into identity.'
      },
    ],
    videos: [
      {
        title: 'How to Get 1% Better Every Day',
        source: 'James Clear',
        week: 1,
        reason: 'Understand the power of small improvements.'
      },
      {
        title: 'Grit: The Power of Passion and Perseverance',
        source: 'Angela Lee Duckworth / TED',
        week: 1,
        reason: 'Learn why stamina matters more than short motivation.'
      },
      {
        title: 'Inside the Mind of a Master Procrastinator',
        source: 'Tim Urban / TED',
        week: 2,
        reason: 'Recognize procrastination patterns.'
      },
      {
        title: 'Deep Work: Rules for Focused Success in a Distracted World',
        source: 'Cal Newport',
        week: 3,
        reason: 'Build focused work blocks.'
      },
      {
        title: 'Start With Why',
        source: 'Simon Sinek / TED',
        week: 4,
        reason: 'Connect action with deeper purpose.'
      },
    ],
    days: [
      { day: 1, task: 'Write your Powerhouse identity rule: “I am the kind of person who finishes what matters.”' },
      { day: 2, task: 'Choose one main goal for the next 30 days.' },
      { day: 3, task: 'Remove one distraction from your workspace.' },
      { day: 4, task: 'Complete one 25-minute deep work block.' },
      { day: 5, task: 'Create a simple habit tracker.' },
      { day: 6, task: 'Plan tomorrow before going to sleep.' },
      { day: 7, task: 'Review week 1: what gave energy, what drained it?' },

      { day: 8, task: 'Do two 25-minute focused work blocks.' },
      { day: 9, task: 'Choose one habit trigger: after waking up, after dinner, or before studying.' },
      { day: 10, task: 'Write your top 3 distractions and remove one.' },
      { day: 11, task: 'Complete the hardest task before entertainment.' },
      { day: 12, task: 'Use a 5-minute reset instead of quitting when tired.' },
      { day: 13, task: 'Schedule one recovery block without guilt.' },
      { day: 14, task: 'Review week 2: where did intensity become chaos?' },

      { day: 15, task: 'Increase one key habit by 10–15%.' },
      { day: 16, task: 'Do one deep work session without phone nearby.' },
      { day: 17, task: 'Say no to one low-value task.' },
      { day: 18, task: 'Write one page about why this goal matters.' },
      { day: 19, task: 'Create a minimum version of your habit for bad days.' },
      { day: 20, task: 'Finish one task fully before starting another.' },
      { day: 21, task: 'Review week 3: what system should stay?' },

      { day: 22, task: 'Design your ideal productive morning.' },
      { day: 23, task: 'Do one focused session and track how you felt after.' },
      { day: 24, task: 'Remove one unnecessary commitment.' },
      { day: 25, task: 'Create a personal discipline rule.' },
      { day: 26, task: 'Practice active rest: walking, stretching, or journaling.' },
      { day: 27, task: 'Prepare a plan for the next 7 days.' },
      { day: 28, task: 'Write your biggest win from the program.' },
      { day: 29, task: 'Choose one habit to continue for 60 more days.' },
      { day: 30, task: 'Final review: what identity did you build?' },
    ],
    steps: [
      {
        title: 'Prevent burnout guardrails',
        description: 'Ambitious profiles need recovery rules.',
        action: 'Schedule one no-pressure recovery block daily.'
      },
    ],
  },

  B: {
    title: 'Builder',
    tone: 'Balanced profile. Progress compounds with consistent systems.',
    programTitle: '30-Day Builder Program',
    programDescription: 'A 30-day system for users who want stable progress, simple routines, and realistic consistency.',
    books: [
      {
        title: 'Atomic Habits',
        author: 'James Clear',
        week: 1,
        reason: 'Create simple habits that are easy to repeat.'
      },
      {
        title: 'The Compound Effect',
        author: 'Darren Hardy',
        week: 1,
        reason: 'Understand how small daily choices create big results.'
      },
      {
        title: 'Make Time',
        author: 'Jake Knapp & John Zeratsky',
        week: 2,
        reason: 'Build a realistic daily focus system.'
      },
      {
        title: 'Mindset',
        author: 'Carol S. Dweck',
        week: 3,
        reason: 'Develop a growth mindset and reduce fear of mistakes.'
      },
      {
        title: 'The One Thing',
        author: 'Gary Keller & Jay Papasan',
        week: 4,
        reason: 'Learn to choose the most important action instead of doing everything.'
      },
    ],
    videos: [
      {
        title: 'Atomic Habits: How to Get 1% Better Every Day',
        source: 'James Clear',
        week: 1,
        reason: 'Learn why small repeated actions matter.'
      },
      {
        title: 'The Power of Believing That You Can Improve',
        source: 'Carol S. Dweck / TED',
        week: 1,
        reason: 'Understand growth mindset.'
      },
      {
        title: 'Inside the Mind of a Master Procrastinator',
        source: 'Tim Urban / TED',
        week: 2,
        reason: 'Recognize why plans are delayed.'
      },
      {
        title: 'How to Gain Control of Your Free Time',
        source: 'Laura Vanderkam / TED',
        week: 3,
        reason: 'Use time intentionally without pressure.'
      },
      {
        title: 'How Great Leaders Inspire Action',
        source: 'Simon Sinek / TED',
        week: 4,
        reason: 'Connect habits with personal meaning.'
      },
    ],
    days: [
      { day: 1, task: 'Write your Builder identity rule: “I am the kind of person who improves step by step.”' },
      { day: 2, task: 'Choose one habit that is realistic for the next 30 days.' },
      { day: 3, task: 'Make the habit smaller until it feels easy to start.' },
      { day: 4, task: 'Attach your habit to an existing routine.' },
      { day: 5, task: 'Track one small win today.' },
      { day: 6, task: 'Plan tomorrow’s first task.' },
      { day: 7, task: 'Review week 1: what was easy to repeat?' },

      { day: 8, task: 'Repeat your minimum habit even if motivation is low.' },
      { day: 9, task: 'Create a simple morning or evening routine.' },
      { day: 10, task: 'Remove one source of friction.' },
      { day: 11, task: 'Do one task before checking social media.' },
      { day: 12, task: 'Write what helped you stay consistent today.' },
      { day: 13, task: 'Prepare your environment for tomorrow.' },
      { day: 14, task: 'Review week 2: what system worked best?' },

      { day: 15, task: 'Improve one habit by a small amount.' },
      { day: 16, task: 'Use a 25-minute focus block.' },
      { day: 17, task: 'Choose one priority for the day.' },
      { day: 18, task: 'Write one lesson from a recent mistake.' },
      { day: 19, task: 'Create a fallback version of your habit.' },
      { day: 20, task: 'Complete one task fully before switching.' },
      { day: 21, task: 'Review week 3: what should become automatic?' },

      { day: 22, task: 'Plan your next 7 days in 10 minutes.' },
      { day: 23, task: 'Repeat your easiest productive habit.' },
      { day: 24, task: 'Say no to one unnecessary distraction.' },
      { day: 25, task: 'Write your personal consistency rule.' },
      { day: 26, task: 'Do one recovery activity without guilt.' },
      { day: 27, task: 'Prepare your final weekly routine.' },
      { day: 28, task: 'Write your biggest progress from the program.' },
      { day: 29, task: 'Choose one habit to continue next month.' },
      { day: 30, task: 'Final review: what system will you keep?' },
    ],
    steps: [
      {
        title: 'Strengthen momentum loops',
        description: 'Your advantage is steady improvement.',
        action: 'End each day by planning tomorrow’s first task.'
      },
    ],
  },

  C: {
    title: 'Explorer',
    tone: 'Discovery profile. Win by reducing friction and raising clarity.',
    programTitle: '30-Day Explorer Program',
    programDescription: 'A 30-day system for users who are still searching for clarity and need small, low-pressure starts.',
    books: [
      {
        title: 'Designing Your Life',
        author: 'Bill Burnett & Dave Evans',
        week: 1,
        reason: 'Explore possible directions without needing one perfect answer.'
      },
      {
        title: 'The Gifts of Imperfection',
        author: 'Brené Brown',
        week: 1,
        reason: 'Reduce pressure and accept imperfect progress.'
      },
      {
        title: 'The War of Art',
        author: 'Steven Pressfield',
        week: 2,
        reason: 'Understand resistance and why starting feels hard.'
      },
      {
        title: 'Mindset',
        author: 'Carol S. Dweck',
        week: 3,
        reason: 'Build confidence through learning, not perfection.'
      },
      {
        title: 'Start With Why',
        author: 'Simon Sinek',
        week: 4,
        reason: 'Clarify the deeper reason behind your actions.'
      },
    ],
    videos: [
      {
        title: 'How to Build a Life You Love',
        source: 'Designing Your Life / Bill Burnett',
        week: 1,
        reason: 'Start thinking about life as experiments, not one fixed plan.'
      },
      {
        title: 'The Power of Vulnerability',
        source: 'Brené Brown / TED',
        week: 1,
        reason: 'Reduce fear of being imperfect.'
      },
      {
        title: 'Inside the Mind of a Master Procrastinator',
        source: 'Tim Urban / TED',
        week: 2,
        reason: 'Understand why starting is often difficult.'
      },
      {
        title: 'The Power of Believing That You Can Improve',
        source: 'Carol S. Dweck / TED',
        week: 3,
        reason: 'Build a learning mindset.'
      },
      {
        title: 'Start With Why',
        source: 'Simon Sinek / TED',
        week: 4,
        reason: 'Clarify personal direction and meaning.'
      },
    ],
    days: [
      { day: 1, task: 'Write your Explorer identity rule: “I am allowed to start before I feel ready.”' },
      { day: 2, task: 'Choose one area of life you want to understand better.' },
      { day: 3, task: 'Write 3 possible goals without judging them.' },
      { day: 4, task: 'Do one 5-minute starter action.' },
      { day: 5, task: 'Write what felt easier than expected.' },
      { day: 6, task: 'Choose one small experiment for tomorrow.' },
      { day: 7, task: 'Review week 1: what gave you clarity?' },

      { day: 8, task: 'Repeat one 5-minute action.' },
      { day: 9, task: 'Remove one reason that makes starting harder.' },
      { day: 10, task: 'Ask yourself: what do I avoid and why?' },
      { day: 11, task: 'Try one new productive environment.' },
      { day: 12, task: 'Write one thing you learned about yourself.' },
      { day: 13, task: 'Do one low-pressure action related to your goal.' },
      { day: 14, task: 'Review week 2: what resistance appeared most often?' },

      { day: 15, task: 'Choose one direction to test for the next 7 days.' },
      { day: 16, task: 'Do one 10-minute focus session.' },
      { day: 17, task: 'Write what kind of person you want to become.' },
      { day: 18, task: 'Talk to one person or watch one story related to your goal.' },
      { day: 19, task: 'Create a minimum habit for unclear days.' },
      { day: 20, task: 'Finish one small task completely.' },
      { day: 21, task: 'Review week 3: what direction feels most alive?' },

      { day: 22, task: 'Create a simple 7-day plan.' },
      { day: 23, task: 'Repeat your most successful starter action.' },
      { day: 24, task: 'Remove one unnecessary pressure from your plan.' },
      { day: 25, task: 'Write your clarity rule: “When I feel lost, I will...”' },
      { day: 26, task: 'Do one calming activity: walk, journal, stretch, or clean your space.' },
      { day: 27, task: 'Choose one goal to continue next month.' },
      { day: 28, task: 'Write your biggest discovery from the program.' },
      { day: 29, task: 'Choose one habit to keep for 30 more days.' },
      { day: 30, task: 'Final review: what became clearer about you?' },
    ],
    steps: [
      {
        title: 'Lower activation energy',
        description: 'Small starts convert intention into action.',
        action: 'Use 5-minute starter ritual before each session.'
      },
    ],
  },
};

function clampLevel(value) {
  if (value >= 2.4) return 'high';
  if (value >= 1.7) return 'medium';
  return 'low';
}

function scoreAnswer(answer) {
  if (answer === 'A') return 3;
  if (answer === 'B') return 2;
  return 1;
}

export function calculateProfileFromAnswers(answers, selectedGoal) {
  const count = { A: 0, B: 0, C: 0 };
  answers.forEach((a) => {
    if (count[a] !== undefined) count[a] += 1;
  });

  const archetype = Object.entries(count).sort((x, y) => y[1] - x[1])[0][0];
  const motivationRaw = (scoreAnswer(answers[0]) + scoreAnswer(answers[3])) / 2;
  const consistencyRaw = (scoreAnswer(answers[4]) + scoreAnswer(answers[1])) / 2;

  return {
    selectedGoal: selectedGoal || 'discipline',
    selectedGoalLabel: GOAL_LABELS[selectedGoal] || 'Self-Discipline',
    archetype,
    archetypeLabel: ARCHETYPE_ENHANCERS[archetype].title,
    motivationLevel: clampLevel(motivationRaw),
    consistencyLevel: clampLevel(consistencyRaw),
    scores: {
      motivation: motivationRaw,
      consistency: consistencyRaw,
      count,
    },
  };
}

function getAdaptiveStep(profile) {
  const { motivationLevel, consistencyLevel } = profile;

  if (motivationLevel === 'high' && consistencyLevel === 'low') {
    return {
      title: 'Convert energy into repeatability',
      description: 'You have strong drive, but routines are unstable.',
      action: 'Choose fixed trigger times for your two most important actions.',
      duration: 'Next 7 days',
    };
  }

  if (motivationLevel === 'low' && consistencyLevel === 'high') {
    return {
      title: 'Reignite purpose while staying on track',
      description: 'Your consistency is strong; renew emotional connection to your why.',
      action: 'Write one outcome journal entry after each completed session.',
      duration: 'Next 10 days',
    };
  }

  if (motivationLevel === 'low' && consistencyLevel === 'low') {
    return {
      title: 'Start with minimum viable momentum',
      description: 'Reduce pressure and build a confidence streak first.',
      action: 'Do 10 minutes daily and track a 7-day streak.',
      duration: 'Week 1',
    };
  }

  return {
    title: 'Scale what already works',
    description: 'You have healthy momentum and consistency.',
    action: 'Increase one key habit by 10-15% next week.',
    duration: 'Week 2',
  };
}

export function generateRoadmap(profile) {
  const baseSteps = BASE_STEPS_BY_GOAL[profile.selectedGoal] || BASE_STEPS_BY_GOAL.discipline;
  const enhancer = ARCHETYPE_ENHANCERS[profile.archetype];
  const adaptiveStep = getAdaptiveStep(profile);

  const steps = [
    { ...baseSteps[0], pillar: 'Foundation' },
    { ...enhancer.steps[0], duration: 'Week 1', pillar: 'Archetype Fit' },
    { ...adaptiveStep, pillar: 'Behavior Design' },
    { ...baseSteps[1], pillar: 'Execution' },
    { ...baseSteps[2], pillar: 'Optimization' },
    { ...baseSteps[3], pillar: 'Scale' },
  ];

return {
  headline: `${profile.archetypeLabel} Roadmap for ${profile.selectedGoalLabel}`,
  summary: `${enhancer.tone} Motivation: ${profile.motivationLevel}. Consistency: ${profile.consistencyLevel}.`,
  steps,
  program: {
    title: enhancer.programTitle || `${profile.archetypeLabel} 30-Day Program`,
    description: enhancer.programDescription || '',
    books: enhancer.books || [],
    videos: enhancer.videos || [],
    days: enhancer.days || [],
  },
  generatedAt: new Date().toISOString(),
};
}
export function saveRoadmapSession(answers, profile, roadmap) {
  localStorage.setItem(STORAGE_KEYS.quizAnswers, JSON.stringify(answers));
  localStorage.setItem(STORAGE_KEYS.profile, JSON.stringify(profile));
  localStorage.setItem(STORAGE_KEYS.roadmap, JSON.stringify(roadmap));
}

export function getStoredRoadmapSession() {
  const selectedGoal = localStorage.getItem(STORAGE_KEYS.selectedGoal);
  const answersRaw = localStorage.getItem(STORAGE_KEYS.quizAnswers);
  const profileRaw = localStorage.getItem(STORAGE_KEYS.profile);
  const roadmapRaw = localStorage.getItem(STORAGE_KEYS.roadmap);

  return {
    selectedGoal,
    answers: answersRaw ? JSON.parse(answersRaw) : [],
    profile: profileRaw ? JSON.parse(profileRaw) : null,
    roadmap: roadmapRaw ? JSON.parse(roadmapRaw) : null,
  };
}

export function renderRoadmap(container, profile, roadmap) {
  if (!container || !profile || !roadmap) return;

  container.innerHTML = `
    <section class="roadmap-shell">
      <div class="roadmap-shell-header">
        <p class="roadmap-kicker">Personal Plan</p>
        <h3 class="roadmap-headline">${roadmap.headline}</h3>
        <p class="roadmap-summary">${roadmap.summary}</p>
        <div class="roadmap-meta">
          <span>Archetype: ${profile.archetypeLabel}</span>
          <span>Motivation: ${profile.motivationLevel}</span>
          <span>Consistency: ${profile.consistencyLevel}</span>
        </div>
      </div>
      <div class="roadmap-grid">
        ${roadmap.steps
          .map(
            (step, index) => `
              <article class="roadmap-card">
                <p class="roadmap-card-step">Step ${index + 1} · ${step.pillar}</p>
                <h4>${step.title}</h4>
                <p>${step.description}</p>
                <p class="roadmap-card-action">${step.action}</p>
                <p class="roadmap-card-duration">${step.duration || ''}</p>
              </article>
            `
          )
          .join('')}
      </div>
    </section>
  `;
}

