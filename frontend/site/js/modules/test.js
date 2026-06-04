import {
  calculateProfileFromAnswers,
  generateRoadmap,
  saveRoadmapSession,
} from './roadmap_engine.js';
import { apiRequest, USER_EMAIL_KEY } from './api.js';

const QUIZ_SESSION_KEY = 'anaida_quiz_session_id';

function getQuizSessionId() {
  const existing = localStorage.getItem(QUIZ_SESSION_KEY);
  if (existing) return existing;

  const generated =
    (window.crypto && typeof window.crypto.randomUUID === 'function')
      ? window.crypto.randomUUID()
      : `quiz-${Date.now()}-${Math.random().toString(16).slice(2)}`;
  localStorage.setItem(QUIZ_SESSION_KEY, generated);
  return generated;
}

async function saveQuizResultToDatabase({ answers, profile, roadmap }) {
  const payload = {
    session_id: getQuizSessionId(),
    email: localStorage.getItem(USER_EMAIL_KEY) || null,
    answers,
    profile,
    roadmap,
  };

  await apiRequest('/users/test-result', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export function initQuiz() {
  const quizContent = document.getElementById('quizContent');
  if (!quizContent) {
    console.error('✗ Quiz: #quizContent element not found!');
    return;
  }

  console.log('✓ Quiz: Initializing...');

  const selectedGoal = localStorage.getItem('anaida_user_goal');

const QUESTIONS = [
  {
    q: 'How often do you think about your goal during the day?',
    options: [
      { label: 'A. It’s always on my mind 🔥', value: 'A' },
      { label: 'B. A few times a day', value: 'B' },
      { label: 'C. Rarely or only when reminded', value: 'C' },
    ]
  },
  {
    q: 'Have you already taken any real steps toward your goal?',
    options: [
      { label: 'A. Yes, I’m already moving forward 💪', value: 'A' },
      { label: 'B. I’m planning and preparing', value: 'B' },
      { label: 'C. Not yet, just thinking about it', value: 'C' },
    ]
  },
  {
    q: 'How clear is your goal?',
    options: [
      { label: 'A. Very clear — I know exactly what I want 🎯', value: 'A' },
      { label: 'B. Somewhat clear', value: 'B' },
      { label: 'C. Still vague or uncertain', value: 'C' },
    ]
  },
  {
    q: 'How do you react when things get difficult?',
    options: [
      { label: 'A. I keep going no matter what 🚀', value: 'A' },
      { label: 'B. I slow down but don’t stop', value: 'B' },
      { label: 'C. I usually give up or pause for long', value: 'C' },
    ]
  },
  {
    q: 'How consistent are your actions toward your goal?',
    options: [
      { label: 'A. I work on it every day ⚡', value: 'A' },
      { label: 'B. A few times a week', value: 'B' },
      { label: 'C. Very irregularly', value: 'C' },
    ]
  },
];

  const RESULTS = {
    A: '⚡ Powerhouse',
    B: '📊 Builder',
    C: '✨ Explorer'
  };

  let answers = [];
  let currentQ = 0;

  function renderQuestion() {
    const q = QUESTIONS[currentQ];

    console.log(`Quiz: Rendering question ${currentQ + 1}/${QUESTIONS.length}`);

    quizContent.innerHTML = `
      ${selectedGoal ? `<p class="quiz-intro">Selected goal: <strong>${selectedGoal}</strong></p>` : ''}
      <h3 class="quiz-question">${q.q}</h3>
      <div class="quiz-options">
        ${q.options.map(opt =>
          `<button class="quiz-option" data-value="${opt.value}">
            ${opt.label}
          </button>`
        ).join('')}
      </div>
      <div class="quiz-nav">
        <button id="next" class="quiz-btn" disabled>Next</button>
      </div>
    `;

    let selected = null;

    document.querySelectorAll('.quiz-option').forEach(btn => {
      btn.onclick = () => {
        document.querySelectorAll('.quiz-option')
          .forEach(b => b.classList.remove('selected'));

        btn.classList.add('selected');
        selected = btn.getAttribute('data-value');
        document.getElementById('next').disabled = false;
      };
    });

    document.getElementById('next').onclick = () => {
      answers.push(selected);
      currentQ++;

      if (currentQ < QUESTIONS.length) {
        renderQuestion();
      } else {
        showResult();
      }
    };
  }

  function showResult() {
    const count = { A: 0, B: 0, C: 0 };
    answers.forEach(a => count[a]++);

    const winner = Object.entries(count)
      .sort((a, b) => b[1] - a[1])[0][0];
    const profile = calculateProfileFromAnswers(answers, selectedGoal);
    const roadmap = generateRoadmap(profile);
    saveRoadmapSession(answers, profile, roadmap);
    void saveQuizResultToDatabase({ answers, profile, roadmap }).catch((error) => {
      console.warn('Failed to save quiz result:', error);
    });

    quizContent.innerHTML = `
      <div class="quiz-result">
        <div class="quiz-result-type">${RESULTS[winner]}</div>
        <p class="quiz-result-text">Your test is complete. Your personal plan is ready.</p>
        <button id="toPlan" class="quiz-btn" style="margin-top:14px;">Open My Plan</button>
        <button id="restart" class="quiz-restart">Restart</button>
      </div>
    `;

    const toPlanBtn = document.getElementById('toPlan');
    if (toPlanBtn) {
      toPlanBtn.onclick = () => {
        window.location.href = 'dashboard.html?tab=program';
      };
    }

    document.getElementById('restart').onclick = () => {
      answers = [];
      currentQ = 0;
      localStorage.removeItem('anaida_quiz_answers');
      localStorage.removeItem('anaida_user_profile');
      localStorage.removeItem('anaida_user_roadmap');
      renderQuestion();
    };
  }

   renderQuestion();
 }

 console.log('✓ Quiz: Fully initialized. Rendering first question...');
