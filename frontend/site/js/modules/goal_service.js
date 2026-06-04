import { apiRequest, USER_EMAIL_KEY } from './api.js';

/* Static fallback goals — shown if the API is unavailable */
const FALLBACK_GOALS = [
  { code: 'focus_productivity',  title: 'Focus & Productivity',      description: 'Improve concentration and reduce distractions to get more done daily.' },
  { code: 'nutrition',           title: 'Nutrition',                  description: 'Fuel your body with the right food for energy and health.' },
  { code: 'self_discipline',     title: 'Self-Discipline',            description: 'Build a consistent routine for workouts, movement, and healthy sleep.' },
  { code: 'studying',            title: 'Studying',                   description: 'Learn faster and more effectively.' },
  { code: 'find_people',         title: 'Find your person / people',  description: 'Connect with like-minded individuals.' },
  { code: 'find_direction',      title: 'Find Identity / Direction',  description: 'Discover your true purpose and path.' },
  { code: 'health',              title: 'Health',                     description: 'Prioritize your physical and mental well-being.' },
];

function readCurrentUserEmail() {
  return localStorage.getItem(USER_EMAIL_KEY) || '';
}

function showMsg(container, text, isError = false) {
  let el = container.querySelector('.goal-service-message');
  if (!el) {
    el = document.createElement('div');
    el.className = 'goal-service-message';
    container.prepend(el);
  }
  el.innerHTML = text;
  el.style.color = isError ? '#ef4444' : '#10b981';
  el.style.marginBottom = '12px';
}

function renderGoalItems(container, goals, onGoalSelected) {
  // Remove only dynamically generated items (keep .goal-service-message if present)
  container.querySelectorAll('.goal-item').forEach(el => el.remove());

  goals.forEach(option => {
    const item = document.createElement('div');
    item.className = 'goal-item';
    item.dataset.goal = option.code;
    item.innerHTML = `
      <span class="goal-name">${option.title}</span>
      <span class="goal-desc">${option.description}</span>
    `;

    item.addEventListener('click', async () => {
      const email = readCurrentUserEmail();

      if (!email) {
        showMsg(
          container,
          `Please <a href="registration.html" style="color:#fff;text-decoration:underline;">register or sign in</a> to save your goal.`,
          true,
        );
        return;
      }

      // Visual selection
      container.querySelectorAll('.goal-item').forEach(i => i.classList.remove('selected'));
      item.classList.add('selected');

      try {
        const saved = await apiRequest('/goals/set', {
          method: 'POST',
          body: JSON.stringify({ email, goal_code: option.code }),
        });

        if (saved?.status === 'success') {
          showMsg(container, '✓ Goal saved to your account.');
          if (onGoalSelected) onGoalSelected(option.code);
          return;
        }

        showMsg(container, saved?.message || 'Could not save goal.', true);
      } catch (err) {
        showMsg(container, err.message || 'Could not save goal.', true);
      }
    });

    container.appendChild(item);
  });
}

export function initGoalSelection(onGoalSelected) {
  const container = document.getElementById('goalListContainer');
  if (!container) return;

  (async () => {
    try {
      const response = await apiRequest('/goals/options');
      const goals = response?.data;
      if (Array.isArray(goals) && goals.length > 0) {
        renderGoalItems(container, goals, onGoalSelected);
        return;
      }
      throw new Error('Empty goal list from server');
    } catch (_err) {
      // Graceful degradation: keep/render fallback goals
      renderGoalItems(container, FALLBACK_GOALS, onGoalSelected);
    }
  })();
}
