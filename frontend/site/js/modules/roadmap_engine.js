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
    steps: [
      { title: 'Prevent burnout guardrails', description: 'Ambitious profiles need recovery rules.', action: 'Schedule one no-pressure recovery block daily.' },
    ],
  },
  B: {
    title: 'Builder',
    tone: 'Balanced profile. Progress compounds with consistent systems.',
    steps: [
      { title: 'Strengthen momentum loops', description: 'Your advantage is steady improvement.', action: 'End each day by planning tomorrow’s first task.' },
    ],
  },
  C: {
    title: 'Explorer',
    tone: 'Discovery profile. Win by reducing friction and raising clarity.',
    steps: [
      { title: 'Lower activation energy', description: 'Small starts convert intention into action.', action: 'Use 5-minute starter ritual before each session.' },
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

