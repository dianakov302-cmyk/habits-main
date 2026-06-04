import { initNavigation, showScreen } from './modules/navigation.js';
import { initPomodoro } from './modules/pomodoro.js';
import { initChat } from './modules/chat.js';
import { initChallenges } from './modules/challenges.js';
import { initAbout } from './modules/about.js';
import { initQuiz } from './modules/test.js';
import { initRegistration } from './modules/registration.js';
import { initGoalSelection } from './modules/goal_service.js';
import { initMotivation } from './modules/motivation.js';
import { initParallax } from './modules/parallax.js';
import { initAuth } from './modules/auth.js';


const page = document.body?.dataset.page;

function initFeaturesPicker() {
  const featuresHome = document.getElementById('featuresHome');
  const pomodoroPanel = document.getElementById('pomodoroPanel');
  const backToFeatures = document.getElementById('backToFeatures');
  const pomodoroCard = document.querySelector('.feature-card[data-feature="pomodoro"]');

  if (!featuresHome || !pomodoroPanel || !pomodoroCard) return;

  pomodoroCard.addEventListener('click', () => {
    featuresHome.style.display = 'none';
    pomodoroPanel.classList.add('active');
  });

  backToFeatures?.addEventListener('click', () => {
    pomodoroPanel.classList.remove('active');
    featuresHome.style.display = 'block';
  });
}

if (page === 'home') {
  initNavigation();
  initPomodoro();
  initFeaturesPicker();
  initChat();
  initChallenges();
  initAbout();
  initMotivation();
  initParallax();

  // Quiz Modal Logic
  const openGoalsBtn = document.getElementById('openGoals');
  const quizModal = document.getElementById('quizModal');
  const closeQuizBtn = document.getElementById('closeQuiz');

  const goToGoals = (e) => {
    if (e) e.preventDefault();
    if (showScreen) {
      showScreen('goal');
    }
  };

  if (openGoalsBtn) {
    openGoalsBtn.onclick = goToGoals;
  }

  if (closeQuizBtn && quizModal) {
    closeQuizBtn.onclick = () => {
      quizModal.classList.remove('open');
    };
  }

  // Close on background click
  if (quizModal) {
    quizModal.onclick = (e) => {
      if (e.target === quizModal) {
        quizModal.classList.remove('open');
      }
    };
  }

  // Goal Selection Logic — after saving, take user to features
  initGoalSelection((goal) => {
    console.log(`Goal chosen: ${goal}`);
    if (showScreen) showScreen('features');
  });
}

if (page === 'test') {
  console.log('✓ App: Initializing test page');
  initQuiz();
}

if (page === 'plan') {
  import('./modules/plan.js').then(({ initPlanPage }) => initPlanPage());
}

if (page === 'registration') {
  console.log('✓ App: Initializing registration page');
  initAuth();        // Keep avatar consistent on auth page
  initRegistration();
}
