import { getStoredRoadmapSession, renderRoadmap } from './roadmap_engine.js';

export function initPlanPage() {
  const container = document.getElementById('planContent');
  const continueBtn = document.getElementById('continueToRegistration');
  if (!container) return;

  const { profile, roadmap } = getStoredRoadmapSession();

  if (profile && roadmap) {
    renderRoadmap(container, profile, roadmap);
  } else {
    container.innerHTML = `
      <div class="quiz-result">
        <div class="quiz-result-type">Plan not found</div>
        <p class="quiz-result-text">Please complete the test first to generate your personal plan.</p>
        <a href="test.html" class="quiz-btn" style="display:inline-block;text-decoration:none;">Go to Test</a>
      </div>
    `;
  }

  if (continueBtn) {
    continueBtn.addEventListener('click', () => {
      window.location.href = 'registration.html?from=plan';
    });
  }
}
