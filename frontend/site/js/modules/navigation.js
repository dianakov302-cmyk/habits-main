import { initAuth } from './auth.js';

export let showScreen;

export function initNavigation() {
  const pills   = document.querySelectorAll('.nav-pill');
  const screens = document.querySelectorAll('.screen');

  if (!pills.length || !screens.length) return;

  showScreen = function(id) {
    screens.forEach(s => s.classList.remove('active'));
    pills.forEach(p   => p.classList.remove('active'));

    const target = document.getElementById(id);
    if (target) target.classList.add('active');

    const pill = document.querySelector(`.nav-pill[data-target="${id}"]`);
    if (pill) pill.classList.add('active');
  };

  pills.forEach(pill => {
    pill.addEventListener('click', () => showScreen(pill.dataset.target));
  });

  // Auth + avatar (avatar click handled inside initAuth)
  initAuth();
}
