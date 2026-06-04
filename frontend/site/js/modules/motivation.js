/**
 * Motivation & Discipline page — animations, scroll reveals,
 * stat counter, particles, and interactive banner.
 */

export function initMotivation() {
  initBannerInteraction();
  initBannerParticles();
  initScrollAnimations();
  initStatCounters();
  initStartButton();
}

/* ── Interactive Banner on Home page ── */
function initBannerInteraction() {
  const banner = document.getElementById('motivationBanner');
  if (!banner) return;

  // Import showScreen from navigation (it's already globally available)
  banner.addEventListener('click', () => {
    // Navigate to motivation screen
    const screens = document.querySelectorAll('.screen');
    const pills = document.querySelectorAll('.nav-pill');
    screens.forEach(s => s.classList.remove('active'));
    pills.forEach(p => p.classList.remove('active'));
    const target = document.getElementById('motivation');
    if (target) target.classList.add('active');
    const pill = document.querySelector('.nav-pill[data-target="motivation"]');
    if (pill) pill.classList.add('active');

    // After showing screen, trigger hero animations
    setTimeout(() => triggerHeroAnimations(), 100);
  });
}

/* ── Spawn floating particles in banner ── */
function initBannerParticles() {
  const container = document.querySelector('.banner-particles');
  if (!container) return;

  for (let i = 0; i < 20; i++) {
    const particle = document.createElement('div');
    particle.classList.add('banner-particle');
    particle.style.left = Math.random() * 100 + '%';
    particle.style.top = (60 + Math.random() * 40) + '%';
    particle.style.animationDelay = (Math.random() * 4) + 's';
    particle.style.animationDuration = (3 + Math.random() * 3) + 's';
    particle.style.width = (2 + Math.random() * 3) + 'px';
    particle.style.height = particle.style.width;
    container.appendChild(particle);
  }
}

/* ── Trigger hero animations when page becomes active ── */
function triggerHeroAnimations() {
  const motivSection = document.getElementById('motivation');
  if (!motivSection) return;

  const heroAnims = motivSection.querySelectorAll('.motiv-hero .anim-slide-up, .motiv-hero .anim-fade');
  heroAnims.forEach(el => el.classList.add('visible'));
}

/* ── Scroll-triggered reveal animations ── */
function initScrollAnimations() {
  const motivSection = document.getElementById('motivation');
  if (!motivSection) return;

  // Observer for elements with anim-reveal class
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.15,
    rootMargin: '0px 0px -50px 0px'
  });

  const revealElements = motivSection.querySelectorAll('.anim-reveal');
  revealElements.forEach(el => observer.observe(el));

  // Also trigger hero animations when the motivation screen becomes active
  const screenObserver = new MutationObserver((mutations) => {
    mutations.forEach(mutation => {
      if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
        if (motivSection.classList.contains('active')) {
          setTimeout(() => triggerHeroAnimations(), 200);
        }
      }
    });
  });
  screenObserver.observe(motivSection, { attributes: true });

  // Also handle nav pill clicks for the motivation tab
  const motivPill = document.querySelector('.nav-pill[data-target="motivation"]');
  if (motivPill) {
    motivPill.addEventListener('click', () => {
      setTimeout(() => triggerHeroAnimations(), 200);
    });
  }
}

/* ── Animated stat counters ── */
function initStatCounters() {
  const statNumbers = document.querySelectorAll('.stat-number[data-target]');
  if (!statNumbers.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCounter(entry.target);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  statNumbers.forEach(el => observer.observe(el));
}

function animateCounter(element) {
  const target = parseInt(element.dataset.target, 10);
  const duration = 2000;
  const startTime = performance.now();

  function update(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    // Ease-out cubic
    const eased = 1 - Math.pow(1 - progress, 3);
    const current = Math.round(eased * target);
    element.textContent = current;

    if (progress < 1) {
      requestAnimationFrame(update);
    }
  }
  requestAnimationFrame(update);
}

/* ── Start Button → navigates to goal screen ── */
function initStartButton() {
  const btn = document.getElementById('motivStartBtn');
  if (!btn) return;

  btn.addEventListener('click', () => {
    const screens = document.querySelectorAll('.screen');
    const pills = document.querySelectorAll('.nav-pill');
    screens.forEach(s => s.classList.remove('active'));
    pills.forEach(p => p.classList.remove('active'));
    const goal = document.getElementById('goal');
    if (goal) goal.classList.add('active');
    const pill = document.querySelector('.nav-pill[data-target="goal"]');
    if (pill) pill.classList.add('active');
  });
}
