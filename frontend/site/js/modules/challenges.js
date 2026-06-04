import { escapeHtml } from './utils.js';
import { apiRequest } from './api.js';

export function initChallenges() {
  const challengeJoin = document.getElementById('challengeJoin');
  const challengeInput = document.getElementById('challengeInput');
  const challengeList = document.getElementById('challengeList');

  if (!challengeJoin || !challengeInput || !challengeList) return;

  function renderChallengeCard(title) {
    const card = document.createElement('div');
    card.className = 'challenge-card';
    card.innerHTML = `
      <div>
        <div class="challenge-card-title">🎯 ${escapeHtml(title)}</div>
        <div class="challenge-card-meta">Community challenge</div>
      </div>
      <button class="challenge-join-small" style="color:var(--emerald);border-color:var(--emerald)">Joined ✓</button>
    `;
    return card;
  }

  async function loadChallenges() {
    try {
      const challenges = await apiRequest('/challenges/');
      challengeList.innerHTML = '';
      challenges.forEach(challenge => {
        challengeList.appendChild(renderChallengeCard(challenge.title || 'Untitled challenge'));
      });
    } catch (error) {
      console.error('Failed to load challenges', error);
    }
  }

  challengeJoin.addEventListener('click', async () => {
    const val = challengeInput.value.trim();
    if (!val) return;

    try {
      await apiRequest('/challenges/create', {
        method: 'POST',
        body: JSON.stringify({ title: val }),
      });
      challengeInput.value = '';
      await loadChallenges();
    } catch (error) {
      console.error('Failed to create challenge', error);
    }
  });

  challengeList.addEventListener('click', event => {
    const btn = event.target.closest('.challenge-join-small');
    if (!btn) return;
    btn.textContent = 'Joined ✓';
    btn.style.color = 'var(--emerald)';
    btn.style.borderColor = 'var(--emerald)';
    btn.disabled = true;
  });

  loadChallenges();
}
