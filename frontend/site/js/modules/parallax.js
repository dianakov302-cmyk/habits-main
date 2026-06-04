/**
 * Parallax scroll effects for the Home page.
 * Creates depth layers that move at different speeds on scroll:
 *  - Star field (slowest)
 *  - Atmospheric glow
 *  - Hero image (medium)
 *  - Logo & CTA (faster, with fade)
 *  - Section content reveals
 */

export function initParallax() {
  const homeScreen = document.getElementById('home');
  if (!homeScreen) return;

  createStarField();
  initScrollParallax(homeScreen);
  initSectionReveals(homeScreen);
}

/* ═══════ Star Field ═══════ */
function createStarField() {
  const container = document.getElementById('parallaxStars');
  if (!container) return;

  const starCount = 80;

  for (let i = 0; i < starCount; i++) {
    const star = document.createElement('div');
    star.classList.add('parallax-star');

    // Random position
    star.style.left = Math.random() * 100 + '%';
    star.style.top = Math.random() * 100 + '%';

    // Random size (1–3px)
    const size = (0.8 + Math.random() * 2.2) + 'px';
    star.style.width = size;
    star.style.height = size;

    // Random twinkle timing
    star.style.setProperty('--star-delay', (Math.random() * 6) + 's');
    star.style.setProperty('--star-duration', (2.5 + Math.random() * 4) + 's');

    // Slight random brightness
    star.style.opacity = 0;

    container.appendChild(star);
  }
}

/* ═══════ Scroll-driven Parallax ═══════ */
function initScrollParallax(scrollContainer) {
  const heroFrame = document.getElementById('heroFrame');
  const heroLogo = document.getElementById('heroLogo');
  const ctaBtn = document.getElementById('ctaJourney');
  const starsLayer = document.getElementById('parallaxStars');
  const glowLayer = document.getElementById('parallaxGlow');
  const scrollIndicator = document.getElementById('heroScrollIndicator');
  const ctaTextSection = document.querySelector('.home-cta-text');
  const ctaTextH1 = ctaTextSection?.querySelector('h1');
  const butterflyImg = document.querySelector('.butterfly-img');
  const butterflySection = document.querySelector('.home-butterfly');
  const journalSection = document.querySelector('.home-journal');
  const journalImg = journalSection?.querySelector('.journal-img-wrap');
  const journalText = journalSection?.querySelector('.journal-text');
  const btcHeadline = document.querySelector('.btc-headline');

  let ticking = false;

  function onScroll() {
    if (ticking) return;
    ticking = true;

    requestAnimationFrame(() => {
      const scrollTop = scrollContainer.scrollTop;
      const vh = window.innerHeight;

      // ── Hero layers ──
      if (heroFrame) {
        // Image scrolls at 0.4x speed — creates depth
        heroFrame.style.transform = `translate3d(0, ${scrollTop * 0.4}px, 0)`;
      }

      if (starsLayer) {
        // Stars scroll very slowly
        starsLayer.style.transform = `translate3d(0, ${scrollTop * 0.12}px, 0)`;
      }

      if (glowLayer) {
        // Glow moves slightly
        glowLayer.style.transform = `translate3d(0, ${scrollTop * 0.25}px, 0)`;
      }

      if (heroLogo) {
        // Logo fades out and moves up relative to scroll
        const logoFade = Math.max(0, 1 - scrollTop / (vh * 0.5));
        heroLogo.style.transform = `translate3d(0, ${scrollTop * 0.2}px, 0)`;
        heroLogo.style.opacity = logoFade;
      }

      if (ctaBtn) {
        // CTA rises and fades
        const ctaFade = Math.max(0, 1 - scrollTop / (vh * 0.45));
        ctaBtn.style.transform = `translate3d(0, ${scrollTop * 0.3}px, 0)`;
        ctaBtn.style.opacity = ctaFade;
      }

      if (scrollIndicator) {
        // Scroll hint fades quickly
        const hintFade = Math.max(0, 1 - scrollTop / (vh * 0.2));
        scrollIndicator.style.opacity = hintFade;
      }

      // ── "Start Your Journey" text section ──
      if (ctaTextH1) {
        const rect = ctaTextSection.getBoundingClientRect();
        if (rect.top < vh && rect.bottom > 0) {
          const progress = (vh - rect.top) / (vh + rect.height);
          const offset = Math.max(0, 80 - progress * 160);
          const opacity = Math.min(1, progress * 2.2);
          ctaTextH1.style.transform = `translate3d(0, ${offset}px, 0)`;
          ctaTextH1.style.opacity = opacity;
        }
      }

      // ── Butterfly section ──
      if (butterflyImg && butterflySection) {
        const rect = butterflySection.getBoundingClientRect();
        if (rect.top < vh && rect.bottom > 0) {
          const progress = (vh - rect.top) / (vh + rect.height);
          const offset = (progress - 0.5) * -50;
          butterflyImg.style.transform = `translate3d(0, ${offset}px, 0)`;
        }
      }

      // ── Journal section ──
      if (journalImg && journalSection) {
        const rect = journalSection.getBoundingClientRect();
        if (rect.top < vh && rect.bottom > 0) {
          const progress = (vh - rect.top) / (vh + rect.height);
          const imgOffset = (progress - 0.5) * -30;
          const textOffset = (progress - 0.5) * -15;
          journalImg.style.transform = `translate3d(0, ${imgOffset}px, 0)`;
          if (journalText) {
            journalText.style.transform = `translate3d(0, ${textOffset}px, 0)`;
          }
        }
      }

      // ── "Break the circle" headline ──
      if (btcHeadline) {
        const rect = btcHeadline.getBoundingClientRect();
        if (rect.top < vh && rect.bottom > 0) {
          const progress = (vh - rect.top) / (vh + rect.height);
          const scale = 0.85 + progress * 0.15;
          const opacity = Math.min(1, progress * 2);
          btcHeadline.style.transform = `translate3d(0, ${(1 - progress) * 40}px, 0) scale(${scale})`;
          btcHeadline.style.opacity = opacity;
        }
      }

      ticking = false;
    });
  }

  scrollContainer.addEventListener('scroll', onScroll, { passive: true });

  // Fire once to set initial state
  onScroll();
}

/* ═══════ Scroll-triggered Section Reveals ═══════ */
function initSectionReveals(scrollContainer) {
  // Observe sections for reveal animations on home page
  const revealElements = scrollContainer.querySelectorAll(
    '.home-cta-text, .home-butterfly, .home-motivation, .home-journal, .home-btc'
  );

  if (!revealElements.length) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('parallax-visible');
          observer.unobserve(entry.target);
        }
      });
    },
    {
      threshold: 0.1,
      rootMargin: '0px 0px -60px 0px'
    }
  );

  revealElements.forEach(el => observer.observe(el));
}
